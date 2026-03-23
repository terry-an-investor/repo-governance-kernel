#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path

from round_control import (
    load_adjudication_file,
    load_exception_contract_file,
    load_round_file,
    locate_exception_contract_file,
    locate_round_file,
    parse_bullet_list,
    project_dir,
)


SUPPORTED_PLAN_TYPES = {
    "rewrite-open-round-then-close-chain",
    "retire-invalidated-exception-contracts",
    "invalidate-invalidated-exception-contracts",
    "enter-execution-with-round-bootstrap",
}


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


def _compile_rewrite_then_close_chain(project_id: str, contract: dict[str, object]) -> list[dict[str, object]]:
    round_id = str(contract.get("round_id") or "").strip()
    if not round_id:
        raise SystemExit("executor plan contract `rewrite-open-round-then-close-chain` requires `round_id`")
    round_path = locate_round_file(project_id, round_id)
    if round_path is None:
        raise SystemExit(f"executor plan contract could not find round `{round_id}`")

    _round_meta, round_sections = load_round_file(round_path)
    rewrite_reason = str(contract.get("rewrite_reason") or "").strip()
    if not rewrite_reason:
        raise SystemExit("executor plan contract requires `rewrite_reason`")
    validation_pending_reason = str(contract.get("validation_pending_reason") or "").strip()
    captured_reason = str(contract.get("captured_reason") or "").strip()
    closed_reason = str(contract.get("closed_reason") or "").strip()
    if not validation_pending_reason or not captured_reason or not closed_reason:
        raise SystemExit(
            "executor plan contract requires `validation_pending_reason`, `captured_reason`, and `closed_reason`"
        )

    rewrite_payload: dict[str, object] = {
        "command": "rewrite-open-round",
        "round_id": round_id,
        "reason": rewrite_reason,
    }
    for source_key, output_key in [
        ("title", "title"),
        ("summary", "summary"),
        ("deliverable", "deliverable"),
        ("validation_plan", "validation_plan"),
    ]:
        value = str(contract.get(source_key) or "").strip()
        if value:
            rewrite_payload[output_key] = value
    for source_key, output_key in [
        ("scope_item", "scope_item"),
        ("scope_path", "scope_path"),
        ("risk", "risk"),
        ("blocker", "blocker"),
        ("status_note", "status_note"),
    ]:
        values = _normalize_list(contract.get(source_key))
        if values:
            rewrite_payload[output_key] = values
    for source_key, output_key in [
        ("replace_scope_items", "replace_scope_items"),
        ("replace_scope_paths", "replace_scope_paths"),
        ("replace_risks", "replace_risks"),
        ("replace_blockers", "replace_blockers"),
    ]:
        if bool(contract.get(source_key)):
            rewrite_payload[output_key] = True

    round_close_chain_payload: dict[str, object] = {
        "command": "round-close-chain",
        "round_id": round_id,
        "validation_pending_reason": validation_pending_reason,
        "captured_reason": captured_reason,
        "closed_reason": closed_reason,
    }
    validated_by = _normalize_list(contract.get("validated_by"))
    if not validated_by:
        existing_plan = str(round_sections.get("Validation Plan", "")).strip()
        validated_by = [existing_plan] if existing_plan else ["Adjudication executor plan validation"]
    round_close_chain_payload["validated_by"] = validated_by
    if bool(contract.get("clear_blockers")):
        round_close_chain_payload["clear_blockers"] = True
    blockers = _normalize_list(contract.get("close_chain_blocker"))
    if blockers:
        round_close_chain_payload["blocker"] = blockers
    risks = _normalize_list(contract.get("close_chain_risk"))
    if risks:
        round_close_chain_payload["risk"] = risks

    return [rewrite_payload, round_close_chain_payload]


def _resolve_target_exception_contract_ids(
    project_id: str,
    contract: dict[str, object],
    adjudication_sections: dict[str, str],
) -> list[str]:
    explicit_ids = _normalize_list(contract.get("exception_contract_id")) + _normalize_list(contract.get("exception_contract_ids"))
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


def _compile_exception_contract_plan(
    project_id: str,
    contract: dict[str, object],
    adjudication_sections: dict[str, str],
    *,
    command_name: str,
) -> list[dict[str, object]]:
    reason = str(contract.get("reason") or "").strip()
    if not reason:
        raise SystemExit(f"executor plan contract `{contract.get('plan_type')}` requires `reason`")

    payloads: list[dict[str, object]] = []
    evidence = _normalize_list(contract.get("evidence"))
    pivot_id = str(contract.get("pivot_id") or "").strip()
    for exception_contract_id in _resolve_target_exception_contract_ids(project_id, contract, adjudication_sections):
        payload: dict[str, object] = {
            "command": command_name,
            "exception_contract_id": exception_contract_id,
            "reason": reason,
        }
        if evidence:
            payload["evidence"] = evidence
        if command_name == "invalidate-exception-contract" and pivot_id:
            payload["pivot_id"] = pivot_id
        payloads.append(payload)
    return payloads


def _compile_enter_execution_with_round_bootstrap(
    contract: dict[str, object],
    adjudication_meta: dict[str, object],
) -> list[dict[str, object]]:
    reason = str(contract.get("reason") or "").strip()
    if not reason:
        raise SystemExit("executor plan contract `enter-execution-with-round-bootstrap` requires `reason`")

    payload: dict[str, object] = {
        "command": "set-phase",
        "phase": "execution",
        "reason": reason,
        "auto_open_round": True,
    }
    objective_id = str(contract.get("objective_id") or adjudication_meta.get("objective_id") or "").strip()
    if objective_id:
        payload["objective_id"] = objective_id

    round_title = str(contract.get("round_title") or adjudication_meta.get("round_title") or "").strip()
    round_deliverable = str(contract.get("round_deliverable") or adjudication_meta.get("round_deliverable") or "").strip()
    round_validation_plan = str(contract.get("round_validation_plan") or adjudication_meta.get("round_validation_plan") or "").strip()
    round_scope_items = _normalize_list(contract.get("round_scope_item")) or _normalize_list(adjudication_meta.get("round_scope_items"))
    if not round_scope_items:
        round_scope_items = _normalize_list(contract.get("round_scope_items"))
    round_scope_paths = _normalize_list(contract.get("round_scope_path")) or _normalize_list(adjudication_meta.get("round_scope_paths"))
    if not round_scope_paths:
        round_scope_paths = _normalize_list(contract.get("round_scope_paths"))

    if not round_title or not round_deliverable or not round_validation_plan or not round_scope_items:
        raise SystemExit(
            "executor plan contract `enter-execution-with-round-bootstrap` requires adjudication round bootstrap fields: "
            "`round_title`, at least one `round_scope_item`, `round_deliverable`, and `round_validation_plan`"
        )

    payload["round_title"] = round_title
    payload["round_deliverable"] = round_deliverable
    payload["round_validation_plan"] = round_validation_plan
    payload["round_scope_item"] = round_scope_items
    if round_scope_paths:
        payload["round_scope_path"] = round_scope_paths

    round_summary = str(contract.get("round_summary") or "").strip()
    if round_summary:
        payload["round_summary"] = round_summary
    round_risks = _normalize_list(contract.get("round_risk")) or _normalize_list(adjudication_meta.get("round_risks"))
    if round_risks:
        payload["round_risk"] = round_risks
    round_blockers = _normalize_list(contract.get("round_blocker")) or _normalize_list(adjudication_meta.get("round_blockers"))
    if round_blockers:
        payload["round_blocker"] = round_blockers
    round_status_note = str(contract.get("round_status_note") or adjudication_meta.get("round_status_note") or "").strip()
    if round_status_note:
        payload["round_status_note"] = round_status_note
    evidence = _normalize_list(contract.get("evidence"))
    if evidence:
        payload["evidence"] = evidence
    scope_review_note = _normalize_list(contract.get("scope_review_note"))
    if scope_review_note:
        payload["scope_review_note"] = scope_review_note
    return [payload]


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
        if plan_type not in SUPPORTED_PLAN_TYPES:
            raise SystemExit(
                f"unsupported executor plan type `{plan_type}`; supported plan types: {', '.join(sorted(SUPPORTED_PLAN_TYPES))}"
            )
        if plan_type == "rewrite-open-round-then-close-chain":
            payloads = _compile_rewrite_then_close_chain(project_id, contract)
        elif plan_type == "retire-invalidated-exception-contracts":
            payloads = _compile_exception_contract_plan(
                project_id,
                contract,
                adjudication_sections,
                command_name="retire-exception-contract",
            )
        elif plan_type == "invalidate-invalidated-exception-contracts":
            payloads = _compile_exception_contract_plan(
                project_id,
                contract,
                adjudication_sections,
                command_name="invalidate-exception-contract",
            )
        elif plan_type == "enter-execution-with-round-bootstrap":
            payloads = _compile_enter_execution_with_round_bootstrap(contract, adjudication_meta)
        else:
            raise SystemExit(f"unsupported executor plan type `{plan_type}`")
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
