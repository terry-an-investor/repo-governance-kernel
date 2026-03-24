#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json

from kernel.round_control import (
    OPEN_TASK_CONTRACT_STATUSES,
    apply_transition_transaction,
    assert_task_contract_command_contract,
    load_round_file,
    load_task_contract_file,
    locate_round_file,
    locate_task_contract_file,
    project_dir,
    render_task_contract_file,
    render_task_contract_guard_lines,
    resolve_anchor,
    task_contract_record_payload,
    timestamp_now,
)
from kernel.transition_specs import mutable_field_specs_for_command


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Rewrite one open task contract without changing its identity.")
    parser.add_argument("--project-id", required=True)
    parser.add_argument("--task-contract-id", required=True)
    parser.add_argument("--reason", required=True)
    for field_spec in mutable_field_specs_for_command("rewrite-open-task-contract"):
        cli_flag = f"--{field_spec.cli_flag}"
        if field_spec.value_kind == "scalar":
            parser.add_argument(cli_flag, default="")
        else:
            parser.add_argument(cli_flag, action="append", default=[])
        if field_spec.replace_flag:
            parser.add_argument(f"--{field_spec.replace_flag.replace('_', '-')}", action="store_true")
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


def _rewrite_field_specs():
    return mutable_field_specs_for_command("rewrite-open-task-contract")


def _previous_field_value(field_spec, payload: dict[str, object]) -> str | list[str]:
    value = payload[field_spec.code]
    if isinstance(value, list):
        return list(value)
    return str(value).strip()


def _incoming_field_value(args: argparse.Namespace, field_spec) -> str | list[str]:
    raw_value = getattr(args, field_spec.payload_key)
    if field_spec.value_kind == "scalar":
        return str(raw_value or "").strip()
    return _clean_list(list(raw_value or []))


def _apply_field_mutation(
    *,
    previous_value: str | list[str],
    incoming_value: str | list[str],
    field_spec,
    reason: str,
    replace: bool,
) -> str | list[str]:
    if field_spec.mutation_mode == "replace_if_present":
        return incoming_value if isinstance(incoming_value, str) and incoming_value else previous_value
    if field_spec.mutation_mode == "merge_unique":
        return _merge_lists(
            list(previous_value) if isinstance(previous_value, list) else [],
            list(incoming_value) if isinstance(incoming_value, list) else [],
            replace=replace,
        )
    if field_spec.mutation_mode == "append_paragraphs":
        parts: list[str] = []
        previous_text = str(previous_value).strip()
        if previous_text:
            parts.append(previous_text)
        if field_spec.include_reason_note:
            parts.append(f"Task contract rewritten because {reason.strip()}")
        parts.extend(item for item in list(incoming_value) if str(item).strip())
        return "\n\n".join(parts).strip()
    raise SystemExit(
        f"unsupported mutable field mutation mode `{field_spec.mutation_mode}` for `{field_spec.command_name}.{field_spec.code}`"
    )


def _material_field_changed(
    *,
    previous_value: str | list[str],
    next_value: str | list[str],
    incoming_value: str | list[str],
    field_spec,
) -> bool:
    if field_spec.material_requires_explicit_input:
        return bool(incoming_value) and next_value != previous_value
    return next_value != previous_value


def _assert_required_field_values(rewritten_values: dict[str, str | list[str]]) -> None:
    required_messages = {
        "intent": "rewrite-open-task-contract requires intent",
        "allowed_changes": "rewrite-open-task-contract requires at least one allowed change",
        "forbidden_changes": "rewrite-open-task-contract requires at least one forbidden change",
        "completion_criteria": "rewrite-open-task-contract requires at least one completion criterion",
        "paths": "rewrite-open-task-contract requires at least one path",
    }
    for field_spec in _rewrite_field_specs():
        if not field_spec.required_after_write:
            continue
        value = rewritten_values[field_spec.code]
        if isinstance(value, list) and value:
            continue
        if isinstance(value, str) and value.strip():
            continue
        raise SystemExit(required_messages.get(field_spec.code, f"rewrite-open-task-contract requires `{field_spec.code}`"))


def _path_is_covered(path: str, scope_paths: list[str]) -> bool:
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
    if not project_dir(args.project_id).exists():
        raise SystemExit(f"project directory not found: {project_dir(args.project_id)}")

    task_contract_path = locate_task_contract_file(args.project_id, args.task_contract_id)
    if task_contract_path is None:
        raise SystemExit(f"task-contract file not found for `{args.task_contract_id}`")

    meta, sections = load_task_contract_file(task_contract_path)
    payload = task_contract_record_payload(meta, sections)
    previous_status = str(payload["status"]).strip()
    if previous_status not in OPEN_TASK_CONTRACT_STATUSES:
        raise SystemExit(
            f"rewrite-open-task-contract requires an open task-contract status in {sorted(OPEN_TASK_CONTRACT_STATUSES)}; found `{previous_status}`"
        )

    round_id = str(payload["round_id"]).strip()
    round_path = locate_round_file(args.project_id, round_id)
    if round_path is None:
        raise SystemExit(f"task-contract `{args.task_contract_id}` references missing round `{round_id}`")
    round_meta, _round_sections = load_round_file(round_path)
    round_scope_paths = [str(item).strip() for item in round_meta.get("paths", []) if str(item).strip()]

    previous_values = {
        field_spec.code: _previous_field_value(field_spec, payload)
        for field_spec in _rewrite_field_specs()
    }
    rewritten_values: dict[str, str | list[str]] = {}
    changed_fields: list[str] = []
    for field_spec in _rewrite_field_specs():
        incoming_value = _incoming_field_value(args, field_spec)
        replace = bool(field_spec.replace_flag and getattr(args, field_spec.replace_flag))
        next_value = _apply_field_mutation(
            previous_value=previous_values[field_spec.code],
            incoming_value=incoming_value,
            field_spec=field_spec,
            reason=args.reason,
            replace=replace,
        )
        rewritten_values[field_spec.code] = next_value
        if _material_field_changed(
            previous_value=previous_values[field_spec.code],
            next_value=next_value,
            incoming_value=incoming_value,
            field_spec=field_spec,
        ):
            changed_fields.append(field_spec.code)
    _assert_required_field_values(rewritten_values)
    if not changed_fields:
        raise SystemExit("rewrite-open-task-contract produced no material task-contract change")

    rewritten_paths = list(rewritten_values["paths"])
    uncovered_paths = [path for path in rewritten_paths if not _path_is_covered(path, round_scope_paths)]
    if uncovered_paths:
        raise SystemExit(
            "task-contract paths escape the referenced round scope after rewrite: "
            + ", ".join(sorted(uncovered_paths))
        )

    anchor = resolve_anchor(args.project_id)
    task_contract_text = render_task_contract_file(
        task_contract_id=args.task_contract_id,
        title=str(rewritten_values["title"]),
        status=previous_status,
        project_id=args.project_id,
        objective_id=str(payload["objective_id"]),
        round_id=round_id,
        anchor=anchor,
        paths=rewritten_paths,
        created_at=str(payload["created_at"]) or timestamp_now().isoformat(timespec="seconds"),
        evidence_refs=list(payload["evidence_refs"]),
        tags=list(payload["tags"]),
        confidence=str(payload["confidence"]),
        phase=str(payload["phase"]) or "execution",
        summary=str(rewritten_values["summary"]),
        intent=str(rewritten_values["intent"]),
        allowed_changes=list(rewritten_values["allowed_changes"]),
        forbidden_changes=list(rewritten_values["forbidden_changes"]),
        completion_criteria=list(rewritten_values["completion_criteria"]),
        resolution=list(payload["resolution"]),
        risks=list(rewritten_values["risks"]),
        status_notes=str(rewritten_values["status_notes"]),
    )

    assert_task_contract_command_contract(
        "rewrite-open-task-contract",
        provided_inputs={"project_id", "task_contract_id", "reason", "mutable_fields"},
    )
    timestamp = timestamp_now().strftime("%Y-%m-%d-%H%M%S")
    _side_effects, event_id, event_path = apply_transition_transaction(
        project_id=args.project_id,
        writes=[
            {"path": task_contract_path, "text": task_contract_text, "label": "durable task contract"},
        ],
        command_name="rewrite-open-task-contract",
        title=f"Rewrote task contract {args.task_contract_id}",
        anchor=anchor,
        previous_state=f"task contract `{args.task_contract_id}` remained `{previous_status}` with fields {', '.join(changed_fields)} pending rewrite",
        next_state=f"task contract `{args.task_contract_id}` still remains `{previous_status}` after rewriting {', '.join(changed_fields)}",
        guards=render_task_contract_guard_lines(
            "rewrite-open-task-contract",
            context={"task_contract_id": args.task_contract_id},
        ),
        evidence=[args.reason.strip(), *changed_fields],
        target_ids=[args.task_contract_id, round_id, str(payload["objective_id"])],
        event_file_stem=f"{timestamp}-{args.task_contract_id}-rewrite-open-task-contract",
    )

    print(
        json.dumps(
            {
                "project_id": args.project_id,
                "task_contract_id": args.task_contract_id,
                "status": previous_status,
                "changed_fields": changed_fields,
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

