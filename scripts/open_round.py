#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path

from round_control import (
    active_objective_path,
    active_round_path,
    apply_transition_transaction,
    assert_round_command_contract,
    durable_markdown_path,
    load_active_objective,
    load_active_round,
    project_dir,
    render_round_guard_lines,
    render_active_round_file,
    render_round_file,
    resolve_anchor,
    rounds_dir,
    slugify,
    timestamp_now,
)


ACTIVE_ROUND_BLOCKING_STATUSES = {"active", "blocked", "validation_pending"}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Open a new active round contract.")
    parser.add_argument("--project-id", required=True)
    parser.add_argument("--title", required=True)
    parser.add_argument("--slug")
    parser.add_argument("--objective-id")
    parser.add_argument("--scope-item", action="append", required=True)
    parser.add_argument("--scope-path", action="append", default=[])
    parser.add_argument("--deliverable", required=True)
    parser.add_argument("--validation-plan", required=True)
    parser.add_argument("--risk", action="append", default=[])
    parser.add_argument("--blocker", action="append", default=[])
    parser.add_argument("--status-note", default="")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    project_path = project_dir(args.project_id)
    if not project_path.exists():
        raise SystemExit(f"project directory not found: {project_path}")

    objective_preface, _objective_sections = load_active_objective(args.project_id)
    if not objective_preface:
        raise SystemExit(f"missing active objective: {active_objective_path(args.project_id)}")

    objective_id = args.objective_id or objective_preface.get("objective id", "")
    objective_status = objective_preface.get("status", "")
    objective_phase = objective_preface.get("phase", "")
    if not objective_id:
        raise SystemExit("active objective is missing `Objective id`")
    if objective_status and objective_status != "active":
        raise SystemExit(f"cannot open round from non-active objective status `{objective_status}`")
    if objective_phase and objective_phase != "execution":
        raise SystemExit(
            f"cannot open round for objective `{objective_id}` while active phase is `{objective_phase}`; "
            "move the objective into `execution` first"
        )

    existing_round_preface, _existing_round_sections = load_active_round(args.project_id)
    existing_round_id = existing_round_preface.get("round id", "")
    existing_round_status = existing_round_preface.get("status", "")
    if existing_round_id and existing_round_status in ACTIVE_ROUND_BLOCKING_STATUSES:
        raise SystemExit(
            f"cannot open a new round while `{existing_round_id}` is still `{existing_round_status}`; "
            "close, capture, block, or abandon it honestly first"
        )

    slug = args.slug or slugify(args.title)
    timestamp = timestamp_now()
    file_stem = f"{timestamp.strftime('%Y-%m-%d-%H%M')}-{slug}"
    round_id = f"round-{timestamp.strftime('%Y-%m-%d-%H%M')}-{slug}"
    anchor = resolve_anchor(args.project_id)

    round_text = render_round_file(
        round_id=round_id,
        title=args.title,
        status="active",
        project_id=args.project_id,
        objective_id=objective_id,
        anchor=anchor,
        paths=args.scope_path,
        created_at=timestamp.isoformat(timespec="seconds"),
        evidence_refs=[],
        tags=["round", "control-plane"],
        confidence="high",
        phase="execution",
        summary=args.deliverable,
        scope_items=args.scope_item,
        deliverable=args.deliverable,
        validation_plan=args.validation_plan,
        risks=args.risk,
        blockers=args.blocker,
        status_notes=args.status_note,
    )
    active_round_text = render_active_round_file(
        round_id=round_id,
        objective_id=objective_id,
        status="active",
        scope_items=args.scope_item,
        deliverable=args.deliverable,
        validation_plan=args.validation_plan,
        risks=args.risk,
        blockers=args.blocker,
    )

    round_path = durable_markdown_path(rounds_dir(args.project_id), file_stem)
    control_path = active_round_path(args.project_id)

    previous_state = (
        f"previous active round: `{existing_round_id}` status `{existing_round_status}`"
        if existing_round_id
        else "no active round was present"
    )
    next_state = f"round `{round_id}` is now active for objective `{objective_id}`"
    assert_round_command_contract(
        "open-round",
        provided_inputs={"project_id", "title", "scope_item", "deliverable", "validation_plan"},
    )
    guards = render_round_guard_lines("open-round", context={"objective_id": objective_id})
    evidence = [args.validation_plan]
    _side_effects, event_id, event_path = apply_transition_transaction(
        project_id=args.project_id,
        writes=[
            {"path": round_path, "text": round_text, "label": "durable round contract"},
            {"path": control_path, "text": active_round_text, "label": "active round projection"},
        ],
        command_name="open-round",
        title=f"Opened round {round_id}",
        anchor=anchor,
        previous_state=previous_state,
        next_state=next_state,
        guards=guards,
        evidence=evidence,
        target_ids=[round_id, objective_id],
        event_file_stem=f"{file_stem}-open-round",
    )

    print(
        json.dumps(
            {
                "project_id": args.project_id,
                "round_id": round_id,
                "objective_id": objective_id,
                "round_path": str(round_path),
                "active_round_path": str(control_path),
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
