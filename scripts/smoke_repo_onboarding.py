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
FIXTURE_ROOT = ROOT / "artifacts" / "fixtures" / "repo-onboarding-host"
PROJECT_ID = "repo-onboarding-host"
GIT_EXE = "C:\\Program Files\\Git\\cmd\\git.exe"
CLI = [sys.executable, "-m", "kernel.cli"]


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


def on_rm_error(func, path, exc_info) -> None:
    os.chmod(path, stat.S_IWRITE)
    func(path)


def cleanup_path(path: Path) -> None:
    if not path.exists():
        return
    if path.is_dir():
        shutil.rmtree(path, onerror=on_rm_error)
        return
    path.unlink()


def ensure_clean_dir(path: Path) -> None:
    cleanup_path(path)
    path.mkdir(parents=True, exist_ok=True)


def init_git_repo(path: Path) -> None:
    run([GIT_EXE, "init"], cwd=path)
    run([GIT_EXE, "config", "user.email", "fixture@example.com"], cwd=path)
    run([GIT_EXE, "config", "user.name", "Fixture Smoke"], cwd=path)


def cli_json(command: str, args: list[str], *, repo_root: Path) -> dict[str, object]:
    completed = run(
        [
            *CLI,
            "--repo-root",
            str(repo_root),
            command,
            *args,
        ],
        cwd=ROOT,
    )
    payload = completed.stdout.strip() or completed.stderr.strip()
    try:
        parsed = json.loads(payload)
    except json.JSONDecodeError as exc:
        raise SystemExit(f"{command} returned invalid json: {exc}") from exc
    if not isinstance(parsed, dict):
        raise SystemExit(f"{command} returned non-object json")
    return parsed


def git_status_porcelain(path: Path) -> str:
    return run([GIT_EXE, "status", "--short"], cwd=path).stdout.strip()


def prepare_dirty_host(path: Path) -> list[str]:
    ensure_clean_dir(path)
    init_git_repo(path)
    (path / "README.md").write_text("baseline host\n", encoding="utf-8", newline="\n")
    run([GIT_EXE, "add", "README.md"], cwd=path)
    run([GIT_EXE, "commit", "-m", "Initial host baseline"], cwd=path)

    (path / "README.md").write_text("baseline host changed\n", encoding="utf-8", newline="\n")
    src_dir = path / "src"
    src_dir.mkdir(parents=True, exist_ok=True)
    (src_dir / "app.py").write_text("print('fixture')\n", encoding="utf-8", newline="\n")
    return ["README.md", "src/app.py"]


def main() -> int:
    result: dict[str, object] | None = None
    try:
        expected_repo_dirty_paths = prepare_dirty_host(FIXTURE_ROOT)
        status_before = git_status_porcelain(FIXTURE_ROOT).replace("\\", "/")
        if "README.md" not in status_before or "src/" not in status_before:
            raise SystemExit("fixture host did not preserve the expected pre-onboarding dirty paths")

        onboarding = cli_json(
            "onboard-repo",
            ["--project-id", PROJECT_ID],
            repo_root=FIXTURE_ROOT,
        )

        if str(onboarding.get("status") or "") != "ok":
            raise SystemExit("onboard-repo did not report ok")
        observed_dirty_paths = sorted(str(item) for item in onboarding.get("observed_repo_dirty_paths", []))
        expected_sorted_dirty_paths = sorted(expected_repo_dirty_paths)
        if observed_dirty_paths != expected_sorted_dirty_paths:
            raise SystemExit(f"unexpected observed repo dirty paths: {observed_dirty_paths}")

        expected_scope_paths = sorted(
            [
                f"state/{PROJECT_ID}",
                "githooks",
                "cross-project",
                "index",
                *expected_repo_dirty_paths,
            ]
        )
        actual_scope_paths = sorted(str(item) for item in onboarding.get("onboarding_scope_paths", []))
        if actual_scope_paths != expected_scope_paths:
            raise SystemExit(f"unexpected onboarding scope paths: {actual_scope_paths}")

        audit = onboarding.get("audit")
        enforce = onboarding.get("enforce")
        if not isinstance(audit, dict) or str(audit.get("status") or "") != "ok":
            raise SystemExit("onboard-repo did not leave audit-control-state ok")
        if not isinstance(enforce, dict) or str(enforce.get("status") or "") != "ok":
            raise SystemExit("onboard-repo did not leave enforce-worktree ok")

        current_task = (FIXTURE_ROOT / "state" / PROJECT_ID / "current" / "current-task.md").read_text(encoding="utf-8")
        expected_workspace_root_line = f"Workspace root: `{str(FIXTURE_ROOT).replace('\\', '/')}`"
        if expected_workspace_root_line not in current_task:
            raise SystemExit("current-task anchor did not record the governed host workspace root")

        status_after = git_status_porcelain(FIXTURE_ROOT).replace("\\", "/")
        expected_status_markers = {
            "README.md": "README.md",
            "src/app.py": "src/",
        }
        for path, marker in expected_status_markers.items():
            if marker not in status_after:
                raise SystemExit(f"pre-existing repo dirty path disappeared after onboarding: {path}")

        result = {
            "status": "ok",
            "project_id": PROJECT_ID,
            "fixture_root": str(FIXTURE_ROOT),
            "observed_repo_dirty_paths": observed_dirty_paths,
            "onboarding_scope_paths": actual_scope_paths,
            "objective_id": onboarding.get("objective_id"),
            "round_id": onboarding.get("round_id"),
            "task_contract_id": onboarding.get("task_contract_id"),
            "audit": audit,
            "enforce": enforce,
        }
    finally:
        cleanup_path(FIXTURE_ROOT)

    print(json.dumps(result, ensure_ascii=True, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
