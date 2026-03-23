#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json

from round_control import (
    build_transition_event_file,
    exception_ledger_path,
    load_exception_contract_file,
    locate_exception_contract_file,
    parse_bullet_list,
    project_dir,
    render_exception_contract_file,
    render_exception_ledger_file,
    resolve_anchor,
    timestamp_now,
    transition_events_dir,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Retire one active exception contract and refresh the exception ledger.")
    parser.add_argument("--project-id", required=True)
    parser.add_argument("--exception-contract-id", required=True)
    parser.add_argument("--reason", required=True)
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

    meta, sections = load_exception_contract_file(contract_path)
    previous_status = str(meta.get("status") or "").strip()
    if previous_status != "active":
        raise SystemExit(
            f"only active exception contracts can be retired honestly; `{args.exception_contract_id}` is `{previous_status or 'unknown'}`"
        )

    anchor = resolve_anchor(args.project_id)
    evidence = [item.strip() for item in args.evidence if item.strip()]
    resolution_parts = [normalize_section(sections.get("Resolution", "")), f"active -> retired: {args.reason.strip()}"]
    if evidence:
        resolution_parts.append("evidence:\n" + "\n".join(f"- {item}" for item in evidence))
    resolution = "\n\n".join(part for part in resolution_parts if part).strip()

    contract_text = render_exception_contract_file(
        exception_contract_id=str(meta.get("id") or "").strip(),
        title=str(meta.get("title") or "").strip(),
        status="retired",
        project_id=str(meta.get("project_id") or args.project_id).strip(),
        objective_id=str(meta.get("objective_id") or "").strip(),
        pivot_id=str(meta.get("pivot_id") or "").strip(),
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
    contract_path.write_text(contract_text, encoding="utf-8")

    ledger_path = exception_ledger_path(args.project_id)
    ledger_path.parent.mkdir(parents=True, exist_ok=True)
    ledger_path.write_text(render_exception_ledger_file(args.project_id), encoding="utf-8")

    event_id, event_text = build_transition_event_file(
        project_id=args.project_id,
        command_name="retire-exception-contract",
        title=f"Retired exception contract {args.exception_contract_id}",
        anchor=anchor,
        previous_state=f"exception contract `{args.exception_contract_id}` status `{previous_status}`",
        next_state=f"exception contract `{args.exception_contract_id}` is now `retired`",
        guards=[
            f"exception contract `{args.exception_contract_id}` exists",
            "only active exception contracts can be retired",
        ],
        side_effects=[
            f"updated durable exception contract `{contract_path.relative_to(project_dir(args.project_id).parent).as_posix()}`",
            f"updated `{ledger_path.relative_to(project_dir(args.project_id).parent).as_posix()}`",
        ],
        evidence=[args.reason, *evidence],
        target_ids=[args.exception_contract_id, str(meta.get("objective_id") or "").strip()],
    )
    event_path = transition_events_dir(args.project_id) / f"{timestamp_now().strftime('%Y-%m-%d-%H%M%S')}-{args.exception_contract_id}-retired.md"
    event_path.parent.mkdir(parents=True, exist_ok=True)
    event_path.write_text(event_text, encoding="utf-8")

    print(
        json.dumps(
            {
                "project_id": args.project_id,
                "exception_contract_id": args.exception_contract_id,
                "previous_status": previous_status,
                "status": "retired",
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
