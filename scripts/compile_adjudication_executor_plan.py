#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path

from round_control import (
    OPEN_ROUND_STATUSES,
    OPEN_TASK_CONTRACT_STATUSES,
    find_rounds,
    load_adjudication_file,
    load_exception_contract_file,
    load_round_file,
    load_task_contract_file,
    locate_exception_contract_file,
    locate_round_file,
    locate_task_contract_file,
    parse_bullet_list,
    project_dir,
    select_open_round_record,
)
from transition_specs import adjudication_plan_spec


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Compile bounded adjudication executor plan contracts into explicit executor followups.")
    parser.add_argument("--project-id", required=True)
    parser.add_argument("--adjudication-id")
    parser.add_argument("--in-place", action="store_true")
    return parser.parse_args()


def _normalize_list(value: object) -> list[str]:
    if isinstance(value, list):
        return [str(item).strip() for item in value if str(item).strip()]
    if isinstance(value, str) and value.strip():
        return [value.strip()]
    return []


def _load_adjudication_record(project_id: str, adjudication_id: str | None) -> tuple[Path, dict[str, object], dict[str, str]]:
    adjudications_dir = project_dir(project_id) / "memory" / "adjudications"
    if not adjudications_dir.exists():
        raise SystemExit(f"adjudication directory not found: {adjudications_dir}")
    records = sorted(adjudications_dir.glob("*.md"))
    if not records:
        raise SystemExit(f"no adjudication records found for project `{project_id}`")
    if adjudication_id:
        for path in records:
            meta, sections = load_adjudication_file(path)
            if str(meta.get("id") or path.stem).strip() == adjudication_id.strip():
                return path, meta, sections
        raise SystemExit(f"adjudication `{adjudication_id}` not found for project `{project_id}`")
    path = records[-1]
    meta, sections = load_adjudication_file(path)
    return path, meta, sections


def _first_scalar(mapping: dict[str, object], source_keys: tuple[str, ...]) -> str:
    for key in source_keys:
        value = str(mapping.get(key) or "").strip()
        if value:
            return value
    return ""


def _first_list(mapping: dict[str, object], source_keys: tuple[str, ...]) -> list[str]:
    for key in source_keys:
        values = _normalize_list(mapping.get(key))
        if values:
            return values
    return []


def _resolve_target_exception_contract_ids(
    project_id: str,
    contract: dict[str, object],
    source_keys: tuple[str, ...],
    adjudication_sections: dict[str, str],
) -> list[str]:
    explicit_ids = _first_list(contract, source_keys)
    candidate_ids = explicit_ids
    if not candidate_ids:
        candidate_ids = parse_bullet_list(adjudication_sections.get("Objects Invalidated", ""))

    if not candidate_ids:
        raise SystemExit(
            "executor exception-contract plan requires at least one target exception contract id, "
            "either through `exception_contract_id`, `exception_contract_ids`, or adjudication `Objects Invalidated`"
        )

    resolved_ids: list[str] = []
    seen: set[str] = set()
    for object_id in candidate_ids:
        normalized_id = str(object_id).strip()
        if not normalized_id or normalized_id in seen:
            continue
        contract_path = locate_exception_contract_file(project_id, normalized_id)
        if contract_path is None:
            if explicit_ids:
                raise SystemExit(f"executor exception-contract plan could not find exception contract `{normalized_id}`")
            continue
        contract_meta, _contract_sections = load_exception_contract_file(contract_path)
        current_status = str(contract_meta.get("status") or "").strip()
        if current_status != "active":
            raise SystemExit(
                f"executor exception-contract plan requires active contracts; `{normalized_id}` is `{current_status or 'unknown'}`"
            )
        seen.add(normalized_id)
        resolved_ids.append(normalized_id)

    if not resolved_ids:
        raise SystemExit("executor exception-contract plan found no active exception contracts in the selected target set")
    return resolved_ids


def _resolve_target_task_contract_ids(
    project_id: str,
    contract: dict[str, object],
    source_keys: tuple[str, ...],
    adjudication_sections: dict[str, str],
) -> list[str]:
    explicit_ids = _first_list(contract, source_keys)
    candidate_ids = explicit_ids
    if not candidate_ids:
        candidate_ids = parse_bullet_list(adjudication_sections.get("Objects Invalidated", ""))

    if not candidate_ids:
        raise SystemExit(
            "executor task-contract plan requires at least one target task contract id, "
            "either through `task_contract_id`, `task_contract_ids`, or adjudication `Objects Invalidated`"
        )

    resolved_ids: list[str] = []
    seen: set[str] = set()
    for object_id in candidate_ids:
        normalized_id = str(object_id).strip()
        if not normalized_id or normalized_id in seen:
            continue
        contract_path = locate_task_contract_file(project_id, normalized_id)
        if contract_path is None:
            if explicit_ids:
                raise SystemExit(f"executor task-contract plan could not find task contract `{normalized_id}`")
            continue
        contract_meta, _contract_sections = load_task_contract_file(contract_path)
        current_status = str(contract_meta.get("status") or "").strip()
        if current_status not in OPEN_TASK_CONTRACT_STATUSES:
            raise SystemExit(
                f"executor task-contract plan requires open task contracts; `{normalized_id}` is `{current_status or 'unknown'}`"
            )
        seen.add(normalized_id)
        resolved_ids.append(normalized_id)

    if not resolved_ids:
        raise SystemExit("executor task-contract plan found no open task contracts in the selected target set")
    return resolved_ids


def _resolve_target_round_id(
    project_id: str,
    contract: dict[str, object],
    source_keys: tuple[str, ...],
    adjudication_meta: dict[str, object],
    adjudication_sections: dict[str, str],
) -> str:
    explicit_round_id = _first_scalar(contract, source_keys)
    if explicit_round_id:
        round_path = locate_round_file(project_id, explicit_round_id)
        if round_path is None:
            raise SystemExit(f"executor round plan could not find round `{explicit_round_id}`")
        round_meta, _round_sections = load_round_file(round_path)
        current_status = str(round_meta.get("status") or "").strip()
        if current_status not in OPEN_ROUND_STATUSES:
            raise SystemExit(
                f"executor round plan requires an open round target; `{explicit_round_id}` is `{current_status or 'unknown'}`"
            )
        return explicit_round_id

    invalidated_ids = parse_bullet_list(adjudication_sections.get("Objects Invalidated", ""))
    open_invalidated_rounds: list[str] = []
    seen_round_ids: set[str] = set()
    for object_id in invalidated_ids:
        normalized_id = str(object_id).strip()
        if not normalized_id or normalized_id in seen_round_ids:
            continue
        round_path = locate_round_file(project_id, normalized_id)
        if round_path is None:
            continue
        round_meta, _round_sections = load_round_file(round_path)
        current_status = str(round_meta.get("status") or "").strip()
        if current_status in OPEN_ROUND_STATUSES:
            seen_round_ids.add(normalized_id)
            open_invalidated_rounds.append(normalized_id)
    if len(open_invalidated_rounds) == 1:
        return open_invalidated_rounds[0]
    if len(open_invalidated_rounds) > 1:
        raise SystemExit(
            "executor round plan found multiple open invalidated rounds; "
            + ", ".join(f"`{round_id}`" for round_id in open_invalidated_rounds)
        )

    objective_id = _first_scalar(contract, ("objective_id",)) or _first_scalar(adjudication_meta, ("objective_id",))
    if objective_id:
        open_rounds = find_rounds(project_id, objective_id=objective_id, statuses=OPEN_ROUND_STATUSES)
        if len(open_rounds) == 1:
            _round_path, round_meta, _round_sections = open_rounds[0]
            return str(round_meta.get("id") or "").strip()
        if len(open_rounds) > 1:
            raise SystemExit(
                f"executor round plan found multiple open rounds for objective `{objective_id}`"
            )

    open_round_record, open_round_issues = select_open_round_record(project_id)
    if open_round_issues:
        raise SystemExit(
            "executor round plan could not resolve one open round target: " + "; ".join(open_round_issues)
        )
    if open_round_record is not None:
        _round_path, round_meta, _round_sections = open_round_record
        return str(round_meta.get("id") or "").strip()

    raise SystemExit(
        "executor round plan could not resolve one open round target from explicit `round_id`, adjudication `Objects Invalidated`, or objective context"
    )


def _resolve_round_validated_by(
    project_id: str,
    *,
    contract: dict[str, object],
    source_keys: tuple[str, ...],
    resolved_payload: dict[str, object],
) -> list[str]:
    validated_by = _first_list(contract, source_keys)
    if validated_by:
        return validated_by

    round_id = str(resolved_payload.get("round_id") or _first_scalar(contract, ("round_id",))).strip()
    if not round_id:
        raise SystemExit("executor plan contract could not resolve `round_id` before deriving `validated_by`")
    round_path = locate_round_file(project_id, round_id)
    if round_path is None:
        raise SystemExit(f"executor plan contract could not find round `{round_id}`")
    _round_meta, round_sections = load_round_file(round_path)
    existing_plan = str(round_sections.get("Validation Plan", "")).strip()
    return [existing_plan] if existing_plan else ["Adjudication executor plan validation"]


def _resolve_binding_value(
    project_id: str,
    *,
    binding,
    contract: dict[str, object],
    adjudication_meta: dict[str, object],
    adjudication_sections: dict[str, str],
    resolved_payload: dict[str, object],
) -> object:
    source_keys = binding.source_keys
    if binding.resolver == "contract_scalar":
        return _first_scalar(contract, source_keys)
    if binding.resolver == "contract_list":
        return _first_list(contract, source_keys)
    if binding.resolver == "contract_bool":
        return any(bool(contract.get(key)) for key in source_keys)
    if binding.resolver == "contract_or_meta_scalar":
        return _first_scalar(contract, source_keys) or _first_scalar(adjudication_meta, source_keys)
    if binding.resolver == "contract_or_meta_list":
        return _first_list(contract, source_keys) or _first_list(adjudication_meta, source_keys)
    if binding.resolver == "exception_contract_target_ids":
        return _resolve_target_exception_contract_ids(project_id, contract, source_keys, adjudication_sections)
    if binding.resolver == "task_contract_target_ids":
        return _resolve_target_task_contract_ids(project_id, contract, source_keys, adjudication_sections)
    if binding.resolver == "round_target_id":
        return _resolve_target_round_id(
            project_id,
            contract,
            source_keys,
            adjudication_meta,
            adjudication_sections,
        )
    if binding.resolver == "round_validated_by_list":
        return _resolve_round_validated_by(
            project_id,
            contract=contract,
            source_keys=source_keys,
            resolved_payload=resolved_payload,
        )
    raise SystemExit(f"unsupported adjudication payload binding resolver `{binding.resolver}`")


def _materialize_payload_templates(
    project_id: str,
    *,
    plan_spec,
    contract: dict[str, object],
    adjudication_meta: dict[str, object],
    adjudication_sections: dict[str, str],
) -> list[dict[str, object]]:
    compiled_payloads: list[dict[str, object]] = []
    for template in plan_spec.payload_templates:
        payloads: list[dict[str, object]] = [{"command": template.command_name}]
        for key, value in template.static_scalar_fields:
            for payload in payloads:
                payload[key] = value
        for key, value in template.static_bool_fields:
            for payload in payloads:
                payload[key] = value

        resolved_payload: dict[str, object] = {}
        for binding in template.bindings:
            value = _resolve_binding_value(
                project_id,
                binding=binding,
                contract=contract,
                adjudication_meta=adjudication_meta,
                adjudication_sections=adjudication_sections,
                resolved_payload=resolved_payload,
            )
            is_empty = (
                value is None
                or (isinstance(value, str) and not value.strip())
                or (isinstance(value, list) and not value)
                or (isinstance(value, bool) and not value)
            )
            if binding.required and is_empty:
                rendered_sources = ", ".join(f"`{source}`" for source in binding.source_keys) or "`<implicit>`"
                raise SystemExit(
                    f"executor plan contract `{plan_spec.plan_type}` could not resolve required payload field `{binding.target_key}` from {rendered_sources}"
                )
            if is_empty:
                continue
            if binding.fanout:
                if not isinstance(value, list):
                    value = [str(value).strip()]
                next_payloads: list[dict[str, object]] = []
                for payload in payloads:
                    for item in value:
                        cloned = dict(payload)
                        cloned[binding.target_key] = item
                        next_payloads.append(cloned)
                payloads = next_payloads
                continue
            resolved_payload[binding.target_key] = value
            for payload in payloads:
                payload[binding.target_key] = value
        compiled_payloads.extend(payloads)
    return compiled_payloads


def compile_plan_contracts(
    project_id: str,
    plan_contracts: list[str],
    *,
    adjudication_meta: dict[str, object] | None = None,
    adjudication_sections: dict[str, str] | None = None,
) -> list[str]:
    adjudication_meta = adjudication_meta or {}
    adjudication_sections = adjudication_sections or {}
    compiled: list[str] = []
    for raw_contract in plan_contracts:
        try:
            contract = json.loads(raw_contract)
        except json.JSONDecodeError as exc:
            raise SystemExit(f"invalid executor plan contract json: {exc}") from exc
        if not isinstance(contract, dict):
            raise SystemExit("executor plan contract must be a JSON object")
        plan_type = str(contract.get("plan_type") or "").strip()
        plan_spec = adjudication_plan_spec(plan_type)
        payloads = _materialize_payload_templates(
            project_id,
            plan_spec=plan_spec,
            contract=contract,
            adjudication_meta=adjudication_meta,
            adjudication_sections=adjudication_sections,
        )
        compiled.extend(json.dumps(payload, ensure_ascii=True, sort_keys=True) for payload in payloads)
    return compiled


def merge_followups(existing_followups: list[str], compiled_followups: list[str]) -> list[str]:
    merged: list[str] = []
    seen: set[str] = set()
    for raw_value in [*compiled_followups, *existing_followups]:
        normalized = raw_value.strip()
        if not normalized or normalized in seen:
            continue
        seen.add(normalized)
        merged.append(normalized)
    return merged


def _replace_frontmatter_list(text: str, key: str, values: list[str]) -> str:
    lines = text.splitlines()
    start = None
    end = None
    for index, line in enumerate(lines):
        if line.strip() == f"{key}:" or line.strip() == f"{key}: []":
            start = index
            end = index + 1
            while end < len(lines) and (lines[end].startswith("  - ") or lines[end].startswith("    ")):
                end += 1
            break
    rendered = [f"{key}: []"] if not values else [f"{key}:"] + [f"  - {json.dumps(value, ensure_ascii=True)}" for value in values]
    if start is None:
        for index, line in enumerate(lines):
            if line.strip() == "---" and index != 0:
                lines[index:index] = rendered
                return "\n".join(lines) + ("\n" if text.endswith("\n") else "")
        raise SystemExit("failed to locate frontmatter terminator while updating adjudication record")
    lines[start:end] = rendered
    return "\n".join(lines) + ("\n" if text.endswith("\n") else "")


def main() -> int:
    args = parse_args()
    if not project_dir(args.project_id).exists():
        raise SystemExit(f"project directory not found: {project_dir(args.project_id)}")

    adjudication_path, meta, sections = _load_adjudication_record(args.project_id, args.adjudication_id)
    plan_contracts = [str(item).strip() for item in meta.get("executor_plan_contracts", []) if str(item).strip()]
    if not plan_contracts:
        raise SystemExit(f"adjudication `{str(meta.get('id') or adjudication_path.stem)}` has no `executor_plan_contracts`")

    compiled_followups = compile_plan_contracts(
        args.project_id,
        plan_contracts,
        adjudication_meta=meta,
        adjudication_sections=sections,
    )
    merged_followups = merge_followups(
        [str(item).strip() for item in meta.get("executor_followups", []) if str(item).strip()],
        compiled_followups,
    )
    if args.in_place:
        text = adjudication_path.read_text(encoding="utf-8")
        updated_text = _replace_frontmatter_list(text, "executor_followups", merged_followups)
        adjudication_path.write_text(updated_text, encoding="utf-8")

    print(
        json.dumps(
            {
                "project_id": args.project_id,
                "adjudication_id": str(meta.get("id") or adjudication_path.stem).strip(),
                "adjudication_path": str(adjudication_path),
                "plan_contract_count": len(plan_contracts),
                "compiled_followup_count": len(compiled_followups),
                "merged_followup_count": len(merged_followups),
                "compiled_followups": [json.loads(item) for item in compiled_followups],
                "merged_followups": [json.loads(item) for item in merged_followups],
                "updated_in_place": bool(args.in_place),
            },
            ensure_ascii=True,
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
