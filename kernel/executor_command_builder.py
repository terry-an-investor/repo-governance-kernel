#!/usr/bin/env python3
from __future__ import annotations

import sys

from kernel.transition_specs import command_allowed_executor_payload_keys, executor_field_specs_for_command, mutable_field_specs_for_command
from kernel.runtime_paths import resolve_repo_root


ROOT = resolve_repo_root()
SCRIPTS = ROOT / "scripts"


def string_list(value: object) -> list[str]:
    if isinstance(value, list):
        return [str(item).strip() for item in value if str(item).strip()]
    if isinstance(value, str) and value.strip():
        return [value.strip()]
    return []


def reject_unknown_payload_keys(command_name: str, payload: dict[str, object]) -> None:
    allowed_keys = command_allowed_executor_payload_keys(command_name)
    unknown_keys = sorted(set(payload) - {"command"} - allowed_keys)
    if unknown_keys:
        raise SystemExit(
            f"executor {command_name} payload carries undeclared private keys: {', '.join(unknown_keys)}"
        )


def append_executor_field_specs(cmd: list[str], payload: dict[str, object], command_name: str) -> None:
    reject_unknown_payload_keys(command_name, payload)
    for field_spec in executor_field_specs_for_command(command_name):
        cli_flag = f"--{field_spec.cli_flag}"
        if field_spec.value_kind == "scalar":
            value = str(payload.get(field_spec.payload_key) or "").strip()
            if field_spec.required and not value:
                raise SystemExit(f"executor {command_name} requires `{field_spec.payload_key}`")
            if value:
                cmd.extend([cli_flag, value])
            continue
        if field_spec.value_kind == "list":
            values = string_list(payload.get(field_spec.payload_key))
            if field_spec.required and not values:
                raise SystemExit(f"executor {command_name} requires `{field_spec.payload_key}`")
            for item in values:
                cmd.extend([cli_flag, item])
            continue
        if field_spec.value_kind == "bool":
            if field_spec.required and not bool(payload.get(field_spec.payload_key)):
                raise SystemExit(f"executor {command_name} requires `{field_spec.payload_key}`")
            if bool(payload.get(field_spec.payload_key)):
                cmd.append(cli_flag)
            continue
        raise SystemExit(
            f"executor {command_name} encountered unsupported executor value kind `{field_spec.value_kind}`"
        )


def append_mutable_field_specs(cmd: list[str], payload: dict[str, object], command_name: str) -> None:
    for field_spec in mutable_field_specs_for_command(command_name):
        cli_flag = f"--{field_spec.cli_flag}"
        if field_spec.value_kind == "scalar":
            value = str(payload.get(field_spec.payload_key) or "").strip()
            if value:
                cmd.extend([cli_flag, value])
        else:
            for item in string_list(payload.get(field_spec.payload_key)):
                cmd.extend([cli_flag, item])
        if field_spec.replace_flag and bool(payload.get(field_spec.replace_flag)):
            cmd.append(f"--{field_spec.replace_flag.replace('_', '-')}")


def build_registry_executor_command(project_id: str, payload: dict[str, object], command_name: str) -> list[str]:
    cmd = [sys.executable, str(SCRIPTS / f"{command_name.replace('-', '_')}.py"), "--project-id", project_id]
    append_executor_field_specs(cmd, payload, command_name)
    append_mutable_field_specs(cmd, payload, command_name)
    return cmd

