#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json

from kernel.round_control import (
    OPEN_ROUND_STATUSES,
    active_round_path,
    apply_transition_transaction,
    assert_task_contract_command_contract,
    durable_markdown_path,
    find_task_contracts,
    load_active_round,
    load_round_file,
    locate_round_file,
    project_dir,
    render_task_contract_file,
    render_task_contract_guard_lines,
    resolve_anchor,
    slugify,
    task_contracts_dir,
    timestamp_now,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Open one durable task contract beneath an active round.")
    parser.add_argument("--project-id", required=True)
    parser.add_argument("--title", required=True)
    parser.add_argument("--summary", default="")
    parser.add_argument("--round-id")
    parser.add_argument("--slug")
    parser.add_argument("--intent", required=True)
    parser.add_argument("--path", action="append", required=True)
    parser.add_argument("--allowed-change", action="append", required=True)
    parser.add_argument("--forbidden-change", action="append", required=True)
    parser.add_argument("--completion-criterion", action="append", required=True)
    parser.add_argument("--risk", action="append", default=[])
    parser.add_argument("--status-note", default="")
    return parser.parse_args()


def path_is_covered(path: str, scope_paths: list[str]) -> bool:
    normalized_path = path.replace("\\", "/").strip().lstrip("./")
    for raw_scope in scope_paths:
        scope = raw_scope.replace("\\", "/").strip().lstrip("./").rstrip("/")
        if not scope:
            continue
        if normalized_path == scope or normalized_path.startswith(scope + "/"):
            return True
    return False


def main() -> int:
    args = parse_args()
    project_path = project_dir(args.project_id)
    if not project_path.exists():
        raise SystemExit(f"project directory not found: {project_path}")

    active_round_preface, _active_round_sections = load_active_round(args.project_id)
    round_id = (args.round_id or active_round_preface.get("round id", "")).strip()
    if not round_id:
        raise SystemExit(
            f"missing active round: {active_round_path(args.project_id)}; "
            "pass --round-id or keep one honest active round projection"
        )

    round_path = locate_round_file(args.project_id, round_id)
    if round_path is None:
        raise SystemExit(f"round `{round_id}` not found in durable round records")
    round_meta, _round_sections = load_round_file(round_path)
    round_status = str(round_meta.get("status") or "").strip()
    if round_status not in OPEN_ROUND_STATUSES:
        raise SystemExit(
            f"cannot attach task contract to round `{round_id}` with non-open status `{round_status or 'unknown'}`"
        )

    round_scope_paths = [str(item).strip() for item in round_meta.get("paths", []) if str(item).strip()]
    uncovered_paths = [path for path in args.path if not path_is_covered(path, round_scope_paths)]
    if uncovered_paths:
        raise SystemExit(
            "task-contract paths escape the round scope: " + ", ".join(sorted(uncovered_paths))
        )

    timestamp = timestamp_now()
    slug = args.slug or slugify(args.title)
    task_contract_id = f"taskc-{timestamp.strftime('%Y-%m-%d-%H%M')}-{slug}"
    file_stem = f"{timestamp.strftime('%Y-%m-%d-%H%M')}-{slug}"
    objective_id = str(round_meta.get("objective_id") or "").strip()
    phase = str(round_meta.get("phase") or "execution").strip() or "execution"
    anchor = resolve_anchor(args.project_id)
    summary = args.summary.strip() or args.intent.strip()

    task_contract_text = render_task_contract_file(
        task_contract_id=task_contract_id,
        title=args.title,
        status="active",
        project_id=args.project_id,
        objective_id=objective_id,
        round_id=round_id,
        anchor=anchor,
        paths=args.path,
        created_at=timestamp.isoformat(timespec="seconds"),
        evidence_refs=[],
        tags=["task-contract", "control-plane"],
        confidence="high",
        phase=phase,
        summary=summary,
        intent=args.intent,
        allowed_changes=args.allowed_change,
        forbidden_changes=args.forbidden_change,
        completion_criteria=args.completion_criterion,
        resolution=[],
        risks=args.risk,
        status_notes=args.status_note,
    )

    task_contract_path = durable_markdown_path(task_contracts_dir(args.project_id), file_stem)
    existing_contract_count = len(find_task_contracts(args.project_id, round_id=round_id))
    previous_state = (
        f"round `{round_id}` already had {existing_contract_count} durable task-contract record(s)"
        if existing_contract_count
        else f"round `{round_id}` had no durable task-contract records"
    )
    next_state = f"task contract `{task_contract_id}` is now active beneath round `{round_id}`"
    assert_task_contract_command_contract(
        "open-task-contract",
        provided_inputs={
            "project_id",
            "round_id",
            "title",
            "intent",
            "paths",
            "allowed_changes",
            "forbidden_changes",
            "completion_criteria",
        },
    )
    guards = render_task_contract_guard_lines("open-task-contract", context={"round_id": round_id})
    _side_effects, event_id, event_path = apply_transition_transaction(
        project_id=args.project_id,
        writes=[
            {
                "path": task_contract_path,
                "text": task_contract_text,
                "label": "durable task contract",
            },
        ],
        command_name="open-task-contract",
        title=f"Opened task contract {task_contract_id}",
        anchor=anchor,
        previous_state=previous_state,
        next_state=next_state,
        guards=guards,
        evidence=[args.intent, *args.completion_criterion],
        target_ids=[task_contract_id, round_id, objective_id],
        event_file_stem=f"{file_stem}-open-task-contract",
    )

    print(
        json.dumps(
            {
                "project_id": args.project_id,
                "task_contract_id": task_contract_id,
                "round_id": round_id,
                "objective_id": objective_id,
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

