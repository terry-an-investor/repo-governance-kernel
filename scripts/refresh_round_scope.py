#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json

from assemble_context import inspect_live_workspace
from audit_control_state import parse_changed_paths, relativize_changed_paths
from control_enforcement import is_control_plane_path
from round_control import (
    OPEN_ROUND_STATUSES,
    active_round_path,
    apply_transition_transaction,
    assert_round_command_contract,
    load_round_file,
    locate_round_file,
    parse_bullet_list,
    project_dir,
    render_round_guard_lines,
    render_active_round_file,
    render_round_file,
    resolve_anchor,
    select_open_round_record,
    timestamp_now,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Refresh the active round scope from live worktree evidence.")
    parser.add_argument("--project-id", required=True)
    parser.add_argument("--round-id", default="")
    parser.add_argument("--reason", required=True)
    parser.add_argument("--evidence", action="append", default=[])
    parser.add_argument("--add-scope-path", action="append", default=[])
    parser.add_argument("--drop-scope-path", action="append", default=[])
    parser.add_argument("--no-live-dirty-paths", action="store_true")
    return parser.parse_args()


def _clean_list(values: list[str]) -> list[str]:
    return [value.strip() for value in values if value.strip()]


def _resolve_round(project_id: str, requested_round_id: str) -> tuple[object, dict[str, object], dict[str, str], str]:
    round_id = requested_round_id.strip()
    if round_id:
        round_path = locate_round_file(project_id, round_id)
        if round_path is None:
            raise SystemExit(f"round file not found for `{round_id}`")
        meta, sections = load_round_file(round_path)
        return round_path, meta, sections, round_id

    open_round_record, issues = select_open_round_record(project_id)
    if issues:
        raise SystemExit("cannot refresh round scope while durable round truth is ambiguous: " + "; ".join(issues))
    if open_round_record is None:
        raise SystemExit("no active or otherwise open round exists")
    round_path, meta, sections = open_round_record
    return round_path, meta, sections, str(meta.get("id") or round_path.stem).strip()


def main() -> int:
    args = parse_args()
    if not project_dir(args.project_id).exists():
        raise SystemExit(f"project directory not found: {project_dir(args.project_id)}")

    round_path, meta, sections, round_id = _resolve_round(args.project_id, args.round_id)
    round_status = str(meta.get("status") or "").strip()
    if round_status not in OPEN_ROUND_STATUSES:
        raise SystemExit(f"cannot refresh scope for round `{round_id}` with non-open status `{round_status}`")

    existing_paths = [str(item).strip() for item in meta.get("paths", []) if str(item).strip()]
    merged_paths = list(existing_paths)

    live_dirty_paths: list[str] = []
    if not args.no_live_dirty_paths:
        anchor = resolve_anchor(args.project_id)
        live_workspace = inspect_live_workspace(anchor)
        if live_workspace.get("status") != "available":
            raise SystemExit("live workspace inspection is unavailable for round-scope refresh")
        live_dirty_paths = [
            path
            for path in relativize_changed_paths(
                parse_changed_paths(str(live_workspace.get("status_short") or "")),
                workspace_root=str(live_workspace.get("workspace_root") or ""),
            )
            if not is_control_plane_path(args.project_id, path)
        ]
        for path in live_dirty_paths:
            if path not in merged_paths:
                merged_paths.append(path)

    for path in _clean_list(args.add_scope_path):
        if path not in merged_paths:
            merged_paths.append(path)

    drop_paths = set(_clean_list(args.drop_scope_path))
    if drop_paths:
        merged_paths = [path for path in merged_paths if path not in drop_paths]

    if merged_paths == existing_paths:
        raise SystemExit("refresh-round-scope produced no scope-path change")
    if not merged_paths:
        raise SystemExit("refresh-round-scope cannot leave the round without any scope paths")

    status_notes = "\n\n".join(
        part
        for part in [
            str(sections.get("Status Notes", "")).strip(),
            f"Scope refreshed because {args.reason.strip()}",
            (
                "Live dirty paths included:\n"
                + "\n".join(f"- {path}" for path in live_dirty_paths)
                if live_dirty_paths
                else ""
            ),
        ]
        if part
    )
    anchor = resolve_anchor(args.project_id)
    round_text = render_round_file(
        round_id=round_id,
        title=str(meta.get("title") or round_id),
        status=round_status,
        project_id=args.project_id,
        objective_id=str(meta.get("objective_id") or "").strip(),
        anchor=anchor,
        paths=merged_paths,
        created_at=str(meta.get("created_at") or "").strip() or timestamp_now().isoformat(timespec="seconds"),
        evidence_refs=[entry for entry in meta.get("evidence_refs", []) if isinstance(entry, dict)],
        tags=[str(item).strip() for item in meta.get("tags", []) if str(item).strip()],
        confidence=str(meta.get("confidence") or "high").strip() or "high",
        phase=str(meta.get("phase") or "execution").strip() or "execution",
        summary=str(sections.get("Summary", "")).strip(),
        scope_items=parse_bullet_list(str(sections.get("Scope", ""))),
        deliverable=str(sections.get("Deliverable", "")).strip(),
        validation_plan=str(sections.get("Validation Plan", "")).strip(),
        risks=parse_bullet_list(str(sections.get("Active Risks", ""))),
        blockers=parse_bullet_list(str(sections.get("Blockers", ""))),
        status_notes=status_notes,
    )
    active_round_text = render_active_round_file(
        round_id=round_id,
        objective_id=str(meta.get("objective_id") or "").strip(),
        status=round_status,
        scope_items=parse_bullet_list(str(sections.get("Scope", ""))),
        deliverable=str(sections.get("Deliverable", "")).strip(),
        validation_plan=str(sections.get("Validation Plan", "")).strip(),
        risks=parse_bullet_list(str(sections.get("Active Risks", ""))),
        blockers=parse_bullet_list(str(sections.get("Blockers", ""))),
    )

    timestamp = timestamp_now().strftime("%Y-%m-%d-%H%M%S")
    assert_round_command_contract(
        "refresh-round-scope",
        provided_inputs={"project_id", "reason"},
    )
    _side_effects, event_id, event_path = apply_transition_transaction(
        project_id=args.project_id,
        writes=[
            {"path": round_path, "text": round_text, "label": "durable round contract"},
            {"path": active_round_path(args.project_id), "text": active_round_text, "label": "active round projection"},
        ],
        command_name="refresh-round-scope",
        title=f"Refreshed round {round_id} scope",
        anchor=anchor,
        previous_state=f"round `{round_id}` had scope paths: {', '.join(existing_paths) or '(none)'}",
        next_state=f"round `{round_id}` now covers scope paths: {', '.join(merged_paths)}",
        guards=render_round_guard_lines("refresh-round-scope", context={"round_id": round_id}),
        evidence=[args.reason.strip()] + _clean_list(args.evidence) + live_dirty_paths,
        target_ids=[round_id, str(meta.get("objective_id") or "").strip()],
        event_file_stem=f"{timestamp}-{round_id}-refresh-round-scope",
    )

    print(
        json.dumps(
            {
                "project_id": args.project_id,
                "round_id": round_id,
                "previous_paths": existing_paths,
                "paths": merged_paths,
                "live_dirty_paths": live_dirty_paths,
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
