#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json

from audit_control_state import audit_project_control_state
from round_control import (
    adjudications_dir,
    project_dir,
    render_adjudication_file,
    resolve_anchor,
    select_active_objective_record,
    slugify,
    timestamp_now,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Record an adjudication over conflicting or weak control state.")
    parser.add_argument("--project-id", required=True)
    parser.add_argument("--title", default="")
    parser.add_argument("--summary", default="")
    parser.add_argument("--question", required=True)
    parser.add_argument("--verdict", required=True)
    parser.add_argument("--retain-id", action="append", default=[])
    parser.add_argument("--invalidate-id", action="append", default=[])
    parser.add_argument("--follow-up", action="append", default=[])
    parser.add_argument("--evidence", action="append", default=[])
    parser.add_argument("--path", action="append", default=[])
    parser.add_argument("--allow-clean", action="store_true")
    return parser.parse_args()


def render_issue_line(issue: dict[str, object]) -> str:
    severity = str(issue.get("severity") or "").strip() or "unknown"
    domain = str(issue.get("domain") or "").strip() or "unknown"
    code = str(issue.get("code") or "").strip() or "unknown"
    message = str(issue.get("message") or "").strip()
    evidence = [str(item).strip() for item in issue.get("evidence", []) if str(item).strip()]
    if evidence:
        return f"[{severity}] {domain}/{code}: {message} | evidence: {', '.join(evidence)}"
    return f"[{severity}] {domain}/{code}: {message}"


def normalize_items(values: list[str]) -> list[str]:
    return [value.strip() for value in values if value.strip()]


def main() -> int:
    args = parse_args()
    project_path = project_dir(args.project_id)
    if not project_path.exists():
        raise SystemExit(f"project directory not found: {project_path}")

    audit_result = audit_project_control_state(args.project_id)
    audit_issues = [issue for issue in audit_result["issues"] if isinstance(issue, dict)]
    if not audit_issues and not args.allow_clean:
        raise SystemExit(
            "adjudication requires at least one audit issue unless --allow-clean is passed; "
            "there is nothing to adjudicate yet"
        )

    timestamp = timestamp_now()
    title = args.title.strip() or f"Adjudicate {args.project_id} control state"
    slug = slugify(title)
    adjudication_id = f"adj-{timestamp.strftime('%Y-%m-%d-%H%M')}-{slug}"
    file_stem = f"{timestamp.strftime('%Y-%m-%d-%H%M')}-{slug}"

    active_objective_record, _objective_issues = select_active_objective_record(args.project_id)
    objective_id = ""
    phase = ""
    if active_objective_record is not None:
        _path, objective_meta, _sections = active_objective_record
        objective_id = str(objective_meta.get("id") or "").strip()
        phase = str(objective_meta.get("phase") or "").strip()

    paths = normalize_items(args.path)
    if not paths:
        paths = [
            f"projects/{args.project_id}/control/",
            f"projects/{args.project_id}/memory/adjudications/",
        ]

    summary = args.summary.strip()
    if not summary:
        summary = (
            f"Adjudication recorded against {len(audit_issues)} current control-state issue(s) "
            f"for project `{args.project_id}`."
        )

    conflict_set = [render_issue_line(issue) for issue in audit_issues]
    evidence = normalize_items(args.evidence)
    evidence.append(f"audit status: {audit_result['status']}")
    evidence.extend(
        f"audit check: {check}"
        for check in audit_result["summary"].get("checks", [])
        if str(check).strip()
    )

    adjudication_text = render_adjudication_file(
        adjudication_id=adjudication_id,
        title=title,
        status="recorded",
        project_id=args.project_id,
        objective_id=objective_id,
        anchor=resolve_anchor(args.project_id),
        paths=paths,
        created_at=timestamp.isoformat(timespec="seconds"),
        evidence_refs=[],
        tags=["adjudication", "control-state"],
        confidence="high",
        phase=phase,
        summary=summary,
        conflict_set=conflict_set,
        adjudication_question=args.question,
        verdict=args.verdict,
        objects_retained=normalize_items(args.retain_id),
        objects_invalidated=normalize_items(args.invalidate_id),
        required_follow_up_transitions=normalize_items(args.follow_up),
        evidence=evidence,
    )

    adjudication_path = adjudications_dir(args.project_id) / f"{file_stem}.md"
    adjudication_path.parent.mkdir(parents=True, exist_ok=True)
    adjudication_path.write_text(adjudication_text, encoding="utf-8")

    print(
        json.dumps(
            {
                "project_id": args.project_id,
                "adjudication_id": adjudication_id,
                "adjudication_path": str(adjudication_path),
                "audit_status": audit_result["status"],
                "issue_count": len(audit_issues),
                "objective_id": objective_id,
            },
            ensure_ascii=True,
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
