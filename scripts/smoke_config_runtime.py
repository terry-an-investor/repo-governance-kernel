#!/usr/bin/env python3
from __future__ import annotations

import json
import os
import shutil
import stat
import subprocess
import sys
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
FIXTURE_ROOT = ROOT / "artifacts" / "fixtures" / "config-runtime-host"
TEMP_HOME_ROOT = Path(tempfile.gettempdir()) / "repo-governance-kernel-config-runtime-home"
CONFIG_DIRNAME = ".repo-governance-kernel"
PROJECT_ID = "config-runtime-host"
PROJECT_LAYER_ID = "config-runtime-project"
LOCAL_LAYER_ID = "config-runtime-local"
ENV_LAYER_ID = "config-runtime-env"
FLAG_LAYER_ID = "config-runtime-flag"
GIT_EXE = "C:\\Program Files\\Git\\cmd\\git.exe"
CLI = [sys.executable, "-m", "kernel.cli"]


def run(cmd: list[str], *, cwd: Path, env: dict[str, str] | None = None) -> subprocess.CompletedProcess[str]:
    completed = subprocess.run(
        cmd,
        cwd=str(cwd),
        capture_output=True,
        text=True,
        check=False,
        env=env,
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


def write_json(path: Path, payload: dict[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=True, indent=2) + "\n", encoding="utf-8")


def runtime_env(extra: dict[str, str] | None = None) -> dict[str, str]:
    env = os.environ.copy()
    env.pop("REPO_GOVERNANCE_ROOT", None)
    env.pop("REPO_GOVERNANCE_PROJECT", None)
    env.pop("REPO_GOVERNANCE_CONFIG_RESOLUTION", None)
    env["HOME"] = str(TEMP_HOME_ROOT)
    env["USERPROFILE"] = str(TEMP_HOME_ROOT)
    if extra:
        env.update(extra)
    return env


def cli_json(
    command: str,
    args: list[str],
    *,
    cwd: Path,
    env: dict[str, str],
    repo_root: Path | None = None,
) -> dict[str, object]:
    cmd = [*CLI]
    if repo_root is not None:
        cmd.extend(["--repo-root", str(repo_root)])
    cmd.extend([command, *args])
    completed = run(cmd, cwd=cwd, env=env)
    payload = completed.stdout.strip() or completed.stderr.strip()
    try:
        parsed = json.loads(payload)
    except json.JSONDecodeError as exc:
        raise SystemExit(f"{command} returned invalid json: {exc}") from exc
    if not isinstance(parsed, dict):
        raise SystemExit(f"{command} returned non-object json")
    return parsed


def main() -> int:
    result: dict[str, object] | None = None
    try:
        ensure_clean_dir(FIXTURE_ROOT)
        ensure_clean_dir(TEMP_HOME_ROOT)
        init_git_repo(FIXTURE_ROOT)

        bootstrap = cli_json(
            "bootstrap-repo",
            ["--project-id", PROJECT_ID],
            cwd=ROOT,
            env=runtime_env(),
            repo_root=FIXTURE_ROOT,
        )

        user_config_path = TEMP_HOME_ROOT / CONFIG_DIRNAME / "config.json"
        write_json(
            user_config_path,
            {
                "repo_root": str(FIXTURE_ROOT),
                "project_id": PROJECT_ID,
            },
        )

        neutral_cwd = TEMP_HOME_ROOT / "neutral-cwd"
        neutral_cwd.mkdir(parents=True, exist_ok=True)
        describe_user = cli_json("describe-config", [], cwd=neutral_cwd, env=runtime_env())
        if str(describe_user["sources"]["repo_root"]) != "user_config":
            raise SystemExit(
                json.dumps(
                    {
                        "error": "unexpected_repo_root_source",
                        "expected": "user_config",
                        "actual": describe_user["sources"]["repo_root"],
                        "describe_user": describe_user,
                    },
                    ensure_ascii=True,
                    indent=2,
                )
            )
        if str(describe_user["sources"]["project_id"]) != "user_config":
            raise SystemExit(
                json.dumps(
                    {
                        "error": "unexpected_project_id_source",
                        "expected": "user_config",
                        "actual": describe_user["sources"]["project_id"],
                        "describe_user": describe_user,
                    },
                    ensure_ascii=True,
                    indent=2,
                )
            )
        if str(describe_user["resolved"]["repo_root"]).replace("\\", "/") != str(FIXTURE_ROOT).replace("\\", "/"):
            raise SystemExit("describe-config returned the wrong user-config repo_root")
        if str(describe_user["resolved"]["project_id"]) != PROJECT_ID:
            raise SystemExit("describe-config returned the wrong user-config project_id")

        audit_from_user_config = cli_json("audit-control-state", [], cwd=neutral_cwd, env=runtime_env())
        if str(audit_from_user_config.get("status") or "") != "ok":
            raise SystemExit("audit-control-state did not resolve project_id from config runtime")
        if str(audit_from_user_config.get("project_id") or "") != PROJECT_ID:
            raise SystemExit("audit-control-state used the wrong project_id from config runtime")

        project_config_path = FIXTURE_ROOT / CONFIG_DIRNAME / "project.json"
        local_override_path = FIXTURE_ROOT / CONFIG_DIRNAME / "local.json"
        write_json(project_config_path, {"project_id": PROJECT_LAYER_ID})
        describe_project = cli_json(
            "describe-config",
            [],
            cwd=neutral_cwd,
            env=runtime_env(),
            repo_root=FIXTURE_ROOT,
        )
        if str(describe_project["sources"]["project_id"]) != "project_config":
            raise SystemExit("project config did not override user config")

        write_json(local_override_path, {"project_id": LOCAL_LAYER_ID})
        describe_local = cli_json(
            "describe-config",
            [],
            cwd=neutral_cwd,
            env=runtime_env(),
            repo_root=FIXTURE_ROOT,
        )
        if str(describe_local["sources"]["project_id"]) != "local_override":
            raise SystemExit("local override did not override project config")
        if str(describe_local["resolved"]["project_id"]) != LOCAL_LAYER_ID:
            raise SystemExit("local override resolved the wrong project_id")

        describe_env = cli_json(
            "describe-config",
            [],
            cwd=neutral_cwd,
            env=runtime_env({"REPO_GOVERNANCE_PROJECT": ENV_LAYER_ID}),
            repo_root=FIXTURE_ROOT,
        )
        if str(describe_env["sources"]["project_id"]) != "environment":
            raise SystemExit("environment did not override local config")
        if str(describe_env["resolved"]["project_id"]) != ENV_LAYER_ID:
            raise SystemExit("environment resolved the wrong project_id")

        describe_flag = cli_json(
            "describe-config",
            ["--project-id", FLAG_LAYER_ID],
            cwd=neutral_cwd,
            env=runtime_env({"REPO_GOVERNANCE_PROJECT": ENV_LAYER_ID}),
            repo_root=FIXTURE_ROOT,
        )
        if str(describe_flag["sources"]["project_id"]) != "flag":
            raise SystemExit("explicit flag did not override environment config")
        if str(describe_flag["resolved"]["project_id"]) != FLAG_LAYER_ID:
            raise SystemExit("explicit flag resolved the wrong project_id")

        result = {
            "status": "ok",
            "bootstrap": bootstrap,
            "user_config": describe_user,
            "project_config_source": describe_project["sources"]["project_id"],
            "local_override_source": describe_local["sources"]["project_id"],
            "environment_source": describe_env["sources"]["project_id"],
            "flag_source": describe_flag["sources"]["project_id"],
            "audit_from_user_config": audit_from_user_config,
        }
    finally:
        cleanup_path(FIXTURE_ROOT)
        cleanup_path(TEMP_HOME_ROOT)

    print(json.dumps(result, ensure_ascii=True, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
