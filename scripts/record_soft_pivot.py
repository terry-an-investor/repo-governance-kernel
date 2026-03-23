#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

from round_control import (
    OPEN_ROUND_STATUSES,
    active_objective_path,
    apply_transition_transaction,
    assert_objective_phase_command_contract,
    merged_tags,
    objective_record_payload,
    pivot_log_path,
    pivots_dir,
    project_dir,
    render_objective_phase_guard_lines,
    render_active_objective_file,
    render_objective_file,
    render_pivot_file,
    render_pivot_log_file,
    resolve_active_objective_record,
    resolve_anchor,
    select_open_round_record,
    slugify,
    timestamp_now,
)


ALLOWED_PHASES = {"exploration", "execution"}
OBJECTIVE_SHAPE_FIELDS = {"problem", "success_criteria", "non_goals", "why_now", "phase"}
SCRIPTS_DIR = Path(__file__).resolve().parent


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Record a soft pivot that keeps the current objective identity but revises its active framing.")
    parser.add_argument("--project-id", required=True)
    parser.add_argument("--objective-id")
    parser.add_argument("--trigger", required=True)
    parser.add_argument("--change-summary", required=True)
    parser.add_argument("--identity-rationale", required=True)
    parser.add_argument("--pivot-title", default="")
    parser.add_argument("--title")
    parser.add_argument("--summary")
    parser.add_argument("--problem")
    parser.add_argument("--success-criterion", action="append", default=[])
    parser.add_argument("--non-goal", action="append", default=[])
    parser.add_argument("--why-now")
    parser.add_argument("--phase", choices=sorted(ALLOWED_PHASES))
    parser.add_argument("--risk", action="append", default=[])
    parser.add_argument("--path", action="append", default=[])
    parser.add_argument("--supersession-notes")
    parser.add_argument("--evidence", action="append", default=[])
    parser.add_argument("--retained-decision", action="append", default=[])
    parser.add_argument("--invalidated-assumption", action="append", default=[])
    parser.add_argument("--next-control-change", action="append", default=[])
    parser.add_argument("--rewrite-open-round", action="store_true")
    parser.add_argument("--round-title", default="")
    parser.add_argument("--round-summary", default="")
    parser.add_argument("--round-scope-item", action="append", default=[])
    parser.add_argument("--round-scope-path", action="append", default=[])
    parser.add_argument("--round-deliverable", default="")
    parser.add_argument("--round-validation-plan", default="")
    parser.add_argument("--round-risk", action="append", default=[])
    parser.add_argument("--round-blocker", action="append", default=[])
    parser.add_argument("--round-status-note", action="append", default=[])
    parser.add_argument("--replace-round-scope-items", action="store_true")
    parser.add_argument("--replace-round-scope-paths", action="store_true")
    parser.add_argument("--replace-round-risks", action="store_true")
    parser.add_argument("--replace-round-blockers", action="store_true")
    return parser.parse_args()


def resolve_optional_string(value: str | None, fallback: str) -> str:
    if value is None:
        return fallback
    return value.strip()


def resolve_optional_list(values: list[str], fallback: list[str]) -> list[str]:
    cleaned = [value.strip() for value in values if value.strip()]
    return cleaned or list(fallback)


def _clean_list(values: list[str]) -> list[str]:
    return [value.strip() for value in values if value.strip()]


def _rewrite_open_round(args: argparse.Namespace, round_id: str, reason: str) -> dict[str, object]:
    cmd = [
        sys.executable,
        str(SCRIPTS_DIR / "rewrite_open_round.py"),
        "--project-id",
        args.project_id,
        "--round-id",
        round_id,
        "--reason",
        reason,
    ]
    if args.round_title.strip():
        cmd.extend(["--title", args.round_title.strip()])
    if args.round_summary.strip():
        cmd.extend(["--summary", args.round_summary.strip()])
    if args.round_deliverable.strip():
        cmd.extend(["--deliverable", args.round_deliverable.strip()])
    if args.round_validation_plan.strip():
        cmd.extend(["--validation-plan", args.round_validation_plan.strip()])
    for item in _clean_list(args.round_scope_item):
        cmd.extend(["--scope-item", item])
    for item in _clean_list(args.round_scope_path):
        cmd.extend(["--scope-path", item])
    for item in _clean_list(args.round_risk):
        cmd.extend(["--risk", item])
    for item in _clean_list(args.round_blocker):
        cmd.extend(["--blocker", item])
    for item in _clean_list(args.round_status_note):
        cmd.extend(["--status-note", item])
    if args.replace_round_scope_items:
        cmd.append("--replace-scope-items")
    if args.replace_round_scope_paths:
        cmd.append("--replace-scope-paths")
    if args.replace_round_risks:
        cmd.append("--replace-risks")
    if args.replace_round_blockers:
        cmd.append("--replace-blockers")
    completed = subprocess.run(
        cmd,
        cwd=str(SCRIPTS_DIR.parent),
        capture_output=True,
        text=True,
        check=False,
    )
    if completed.returncode != 0:
        raise SystemExit(completed.stderr.strip() or completed.stdout.strip() or "rewrite-open-round failed during soft pivot")
    try:
        return json.loads(completed.stdout)
    except json.JSONDecodeError as exc:
        raise SystemExit(f"rewrite-open-round returned invalid json during soft pivot: {exc}") from exc


def main() -> int:
    args = parse_args()
    if not project_dir(args.project_id).exists():
        raise SystemExit(f"project directory not found: {project_dir(args.project_id)}")

    objective_path, meta, sections, objective_id = resolve_active_objective_record(
        args.project_id,
        objective_id=args.objective_id or "",
    )
    payload = objective_record_payload(meta, sections)

    next_title = resolve_optional_string(args.title, str(payload["title"]))
    next_summary = resolve_optional_string(args.summary, str(payload["summary"]))
    next_problem = resolve_optional_string(args.problem, str(payload["problem"]))
    next_success_criteria = resolve_optional_list(args.success_criterion, list(payload["success_criteria"]))
    next_non_goals = resolve_optional_list(args.non_goal, list(payload["non_goals"]))
    next_why_now = resolve_optional_string(args.why_now, str(payload["why_now"]))
    next_phase = resolve_optional_string(args.phase, str(payload["phase"]))
    next_risks = resolve_optional_list(args.risk, list(payload["current_risks"]))
    next_paths = resolve_optional_list(args.path, list(payload["paths"]))
    next_supersession_notes = resolve_optional_string(args.supersession_notes, str(payload["supersession_notes"]))

    if not next_problem:
        raise SystemExit("soft pivot requires a non-empty resulting problem statement")
    if not next_success_criteria:
        raise SystemExit("soft pivot requires at least one resulting success criterion")
    if not next_non_goals:
        raise SystemExit("soft pivot requires at least one resulting non-goal")
    if next_phase not in ALLOWED_PHASES:
        raise SystemExit(f"soft pivot requires phase in {sorted(ALLOWED_PHASES)}")

    changed_fields: list[str] = []
    comparisons = {
        "title": (str(payload["title"]), next_title),
        "summary": (str(payload["summary"]), next_summary),
        "problem": (str(payload["problem"]), next_problem),
        "success_criteria": (list(payload["success_criteria"]), next_success_criteria),
        "non_goals": (list(payload["non_goals"]), next_non_goals),
        "why_now": (str(payload["why_now"]), next_why_now),
        "phase": (str(payload["phase"]), next_phase),
        "current_risks": (list(payload["current_risks"]), next_risks),
        "paths": (list(payload["paths"]), next_paths),
        "supersession_notes": (str(payload["supersession_notes"]), next_supersession_notes),
    }
    for field_name, (previous_value, next_value) in comparisons.items():
        if previous_value != next_value:
            changed_fields.append(field_name)
    if not changed_fields:
        raise SystemExit("soft pivot produced no material objective change")

    open_round_record, round_issues = select_open_round_record(args.project_id)
    if round_issues:
        raise SystemExit("cannot record soft pivot while durable round truth is ambiguous: " + "; ".join(round_issues))
    if next_phase == "execution":
        if open_round_record is None:
            raise SystemExit(
                f"cannot move objective `{objective_id}` into execution via soft pivot without one durable open round"
            )
        round_objective_id = str(open_round_record[1].get("objective_id") or "").strip()
        if round_objective_id != objective_id:
            raise SystemExit(
                f"execution-phase soft pivot requires the durable open round to stay aligned with objective `{objective_id}`; "
                f"found round objective `{round_objective_id}`"
            )
    if open_round_record is not None and OBJECTIVE_SHAPE_FIELDS.intersection(changed_fields) and not (args.next_control_change or args.rewrite_open_round):
        round_id = str(open_round_record[1].get("id") or open_round_record[0].stem).strip()
        raise SystemExit(
            f"soft pivot changed objective shape while durable open round `{round_id}` remains active; "
            "record at least one --next-control-change item or pass --rewrite-open-round"
        )

    anchor = resolve_anchor(args.project_id)
    objective_text = render_objective_file(
        objective_id=objective_id,
        title=next_title,
        status="active",
        project_id=args.project_id,
        anchor=anchor,
        paths=next_paths,
        created_at=str(payload["created_at"]) or timestamp_now().isoformat(timespec="seconds"),
        evidence_refs=list(payload["evidence_refs"]),
        tags=merged_tags(
            list(payload["tags"]),
            drop={"closed", "invalidated", "superseded"},
            add=["active"],
        ),
        confidence=str(payload["confidence"]),
        phase=next_phase,
        supersedes=list(payload["supersedes"]),
        superseded_by=list(payload["superseded_by"]),
        summary=next_summary,
        problem=next_problem,
        success_criteria=next_success_criteria,
        non_goals=next_non_goals,
        why_now=next_why_now,
        current_risks=next_risks,
        supersession_notes=next_supersession_notes,
    )
    active_objective_text = render_active_objective_file(
        objective_id=objective_id,
        phase=next_phase,
        status="active",
        problem=next_problem,
        success_criteria=next_success_criteria,
        non_goals=next_non_goals,
        why_now=next_why_now,
        current_risks=next_risks,
    )

    timestamp = timestamp_now()
    pivot_slug = slugify(args.pivot_title or f"soft-pivot-{objective_id}")
    pivot_id = f"piv-{timestamp.strftime('%Y-%m-%d-%H%M')}-{pivot_slug}"
    pivot_path = pivots_dir(args.project_id) / f"{timestamp.strftime('%Y-%m-%d-%H%M')}-{pivot_slug}.md"
    pivot_text = render_pivot_file(
        pivot_id=pivot_id,
        title=args.pivot_title.strip() or f"Soft pivot on {objective_id}",
        status="active",
        project_id=args.project_id,
        objective_id=objective_id,
        anchor=anchor,
        paths=next_paths,
        created_at=timestamp.isoformat(timespec="seconds"),
        evidence_refs=[],
        tags=["pivot", "soft"],
        confidence="high",
        phase=next_phase,
        supersedes=[],
        superseded_by=[],
        summary=args.change_summary.strip(),
        pivot_type="Soft pivot.",
        trigger=args.trigger,
        change_summary=args.change_summary,
        identity_rationale=args.identity_rationale,
        previous_objective=f"`{objective_id}` {str(payload['title']).strip()}".strip(),
        new_objective=f"`{objective_id}` {next_title}".strip(),
        evidence=[item.strip() for item in args.evidence if item.strip()],
        decisions_retained=[item.strip() for item in args.retained_decision if item.strip()],
        assumptions_invalidated=[item.strip() for item in args.invalidated_assumption if item.strip()],
        next_control_changes=[item.strip() for item in args.next_control_change if item.strip()],
    )

    active_path = active_objective_path(args.project_id)
    pivot_path_projection = pivot_log_path(args.project_id)
    assert_objective_phase_command_contract(
        "record-soft-pivot",
        provided_inputs={
            "project_id",
            "objective_id",
            "trigger",
            "change_summary",
            "identity_rationale",
        },
        satisfied_guard_codes={
            "target_matches_active_objective",
            "material_objective_change_present",
            "resulting_objective_fields_present",
            "execution_phase_round_alignment_preserved",
            "round_review_path_explicit_when_objective_shape_changes",
        },
        write_targets={
            "durable:objective",
            "durable:pivot",
            "control:active-objective",
            "control:pivot-log",
            "memory:transition-event",
        },
    )
    _side_effects, event_id, event_path = apply_transition_transaction(
        project_id=args.project_id,
        writes=[
            {"path": objective_path, "text": objective_text, "label": "durable objective"},
            {"path": pivot_path, "text": pivot_text, "label": "durable pivot"},
            {"path": active_path, "text": active_objective_text, "label": "active objective projection"},
            {"path": pivot_path_projection, "text": lambda: render_pivot_log_file(args.project_id), "label": "pivot-log projection"},
        ],
        command_name="record-soft-pivot",
        title=f"Recorded soft pivot on {objective_id}",
        anchor=anchor,
        previous_state=f"objective `{objective_id}` was active as `{str(payload['title']).strip()}` in phase `{str(payload['phase'])}`",
        next_state=f"objective `{objective_id}` remains active as `{next_title}` in phase `{next_phase}` and pivot `{pivot_id}` is recorded",
        guards=render_objective_phase_guard_lines(
            "record-soft-pivot",
            context={"objective_id": objective_id},
        ),
        evidence=[args.trigger, args.change_summary, args.identity_rationale]
        + [item.strip() for item in args.evidence if item.strip()],
        target_ids=[objective_id, pivot_id],
        event_file_stem=f"{timestamp.strftime('%Y-%m-%d-%H%M%S')}-{objective_id}-soft-pivot",
    )

    rewrite_result: dict[str, object] | None = None
    if open_round_record is not None and OBJECTIVE_SHAPE_FIELDS.intersection(changed_fields) and args.rewrite_open_round:
        round_id = str(open_round_record[1].get("id") or open_round_record[0].stem).strip()
        rewrite_result = _rewrite_open_round(
            args,
            round_id,
            f"Soft pivot `{pivot_id}` changed objective shape and the bounded round must be rewritten to stay aligned.",
        )
    print(
        json.dumps(
            {
                "project_id": args.project_id,
                "objective_id": objective_id,
                "pivot_id": pivot_id,
                "changed_fields": changed_fields,
                "objective_path": str(objective_path),
                "pivot_path": str(pivot_path),
                "active_objective_path": str(active_path),
                "pivot_log_path": str(pivot_path_projection),
                "transition_event_id": event_id,
                "transition_event_path": str(event_path),
                "round_rewrite": rewrite_result,
            },
            ensure_ascii=True,
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
