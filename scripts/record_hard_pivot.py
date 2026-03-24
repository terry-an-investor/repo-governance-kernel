#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json

from round_control import (
    OPEN_TASK_CONTRACT_STATUSES,
    active_objective_path,
    apply_transition_transaction,
    assert_objective_phase_command_contract,
    find_rounds,
    find_task_contracts,
    merged_tags,
    objective_record_payload,
    objectives_dir,
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
    slugify,
    timestamp_now,
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

def main() -> int:
    args = parse_args()
    project_path = project_dir(args.project_id)
    if not project_path.exists():
        raise SystemExit(f"project directory not found: {project_path}")

    objective_path, previous_meta, previous_sections, previous_objective_id = resolve_active_objective_record(
        args.project_id,
        objective_id=args.previous_objective_id or "",
    )
    previous_payload = objective_record_payload(previous_meta, previous_sections)

    blocking_round_records = find_rounds(
        args.project_id,
        objective_id=previous_objective_id,
        statuses=BLOCKING_ROUND_STATUSES,
    )
    if blocking_round_records:
        rendered_rounds = ", ".join(
            f"`{str(meta.get('id') or path.stem)}` ({str(meta.get('status') or 'unknown').strip()})"
            for path, meta, _sections in blocking_round_records
        )
        raise SystemExit(
            f"cannot hard-pivot while durable blocking rounds remain against objective `{previous_objective_id}`: "
            f"{rendered_rounds}; close, capture, abandon, or explicitly re-scope them first"
        )

    blocking_task_contracts = find_task_contracts(
        args.project_id,
        objective_id=previous_objective_id,
        statuses=OPEN_TASK_CONTRACT_STATUSES,
    )
    if blocking_task_contracts:
        rendered_contracts = ", ".join(
            f"`{str(meta.get('id') or path.stem)}` ({str(meta.get('status') or 'unknown').strip()})"
            for path, meta, _sections in blocking_task_contracts
        )
        raise SystemExit(
            f"cannot hard-pivot while draft or active task contracts remain against objective `{previous_objective_id}`: "
            f"{rendered_contracts}; complete, abandon, invalidate, or retarget them first"
        )

    timestamp = timestamp_now()
    slug = slugify(args.title)
    objective_id = f"obj-{timestamp.strftime('%Y-%m-%d-%H%M')}-{slug}"
    objective_file_stem = f"{timestamp.strftime('%Y-%m-%d-%H%M')}-{slug}"
    pivot_slug = slugify(args.pivot_title or f"hard-pivot-{previous_objective_id}-to-{objective_id}")
    pivot_id = f"piv-{timestamp.strftime('%Y-%m-%d-%H%M')}-{pivot_slug}"
    pivot_file_stem = f"{timestamp.strftime('%Y-%m-%d-%H%M')}-{pivot_slug}"
    anchor = resolve_anchor(args.project_id)

    previous_superseded_by = list(previous_payload["superseded_by"])
    if objective_id not in previous_superseded_by:
        previous_superseded_by.append(objective_id)

    previous_objective_text = render_objective_file(
        objective_id=previous_objective_id,
        title=str(previous_payload["title"]),
        status="superseded",
        project_id=args.project_id,
        anchor=anchor,
        paths=list(previous_payload["paths"]),
        created_at=str(previous_payload["created_at"]) or timestamp.isoformat(timespec="seconds"),
        evidence_refs=list(previous_payload["evidence_refs"]),
        tags=merged_tags(
            list(previous_payload["tags"]),
            drop={"active"},
            add=["superseded"],
        ),
        confidence=str(previous_payload["confidence"]),
        phase=str(previous_payload["phase"]) or args.phase,
        supersedes=list(previous_payload["supersedes"]),
        superseded_by=previous_superseded_by,
        summary=str(previous_payload["summary"]),
        problem=str(previous_payload["problem"]),
        success_criteria=list(previous_payload["success_criteria"]),
        non_goals=list(previous_payload["non_goals"]),
        why_now=str(previous_payload["why_now"]),
        current_risks=list(previous_payload["current_risks"]),
        supersession_notes="\n\n".join(
            part
            for part in [
                str(previous_payload["supersession_notes"]),
                f"Superseded by `{objective_id}` because {args.trigger.strip()}",
            ]
            if part
        ),
    )
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
        change_summary=args.summary.strip() or args.problem.strip(),
        identity_rationale="A new objective id is required because the prior objective line was superseded rather than revised in place.",
        previous_objective=f"`{previous_objective_id}` {str(previous_payload['title']).strip()}".strip(),
        new_objective=f"`{objective_id}` {args.title}".strip(),
        evidence=[item.strip() for item in args.evidence if item.strip()],
        decisions_retained=[item.strip() for item in args.retained_decision if item.strip()],
        assumptions_invalidated=[item.strip() for item in args.invalidated_assumption if item.strip()],
        next_control_changes=[item.strip() for item in args.next_control_change if item.strip()],
    )
    pivot_path = pivots_dir(args.project_id) / f"{pivot_file_stem}.md"

    active_path = active_objective_path(args.project_id)
    active_objective_text = render_active_objective_file(
        objective_id=objective_id,
        phase=args.phase,
        status="active",
        problem=args.problem,
        success_criteria=args.success_criterion,
        non_goals=args.non_goal,
        why_now=args.why_now,
        current_risks=args.risk,
    )

    pivot_log = pivot_log_path(args.project_id)
    assert_objective_phase_command_contract(
        "record-hard-pivot",
        provided_inputs={
            "project_id",
            "previous_objective_id",
            "title",
            "problem",
            "success_criteria",
            "non_goals",
            "phase",
            "trigger",
        },
    )
    _side_effects, event_id, event_path = apply_transition_transaction(
        project_id=args.project_id,
        writes=[
            {"path": objective_path, "text": previous_objective_text, "label": "superseded objective"},
            {"path": new_objective_path, "text": new_objective_text, "label": "durable objective"},
            {"path": pivot_path, "text": pivot_text, "label": "durable pivot"},
            {"path": active_path, "text": active_objective_text, "label": "active objective projection"},
            {"path": pivot_log, "text": lambda: render_pivot_log_file(args.project_id), "label": "pivot-log projection"},
        ],
        command_name="record-hard-pivot",
        title=f"Recorded hard pivot from {previous_objective_id} to {objective_id}",
        anchor=anchor,
        previous_state=f"objective `{previous_objective_id}` was active",
        next_state=f"objective `{objective_id}` is now active and pivot `{pivot_id}` is recorded",
        guards=render_objective_phase_guard_lines(
            "record-hard-pivot",
            context={"previous_objective_id": previous_objective_id},
        ),
        evidence=[args.trigger] + [item.strip() for item in args.evidence if item.strip()],
        target_ids=[previous_objective_id, objective_id, pivot_id],
        event_file_stem=f"{pivot_file_stem}-record-hard-pivot",
    )

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
