#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path

from round_control import load_adjudication_file, load_round_file, locate_round_file, project_dir


SUPPORTED_PLAN_TYPES = {
    "rewrite-open-round-then-close-chain",
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


def compile_plan_contracts(project_id: str, plan_contracts: list[str]) -> list[str]:
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

    adjudication_path, meta, _sections = _load_adjudication_record(args.project_id, args.adjudication_id)
    plan_contracts = [str(item).strip() for item in meta.get("executor_plan_contracts", []) if str(item).strip()]
    if not plan_contracts:
        raise SystemExit(f"adjudication `{str(meta.get('id') or adjudication_path.stem)}` has no `executor_plan_contracts`")

    compiled_followups = compile_plan_contracts(args.project_id, plan_contracts)
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
