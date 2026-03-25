#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json

from kernel.round_control import (
    OPEN_ROUND_STATUSES,
    active_objective_path,
    apply_transition_transaction,
    assert_no_unresolved_task_contracts,
    assert_objective_phase_command_contract,
    find_exception_contracts,
    find_rounds,
    merged_tags,
    objective_record_payload,
    pivot_log_path,
    project_dir,
    render_objective_phase_guard_lines,
    render_objective_file,
    render_pivot_log_file,
    resolve_active_objective_record,
    resolve_anchor,
    timestamp_now,
)


ALLOWED_CLOSING_STATUSES = {"closed", "invalidated"}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Close the active objective line without creating a successor objective.")
    parser.add_argument("--project-id", required=True)
    parser.add_argument("--objective-id")
    parser.add_argument("--closing-status", required=True, choices=sorted(ALLOWED_CLOSING_STATUSES))
    parser.add_argument("--reason", required=True)
    parser.add_argument("--evidence", action="append", default=[])
    parser.add_argument("--supersession-note", default="")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if not project_dir(args.project_id).exists():
        raise SystemExit(f"project directory not found: {project_dir(args.project_id)}")

    objective_path, meta, sections, objective_id = resolve_active_objective_record(
        args.project_id,
        objective_id=args.objective_id or "",
    )
    payload = objective_record_payload(meta, sections)

    blocking_rounds = find_rounds(
        args.project_id,
        objective_id=objective_id,
        statuses=OPEN_ROUND_STATUSES,
    )
    if blocking_rounds:
        rendered_rounds = ", ".join(
            f"`{str(round_meta.get('id') or round_path.stem)}` ({str(round_meta.get('status') or 'unknown').strip()})"
            for round_path, round_meta, _round_sections in blocking_rounds
        )
        raise SystemExit(
            f"cannot close objective `{objective_id}` while durable open rounds remain attached: {rendered_rounds}; "
            "close, capture, or abandon those rounds first"
        )

    assert_no_unresolved_task_contracts(
        args.project_id,
        objective_id=objective_id,
        transition_target=f"close objective `{objective_id}`",
        remediation="complete, abandon, or invalidate those task contracts first",
    )

    active_exception_contracts = find_exception_contracts(
        args.project_id,
        objective_id=objective_id,
        statuses={"active"},
    )
    if active_exception_contracts:
        rendered_contracts = ", ".join(
            f"`{str(contract_meta.get('id') or contract_path.stem)}`"
            for contract_path, contract_meta, _contract_sections in active_exception_contracts
        )
        raise SystemExit(
            f"cannot close objective `{objective_id}` while active exception contracts remain attached: {rendered_contracts}; "
            "retire or invalidate them first"
        )

    anchor = resolve_anchor(args.project_id)
    closure_note = f"{args.closing_status.capitalize()} because {args.reason.strip()}"
    if args.supersession_note.strip():
        closure_note = f"{closure_note}\n\n{args.supersession_note.strip()}"

    objective_text = render_objective_file(
        objective_id=objective_id,
        title=str(payload["title"]),
        status=args.closing_status,
        project_id=args.project_id,
        anchor=anchor,
        paths=list(payload["paths"]),
        created_at=str(payload["created_at"]) or timestamp_now().isoformat(timespec="seconds"),
        evidence_refs=list(payload["evidence_refs"]),
        tags=merged_tags(
            list(payload["tags"]),
            drop={"active", "superseded", "closed", "invalidated"},
            add=[args.closing_status],
        ),
        confidence=str(payload["confidence"]),
        phase=str(payload["phase"]),
        supersedes=list(payload["supersedes"]),
        superseded_by=list(payload["superseded_by"]),
        summary=str(payload["summary"]),
        problem=str(payload["problem"]),
        success_criteria=list(payload["success_criteria"]),
        non_goals=list(payload["non_goals"]),
        why_now=str(payload["why_now"]),
        current_risks=list(payload["current_risks"]),
        supersession_notes="\n\n".join(
            part
            for part in [str(payload["supersession_notes"]), closure_note]
            if part
        ),
    )

    active_path = active_objective_path(args.project_id)
    pivot_path = pivot_log_path(args.project_id)
    timestamp = timestamp_now().strftime("%Y-%m-%d-%H%M%S")
    assert_objective_phase_command_contract(
        "close-objective",
        provided_inputs={"project_id", "objective_id", "closing_status", "reason"},
    )
    _side_effects, event_id, event_path = apply_transition_transaction(
        project_id=args.project_id,
        writes=[
            {"path": objective_path, "text": objective_text, "label": "durable objective"},
            {"path": active_path, "text": None, "label": "active objective projection"},
            {"path": pivot_path, "text": lambda: render_pivot_log_file(args.project_id), "label": "pivot-log projection"},
        ],
        command_name="close-objective",
        title=f"Closed objective {objective_id} as {args.closing_status}",
        anchor=anchor,
        previous_state=f"objective `{objective_id}` was active",
        next_state=f"objective `{objective_id}` is now `{args.closing_status}` and no active objective remains",
        guards=render_objective_phase_guard_lines(
            "close-objective",
            context={"objective_id": objective_id, "closing_status": args.closing_status},
        ),
        evidence=[args.reason] + [item.strip() for item in args.evidence if item.strip()],
        target_ids=[objective_id],
        event_file_stem=f"{timestamp}-{objective_id}-{args.closing_status}",
    )

    print(
        json.dumps(
            {
                "project_id": args.project_id,
                "objective_id": objective_id,
                "closing_status": args.closing_status,
                "objective_path": str(objective_path),
                "active_objective_path": str(active_path),
                "pivot_log_path": str(pivot_path),
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

