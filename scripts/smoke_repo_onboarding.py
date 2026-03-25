#!/usr/bin/env python3
from __future__ import annotations

import json
import os
import shutil
import stat
import subprocess
import sys
from pathlib import Path

from git_exec import GIT_EXE


ROOT = Path(__file__).resolve().parent.parent
DIRECT_FIXTURE_ROOT = ROOT / "artifacts" / "fixtures" / "repo-onboarding-host"
INTENT_FIXTURE_ROOT = ROOT / "artifacts" / "fixtures" / "repo-onboarding-intent-host"
PROJECT_ID = "repo-onboarding-host"
INTENT_PROJECT_ID = "repo-onboarding-intent-host"
CLI = [sys.executable, "-m", "kernel.cli"]


def run(cmd: list[str], *, cwd: Path, expect_success: bool = True) -> subprocess.CompletedProcess[str]:
    completed = subprocess.run(
        cmd,
        cwd=str(cwd),
        capture_output=True,
        text=True,
        check=False,
    )
    if expect_success and completed.returncode != 0:
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


def cli_json(command: str, args: list[str], *, repo_root: Path, expect_success: bool = True) -> dict[str, object]:
    completed = run(
        [
            *CLI,
            "--repo-root",
            str(repo_root),
            command,
            *args,
        ],
        cwd=ROOT,
        expect_success=expect_success,
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


def assert_onboarding_result(
    *,
    onboarding: dict[str, object],
    fixture_root: Path,
    project_id: str,
    expected_repo_dirty_paths: list[str],
    expected_entrypoint: str,
) -> dict[str, object]:
    if str(onboarding.get("status") or "") != "ok":
        raise SystemExit("onboard-repo did not report ok")

    result_contract = onboarding.get("result_contract")
    if not isinstance(result_contract, dict):
        raise SystemExit("onboard-repo result is missing result_contract")
    if str(result_contract.get("flow_name") or "") != "repo-onboarding":
        raise SystemExit("unexpected onboarding flow_name")
    if str(result_contract.get("entrypoint") or "") != expected_entrypoint:
        raise SystemExit("unexpected onboarding entrypoint")

    contract = onboarding.get("flow_contract")
    if not isinstance(contract, dict):
        raise SystemExit("onboard-repo result is missing flow_contract")
    if str(contract.get("intent_class") or "") != "repo-first-host-onboarding":
        raise SystemExit("unexpected onboarding intent_class")
    if str(contract.get("bundle_name") or "") != "onboard-repo":
        raise SystemExit("unexpected onboarding bundle_name")

    execution = onboarding.get("execution")
    if not isinstance(execution, dict):
        raise SystemExit("onboard-repo result is missing execution")
    compiled = execution.get("compiled_bundle")
    if not isinstance(compiled, dict):
        raise SystemExit("onboard-repo result is missing execution.compiled_bundle")
    observed_dirty_paths = sorted(str(item) for item in compiled.get("observed_repo_dirty_paths", []))
    expected_sorted_dirty_paths = sorted(expected_repo_dirty_paths)
    if observed_dirty_paths != expected_sorted_dirty_paths:
        raise SystemExit(f"unexpected observed repo dirty paths: {observed_dirty_paths}")

    expected_scope_paths = sorted(
        [
            f"state/{project_id}",
            "githooks",
            "cross-project",
            "index",
            *expected_repo_dirty_paths,
        ]
    )
    actual_scope_paths = sorted(str(item) for item in compiled.get("onboarding_scope_paths", []))
    if actual_scope_paths != expected_scope_paths:
        raise SystemExit(f"unexpected onboarding scope paths: {actual_scope_paths}")

    outcome = onboarding.get("outcome")
    if not isinstance(outcome, dict):
        raise SystemExit("onboard-repo result is missing outcome")
    control_state = outcome.get("created_control_state")
    if not isinstance(control_state, dict):
        raise SystemExit("onboard-repo result is missing outcome.created_control_state")
    for field in ("objective_id", "round_id", "task_contract_id"):
        if not str(control_state.get(field) or "").strip():
            raise SystemExit(f"onboard-repo result is missing outcome.created_control_state.{field}")

    postconditions = onboarding.get("postconditions")
    if not isinstance(postconditions, dict):
        raise SystemExit("onboard-repo result is missing postconditions")
    audit = postconditions.get("audit")
    enforce = postconditions.get("enforce")
    if not isinstance(audit, dict) or str(postconditions.get("audit_status") or "") != "ok":
        raise SystemExit("onboard-repo did not leave audit-control-state ok")
    if not isinstance(enforce, dict) or str(postconditions.get("enforce_status") or "") != "ok":
        raise SystemExit("onboard-repo did not leave enforce-worktree ok")

    next_actions = onboarding.get("next_actions")
    if not isinstance(next_actions, list) or len(next_actions) < 3:
        raise SystemExit("onboard-repo result is missing stable next_actions")

    current_task = (fixture_root / "state" / project_id / "current" / "current-task.md").read_text(encoding="utf-8")
    normalized_fixture_root = str(fixture_root).replace("\\", "/")
    expected_workspace_root_line = f"Workspace root: `{normalized_fixture_root}`"
    if expected_workspace_root_line not in current_task:
        raise SystemExit("current-task anchor did not record the governed host workspace root")

    status_after = git_status_porcelain(fixture_root).replace("\\", "/")
    expected_status_markers = {
        "README.md": "README.md",
        "src/app.py": "src/",
    }
    for path, marker in expected_status_markers.items():
        if marker not in status_after:
            raise SystemExit(f"pre-existing repo dirty path disappeared after onboarding: {path}")

    return {
        "status": "ok",
        "project_id": project_id,
        "fixture_root": str(fixture_root),
        "observed_repo_dirty_paths": observed_dirty_paths,
        "onboarding_scope_paths": actual_scope_paths,
        "objective_id": control_state.get("objective_id"),
        "round_id": control_state.get("round_id"),
        "task_contract_id": control_state.get("task_contract_id"),
        "audit": audit,
        "enforce": enforce,
        "next_actions": next_actions,
    }


def main() -> int:
    result: dict[str, object] | None = None
    try:
        expected_repo_dirty_paths = prepare_dirty_host(DIRECT_FIXTURE_ROOT)
        status_before = git_status_porcelain(DIRECT_FIXTURE_ROOT).replace("\\", "/")
        if "README.md" not in status_before or "src/" not in status_before:
            raise SystemExit("fixture host did not preserve the expected pre-onboarding dirty paths")

        onboarding = cli_json(
            "onboard-repo",
            ["--project-id", PROJECT_ID],
            repo_root=DIRECT_FIXTURE_ROOT,
        )
        direct_result = assert_onboarding_result(
            onboarding=onboarding,
            fixture_root=DIRECT_FIXTURE_ROOT,
            project_id=PROJECT_ID,
            expected_repo_dirty_paths=expected_repo_dirty_paths,
            expected_entrypoint="onboard-repo",
        )
        blocked_onboarding = cli_json(
            "onboard-repo",
            ["--project-id", PROJECT_ID],
            repo_root=DIRECT_FIXTURE_ROOT,
            expect_success=False,
        )
        blocked_payload = blocked_onboarding.get("blocked")
        if str(blocked_onboarding.get("status") or "") != "blocked":
            raise SystemExit("repeat onboard-repo should report blocked")
        if not isinstance(blocked_payload, dict) or str(blocked_payload.get("code") or "") != "project_history_not_empty":
            raise SystemExit("repeat onboard-repo should identify project_history_not_empty")
        if str((blocked_onboarding.get("result_contract") or {}).get("entrypoint") or "") != "onboard-repo":
            raise SystemExit("repeat onboard-repo blocked payload should keep the direct entrypoint")

        expected_intent_dirty_paths = prepare_dirty_host(INTENT_FIXTURE_ROOT)
        intent_payload = cli_json(
            "onboard-repo-from-intent",
            [
                "--project-id",
                INTENT_PROJECT_ID,
                "--request",
                "Initialize governance for this repo.",
            ],
            repo_root=INTENT_FIXTURE_ROOT,
        )
        compiled_intent = intent_payload.get("intent_compilation")
        if not isinstance(compiled_intent, dict):
            raise SystemExit("onboard-repo-from-intent result is missing intent_compilation")
        if str(compiled_intent.get("intent_class") or "") != "repo-first-host-onboarding":
            raise SystemExit("unexpected onboarding intent_compilation.intent_class")
        if str(compiled_intent.get("bundle_name") or "") != "onboard-repo":
            raise SystemExit("unexpected onboarding intent_compilation.bundle_name")
        intent_result = assert_onboarding_result(
            onboarding=intent_payload,
            fixture_root=INTENT_FIXTURE_ROOT,
            project_id=INTENT_PROJECT_ID,
            expected_repo_dirty_paths=expected_intent_dirty_paths,
            expected_entrypoint="onboard-repo-from-intent",
        )
        blocked_intent = cli_json(
            "onboard-repo-from-intent",
            [
                "--project-id",
                INTENT_PROJECT_ID,
                "--request",
                "Monitor this repo continuously.",
            ],
            repo_root=INTENT_FIXTURE_ROOT,
            expect_success=False,
        )
        blocked_intent_payload = blocked_intent.get("blocked")
        if str(blocked_intent.get("status") or "") != "blocked":
            raise SystemExit("monitoring onboarding intent should report blocked")
        if not isinstance(blocked_intent_payload, dict) or str(blocked_intent_payload.get("code") or "") != "unsupported_request_scope":
            raise SystemExit("monitoring onboarding intent should identify unsupported_request_scope")
        if str((blocked_intent.get("result_contract") or {}).get("entrypoint") or "") != "onboard-repo-from-intent":
            raise SystemExit("blocked onboarding intent should keep the intent entrypoint")

        result = {
            "status": "ok",
            "direct_onboarding": direct_result,
            "intent_onboarding": intent_result,
            "intent_compilation": compiled_intent,
            "blocked_direct": blocked_onboarding,
            "blocked_intent": blocked_intent,
        }
    finally:
        cleanup_path(DIRECT_FIXTURE_ROOT)
        cleanup_path(INTENT_FIXTURE_ROOT)

    print(json.dumps(result, ensure_ascii=True, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
