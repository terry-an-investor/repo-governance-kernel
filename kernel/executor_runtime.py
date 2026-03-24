#!/usr/bin/env python3
from __future__ import annotations

import json
import subprocess
import sys

from kernel.executor_command_builder import build_registry_executor_command
from kernel.runtime_paths import resolve_repo_root


ROOT = resolve_repo_root()


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


def run_cli_command(
    command_name: str,
    args: list[str],
    *,
    failure_message: str,
) -> tuple[bool, str]:
    completed = subprocess.run(
        [
            sys.executable,
            "-m",
            "kernel.cli",
            "--repo-root",
            str(ROOT),
            command_name,
            *args,
        ],
        cwd=str(ROOT),
        capture_output=True,
        text=True,
        check=False,
    )
    if completed.returncode != 0:
        return False, completed.stderr.strip() or completed.stdout.strip() or failure_message
    return True, completed.stdout.strip()


def run_cli_command_json(
    command_name: str,
    args: list[str],
    *,
    failure_message: str,
) -> dict[str, object]:
    success, detail = run_cli_command(
        command_name,
        args,
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


def run_registry_command(
    project_id: str,
    payload: dict[str, object],
    command_name: str,
    *,
    failure_message: str,
) -> tuple[bool, str]:
    cmd, env = build_registry_executor_command(project_id, payload, command_name)
    completed = subprocess.run(
        cmd,
        cwd=str(ROOT),
        capture_output=True,
        text=True,
        check=False,
        env=env,
    )
    if completed.returncode != 0:
        return False, completed.stderr.strip() or completed.stdout.strip() or failure_message
    return True, completed.stdout.strip()


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

