#!/usr/bin/env python3
from __future__ import annotations

import json
import os
import shutil
import stat
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
SCRIPTS = ROOT / "scripts"


def parse_last_json_object(text: str) -> dict:
    stripped = text.strip()
    if not stripped:
        raise json.JSONDecodeError("empty output", text, 0)
    for index, char in enumerate(stripped):
        if char != "{":
            continue
        candidate = stripped[index:]
        try:
            return json.loads(candidate)
        except json.JSONDecodeError:
            continue
    raise json.JSONDecodeError("no json object found", text, 0)


def run_json(script_name: str, *args: str, expect_failure: bool = False) -> dict:
    cmd = [sys.executable, str(SCRIPTS / script_name), *args]
    completed = subprocess.run(
        cmd,
        cwd=str(ROOT),
        capture_output=True,
        text=True,
        check=False,
    )
    if completed.returncode != 0 and not expect_failure:
        raise SystemExit(
            json.dumps(
                {
                    "script": script_name,
                    "args": list(args),
                    "returncode": completed.returncode,
                    "stdout": completed.stdout,
                    "stderr": completed.stderr,
                },
                ensure_ascii=True,
                indent=2,
            )
        )
    if completed.returncode == 0 and expect_failure:
        raise SystemExit(f"{script_name} unexpectedly succeeded")
    payload = completed.stdout if completed.stdout.strip() else completed.stderr
    try:
        return parse_last_json_object(payload)
    except json.JSONDecodeError as exc:
        raise SystemExit(
            json.dumps(
                {
                    "script": script_name,
                    "args": list(args),
                    "returncode": completed.returncode,
                    "stdout": completed.stdout,
                    "stderr": completed.stderr,
                    "decode_error": str(exc),
                },
                ensure_ascii=True,
                indent=2,
            )
        )


def run_plain(script_name: str, *args: str) -> None:
    cmd = [sys.executable, str(SCRIPTS / script_name), *args]
    subprocess.run(cmd, cwd=str(ROOT), check=True)


def run_git(repo_dir: Path, *args: str) -> None:
    subprocess.run(["git", "-C", str(repo_dir), *args], cwd=str(ROOT), check=True)


def on_rm_error(func, path, exc_info) -> None:
    os.chmod(path, stat.S_IWRITE)
    func(path)


def reset_fixture_repo(fixture_dir: Path) -> None:
    if fixture_dir.exists():
        shutil.rmtree(fixture_dir, onerror=on_rm_error)


def init_fixture_repo(fixture_dir: Path, *, commit_message: str) -> None:
    run_git(fixture_dir, "init")
    run_git(fixture_dir, "config", "user.email", "fixture@example.com")
    run_git(fixture_dir, "config", "user.name", "Fixture Smoke")
    run_git(fixture_dir, "add", ".")
    run_git(fixture_dir, "commit", "-m", commit_message)
