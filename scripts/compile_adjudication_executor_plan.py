#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path

from resolver_runtime import (
    first_list,
    first_scalar,
    normalize_list as _normalize_list,
    resolve_round_validated_by,
    resolve_target_exception_contract_ids,
    resolve_target_round_id,
    resolve_target_task_contract_ids,
)
from round_control import (
    load_adjudication_file,
    project_dir,
)
from transition_specs import adjudication_plan_spec


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Compile bounded adjudication executor plan contracts into explicit executor followups.")
    parser.add_argument("--project-id", required=True)
    parser.add_argument("--adjudication-id")
    parser.add_argument("--in-place", action="store_true")
    return parser.parse_args()

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

def _resolve_contract_scalar(
    project_id: str,
    *,
    binding,
    contract: dict[str, object],
    adjudication_meta: dict[str, object],
    adjudication_sections: dict[str, str],
    resolved_payload: dict[str, object],
) -> object:
    return first_scalar(contract, binding.source_keys)


def _resolve_contract_list(
    project_id: str,
    *,
    binding,
    contract: dict[str, object],
    adjudication_meta: dict[str, object],
    adjudication_sections: dict[str, str],
    resolved_payload: dict[str, object],
) -> object:
    return first_list(contract, binding.source_keys)


def _resolve_contract_bool(
    project_id: str,
    *,
    binding,
    contract: dict[str, object],
    adjudication_meta: dict[str, object],
    adjudication_sections: dict[str, str],
    resolved_payload: dict[str, object],
) -> object:
    return any(bool(contract.get(key)) for key in binding.source_keys)


def _resolve_contract_or_meta_scalar(
    project_id: str,
    *,
    binding,
    contract: dict[str, object],
    adjudication_meta: dict[str, object],
    adjudication_sections: dict[str, str],
    resolved_payload: dict[str, object],
) -> object:
    return first_scalar(contract, binding.source_keys) or first_scalar(adjudication_meta, binding.source_keys)


def _resolve_contract_or_meta_list(
    project_id: str,
    *,
    binding,
    contract: dict[str, object],
    adjudication_meta: dict[str, object],
    adjudication_sections: dict[str, str],
    resolved_payload: dict[str, object],
) -> object:
    return first_list(contract, binding.source_keys) or first_list(adjudication_meta, binding.source_keys)


def _resolve_exception_contract_target_ids(
    project_id: str,
    *,
    binding,
    contract: dict[str, object],
    adjudication_meta: dict[str, object],
    adjudication_sections: dict[str, str],
    resolved_payload: dict[str, object],
) -> object:
    return resolve_target_exception_contract_ids(project_id, contract, binding.source_keys, adjudication_sections)


def _resolve_task_contract_target_ids(
    project_id: str,
    *,
    binding,
    contract: dict[str, object],
    adjudication_meta: dict[str, object],
    adjudication_sections: dict[str, str],
    resolved_payload: dict[str, object],
) -> object:
    return resolve_target_task_contract_ids(project_id, contract, binding.source_keys, adjudication_sections)


def _resolve_round_target_id(
    project_id: str,
    *,
    binding,
    contract: dict[str, object],
    adjudication_meta: dict[str, object],
    adjudication_sections: dict[str, str],
    resolved_payload: dict[str, object],
) -> object:
    return resolve_target_round_id(
        project_id,
        contract,
        binding.source_keys,
        adjudication_meta,
        adjudication_sections,
    )


def _resolve_round_validated_by_list(
    project_id: str,
    *,
    binding,
    contract: dict[str, object],
    adjudication_meta: dict[str, object],
    adjudication_sections: dict[str, str],
    resolved_payload: dict[str, object],
) -> object:
    return resolve_round_validated_by(
        project_id,
        contract=contract,
        source_keys=binding.source_keys,
        resolved_payload=resolved_payload,
    )


ADJUDICATION_BINDING_RESOLVERS = {
    "contract_scalar": _resolve_contract_scalar,
    "contract_list": _resolve_contract_list,
    "contract_bool": _resolve_contract_bool,
    "contract_or_meta_scalar": _resolve_contract_or_meta_scalar,
    "contract_or_meta_list": _resolve_contract_or_meta_list,
    "exception_contract_target_ids": _resolve_exception_contract_target_ids,
    "task_contract_target_ids": _resolve_task_contract_target_ids,
    "round_target_id": _resolve_round_target_id,
    "round_validated_by_list": _resolve_round_validated_by_list,
}


def _apply_plan_target_resolution(
    project_id: str,
    *,
    plan_spec,
    contract: dict[str, object],
    adjudication_meta: dict[str, object],
    adjudication_sections: dict[str, str],
) -> None:
    target_resolution = str(plan_spec.target_resolution or "").strip()
    if target_resolution == "explicit_or_adjudication_objective":
        if not (first_scalar(contract, ("objective_id",)) or first_scalar(adjudication_meta, ("objective_id",))):
            raise SystemExit(
                f"executor plan `{plan_spec.plan_type}` could not resolve objective target from explicit input or adjudication context"
            )
        return
    if target_resolution == "explicit_round_id_or_invalidated_open_round_or_open_round_for_objective_context":
        resolve_target_round_id(project_id, contract, ("round_id",), adjudication_meta, adjudication_sections)
        return
    if target_resolution == "resolve_open_task_contracts_from_explicit_ids_or_invalidated_objects":
        resolve_target_task_contract_ids(project_id, contract, ("task_contract_id", "task_contract_ids"), adjudication_sections)
        return
    if target_resolution == "resolve_open_task_contracts_from_invalidated_objects":
        resolve_target_task_contract_ids(project_id, contract, tuple(), adjudication_sections)
        return
    if target_resolution == "resolve_active_exception_contracts_from_invalidated_objects":
        resolve_target_exception_contract_ids(project_id, contract, tuple(), adjudication_sections)
        return
    raise SystemExit(f"unsupported adjudication plan target-resolution `{target_resolution}`")


def _resolve_binding_value(
    project_id: str,
    *,
    binding,
    contract: dict[str, object],
    adjudication_meta: dict[str, object],
    adjudication_sections: dict[str, str],
    resolved_payload: dict[str, object],
) -> object:
    resolver = ADJUDICATION_BINDING_RESOLVERS.get(binding.resolver)
    if resolver is None:
        raise SystemExit(f"unsupported adjudication payload binding resolver `{binding.resolver}`")
    return resolver(
        project_id,
        binding=binding,
        contract=contract,
        adjudication_meta=adjudication_meta,
        adjudication_sections=adjudication_sections,
        resolved_payload=resolved_payload,
    )


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
        _apply_plan_target_resolution(
            project_id,
            plan_spec=plan_spec,
            contract=contract,
            adjudication_meta=adjudication_meta,
            adjudication_sections=adjudication_sections,
        )
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
