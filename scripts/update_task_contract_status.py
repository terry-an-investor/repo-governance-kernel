#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json

from round_control import (
    OPEN_TASK_CONTRACT_STATUSES,
    TASK_CONTRACT_STATUS_TRANSITIONS,
    apply_transition_transaction,
    assert_task_contract_command_contract,
    load_task_contract_file,
    locate_task_contract_file,
    project_dir,
    render_task_contract_file,
    render_task_contract_guard_lines,
    resolve_anchor,
    task_contract_record_payload,
    timestamp_now,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Update the status of one durable task contract.")
    parser.add_argument("--project-id", required=True)
    parser.add_argument("--task-contract-id", required=True)
    parser.add_argument("--status", required=True, choices=sorted(TASK_CONTRACT_STATUS_TRANSITIONS))
    parser.add_argument("--reason", required=True)
    parser.add_argument("--resolution", action="append", default=[])
    parser.add_argument("--risk", action="append", default=[])
    parser.add_argument("--status-note", action="append", default=[])
    return parser.parse_args()


def _clean_list(values: list[str]) -> list[str]:
    return [value.strip() for value in values if value.strip()]


def main() -> int:
    args = parse_args()
    if not project_dir(args.project_id).exists():
        raise SystemExit(f"project directory not found: {project_dir(args.project_id)}")

    task_contract_path = locate_task_contract_file(args.project_id, args.task_contract_id)
    if task_contract_path is None:
        raise SystemExit(f"task-contract file not found for `{args.task_contract_id}`")

    meta, sections = load_task_contract_file(task_contract_path)
    payload = task_contract_record_payload(meta, sections)
    previous_status = str(payload["status"]).strip()
    if not previous_status:
        raise SystemExit(f"task contract `{args.task_contract_id}` is missing status")

    allowed = TASK_CONTRACT_STATUS_TRANSITIONS.get(previous_status, set())
    if args.status not in allowed:
        raise SystemExit(
            f"illegal task-contract transition `{previous_status} -> {args.status}` for `{args.task_contract_id}`"
        )

    resolution = list(payload["resolution"]) + _clean_list(args.resolution)
    if args.status == "completed" and not resolution:
        raise SystemExit("completed task-contract status requires at least one --resolution entry")

    risks = list(payload["risks"]) + _clean_list(args.risk)
    status_note_parts = [str(payload["status_notes"]).strip(), f"{previous_status} -> {args.status}: {args.reason.strip()}"]
    if resolution and args.status == "completed":
        status_note_parts.append("resolution recorded:\n" + "\n".join(f"- {item}" for item in resolution))
    status_note_parts.extend(_clean_list(args.status_note))
    status_notes = "\n\n".join(part for part in status_note_parts if part).strip()

    anchor = resolve_anchor(args.project_id)
    task_contract_text = render_task_contract_file(
        task_contract_id=args.task_contract_id,
        title=str(payload["title"]),
        status=args.status,
        project_id=args.project_id,
        objective_id=str(payload["objective_id"]),
        round_id=str(payload["round_id"]),
        anchor=anchor,
        paths=list(payload["paths"]),
        created_at=str(payload["created_at"]) or timestamp_now().isoformat(timespec="seconds"),
        evidence_refs=list(payload["evidence_refs"]),
        tags=list(payload["tags"]),
        confidence=str(payload["confidence"]),
        phase=str(payload["phase"]) or "execution",
        summary=str(payload["summary"]),
        intent=str(payload["intent"]),
        allowed_changes=list(payload["allowed_changes"]),
        forbidden_changes=list(payload["forbidden_changes"]),
        completion_criteria=list(payload["completion_criteria"]),
        resolution=resolution,
        risks=risks,
        status_notes=status_notes,
    )

    assert_task_contract_command_contract(
        "update-task-contract-status",
        provided_inputs={"project_id", "task_contract_id", "status", "reason"},
    )
    timestamp = timestamp_now().strftime("%Y-%m-%d-%H%M%S")
    _side_effects, event_id, event_path = apply_transition_transaction(
        project_id=args.project_id,
        writes=[
            {"path": task_contract_path, "text": task_contract_text, "label": "durable task contract"},
        ],
        command_name="update-task-contract-status",
        title=f"Updated task contract {args.task_contract_id} to {args.status}",
        anchor=anchor,
        previous_state=f"task contract `{args.task_contract_id}` status `{previous_status}`",
        next_state=f"task contract `{args.task_contract_id}` is now `{args.status}`",
        guards=render_task_contract_guard_lines(
            "update-task-contract-status",
            context={
                "task_contract_id": args.task_contract_id,
                "previous_status": previous_status,
                "next_status": args.status,
            },
        ),
        evidence=[args.reason, *_clean_list(args.resolution)],
        target_ids=[args.task_contract_id, str(payload["round_id"]), str(payload["objective_id"])],
        event_file_stem=f"{timestamp}-{args.task_contract_id}-{args.status}",
    )

    print(
        json.dumps(
            {
                "project_id": args.project_id,
                "task_contract_id": args.task_contract_id,
                "previous_status": previous_status,
                "status": args.status,
                "task_contract_path": str(task_contract_path),
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
