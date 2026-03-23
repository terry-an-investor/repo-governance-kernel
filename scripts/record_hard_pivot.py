#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json

from round_control import (
    active_objective_path,
    build_transition_event_file,
    load_active_objective,
    load_active_round,
    load_objective_file,
    locate_objective_file,
    objectives_dir,
    parse_bullet_list,
    pivot_log_path,
    pivots_dir,
    project_dir,
    render_active_objective_file,
    render_objective_file,
    render_pivot_file,
    render_pivot_log_file,
    resolve_anchor,
    slugify,
    timestamp_now,
    transition_events_dir,
)


ALLOWED_PHASES = {"exploration", "execution"}
BLOCKING_ROUND_STATUSES = {"active", "blocked", "validation_pending"}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Record a hard pivot to a new active objective.")
    parser.add_argument("--project-id", required=True)
    parser.add_argument("--previous-objective-id")
    parser.add_argument("--title", required=True)
    parser.add_argument("--summary", default="")
    parser.add_argument("--problem", required=True)
    parser.add_argument("--success-criterion", action="append", required=True)
    parser.add_argument("--non-goal", action="append", required=True)
    parser.add_argument("--why-now", required=True)
    parser.add_argument("--phase", required=True, choices=sorted(ALLOWED_PHASES))
    parser.add_argument("--trigger", required=True)
    parser.add_argument("--pivot-title", default="")
    parser.add_argument("--evidence", action="append", default=[])
    parser.add_argument("--retained-decision", action="append", default=[])
    parser.add_argument("--invalidated-assumption", action="append", default=[])
    parser.add_argument("--next-control-change", action="append", default=[])
    parser.add_argument("--risk", action="append", default=[])
    parser.add_argument("--path", action="append", default=[])
    parser.add_argument("--supersession-notes", default="")
    return parser.parse_args()


def normalize_section_text(text: str) -> str:
    value = text.strip()
    return "" if value in {"", "_none recorded_"} else value


def merged_tags(existing: list[str], *, drop: set[str], add: list[str]) -> list[str]:
    seen: set[str] = set()
    result: list[str] = []
    for tag in existing:
        cleaned = str(tag).strip()
        if not cleaned or cleaned in drop or cleaned in seen:
            continue
        seen.add(cleaned)
        result.append(cleaned)
    for tag in add:
        cleaned = str(tag).strip()
        if not cleaned or cleaned in seen:
            continue
        seen.add(cleaned)
        result.append(cleaned)
    return result


def main() -> int:
    args = parse_args()
    project_path = project_dir(args.project_id)
    if not project_path.exists():
        raise SystemExit(f"project directory not found: {project_path}")

    active_objective_preface, _active_objective_sections = load_active_objective(args.project_id)
    previous_objective_id = args.previous_objective_id or active_objective_preface.get("objective id", "")
    if not previous_objective_id:
        raise SystemExit("missing previous objective id; pass --previous-objective-id or maintain control/active-objective.md")

    objective_path = locate_objective_file(args.project_id, previous_objective_id)
    if objective_path is None:
        raise SystemExit(f"objective file not found for `{previous_objective_id}`")

    previous_meta, previous_sections = load_objective_file(objective_path)
    previous_status = str(previous_meta.get("status") or "").strip()
    if previous_status != "active":
        raise SystemExit(f"hard pivot requires an active previous objective; `{previous_objective_id}` is `{previous_status or 'unknown'}`")

    active_round_preface, _active_round_sections = load_active_round(args.project_id)
    active_round_id = active_round_preface.get("round id", "")
    active_round_status = active_round_preface.get("status", "")
    active_round_objective_id = active_round_preface.get("objective id", "")
    if (
        active_round_id
        and active_round_objective_id == previous_objective_id
        and active_round_status in BLOCKING_ROUND_STATUSES
    ):
        raise SystemExit(
            f"cannot hard-pivot while round `{active_round_id}` is still `{active_round_status}` against "
            f"objective `{previous_objective_id}`; close, capture, abandon, or explicitly re-scope the round first"
        )

    timestamp = timestamp_now()
    slug = slugify(args.title)
    objective_id = f"obj-{timestamp.strftime('%Y-%m-%d-%H%M')}-{slug}"
    objective_file_stem = f"{timestamp.strftime('%Y-%m-%d-%H%M')}-{slug}"
    pivot_slug = slugify(args.pivot_title or f"hard-pivot-{previous_objective_id}-to-{objective_id}")
    pivot_id = f"piv-{timestamp.strftime('%Y-%m-%d-%H%M')}-{pivot_slug}"
    pivot_file_stem = f"{timestamp.strftime('%Y-%m-%d-%H%M')}-{pivot_slug}"
    anchor = resolve_anchor(args.project_id)

    previous_superseded_by = [str(item).strip() for item in previous_meta.get("superseded_by", []) if str(item).strip()]
    if objective_id not in previous_superseded_by:
        previous_superseded_by.append(objective_id)

    previous_objective_text = render_objective_file(
        objective_id=previous_objective_id,
        title=str(previous_meta.get("title") or previous_objective_id),
        status="superseded",
        project_id=args.project_id,
        anchor=anchor,
        paths=[str(item).strip() for item in previous_meta.get("paths", []) if str(item).strip()],
        created_at=str(previous_meta.get("created_at") or "").strip() or timestamp.isoformat(timespec="seconds"),
        evidence_refs=[entry for entry in previous_meta.get("evidence_refs", []) if isinstance(entry, dict)],
        tags=merged_tags(
            [str(item).strip() for item in previous_meta.get("tags", []) if str(item).strip()],
            drop={"active"},
            add=["superseded"],
        ),
        confidence=str(previous_meta.get("confidence") or "high").strip() or "high",
        phase=str(previous_meta.get("phase") or args.phase).strip() or args.phase,
        supersedes=[str(item).strip() for item in previous_meta.get("supersedes", []) if str(item).strip()],
        superseded_by=previous_superseded_by,
        summary=normalize_section_text(previous_sections.get("Summary", "")),
        problem=normalize_section_text(previous_sections.get("Problem", "")),
        success_criteria=parse_bullet_list(previous_sections.get("Success Criteria", "")),
        non_goals=parse_bullet_list(previous_sections.get("Non-Goals", "")),
        why_now=normalize_section_text(previous_sections.get("Why Now", "")),
        current_risks=parse_bullet_list(previous_sections.get("Active Risks", "")),
        supersession_notes="\n\n".join(
            part
            for part in [
                normalize_section_text(previous_sections.get("Supersession Notes", "")),
                f"Superseded by `{objective_id}` because {args.trigger.strip()}",
            ]
            if part
        ),
    )
    objective_path.write_text(previous_objective_text, encoding="utf-8")

    summary = args.summary.strip() or args.problem.strip()
    new_objective_text = render_objective_file(
        objective_id=objective_id,
        title=args.title,
        status="active",
        project_id=args.project_id,
        anchor=anchor,
        paths=args.path,
        created_at=timestamp.isoformat(timespec="seconds"),
        evidence_refs=[],
        tags=["objective", "active"],
        confidence="high",
        phase=args.phase,
        supersedes=[previous_objective_id],
        superseded_by=[],
        summary=summary,
        problem=args.problem,
        success_criteria=args.success_criterion,
        non_goals=args.non_goal,
        why_now=args.why_now,
        current_risks=args.risk,
        supersession_notes=args.supersession_notes,
    )
    new_objective_path = objectives_dir(args.project_id) / f"{objective_file_stem}.md"
    new_objective_path.parent.mkdir(parents=True, exist_ok=True)
    new_objective_path.write_text(new_objective_text, encoding="utf-8")

    pivot_title = args.pivot_title.strip() or f"Hard pivot to {args.title}"
    pivot_text = render_pivot_file(
        pivot_id=pivot_id,
        title=pivot_title,
        status="active",
        project_id=args.project_id,
        objective_id=objective_id,
        anchor=anchor,
        paths=args.path,
        created_at=timestamp.isoformat(timespec="seconds"),
        evidence_refs=[],
        tags=["pivot", "hard"],
        confidence="high",
        phase=args.phase,
        supersedes=[previous_objective_id],
        superseded_by=[],
        summary=f"Hard pivot from `{previous_objective_id}` to `{objective_id}`.",
        pivot_type="Hard pivot.",
        trigger=args.trigger,
        previous_objective=f"`{previous_objective_id}` {previous_meta.get('title', '').strip()}".strip(),
        new_objective=f"`{objective_id}` {args.title}".strip(),
        evidence=[item.strip() for item in args.evidence if item.strip()],
        decisions_retained=[item.strip() for item in args.retained_decision if item.strip()],
        assumptions_invalidated=[item.strip() for item in args.invalidated_assumption if item.strip()],
        next_control_changes=[item.strip() for item in args.next_control_change if item.strip()],
    )
    pivot_path = pivots_dir(args.project_id) / f"{pivot_file_stem}.md"
    pivot_path.parent.mkdir(parents=True, exist_ok=True)
    pivot_path.write_text(pivot_text, encoding="utf-8")

    active_path = active_objective_path(args.project_id)
    active_path.parent.mkdir(parents=True, exist_ok=True)
    active_path.write_text(
        render_active_objective_file(
            objective_id=objective_id,
            phase=args.phase,
            status="active",
            problem=args.problem,
            success_criteria=args.success_criterion,
            non_goals=args.non_goal,
            why_now=args.why_now,
            current_risks=args.risk,
        ),
        encoding="utf-8",
    )

    pivot_log = pivot_log_path(args.project_id)
    pivot_log.parent.mkdir(parents=True, exist_ok=True)
    pivot_log.write_text(render_pivot_log_file(args.project_id), encoding="utf-8")

    event_id, event_text = build_transition_event_file(
        project_id=args.project_id,
        command_name="record-hard-pivot",
        title=f"Recorded hard pivot from {previous_objective_id} to {objective_id}",
        anchor=anchor,
        previous_state=f"objective `{previous_objective_id}` was active",
        next_state=f"objective `{objective_id}` is now active and pivot `{pivot_id}` is recorded",
        guards=[
            f"objective `{previous_objective_id}` exists and is active",
            "new objective fields are present",
            "no still-active round remains tied to the previous objective",
        ],
        side_effects=[
            f"updated superseded objective `{objective_path.relative_to(project_path.parent).as_posix()}`",
            f"wrote new objective `{new_objective_path.relative_to(project_path.parent).as_posix()}`",
            f"wrote pivot `{pivot_path.relative_to(project_path.parent).as_posix()}`",
            f"updated `{active_path.relative_to(project_path.parent).as_posix()}`",
            f"updated `{pivot_log.relative_to(project_path.parent).as_posix()}`",
        ],
        evidence=[args.trigger] + [item.strip() for item in args.evidence if item.strip()],
        target_ids=[previous_objective_id, objective_id, pivot_id],
    )
    event_path = transition_events_dir(args.project_id) / f"{pivot_file_stem}-record-hard-pivot.md"
    event_path.parent.mkdir(parents=True, exist_ok=True)
    event_path.write_text(event_text, encoding="utf-8")

    print(
        json.dumps(
            {
                "project_id": args.project_id,
                "previous_objective_id": previous_objective_id,
                "objective_id": objective_id,
                "pivot_id": pivot_id,
                "previous_objective_path": str(objective_path),
                "objective_path": str(new_objective_path),
                "pivot_path": str(pivot_path),
                "active_objective_path": str(active_path),
                "pivot_log_path": str(pivot_log),
                "transition_event_id": event_id,
                "transition_event_path": str(event_path),
            },
            ensure_ascii=True,
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
