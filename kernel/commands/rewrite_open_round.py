#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json

from kernel.round_control import (
    OPEN_ROUND_STATUSES,
    OPEN_TASK_CONTRACT_STATUSES,
    active_round_path,
    apply_transition_transaction,
    assert_round_command_contract,
    find_task_contracts,
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
from kernel.transition_specs import mutable_field_specs_for_command


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Rewrite one open round contract without changing its identity.")
    parser.add_argument("--project-id", required=True)
    parser.add_argument("--round-id")
    parser.add_argument("--reason", required=True)
    for field_spec in mutable_field_specs_for_command("rewrite-open-round"):
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
    return mutable_field_specs_for_command("rewrite-open-round")


def _previous_field_value(field_spec, meta: dict[str, object], sections: dict[str, str]) -> str | list[str]:
    if field_spec.storage_kind == "meta_scalar":
        return str(meta.get(field_spec.storage_key) or "").strip()
    if field_spec.storage_kind == "meta_list":
        return [str(item).strip() for item in meta.get(field_spec.storage_key, []) if str(item).strip()]
    if field_spec.storage_kind == "section_text":
        return str(sections.get(field_spec.storage_key, "")).strip()
    if field_spec.storage_kind == "section_bullets":
        return parse_bullet_list(str(sections.get(field_spec.storage_key, "")))
    raise SystemExit(
        f"unsupported mutable field storage kind `{field_spec.storage_kind}` for `{field_spec.command_name}.{field_spec.code}`"
    )


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
            parts.append(f"Round rewritten because {reason.strip()}")
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
        "scope_items": "rewrite-open-round requires at least one scope item",
        "deliverable": "rewrite-open-round requires a deliverable",
        "validation_plan": "rewrite-open-round requires a validation plan",
        "paths": "rewrite-open-round requires at least one scope path",
    }
    for field_spec in _rewrite_field_specs():
        if not field_spec.required_after_write:
            continue
        value = rewritten_values[field_spec.code]
        if isinstance(value, list) and value:
            continue
        if isinstance(value, str) and value.strip():
            continue
        raise SystemExit(required_messages.get(field_spec.code, f"rewrite-open-round requires `{field_spec.code}`"))


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

    previous_values = {
        field_spec.code: _previous_field_value(field_spec, meta, sections)
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
        raise SystemExit("rewrite-open-round produced no material round change")

    rewritten_scope_paths = list(rewritten_values["paths"])
    open_task_contracts = find_task_contracts(
        args.project_id,
        round_id=round_id,
        statuses=OPEN_TASK_CONTRACT_STATUSES,
    )
    uncovered_task_contract_paths: list[str] = []
    for task_path, task_meta, _task_sections in open_task_contracts:
        task_contract_id = str(task_meta.get("id") or task_path.stem).strip()
        for task_scope_path in [str(item).strip() for item in task_meta.get("paths", []) if str(item).strip()]:
            if not _path_is_covered(task_scope_path, rewritten_scope_paths):
                uncovered_task_contract_paths.append(f"{task_contract_id}: {task_scope_path}")
    if uncovered_task_contract_paths:
        raise SystemExit(
            "rewrite-open-round would strand draft or active task-contract paths outside the rewritten round scope: "
            + ", ".join(uncovered_task_contract_paths)
        )

    anchor = resolve_anchor(args.project_id)
    round_text = render_round_file(
        round_id=round_id,
        title=str(rewritten_values["title"]),
        status=previous_status,
        project_id=args.project_id,
        objective_id=str(meta.get("objective_id") or "").strip(),
        anchor=anchor,
        paths=list(rewritten_values["paths"]),
        created_at=str(meta.get("created_at") or "").strip() or timestamp_now().isoformat(timespec="seconds"),
        evidence_refs=[entry for entry in meta.get("evidence_refs", []) if isinstance(entry, dict)],
        tags=[str(item).strip() for item in meta.get("tags", []) if str(item).strip()],
        confidence=str(meta.get("confidence") or "high").strip() or "high",
        phase=str(meta.get("phase") or "execution").strip() or "execution",
        summary=str(rewritten_values["summary"]),
        scope_items=list(rewritten_values["scope_items"]),
        deliverable=str(rewritten_values["deliverable"]),
        validation_plan=str(rewritten_values["validation_plan"]),
        risks=list(rewritten_values["risks"]),
        blockers=list(rewritten_values["blockers"]),
        status_notes=str(rewritten_values["status_notes"]),
    )
    active_round_text = render_active_round_file(
        round_id=round_id,
        objective_id=str(meta.get("objective_id") or "").strip(),
        status=previous_status,
        scope_items=list(rewritten_values["scope_items"]),
        deliverable=str(rewritten_values["deliverable"]),
        validation_plan=str(rewritten_values["validation_plan"]),
        risks=list(rewritten_values["risks"]),
        blockers=list(rewritten_values["blockers"]),
    )

    timestamp = timestamp_now().strftime("%Y-%m-%d-%H%M%S")
    assert_round_command_contract(
        "rewrite-open-round",
        provided_inputs={"project_id", "round_id", "reason", "mutable_fields"},
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

