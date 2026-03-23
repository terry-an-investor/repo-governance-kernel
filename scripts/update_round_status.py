#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json

from round_control import (
    OPEN_ROUND_STATUSES,
    active_round_path,
    apply_transition_transaction,
    load_active_round,
    load_round_file,
    locate_round_file,
    parse_bullet_list,
    project_dir,
    render_active_round_file,
    render_round_file,
    resolve_anchor,
    timestamp_now,
    transition_events_dir,
)


ALLOWED_TRANSITIONS = {
    "draft": {"active", "abandoned"},
    "active": {"blocked", "validation_pending", "abandoned"},
    "blocked": {"active", "abandoned"},
    "validation_pending": {"captured", "blocked", "abandoned"},
    "captured": {"closed"},
    "closed": set(),
    "abandoned": set(),
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Update the status of an existing round.")
    parser.add_argument("--project-id", required=True)
    parser.add_argument("--status", required=True, choices=sorted(ALLOWED_TRANSITIONS))
    parser.add_argument("--round-id")
    parser.add_argument("--reason", required=True)
    parser.add_argument("--validated-by", action="append", default=[])
    parser.add_argument("--blocker", action="append", default=[])
    parser.add_argument("--risk", action="append", default=[])
    parser.add_argument("--clear-blockers", action="store_true")
    return parser.parse_args()


def normalize_section_text(text: str) -> str:
    value = text.strip()
    return "" if value in {"", "_none recorded_"} else value


def main() -> int:
    args = parse_args()
    if not project_dir(args.project_id).exists():
        raise SystemExit(f"project directory not found: {project_dir(args.project_id)}")

    active_round_preface, _active_round_sections = load_active_round(args.project_id)
    round_id = args.round_id or active_round_preface.get("round id", "")
    if not round_id:
        raise SystemExit("missing round id; pass --round-id or maintain control/active-round.md")

    round_path = locate_round_file(args.project_id, round_id)
    if round_path is None:
        raise SystemExit(f"round file not found for `{round_id}`")

    meta, sections = load_round_file(round_path)
    previous_status = str(meta.get("status") or "").strip()
    if not previous_status:
        raise SystemExit(f"round `{round_id}` is missing status")

    allowed = ALLOWED_TRANSITIONS.get(previous_status, set())
    if args.status not in allowed:
        raise SystemExit(f"illegal transition `{previous_status} -> {args.status}` for round `{round_id}`")

    if args.status == "captured" and not args.validated_by:
        raise SystemExit("captured status requires at least one --validated-by entry")

    title = str(meta.get("title") or round_id)
    objective_id = str(meta.get("objective_id") or active_round_preface.get("objective id", "")).strip()
    paths = [str(item).strip() for item in meta.get("paths", []) if str(item).strip()]
    created_at = str(meta.get("created_at") or "").strip() or timestamp_now().isoformat(timespec="seconds")
    evidence_refs = [entry for entry in meta.get("evidence_refs", []) if isinstance(entry, dict)]
    tags = [str(item).strip() for item in meta.get("tags", []) if str(item).strip()]
    confidence = str(meta.get("confidence") or "high").strip() or "high"
    phase = str(meta.get("phase") or "execution").strip() or "execution"
    summary = normalize_section_text(sections.get("Summary", ""))
    scope_items = parse_bullet_list(sections.get("Scope", ""))
    deliverable = normalize_section_text(sections.get("Deliverable", ""))
    validation_plan_parts = [normalize_section_text(sections.get("Validation Plan", ""))]
    validation_plan_parts.extend(item.strip() for item in args.validated_by if item.strip())
    validation_plan = "\n".join(part for part in validation_plan_parts if part).strip()

    existing_risks = parse_bullet_list(sections.get("Active Risks", ""))
    risks = existing_risks + [item.strip() for item in args.risk if item.strip()]

    if args.clear_blockers:
        blockers = [item.strip() for item in args.blocker if item.strip()]
    else:
        blockers = parse_bullet_list(sections.get("Blockers", "")) + [item.strip() for item in args.blocker if item.strip()]

    status_notes_parts = [normalize_section_text(sections.get("Status Notes", "")), f"{previous_status} -> {args.status}: {args.reason.strip()}"]
    if args.validated_by:
        status_notes_parts.append("validated by:\n" + "\n".join(f"- {item.strip()}" for item in args.validated_by if item.strip()))
    status_notes = "\n\n".join(part for part in status_notes_parts if part).strip()

    anchor = resolve_anchor(args.project_id)
    round_text = render_round_file(
        round_id=round_id,
        title=title,
        status=args.status,
        project_id=args.project_id,
        objective_id=objective_id,
        anchor=anchor,
        paths=paths,
        created_at=created_at,
        evidence_refs=evidence_refs,
        tags=tags,
        confidence=confidence,
        phase=phase,
        summary=summary,
        scope_items=scope_items,
        deliverable=deliverable,
        validation_plan=validation_plan,
        risks=risks,
        blockers=blockers,
        status_notes=status_notes,
    )
    control_path = active_round_path(args.project_id)
    active_round_text = None
    control_write: dict[str, object] = {"path": control_path, "text": None, "label": "active round projection"}
    if args.status in OPEN_ROUND_STATUSES:
        active_round_text = render_active_round_file(
            round_id=round_id,
            objective_id=objective_id,
            status=args.status,
            scope_items=scope_items,
            deliverable=deliverable,
            validation_plan=validation_plan,
            risks=risks,
            blockers=blockers,
        )
        control_write["text"] = active_round_text

    next_state = f"round `{round_id}` is now `{args.status}`"
    guards = [
        f"round `{round_id}` exists",
        f"transition `{previous_status} -> {args.status}` is legal",
    ]
    if args.status == "captured":
        guards.append("captured status includes at least one validation record")
    evidence = [args.reason] + [item.strip() for item in args.validated_by if item.strip()]
    timestamp = timestamp_now().strftime("%Y-%m-%d-%H%M%S")
    _side_effects, event_id, event_path = apply_transition_transaction(
        project_id=args.project_id,
        writes=[
            {"path": round_path, "text": round_text, "label": "durable round contract"},
            control_write,
        ],
        command_name="update-round-status",
        title=f"Updated round {round_id} to {args.status}",
        anchor=anchor,
        previous_state=f"round `{round_id}` status `{previous_status}`",
        next_state=next_state,
        guards=guards,
        evidence=evidence,
        target_ids=[round_id, objective_id],
        event_file_stem=f"{timestamp}-{round_id}-{args.status}",
    )

    print(
        json.dumps(
            {
                "project_id": args.project_id,
                "round_id": round_id,
                "previous_status": previous_status,
                "status": args.status,
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
