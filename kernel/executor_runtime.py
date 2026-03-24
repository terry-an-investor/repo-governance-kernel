#!/usr/bin/env python3
from __future__ import annotations

import json
import subprocess
from pathlib import Path

from kernel.executor_command_builder import build_registry_executor_command


ROOT = Path(__file__).resolve().parent.parent


def run_command(cmd: list[str], *, failure_message: str) -> tuple[bool, str]:
    completed = subprocess.run(
        cmd,
        cwd=str(ROOT),
        capture_output=True,
        text=True,
        check=False,
    )
    if completed.returncode != 0:
        return False, completed.stderr.strip() or completed.stdout.strip() or failure_message
    return True, completed.stdout.strip()


def run_registry_command(
    project_id: str,
    payload: dict[str, object],
    command_name: str,
    *,
    failure_message: str,
) -> tuple[bool, str]:
    cmd = build_registry_executor_command(project_id, payload, command_name)
    return run_command(cmd, failure_message=failure_message)


def run_registry_command_json(
    project_id: str,
    payload: dict[str, object],
    command_name: str,
    *,
    failure_message: str,
) -> dict[str, object]:
    success, detail = run_registry_command(
        project_id,
        payload,
        command_name,
        failure_message=failure_message,
    )
    if not success:
        raise SystemExit(detail)
    try:
        parsed = json.loads(detail)
    except json.JSONDecodeError as exc:
        raise SystemExit(f"{command_name} returned invalid json: {exc}") from exc
    if not isinstance(parsed, dict):
        raise SystemExit(f"{command_name} returned non-object json")
    return parsed

