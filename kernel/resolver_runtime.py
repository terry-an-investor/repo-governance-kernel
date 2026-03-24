#!/usr/bin/env python3
from __future__ import annotations

from kernel.round_control import (
    OPEN_ROUND_STATUSES,
    OPEN_TASK_CONTRACT_STATUSES,
    find_rounds,
    load_exception_contract_file,
    load_objective_file,
    load_round_file,
    load_task_contract_file,
    locate_exception_contract_file,
    locate_objective_file,
    locate_round_file,
    locate_task_contract_file,
    parse_bullet_list,
    select_open_round_record,
)


def normalize_list(value: object) -> list[str]:
    if isinstance(value, list):
        return [str(item).strip() for item in value if str(item).strip()]
    if isinstance(value, str) and value.strip():
        return [value.strip()]
    return []


def first_scalar(mapping: dict[str, object], source_keys: tuple[str, ...]) -> str:
    for key in source_keys:
        value = str(mapping.get(key) or "").strip()
        if value:
            return value
    return ""


def first_list(mapping: dict[str, object], source_keys: tuple[str, ...]) -> list[str]:
    for key in source_keys:
        values = normalize_list(mapping.get(key))
        if values:
            return values
    return []


def resolve_round_status_from_round_id(project_id: str, payload: dict[str, object]) -> str:
    round_id = first_scalar(payload, ("round_id",))
    if not round_id:
        raise SystemExit("bundle state resolver `round_status_from_round_id` requires `round_id`")
    round_path = locate_round_file(project_id, round_id)
    if round_path is None:
        raise SystemExit(f"bundle state resolver could not find round `{round_id}`")
    round_meta, _sections = load_round_file(round_path)
    current_status = str(round_meta.get("status") or "").strip()
    if not current_status:
        raise SystemExit(f"bundle state resolver found round `{round_id}` without a status")
    return current_status


def resolve_hard_pivot_bundle_state(project_id: str, payload: dict[str, object]) -> str:
    previous_objective_id = first_scalar(payload, ("previous_objective_id",))
    if not previous_objective_id:
        raise SystemExit(
            "bundle state resolver `hard_pivot_bundle_state_from_previous_objective_and_round` requires `previous_objective_id`"
        )
    objective_path = locate_objective_file(project_id, previous_objective_id)
    if objective_path is None:
        raise SystemExit(
            f"bundle state resolver could not find previous objective `{previous_objective_id}`"
        )
    objective_meta, _objective_sections = load_objective_file(objective_path)
    objective_status = str(objective_meta.get("status") or "").strip()
    if objective_status == "superseded":
        return "pivoted"

    return resolve_round_close_target_state(project_id, payload)


def resolve_target_exception_contract_ids(
    project_id: str,
    contract: dict[str, object],
    source_keys: tuple[str, ...],
    adjudication_sections: dict[str, str],
) -> list[str]:
    explicit_ids = first_list(contract, source_keys)
    candidate_ids = explicit_ids or parse_bullet_list(adjudication_sections.get("Objects Invalidated", ""))
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


def resolve_target_task_contract_ids(
    project_id: str,
    contract: dict[str, object],
    source_keys: tuple[str, ...],
    adjudication_sections: dict[str, str],
) -> list[str]:
    explicit_ids = first_list(contract, source_keys)
    candidate_ids = explicit_ids or parse_bullet_list(adjudication_sections.get("Objects Invalidated", ""))
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


def resolve_target_round_id(
    project_id: str,
    contract: dict[str, object],
    source_keys: tuple[str, ...],
    adjudication_meta: dict[str, object],
    adjudication_sections: dict[str, str],
) -> str:
    explicit_round_id = first_scalar(contract, source_keys)
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

    objective_id = first_scalar(contract, ("objective_id",)) or first_scalar(adjudication_meta, ("objective_id",))
    if objective_id:
        open_rounds = find_rounds(project_id, objective_id=objective_id, statuses=OPEN_ROUND_STATUSES)
        if len(open_rounds) == 1:
            _round_path, round_meta, _round_sections = open_rounds[0]
            return str(round_meta.get("id") or "").strip()
        if len(open_rounds) > 1:
            raise SystemExit(f"executor round plan found multiple open rounds for objective `{objective_id}`")

    open_round_record, open_round_issues = select_open_round_record(project_id)
    if open_round_issues:
        raise SystemExit("executor round plan could not resolve one open round target: " + "; ".join(open_round_issues))
    if open_round_record is not None:
        _round_path, round_meta, _round_sections = open_round_record
        return str(round_meta.get("id") or "").strip()

    raise SystemExit(
        "executor round plan could not resolve one open round target from explicit `round_id`, adjudication `Objects Invalidated`, or objective context"
    )


def resolve_round_close_target_id(
    project_id: str,
    contract: dict[str, object],
    source_keys: tuple[str, ...],
    adjudication_meta: dict[str, object],
    adjudication_sections: dict[str, str],
) -> str:
    explicit_round_id = first_scalar(contract, source_keys)
    candidate_ids: list[str] = []
    if explicit_round_id:
        candidate_ids.append(explicit_round_id)
    candidate_ids.extend(parse_bullet_list(adjudication_sections.get("Objects Invalidated", "")))

    seen_round_ids: set[str] = set()
    close_capable_rounds: list[str] = []
    for object_id in candidate_ids:
        normalized_id = str(object_id).strip()
        if not normalized_id or normalized_id in seen_round_ids:
            continue
        round_path = locate_round_file(project_id, normalized_id)
        if round_path is None:
            if explicit_round_id and normalized_id == explicit_round_id:
                raise SystemExit(f"executor round-close plan could not find round `{normalized_id}`")
            continue
        round_meta, _round_sections = load_round_file(round_path)
        current_status = str(round_meta.get("status") or "").strip()
        if current_status in {"blocked", *OPEN_ROUND_STATUSES - {"blocked"}}:
            seen_round_ids.add(normalized_id)
            close_capable_rounds.append(normalized_id)
            if explicit_round_id:
                return normalized_id
    if len(close_capable_rounds) == 1:
        return close_capable_rounds[0]
    if len(close_capable_rounds) > 1:
        raise SystemExit(
            "executor round-close plan found multiple close-capable rounds; "
            + ", ".join(f"`{round_id}`" for round_id in close_capable_rounds)
        )

    objective_id = first_scalar(contract, ("previous_objective_id", "objective_id")) or first_scalar(
        adjudication_meta,
        ("objective_id",),
    )
    if objective_id:
        objective_rounds = find_rounds(
            project_id,
            objective_id=objective_id,
            statuses={"draft", "active", "blocked", "validation_pending", "captured"},
        )
        if len(objective_rounds) == 1:
            _round_path, round_meta, _round_sections = objective_rounds[0]
            return str(round_meta.get("id") or "").strip()
        if len(objective_rounds) > 1:
            raise SystemExit(f"executor round-close plan found multiple close-capable rounds for objective `{objective_id}`")

    raise SystemExit(
        "executor round-close plan could not resolve one round target from explicit `round_id`, adjudication `Objects Invalidated`, or objective context"
    )


def resolve_round_close_target_state(project_id: str, payload: dict[str, object]) -> str:
    round_id = first_scalar(payload, ("round_id",))
    if not round_id:
        raise SystemExit("bundle state resolver requires `round_id`")
    round_path = locate_round_file(project_id, round_id)
    if round_path is None:
        raise SystemExit(f"bundle state resolver could not find round `{round_id}`")
    round_meta, _sections = load_round_file(round_path)
    current_status = str(round_meta.get("status") or "").strip()
    if not current_status:
        raise SystemExit(f"bundle state resolver found round `{round_id}` without a status")
    if current_status not in {"active", "blocked", "validation_pending", "captured", "closed"}:
        raise SystemExit(
            f"bundle state resolver requires a close-capable round status; `{round_id}` is `{current_status}`"
        )
    return current_status


def resolve_round_validated_by(
    project_id: str,
    *,
    contract: dict[str, object],
    source_keys: tuple[str, ...],
    resolved_payload: dict[str, object],
) -> list[str]:
    validated_by = first_list(contract, source_keys)
    if validated_by:
        return validated_by

    round_id = str(resolved_payload.get("round_id") or first_scalar(contract, ("round_id",))).strip()
    if not round_id:
        raise SystemExit("executor plan contract could not resolve `round_id` before deriving `validated_by`")
    round_path = locate_round_file(project_id, round_id)
    if round_path is None:
        raise SystemExit(f"executor plan contract could not find round `{round_id}`")
    _round_meta, round_sections = load_round_file(round_path)
    existing_plan = str(round_sections.get("Validation Plan", "")).strip()
    return [existing_plan] if existing_plan else ["Adjudication executor plan validation"]

