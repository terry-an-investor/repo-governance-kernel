#!/usr/bin/env python3
from __future__ import annotations

from kernel.executor_command_builder import string_list
from kernel.executor_runtime import run_registry_command
from kernel.resolver_runtime import resolve_hard_pivot_bundle_state, resolve_round_status_from_round_id
from kernel.transition_specs import (
    bundle_allowed_payload_keys,
    bundle_field_specs,
    bundle_governance_names,
    bundle_governance_spec,
    bundle_route_state_spec,
    bundle_step_template_spec,
    executor_supported_command_names,
)


def _string_list(value: object) -> list[str]:
    return string_list(value)


def _field_value_present(value_kind: str, value: object) -> bool:
    if value_kind == "scalar":
        return bool(str(value or "").strip())
    if value_kind == "list":
        return bool(_string_list(value))
    if value_kind == "bool":
        return bool(value)
    raise SystemExit(f"unsupported executor value kind `{value_kind}`")


def _validate_bundle_payload(payload: dict[str, object], bundle_name: str) -> None:
    unknown_keys = sorted(set(payload) - {"command"} - bundle_allowed_payload_keys(bundle_name))
    if unknown_keys:
        raise SystemExit(
            f"executor {bundle_name} payload carries undeclared private keys: {', '.join(unknown_keys)}"
        )
    for field_spec in bundle_field_specs(bundle_name):
        if field_spec.required and not _field_value_present(field_spec.value_kind, payload.get(field_spec.payload_key)):
            raise SystemExit(f"executor {bundle_name} requires `{field_spec.payload_key}`")


def bundle_executor_handler_names() -> list[str]:
    return sorted(bundle_governance_names())


def validate_bundle_governance_executor_contracts() -> None:
    governed_bundle_names = set(bundle_governance_names())
    executor_bundle_names = set(bundle_executor_handler_names())
    missing_executor_handlers = sorted(governed_bundle_names - executor_bundle_names)
    undocumented_executor_handlers = sorted(executor_bundle_names - governed_bundle_names)
    if missing_executor_handlers or undocumented_executor_handlers:
        details: list[str] = []
        if missing_executor_handlers:
            details.append(
                "missing executor handlers for governed bundle wrappers: "
                + ", ".join(f"`{name}`" for name in missing_executor_handlers)
            )
        if undocumented_executor_handlers:
            details.append(
                "executor exposes ungoverned bundle handlers: "
                + ", ".join(f"`{name}`" for name in undocumented_executor_handlers)
            )
        raise SystemExit("; ".join(details))


def supported_executor_commands() -> set[str]:
    validate_bundle_governance_executor_contracts()
    return set(executor_supported_command_names()) | set(bundle_executor_handler_names())


def resolve_constant_start_state(_project_id: str, _payload: dict[str, object]) -> str:
    return "start"


GOVERNED_BUNDLE_STATE_RESOLVERS = {
    "round_status_from_round_id": resolve_round_status_from_round_id,
    "hard_pivot_bundle_state_from_previous_objective_and_round": resolve_hard_pivot_bundle_state,
    "constant_start_state": resolve_constant_start_state,
}


def _resolve_bundle_current_state(project_id: str, bundle_name: str, payload: dict[str, object]) -> str:
    resolver_name = bundle_governance_spec(bundle_name).state_resolver
    resolver = GOVERNED_BUNDLE_STATE_RESOLVERS.get(resolver_name)
    if resolver is None:
        raise SystemExit(f"unsupported bundle state resolver `{resolver_name}`")
    return str(resolver(project_id, payload)).strip()


def _materialize_bundle_step_payload(
    bundle_name: str,
    bundle_payload: dict[str, object],
    *,
    from_state: str,
) -> tuple[str, str, str, dict[str, object]]:
    step_template = bundle_step_template_spec(bundle_name, from_state)
    command_name = step_template.command_name
    payload: dict[str, object] = {}
    for key, value in step_template.static_scalar_fields:
        payload[key] = value
    for key, value in step_template.static_bool_fields:
        payload[key] = value
    for binding in step_template.bindings:
        raw_value = bundle_payload.get(binding.source_key)
        if binding.value_kind == "scalar":
            value = str(raw_value or "").strip()
            if value:
                payload[binding.target_key] = value
            continue
        if binding.value_kind == "list":
            values = _string_list(raw_value)
            if values:
                payload[binding.target_key] = values
            continue
        if binding.value_kind == "bool":
            if bool(raw_value):
                payload[binding.target_key] = True
            continue
        raise SystemExit(
            f"bundle `{bundle_name}` step template `{step_template.label}` uses unsupported value kind `{binding.value_kind}`"
        )
    return step_template.label, command_name, step_template.to_state, payload


def execute_governed_bundle(project_id: str, payload: dict[str, object], bundle_name: str) -> tuple[bool, str]:
    _validate_bundle_payload(payload, bundle_name)
    current_state = _resolve_bundle_current_state(project_id, bundle_name, payload)
    route_state_spec = bundle_route_state_spec(bundle_name, current_state)
    round_id = str(payload.get("round_id") or "").strip()
    if route_state_spec.terminal:
        target_label = f"round `{round_id}`" if round_id else f"bundle `{bundle_name}` target"
        return True, f"{target_label} already {current_state}"

    missing_required_payloads = [
        key
        for key in route_state_spec.required_payload_keys
        if not _field_value_present(
            next(field.value_kind for field in bundle_field_specs(bundle_name) if field.payload_key == key),
            payload.get(key),
        )
    ]
    if missing_required_payloads:
        raise SystemExit(
            f"executor {bundle_name} requires {', '.join(f'`{key}`' for key in missing_required_payloads)} when target is `{current_state}`"
        )

    executed_steps: list[str] = []
    while True:
        route_state_spec = bundle_route_state_spec(bundle_name, current_state)
        if route_state_spec.terminal:
            break
        step_label, command_name, next_state, step_payload = _materialize_bundle_step_payload(
            bundle_name,
            payload,
            from_state=current_state,
        )
        if command_name in bundle_governance_names():
            success, detail = execute_governed_bundle(project_id, {"command": command_name, **step_payload}, command_name)
        else:
            success, detail = run_registry_command(
                project_id,
                step_payload,
                command_name,
                failure_message="executor follow-up failed",
            )
        if not success:
            target_label = f"round `{round_id}`" if round_id else f"bundle `{bundle_name}` target"
            return False, f"{target_label} {step_label} failed: {detail}"
        executed_steps.append(step_label)
        current_state = next_state

    target_label = f"round `{round_id}`" if round_id else f"bundle `{bundle_name}` target"
    return True, f"executed {bundle_name} for {target_label} ({', '.join(executed_steps)})"
