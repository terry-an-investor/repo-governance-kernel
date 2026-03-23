#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json

from round_control import (
    OPEN_ROUND_STATUSES,
    active_round_path,
    apply_transition_transaction,
    assert_round_command_contract,
    load_active_round,
    load_round_file,
    locate_round_file,
    parse_bullet_list,
    project_dir,
    render_round_guard_lines,
    render_active_round_file,
    render_round_file,
    resolve_anchor,
    timestamp_now,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Rewrite one open round contract without changing its identity.")
    parser.add_argument("--project-id", required=True)
    parser.add_argument("--round-id")
    parser.add_argument("--reason", required=True)
    parser.add_argument("--title")
    parser.add_argument("--summary")
    parser.add_argument("--scope-item", action="append", default=[])
    parser.add_argument("--deliverable")
    parser.add_argument("--validation-plan")
    parser.add_argument("--risk", action="append", default=[])
    parser.add_argument("--blocker", action="append", default=[])
    parser.add_argument("--status-note", action="append", default=[])
    parser.add_argument("--scope-path", action="append", default=[])
    parser.add_argument("--replace-scope-items", action="store_true")
    parser.add_argument("--replace-risks", action="store_true")
    parser.add_argument("--replace-blockers", action="store_true")
    parser.add_argument("--replace-scope-paths", action="store_true")
    return parser.parse_args()


def _clean_list(values: list[str]) -> list[str]:
    return [value.strip() for value in values if value.strip()]


def _merge_lists(existing: list[str], additions: list[str], *, replace: bool) -> list[str]:
    if replace:
        return additions
    merged = list(existing)
    for item in additions:
        if item not in merged:
            merged.append(item)
    return merged


def main() -> int:
    args = parse_args()
    if not project_dir(args.project_id).exists():
        raise SystemExit(f"project directory not found: {project_dir(args.project_id)}")

    active_round_preface, _ = load_active_round(args.project_id)
    round_id = (args.round_id or active_round_preface.get("round id", "")).strip()
    if not round_id:
        raise SystemExit("missing round id; pass --round-id or maintain control/active-round.md")

    round_path = locate_round_file(args.project_id, round_id)
    if round_path is None:
        raise SystemExit(f"round file not found for `{round_id}`")

    meta, sections = load_round_file(round_path)
    previous_status = str(meta.get("status") or "").strip()
    if previous_status not in OPEN_ROUND_STATUSES:
        raise SystemExit(
            f"rewrite-open-round requires an open round status in {sorted(OPEN_ROUND_STATUSES)}; found `{previous_status}`"
        )

    previous_scope_items = parse_bullet_list(str(sections.get("Scope", "")))
    previous_risks = parse_bullet_list(str(sections.get("Active Risks", "")))
    previous_blockers = parse_bullet_list(str(sections.get("Blockers", "")))
    previous_paths = [str(item).strip() for item in meta.get("paths", []) if str(item).strip()]
    previous_status_notes = str(sections.get("Status Notes", "")).strip()

    next_title = (args.title or str(meta.get("title") or round_id)).strip()
    next_summary = (args.summary or str(sections.get("Summary", ""))).strip()
    next_scope_items = _merge_lists(previous_scope_items, _clean_list(args.scope_item), replace=args.replace_scope_items)
    next_deliverable = (args.deliverable or str(sections.get("Deliverable", ""))).strip()
    next_validation_plan = (args.validation_plan or str(sections.get("Validation Plan", ""))).strip()
    next_risks = _merge_lists(previous_risks, _clean_list(args.risk), replace=args.replace_risks)
    next_blockers = _merge_lists(previous_blockers, _clean_list(args.blocker), replace=args.replace_blockers)
    next_paths = _merge_lists(previous_paths, _clean_list(args.scope_path), replace=args.replace_scope_paths)
    next_status_notes = "\n\n".join(
        part
        for part in [
            previous_status_notes,
            f"Round rewritten because {args.reason.strip()}",
            *[item for item in _clean_list(args.status_note)],
        ]
        if part
    ).strip()

    if not next_scope_items:
        raise SystemExit("rewrite-open-round requires at least one scope item")
    if not next_deliverable:
        raise SystemExit("rewrite-open-round requires a deliverable")
    if not next_validation_plan:
        raise SystemExit("rewrite-open-round requires a validation plan")
    if not next_paths:
        raise SystemExit("rewrite-open-round requires at least one scope path")

    changed_fields: list[str] = []
    if next_title != str(meta.get("title") or round_id).strip():
        changed_fields.append("title")
    if next_summary != str(sections.get("Summary", "")).strip():
        changed_fields.append("summary")
    if next_scope_items != previous_scope_items:
        changed_fields.append("scope_items")
    if next_deliverable != str(sections.get("Deliverable", "")).strip():
        changed_fields.append("deliverable")
    if next_validation_plan != str(sections.get("Validation Plan", "")).strip():
        changed_fields.append("validation_plan")
    if next_risks != previous_risks:
        changed_fields.append("risks")
    if next_blockers != previous_blockers:
        changed_fields.append("blockers")
    if next_paths != previous_paths:
        changed_fields.append("paths")
    if not changed_fields:
        raise SystemExit("rewrite-open-round produced no material round change")

    anchor = resolve_anchor(args.project_id)
    round_text = render_round_file(
        round_id=round_id,
        title=next_title,
        status=previous_status,
        project_id=args.project_id,
        objective_id=str(meta.get("objective_id") or "").strip(),
        anchor=anchor,
        paths=next_paths,
        created_at=str(meta.get("created_at") or "").strip() or timestamp_now().isoformat(timespec="seconds"),
        evidence_refs=[entry for entry in meta.get("evidence_refs", []) if isinstance(entry, dict)],
        tags=[str(item).strip() for item in meta.get("tags", []) if str(item).strip()],
        confidence=str(meta.get("confidence") or "high").strip() or "high",
        phase=str(meta.get("phase") or "execution").strip() or "execution",
        summary=next_summary,
        scope_items=next_scope_items,
        deliverable=next_deliverable,
        validation_plan=next_validation_plan,
        risks=next_risks,
        blockers=next_blockers,
        status_notes=next_status_notes,
    )
    active_round_text = render_active_round_file(
        round_id=round_id,
        objective_id=str(meta.get("objective_id") or "").strip(),
        status=previous_status,
        scope_items=next_scope_items,
        deliverable=next_deliverable,
        validation_plan=next_validation_plan,
        risks=next_risks,
        blockers=next_blockers,
    )

    timestamp = timestamp_now().strftime("%Y-%m-%d-%H%M%S")
    guard_codes = {
        "round_remains_open",
        "rewrite_reason_present",
        "rewritten_round_contract_stays_complete",
        "round_identity_preserved",
        "rewrite_produces_material_change",
    }
    assert_round_command_contract(
        "rewrite-open-round",
        provided_inputs={"project_id", "round_id", "reason", "mutable_fields"},
        satisfied_guard_codes=guard_codes,
        write_targets={"durable:round", "control:active-round", "memory:transition-event"},
        durable_owners={"memory:round"},
        projection_owners={"control:active-round"},
        artifact_owners=set(),
        live_inspection_owners=set(),
    )
    _side_effects, event_id, event_path = apply_transition_transaction(
        project_id=args.project_id,
        writes=[
            {"path": round_path, "text": round_text, "label": "durable round contract"},
            {"path": active_round_path(args.project_id), "text": active_round_text, "label": "active round projection"},
        ],
        command_name="rewrite-open-round",
        title=f"Rewrote round {round_id}",
        anchor=anchor,
        previous_state=f"round `{round_id}` remained `{previous_status}` with fields {', '.join(changed_fields)} pending rewrite",
        next_state=f"round `{round_id}` still remains `{previous_status}` after rewriting {', '.join(changed_fields)}",
        guards=render_round_guard_lines("rewrite-open-round", context={"round_id": round_id}),
        evidence=[args.reason.strip(), *changed_fields],
        target_ids=[round_id, str(meta.get("objective_id") or "").strip()],
        event_file_stem=f"{timestamp}-{round_id}-rewrite-open-round",
    )

    print(
        json.dumps(
            {
                "project_id": args.project_id,
                "round_id": round_id,
                "status": previous_status,
                "changed_fields": changed_fields,
                "round_path": str(round_path),
                "active_round_path": str(active_round_path(args.project_id)),
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
