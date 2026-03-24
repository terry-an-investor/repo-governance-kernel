#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json

from kernel.round_control import (
    apply_transition_transaction,
    assert_exception_contract_command_contract,
    exception_ledger_path,
    load_exception_contract_file,
    locate_exception_contract_file,
    locate_pivot_file,
    parse_bullet_list,
    project_dir,
    render_exception_contract_guard_lines,
    render_exception_contract_file,
    render_exception_ledger_file,
    resolve_anchor,
    timestamp_now,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Invalidate one active exception contract and refresh the exception ledger.")
    parser.add_argument("--project-id", required=True)
    parser.add_argument("--exception-contract-id", required=True)
    parser.add_argument("--reason", required=True)
    parser.add_argument("--pivot-id")
    parser.add_argument("--evidence", action="append", default=[])
    return parser.parse_args()


def normalize_section(text: str) -> str:
    value = text.strip()
    return "" if value in {"", "_none recorded_"} else value


def main() -> int:
    args = parse_args()
    if not project_dir(args.project_id).exists():
        raise SystemExit(f"project directory not found: {project_dir(args.project_id)}")

    contract_path = locate_exception_contract_file(args.project_id, args.exception_contract_id)
    if contract_path is None:
        raise SystemExit(f"exception contract file not found for `{args.exception_contract_id}`")
    if args.pivot_id and locate_pivot_file(args.project_id, args.pivot_id) is None:
        raise SystemExit(f"pivot `{args.pivot_id}` not found for project `{args.project_id}`")

    meta, sections = load_exception_contract_file(contract_path)
    previous_status = str(meta.get("status") or "").strip()
    if previous_status != "active":
        raise SystemExit(
            f"only active exception contracts can be invalidated honestly; `{args.exception_contract_id}` is `{previous_status or 'unknown'}`"
        )

    anchor = resolve_anchor(args.project_id)
    evidence = [item.strip() for item in args.evidence if item.strip()]
    resolution_parts = [normalize_section(sections.get("Resolution", "")), f"active -> invalidated: {args.reason.strip()}"]
    if args.pivot_id:
        resolution_parts.append(f"pivot: `{args.pivot_id}`")
    if evidence:
        resolution_parts.append("evidence:\n" + "\n".join(f"- {item}" for item in evidence))
    resolution = "\n\n".join(part for part in resolution_parts if part).strip()

    contract_text = render_exception_contract_file(
        exception_contract_id=str(meta.get("id") or "").strip(),
        title=str(meta.get("title") or "").strip(),
        status="invalidated",
        project_id=str(meta.get("project_id") or args.project_id).strip(),
        objective_id=str(meta.get("objective_id") or "").strip(),
        pivot_id=(args.pivot_id or str(meta.get("pivot_id") or "")).strip(),
        anchor=anchor,
        paths=[str(item).strip() for item in meta.get("paths", []) if str(item).strip()],
        created_at=str(meta.get("created_at") or "").strip() or timestamp_now().isoformat(timespec="seconds"),
        evidence_refs=[entry for entry in meta.get("evidence_refs", []) if isinstance(entry, dict)],
        tags=[str(item).strip() for item in meta.get("tags", []) if str(item).strip()],
        confidence=str(meta.get("confidence") or "high").strip() or "high",
        phase=str(meta.get("phase") or "execution").strip() or "execution",
        summary=normalize_section(sections.get("Summary", "")),
        reason=normalize_section(sections.get("Reason", "")),
        temporary_behavior=normalize_section(sections.get("Temporary Behavior", "")),
        risk=normalize_section(sections.get("Risk", "")),
        exit_condition=normalize_section(sections.get("Exit Condition", "")),
        owner_scope=parse_bullet_list(sections.get("Owner Scope", "")),
        evidence=[*parse_bullet_list(sections.get("Evidence", "")), *evidence],
        resolution=resolution,
    )
    ledger_path = exception_ledger_path(args.project_id)
    timestamp = timestamp_now().strftime("%Y-%m-%d-%H%M%S")
    assert_exception_contract_command_contract(
        "invalidate-exception-contract",
        provided_inputs={"project_id", "exception_contract_id", "reason"},
    )
    _side_effects, event_id, event_path = apply_transition_transaction(
        project_id=args.project_id,
        writes=[
            {"path": contract_path, "text": contract_text, "label": "durable exception contract"},
            {"path": ledger_path, "text": lambda: render_exception_ledger_file(args.project_id), "label": "exception-ledger projection"},
        ],
        command_name="invalidate-exception-contract",
        title=f"Invalidated exception contract {args.exception_contract_id}",
        anchor=anchor,
        previous_state=f"exception contract `{args.exception_contract_id}` status `{previous_status}`",
        next_state=f"exception contract `{args.exception_contract_id}` is now `invalidated`",
        guards=render_exception_contract_guard_lines(
            "invalidate-exception-contract",
            context={"exception_contract_id": args.exception_contract_id, "pivot_id": (args.pivot_id or "").strip()},
        ),
        evidence=[args.reason, *([args.pivot_id] if args.pivot_id else []), *evidence],
        target_ids=[args.exception_contract_id, str(meta.get("objective_id") or "").strip(), (args.pivot_id or "").strip()],
        event_file_stem=f"{timestamp}-{args.exception_contract_id}-invalidated",
    )

    print(
        json.dumps(
            {
                "project_id": args.project_id,
                "exception_contract_id": args.exception_contract_id,
                "previous_status": previous_status,
                "status": "invalidated",
                "pivot_id": (args.pivot_id or "").strip(),
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

