#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json

from round_control import (
    active_objective_path,
    apply_transition_transaction,
    assert_exception_contract_command_contract,
    exception_contracts_dir,
    exception_ledger_path,
    load_active_objective,
    project_dir,
    render_exception_contract_guard_lines,
    render_exception_contract_file,
    render_exception_ledger_file,
    resolve_anchor,
    slugify,
    timestamp_now,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Create one active exception contract and project it into the exception ledger.")
    parser.add_argument("--project-id", required=True)
    parser.add_argument("--title", required=True)
    parser.add_argument("--slug")
    parser.add_argument("--objective-id")
    parser.add_argument("--summary", required=True)
    parser.add_argument("--reason", required=True)
    parser.add_argument("--temporary-behavior", required=True)
    parser.add_argument("--risk", required=True)
    parser.add_argument("--exit-condition", required=True)
    parser.add_argument("--owner-scope", action="append", required=True)
    parser.add_argument("--path", action="append", default=[])
    parser.add_argument("--evidence", action="append", default=[])
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    project_path = project_dir(args.project_id)
    if not project_path.exists():
        raise SystemExit(f"project directory not found: {project_path}")

    objective_preface, _objective_sections = load_active_objective(args.project_id)
    if not objective_preface:
        raise SystemExit(f"missing active objective: {active_objective_path(args.project_id)}")

    active_objective_id = objective_preface.get("objective id", "")
    objective_status = objective_preface.get("status", "")
    objective_id = (args.objective_id or active_objective_id).strip()
    if not objective_id:
        raise SystemExit("active objective is missing `Objective id`")
    if objective_status and objective_status != "active":
        raise SystemExit(f"cannot activate exception contract from non-active objective status `{objective_status}`")
    if objective_id != active_objective_id:
        raise SystemExit(
            f"exception contract objective `{objective_id}` does not match active objective `{active_objective_id}`"
        )

    timestamp = timestamp_now()
    slug = args.slug or slugify(args.title)
    file_stem = f"{timestamp.strftime('%Y-%m-%d-%H%M')}-{slug}"
    exception_contract_id = f"exc-{timestamp.strftime('%Y-%m-%d-%H%M')}-{slug}"
    anchor = resolve_anchor(args.project_id)

    exception_contract_text = render_exception_contract_file(
        exception_contract_id=exception_contract_id,
        title=args.title,
        status="active",
        project_id=args.project_id,
        objective_id=objective_id,
        pivot_id="",
        anchor=anchor,
        paths=[item.strip() for item in args.path if item.strip()],
        created_at=timestamp.isoformat(timespec="seconds"),
        evidence_refs=[],
        tags=["exception-contract", "control-plane"],
        confidence="high",
        phase="execution",
        summary=args.summary,
        reason=args.reason,
        temporary_behavior=args.temporary_behavior,
        risk=args.risk,
        exit_condition=args.exit_condition,
        owner_scope=[item.strip() for item in args.owner_scope if item.strip()],
        evidence=[item.strip() for item in args.evidence if item.strip()],
        resolution="",
    )
    contract_path = exception_contracts_dir(args.project_id) / f"{file_stem}.md"
    ledger_path = exception_ledger_path(args.project_id)
    assert_exception_contract_command_contract(
        "activate-exception-contract",
        provided_inputs={"project_id", "title", "summary", "reason", "temporary_behavior", "risk", "owner_scope", "exit_condition"},
        satisfied_guard_codes={"active_objective_available", "exception_contract_required_fields_present"},
        write_targets={"durable:exception-contract", "control:exception-ledger", "memory:transition-event"},
        durable_owners={"memory:exception-contract"},
        projection_owners={"control:exception-ledger"},
        artifact_owners=set(),
        live_inspection_owners=set(),
    )
    _side_effects, event_id, event_path = apply_transition_transaction(
        project_id=args.project_id,
        writes=[
            {"path": contract_path, "text": exception_contract_text, "label": "durable exception contract"},
            {"path": ledger_path, "text": lambda: render_exception_ledger_file(args.project_id), "label": "exception-ledger projection"},
        ],
        command_name="activate-exception-contract",
        title=f"Activated exception contract {exception_contract_id}",
        anchor=anchor,
        previous_state="exception contract did not exist",
        next_state=f"exception contract `{exception_contract_id}` is now active on objective `{objective_id}`",
        guards=render_exception_contract_guard_lines(
            "activate-exception-contract",
            context={"objective_id": objective_id},
        ),
        evidence=[args.reason, args.exit_condition, *[item.strip() for item in args.evidence if item.strip()]],
        target_ids=[exception_contract_id, objective_id],
        event_file_stem=f"{file_stem}-activate-exception-contract",
    )

    print(
        json.dumps(
            {
                "project_id": args.project_id,
                "exception_contract_id": exception_contract_id,
                "objective_id": objective_id,
                "exception_contract_path": str(contract_path),
                "exception_ledger_path": str(ledger_path),
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
