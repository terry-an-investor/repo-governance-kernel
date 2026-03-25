from __future__ import annotations

import json
from pathlib import Path


PUBLIC_FLOW_RESULT_SCHEMA = "repo-governance-kernel.public-flow-result"
PUBLIC_FLOW_RESULT_VERSION = "1"
PUBLIC_FLOW_AUTOMATION_SCOPE = "bounded-registry-owned-execution"


def _normalize_path(value: str) -> str:
    return str(Path(value).expanduser().resolve()).replace("\\", "/")


def _string_list(items: list[str] | None) -> list[str]:
    if not items:
        return []
    normalized: list[str] = []
    for item in items:
        candidate = str(item).strip()
        if candidate:
            normalized.append(candidate)
    return normalized


def public_flow_result_contract(flow_name: str, entrypoint: str, entry_kind: str) -> dict[str, str]:
    return {
        "schema": PUBLIC_FLOW_RESULT_SCHEMA,
        "version": PUBLIC_FLOW_RESULT_VERSION,
        "flow_name": flow_name,
        "entrypoint": entrypoint,
        "entry_kind": entry_kind,
        "automation_scope": PUBLIC_FLOW_AUTOMATION_SCOPE,
    }


def blocked_details(
    *,
    stage: str,
    code: str,
    message: str,
    meaning: str,
    suggested_next_actions: list[str] | None = None,
    details: dict[str, object] | None = None,
) -> dict[str, object]:
    payload: dict[str, object] = {
        "stage": stage,
        "code": code,
        "message": message,
        "meaning": meaning,
        "suggested_next_actions": _string_list(suggested_next_actions),
    }
    if details:
        payload["details"] = details
    return payload


def build_public_flow_payload(
    *,
    status: str,
    flow_name: str,
    entrypoint: str,
    entry_kind: str,
    project_id: str = "",
    workspace_root: str = "",
    source_repo: str = "",
    flow_contract: dict[str, object] | None = None,
    intent_compilation: dict[str, object] | None = None,
    execution: dict[str, object] | None = None,
    outcome: dict[str, object] | None = None,
    postconditions: dict[str, object] | None = None,
    next_actions: list[str] | None = None,
    blocked: dict[str, object] | None = None,
) -> dict[str, object]:
    payload: dict[str, object] = {
        "status": status,
        "result_contract": public_flow_result_contract(flow_name, entrypoint, entry_kind),
    }
    if project_id.strip():
        payload["project_id"] = project_id.strip()
    if workspace_root.strip():
        payload["workspace_root"] = _normalize_path(workspace_root)
    if source_repo.strip():
        payload["source_repo"] = _normalize_path(source_repo)
    if flow_contract is not None:
        payload["flow_contract"] = flow_contract
    if intent_compilation is not None:
        payload["intent_compilation"] = intent_compilation
    if execution is not None:
        payload["execution"] = execution
    if outcome is not None:
        payload["outcome"] = outcome
    if postconditions is not None:
        payload["postconditions"] = postconditions
    normalized_actions = _string_list(next_actions)
    if normalized_actions:
        payload["next_actions"] = normalized_actions
    if blocked is not None:
        payload["blocked"] = blocked
    return payload


def render_public_flow_payload(**kwargs: object) -> str:
    return json.dumps(build_public_flow_payload(**kwargs), ensure_ascii=True, indent=2)


def parse_json_dict(text: str) -> dict[str, object] | None:
    candidate = str(text or "").strip()
    if not candidate:
        return None
    try:
        parsed = json.loads(candidate)
    except json.JSONDecodeError:
        return None
    if not isinstance(parsed, dict):
        return None
    return parsed


def reframe_public_flow_payload(
    payload: dict[str, object],
    *,
    entrypoint: str,
    entry_kind: str,
    intent_compilation: dict[str, object] | None = None,
) -> dict[str, object]:
    result_contract = payload.get("result_contract")
    if not isinstance(result_contract, dict):
        raise SystemExit("public flow payload is missing result_contract")
    flow_name = str(result_contract.get("flow_name") or "").strip()
    if not flow_name:
        raise SystemExit("public flow payload result_contract is missing flow_name")

    reframed = dict(payload)
    reframed["result_contract"] = public_flow_result_contract(flow_name, entrypoint, entry_kind)
    if intent_compilation is not None:
        reframed["intent_compilation"] = intent_compilation
    return reframed
