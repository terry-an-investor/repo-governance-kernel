#!/usr/bin/env python3
from __future__ import annotations

import json
import shutil
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
FIXTURE_ROOT = ROOT / "artifacts" / "fixtures" / "bootstrap-host"
PROJECT_ID = "bootstrap-host"


def run(cmd: list[str], *, cwd: Path) -> subprocess.CompletedProcess[str]:
    completed = subprocess.run(
        cmd,
        cwd=str(cwd),
        capture_output=True,
        text=True,
        check=False,
    )
    if completed.returncode != 0:
        raise SystemExit(
            json.dumps(
                {
                    "cmd": cmd,
                    "cwd": str(cwd),
                    "returncode": completed.returncode,
                    "stdout": completed.stdout,
                    "stderr": completed.stderr,
                },
                ensure_ascii=True,
                indent=2,
            )
        )
    return completed


def main() -> int:
    if FIXTURE_ROOT.exists():
        shutil.rmtree(FIXTURE_ROOT)
    FIXTURE_ROOT.mkdir(parents=True, exist_ok=True)

    run(["C:\\Program Files\\Git\\cmd\\git.exe", "init"], cwd=FIXTURE_ROOT)
    run(["C:\\Program Files\\Git\\cmd\\git.exe", "config", "user.email", "fixture@example.com"], cwd=FIXTURE_ROOT)
    run(["C:\\Program Files\\Git\\cmd\\git.exe", "config", "user.name", "Fixture Smoke"], cwd=FIXTURE_ROOT)

    bootstrap = run(
        [
            sys.executable,
            "-m",
            "kernel.cli",
            "--repo-root",
            str(FIXTURE_ROOT),
            "bootstrap-repo",
            "--project-id",
            PROJECT_ID,
        ],
        cwd=ROOT,
    )
    bootstrap_payload = json.loads(bootstrap.stdout)

    expected_paths = [
        FIXTURE_ROOT / ".githooks" / "pre-commit",
        FIXTURE_ROOT / ".githooks" / "pre-push",
        FIXTURE_ROOT / "projects" / PROJECT_ID / "control" / "constitution.md",
        FIXTURE_ROOT / "projects" / PROJECT_ID / "current" / "current-task.md",
        FIXTURE_ROOT / "projects" / PROJECT_ID / "control" / "pivot-log.md",
        FIXTURE_ROOT / "projects" / PROJECT_ID / "control" / "exception-ledger.md",
    ]
    missing = [str(path) for path in expected_paths if not path.exists()]
    if missing:
        raise SystemExit(f"bootstrap did not create expected paths: {', '.join(missing)}")

    hooks_path = run(
        ["C:\\Program Files\\Git\\cmd\\git.exe", "config", "--get", "core.hooksPath"],
        cwd=FIXTURE_ROOT,
    ).stdout.strip().replace("\\", "/")
    expected_hooks_path = str(FIXTURE_ROOT / ".githooks").replace("\\", "/")
    if hooks_path != expected_hooks_path:
        raise SystemExit(f"unexpected hooksPath `{hooks_path}`; expected `{expected_hooks_path}`")

    constitution_text = (FIXTURE_ROOT / "projects" / PROJECT_ID / "control" / "constitution.md").read_text(encoding="utf-8")
    if "Audit Hooks" not in constitution_text:
        raise SystemExit("bootstrap constitution is missing audit hooks")

    print(
        json.dumps(
            {
                "status": "ok",
                "project_id": PROJECT_ID,
                "fixture_root": str(FIXTURE_ROOT),
                "bootstrap": bootstrap_payload,
                "hooks_path": hooks_path,
            },
            ensure_ascii=True,
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
