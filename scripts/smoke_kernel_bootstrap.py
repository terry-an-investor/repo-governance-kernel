#!/usr/bin/env python3
from __future__ import annotations

import json
import os
import shutil
import stat
import subprocess
import sys
import tomllib
from pathlib import Path

from git_exec import GIT_EXE


ROOT = Path(__file__).resolve().parent.parent
SOURCE_FIXTURE_ROOT = ROOT / "artifacts" / "fixtures" / "bootstrap-host"
INSTALLED_FIXTURE_ROOT = ROOT / "artifacts" / "fixtures" / "bootstrap-host-installed"
INSTALLED_EXTERNAL_TARGET_ROOT = ROOT / "artifacts" / "fixtures" / "bootstrap-external-target-installed"
INSTALL_ROOT = ROOT / "artifacts" / "fixtures" / "bootstrap-package-install"
INSTALLED_DRAFT_PATH = ROOT / "artifacts" / "fixtures" / "bootstrap-external-target-installed-draft.md"
INSTALLED_REPORT_PATH = ROOT / "artifacts" / "fixtures" / "bootstrap-external-target-installed-report.md"
SOURCE_PROJECT_ID = "bootstrap-host"
INSTALLED_PROJECT_ID = "bootstrap-host-installed"
SOURCE_CLI = [sys.executable, "-m", "kernel.cli"]


def run(
    cmd: list[str],
    *,
    cwd: Path,
    env: dict[str, str] | None = None,
) -> subprocess.CompletedProcess[str]:
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


def project_version() -> str:
    pyproject = tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))
    return str(pyproject["project"]["version"]).strip()


def ensure_clean_dir(path: Path) -> None:
    cleanup_path(path)
    path.mkdir(parents=True, exist_ok=True)


def init_git_repo(path: Path) -> None:
    run([GIT_EXE, "init"], cwd=path)
    run([GIT_EXE, "config", "user.email", "fixture@example.com"], cwd=path)
    run([GIT_EXE, "config", "user.name", "Fixture Smoke"], cwd=path)


def commit_all_changes(path: Path, message: str) -> None:
    run([GIT_EXE, "add", "."], cwd=path)
    # The first fixture baseline commit establishes HEAD after bootstrap.
    run([GIT_EXE, "commit", "--no-verify", "-m", message], cwd=path)


def cli_json(
    cli_cmd: list[str],
    *,
    repo_root: Path,
    command: str,
    args: list[str],
    cwd: Path,
    env: dict[str, str] | None = None,
) -> dict[str, object]:
    completed = run(
        [
            *cli_cmd,
            "--repo-root",
            str(repo_root),
            command,
            *args,
        ],
        cwd=cwd,
        env=env,
    )
    payload = completed.stdout.strip() or completed.stderr.strip()
    try:
        parsed = json.loads(payload)
    except json.JSONDecodeError as exc:
        raise SystemExit(f"{command} returned invalid json: {exc}") from exc
    if not isinstance(parsed, dict):
        raise SystemExit(f"{command} returned non-object json")
    return parsed


def assert_bootstrap_host(
    fixture_root: Path,
    project_id: str,
    *,
    bootstrap_payload: dict[str, object],
) -> dict[str, object]:
    expected_paths = [
        fixture_root / ".githooks" / "pre-commit",
        fixture_root / ".githooks" / "pre-push",
        fixture_root / "state" / project_id / "control" / "constitution.md",
        fixture_root / "state" / project_id / "current" / "current-task.md",
        fixture_root / "state" / project_id / "control" / "pivot-log.md",
        fixture_root / "state" / project_id / "control" / "exception-ledger.md",
    ]
    missing = [str(path) for path in expected_paths if not path.exists()]
    if missing:
        raise SystemExit(f"bootstrap did not create expected paths: {', '.join(missing)}")

    hooks_path = run(
        [GIT_EXE, "config", "--get", "core.hooksPath"],
        cwd=fixture_root,
    ).stdout.strip().replace("\\", "/")
    expected_hooks_path = str(fixture_root / ".githooks").replace("\\", "/")
    if hooks_path != expected_hooks_path:
        raise SystemExit(f"unexpected hooksPath `{hooks_path}`; expected `{expected_hooks_path}`")

    constitution_text = (fixture_root / "state" / project_id / "control" / "constitution.md").read_text(
        encoding="utf-8"
    )
    if "Audit Hooks" not in constitution_text:
        raise SystemExit("bootstrap constitution is missing audit hooks")

    return {
        "bootstrap": bootstrap_payload,
        "hooks_path": hooks_path,
    }


def write_project_config(repo_root: Path, project_id: str) -> Path:
    config_path = repo_root / ".repo-governance-kernel" / "project.json"
    config_path.parent.mkdir(parents=True, exist_ok=True)
    config_path.write_text(
        json.dumps({"project_id": project_id}, ensure_ascii=True, indent=2) + "\n",
        encoding="utf-8",
    )
    return config_path


def assert_config_runtime_resolution(
    *,
    repo_root: Path,
    project_id: str,
    cli_cmd: list[str],
    env: dict[str, str] | None = None,
) -> dict[str, object]:
    config_path = write_project_config(repo_root, project_id)
    describe_payload = cli_json(
        cli_cmd,
        repo_root=repo_root,
        command="describe-config",
        args=[],
        cwd=ROOT,
        env=env,
    )
    if str(describe_payload["sources"]["project_id"]) != "project_config":
        raise SystemExit("describe-config did not resolve project_id from project config")
    if str(describe_payload["resolved"]["project_id"]) != project_id:
        raise SystemExit("describe-config resolved the wrong project_id from project config")

    audit_payload = cli_json(
        cli_cmd,
        repo_root=repo_root,
        command="audit-control-state",
        args=[],
        cwd=ROOT,
        env=env,
    )
    if str(audit_payload.get("status") or "") == "blocked":
        raise SystemExit("audit-control-state stayed blocked when project_id should resolve from config")
    if str(audit_payload.get("project_id") or "") != project_id:
        raise SystemExit("audit-control-state resolved the wrong config-derived project_id")

    return {
        "config_path": str(config_path),
        "describe_config": describe_payload,
        "audit_from_project_config": audit_payload,
    }


def bootstrap_and_audit(
    *,
    fixture_root: Path,
    project_id: str,
    cli_cmd: list[str],
    env: dict[str, str] | None = None,
    commit_after_bootstrap: bool = False,
) -> dict[str, object]:
    ensure_clean_dir(fixture_root)
    init_git_repo(fixture_root)

    bootstrap = cli_json(
        cli_cmd,
        repo_root=fixture_root,
        command="bootstrap-repo",
        args=["--project-id", project_id],
        cwd=ROOT,
        env=env,
    )
    bootstrap_checks = assert_bootstrap_host(fixture_root, project_id, bootstrap_payload=bootstrap)

    audit_payload = cli_json(
        cli_cmd,
        repo_root=fixture_root,
        command="audit-control-state",
        args=["--project-id", project_id],
        cwd=ROOT,
        env=env,
    )
    if audit_payload.get("status") == "blocked":
        raise SystemExit(
            json.dumps(
                {
                    "message": "bootstrap host audit is still blocked after bootstrap",
                    "audit": audit_payload,
                },
                ensure_ascii=True,
                indent=2,
            )
        )

    if commit_after_bootstrap:
        commit_all_changes(fixture_root, "Commit bootstrapped governance baseline")

    return {
        "project_id": project_id,
        "fixture_root": str(fixture_root),
        "bootstrap": bootstrap_checks["bootstrap"],
        "audit": audit_payload,
        "hooks_path": bootstrap_checks["hooks_path"],
        "committed_bootstrap_baseline": commit_after_bootstrap,
    }


def write_external_target_fixture(path: Path) -> list[str]:
    ensure_clean_dir(path)
    init_git_repo(path)
    (path / "README.md").write_text("external fixture\n", encoding="utf-8", newline="\n")
    baseline_doc = path / "docs" / "baseline.md"
    baseline_doc.parent.mkdir(parents=True, exist_ok=True)
    baseline_doc.write_text("baseline\n", encoding="utf-8", newline="\n")
    run([GIT_EXE, "add", "README.md", "docs/baseline.md"], cwd=path)
    run([GIT_EXE, "commit", "-m", "Initial external fixture baseline"], cwd=path)

    dirty_paths = [
        "docs/baseline.md",
        "docs/close_reading/README.md",
        "docs/close_reading/theme_close_read.md",
    ]
    (path / "docs" / "baseline.md").write_text("baseline changed\n", encoding="utf-8", newline="\n")
    (path / "docs" / "close_reading" / "README.md").parent.mkdir(parents=True, exist_ok=True)
    (path / "docs" / "close_reading" / "README.md").write_text("close reading\n", encoding="utf-8", newline="\n")
    (path / "docs" / "close_reading" / "theme_close_read.md").write_text("theme close read\n", encoding="utf-8", newline="\n")
    return dirty_paths


def onboard_governed_host(
    *,
    cli_cmd: list[str],
    repo_root: Path,
    project_id: str,
    env: dict[str, str] | None = None,
) -> dict[str, object]:
    onboarding = cli_json(
        cli_cmd,
        repo_root=repo_root,
        command="onboard-repo",
        args=[
            "--project-id",
            project_id,
        ],
        cwd=ROOT,
        env=env,
    )
    if str(onboarding.get("status") or "") != "ok":
        raise SystemExit("onboard-repo did not report ok")
    if str((onboarding.get("result_contract") or {}).get("entrypoint") or "") != "onboard-repo":
        raise SystemExit("installed onboard-repo did not report the direct entrypoint contract")
    return onboarding


def assert_public_surface(payload: dict[str, object]) -> dict[str, object]:
    expected_commands = {
        "describe-config",
        "describe-public-surface",
        "audit-control-state",
        "enforce-worktree",
        "bootstrap-repo",
        "onboard-repo",
        "onboard-repo-from-intent",
        "assess-external-target-once",
        "assess-external-target-from-intent",
    }
    public_commands = payload.get("public_commands")
    if not isinstance(public_commands, list):
        raise SystemExit("describe-public-surface is missing public_commands")
    if str(payload.get("released_version") or "") != "0.1.0b1":
        raise SystemExit("describe-public-surface should report released_version as 0.1.0b1")
    if str(payload.get("source_line_target_version") or "") != "0.1.0b1":
        raise SystemExit("describe-public-surface should report source_line_target_version as 0.1.0b1")
    observed_commands = {
        str(item.get("name") or "").strip()
        for item in public_commands
        if isinstance(item, dict)
    }
    if observed_commands != expected_commands:
        raise SystemExit(
            json.dumps(
                {
                    "message": "unexpected public beta command set",
                    "expected": sorted(expected_commands),
                    "observed": sorted(observed_commands),
                },
                ensure_ascii=True,
                indent=2,
            )
        )

    repo_wrappers = payload.get("repo_owned_agent_wrappers")
    if not isinstance(repo_wrappers, list) or not any(
        isinstance(item, dict) and str(item.get("name") or "").strip() == "use-repo-governance-kernel"
        for item in repo_wrappers
    ):
        raise SystemExit("describe-public-surface is missing the repo-owned agent wrapper")

    stable_public_flow_results = payload.get("stable_public_flow_results")
    if not isinstance(stable_public_flow_results, dict):
        raise SystemExit("describe-public-surface is missing stable_public_flow_results")
    if str(stable_public_flow_results.get("status") or "") != "b1":
        raise SystemExit("describe-public-surface should mark stable_public_flow_results as b1")
    entrypoints = stable_public_flow_results.get("entrypoints")
    if not isinstance(entrypoints, dict):
        raise SystemExit("stable_public_flow_results is missing entrypoints")
    if set(str(key) for key in entrypoints.keys()) != expected_commands - {
        "describe-config",
        "describe-public-surface",
        "audit-control-state",
        "enforce-worktree",
        "bootstrap-repo",
    }:
        raise SystemExit("stable_public_flow_results did not describe the four public flow entrypoints")
    blocked_required_fields = stable_public_flow_results.get("blocked_detail_required_fields")
    if not isinstance(blocked_required_fields, list) or "code" not in blocked_required_fields:
        raise SystemExit("stable_public_flow_results is missing blocked detail field requirements")
    onboarding_subcontracts = (entrypoints.get("onboard-repo-from-intent") or {}).get("stable_subcontracts")
    assessment_subcontracts = (entrypoints.get("assess-external-target-from-intent") or {}).get("stable_subcontracts")
    onboarding_candidate_subcontracts = (entrypoints.get("onboard-repo-from-intent") or {}).get("candidate_subcontracts")
    assessment_candidate_subcontracts = (entrypoints.get("assess-external-target-from-intent") or {}).get(
        "candidate_subcontracts"
    )
    if not isinstance(onboarding_subcontracts, dict) or "intent_compilation" not in onboarding_subcontracts:
        raise SystemExit("stable_public_flow_results is missing onboarding intent subcontract detail")
    if not isinstance(assessment_subcontracts, dict) or "flow_contract" not in assessment_subcontracts:
        raise SystemExit("stable_public_flow_results is missing external assessment flow subcontract detail")
    if str(stable_public_flow_results.get("candidate_status") or "") != "candidate":
        raise SystemExit("stable_public_flow_results is missing the generic candidate status marker")
    if not isinstance(onboarding_candidate_subcontracts, dict) or "execution.compiled_bundle" not in onboarding_candidate_subcontracts:
        raise SystemExit("stable_public_flow_results is missing onboarding candidate evidence subcontract detail")
    if not isinstance(assessment_candidate_subcontracts, dict) or "outcome" not in assessment_candidate_subcontracts:
        raise SystemExit("stable_public_flow_results is missing assessment candidate evidence subcontract detail")
    onboarding_intent_fields = (onboarding_subcontracts.get("intent_compilation") or {}).get("required_fields")
    assessment_flow_fields = (assessment_subcontracts.get("flow_contract") or {}).get("required_fields")
    onboarding_stable_execution_fields = ((onboarding_subcontracts.get("execution") or {}).get("required_fields"))
    assessment_stable_postcondition_fields = (
        (assessment_subcontracts.get("postconditions") or {}).get("required_fields")
    )
    onboarding_candidate_compiled_fields = (
        (onboarding_candidate_subcontracts.get("execution.compiled_bundle") or {}).get("required_fields")
    )
    assessment_candidate_outcome_fields = (
        (assessment_candidate_subcontracts.get("outcome") or {}).get("required_fields")
    )
    if not isinstance(onboarding_intent_fields, list) or "bundle_name" not in onboarding_intent_fields:
        raise SystemExit("stable onboarding intent subcontract is missing bundle_name")
    if not isinstance(assessment_flow_fields, list) or "scope_strategy" not in assessment_flow_fields:
        raise SystemExit("stable external assessment flow subcontract is missing scope_strategy")
    if not isinstance(onboarding_stable_execution_fields, list) or "bundle_detail" not in onboarding_stable_execution_fields:
        raise SystemExit("stable onboarding execution is missing bundle_detail")
    if not isinstance(assessment_stable_postcondition_fields, list) or "audit_status" not in assessment_stable_postcondition_fields:
        raise SystemExit("stable assessment postconditions is missing audit_status")
    if not isinstance(onboarding_candidate_compiled_fields, list) or "onboarding_scope_paths" not in onboarding_candidate_compiled_fields:
        raise SystemExit("onboarding candidate execution.compiled_bundle is missing onboarding_scope_paths")
    if not isinstance(assessment_candidate_outcome_fields, list) or "adopted_task_paths" not in assessment_candidate_outcome_fields:
        raise SystemExit("assessment candidate outcome is missing adopted_task_paths")

    return {
        "target_version": payload.get("target_version"),
        "released_version": payload.get("released_version"),
        "source_line_target_version": payload.get("source_line_target_version"),
        "status": payload.get("status"),
        "public_command_count": len(public_commands),
        "repo_owned_agent_wrapper_count": len(repo_wrappers),
        "stable_public_flow_entrypoint_count": len(entrypoints),
        "stable_public_subcontract_entrypoint_count": sum(
            1
            for entry in entrypoints.values()
            if isinstance(entry, dict) and isinstance(entry.get("stable_subcontracts"), dict) and entry["stable_subcontracts"]
        ),
        "candidate_public_subcontract_entrypoint_count": sum(
            1
            for entry in entrypoints.values()
            if isinstance(entry, dict)
            and isinstance(entry.get("candidate_subcontracts"), dict)
            and entry["candidate_subcontracts"]
        ),
    }


def prepare_installed_cli() -> tuple[list[str], dict[str, str], str]:
    ensure_clean_dir(INSTALL_ROOT)
    venv_root = INSTALL_ROOT / ".venv"
    run(["uv", "venv", str(venv_root)], cwd=ROOT)

    run(["uv", "build"], cwd=ROOT)
    version = project_version()
    wheel_path = ROOT / "dist" / f"repo_governance_kernel-{version}-py3-none-any.whl"
    if not wheel_path.exists():
        raise SystemExit(f"expected built wheel not found: {wheel_path}")

    installed_python = venv_root / "Scripts" / "python.exe"
    if not installed_python.exists():
        raise SystemExit(f"expected installed python not found: {installed_python}")
    run(
        [
            "uv",
            "pip",
            "install",
            "--python",
            str(installed_python),
            "--force-reinstall",
            str(wheel_path),
        ],
        cwd=ROOT,
    )

    installed_cli: Path | None = None
    for candidate in [
        venv_root / "Scripts" / "repo-governance-kernel.exe",
        venv_root / "Scripts" / "repo-governance-kernel",
        venv_root / "Scripts" / "repo-governance-kernel.cmd",
    ]:
        if candidate.exists():
            installed_cli = candidate
            break
    if installed_cli is None:
        raise SystemExit(f"installed console entrypoint not found under {venv_root / 'Scripts'}")

    installed_env = os.environ.copy()
    installed_env["PATH"] = str(venv_root / "Scripts") + os.pathsep + installed_env.get("PATH", "")
    help_output = run([str(installed_cli), "--help"], cwd=ROOT, env=installed_env).stdout
    return [str(installed_cli)], installed_env, help_output


def git_status_short(path: Path) -> str:
    return run([GIT_EXE, "status", "--short"], cwd=path).stdout.strip()


def git_head(path: Path) -> str:
    return run([GIT_EXE, "rev-parse", "HEAD"], cwd=path).stdout.strip()


def run_installed_external_assessment(
    *,
    cli_cmd: list[str],
    env: dict[str, str],
    governed_root: Path,
    project_id: str,
    external_target_root: Path,
    expected_dirty_paths: list[str],
) -> dict[str, object]:
    cleanup_path(INSTALLED_DRAFT_PATH)
    cleanup_path(INSTALLED_REPORT_PATH)

    target_head_before = git_head(external_target_root)
    target_status_before = git_status_short(external_target_root)
    if not target_status_before:
        raise SystemExit("installed external target fixture should be dirty before assessment")

    workflow = cli_json(
        cli_cmd,
        repo_root=governed_root,
        command="assess-external-target-once",
        args=[
            "--project-id",
            project_id,
            "--workspace-root",
            str(external_target_root).replace("\\", "/"),
            "--source-repo",
            str(external_target_root).replace("\\", "/"),
            "--draft-output",
            str(INSTALLED_DRAFT_PATH),
            "--report-output",
            str(INSTALLED_REPORT_PATH),
        ],
        cwd=ROOT,
        env=env,
    )

    if not INSTALLED_DRAFT_PATH.exists():
        raise SystemExit(f"installed package draft output missing: {INSTALLED_DRAFT_PATH}")
    if not INSTALLED_REPORT_PATH.exists():
        raise SystemExit(f"installed package report output missing: {INSTALLED_REPORT_PATH}")

    draft_text = INSTALLED_DRAFT_PATH.read_text(encoding="utf-8")
    if "External Target Shadow Scope Draft" not in draft_text:
        raise SystemExit("installed package draft output missing expected title")

    report_text = INSTALLED_REPORT_PATH.read_text(encoding="utf-8")
    if "Host Shadow Adoption Assessment Report" not in report_text:
        raise SystemExit("installed package assessment report missing expected title")

    outcome = workflow.get("outcome")
    if not isinstance(outcome, dict):
        raise SystemExit("installed package workflow missing outcome payload")
    assessment = outcome.get("assessment")
    if not isinstance(assessment, dict):
        raise SystemExit("installed package workflow missing assessment payload")
    final_enforce = assessment.get("final_enforce")
    if not isinstance(final_enforce, dict) or str(final_enforce.get("status")) != "ok":
        raise SystemExit("installed package external-target workflow should finish with enforce-worktree ok")

    assessment_contract = assessment.get("assessment_contract")
    if not isinstance(assessment_contract, dict):
        raise SystemExit("installed package workflow missing assessment contract")
    if assessment_contract.get("mode") != "external-target-shadow":
        raise SystemExit(f"unexpected installed assessment mode: {assessment_contract.get('mode')}")

    actual_dirty_paths = sorted(str(item) for item in outcome["draft"]["dirty_paths"])
    expected_sorted = sorted(expected_dirty_paths)
    if actual_dirty_paths != expected_sorted:
        raise SystemExit(f"unexpected installed draft dirty paths: {actual_dirty_paths}")

    adopted_round_scope_paths = sorted(str(item) for item in outcome["adopted_round_scope_paths"])
    adopted_task_paths = sorted(str(item) for item in outcome["adopted_task_paths"])
    if adopted_round_scope_paths != expected_sorted:
        raise SystemExit(f"installed workflow adopted unexpected round scope paths: {adopted_round_scope_paths}")
    if adopted_task_paths != expected_sorted:
        raise SystemExit(f"installed workflow adopted unexpected task paths: {adopted_task_paths}")

    target_head_after = git_head(external_target_root)
    target_status_after = git_status_short(external_target_root)
    if target_head_after != target_head_before:
        raise SystemExit("installed package assessment should not move the external target HEAD")
    if target_status_after != target_status_before:
        raise SystemExit("installed package assessment should not mutate the external target worktree")

    return {
        "workflow": workflow,
        "draft_path": str(INSTALLED_DRAFT_PATH),
        "report_path": str(INSTALLED_REPORT_PATH),
        "target_head_before": target_head_before,
        "target_head_after": target_head_after,
        "target_status_before": target_status_before,
        "target_status_after": target_status_after,
    }


def main() -> int:
    cleanup_targets = [
        SOURCE_FIXTURE_ROOT,
        INSTALLED_FIXTURE_ROOT,
        INSTALLED_EXTERNAL_TARGET_ROOT,
        INSTALL_ROOT,
        INSTALLED_DRAFT_PATH,
        INSTALLED_REPORT_PATH,
    ]
    result: dict[str, object] | None = None
    try:
        source_host = bootstrap_and_audit(
            fixture_root=SOURCE_FIXTURE_ROOT,
            project_id=SOURCE_PROJECT_ID,
            cli_cmd=SOURCE_CLI,
        )

        installed_cli, installed_env, installed_help = prepare_installed_cli()
        if (
            "bootstrap-repo" not in installed_help
            or "onboard-repo" not in installed_help
            or "onboard-repo-from-intent" not in installed_help
            or "assess-external-target-once" not in installed_help
            or "describe-public-surface" not in installed_help
        ):
            raise SystemExit("installed package help is missing expected commands")

        public_surface = cli_json(
            installed_cli,
            repo_root=ROOT,
            command="describe-public-surface",
            args=[],
            cwd=ROOT,
            env=installed_env,
        )
        public_surface_summary = assert_public_surface(public_surface)

        installed_host = bootstrap_and_audit(
            fixture_root=INSTALLED_FIXTURE_ROOT,
            project_id=INSTALLED_PROJECT_ID,
            cli_cmd=installed_cli,
            env=installed_env,
            commit_after_bootstrap=True,
        )
        installed_config_runtime = assert_config_runtime_resolution(
            repo_root=INSTALLED_FIXTURE_ROOT,
            project_id=INSTALLED_PROJECT_ID,
            cli_cmd=installed_cli,
            env=installed_env,
        )
        commit_all_changes(INSTALLED_FIXTURE_ROOT, "Commit config runtime fixture")

        workflow_setup = onboard_governed_host(
            cli_cmd=installed_cli,
            repo_root=INSTALLED_FIXTURE_ROOT,
            project_id=INSTALLED_PROJECT_ID,
            env=installed_env,
        )
        dirty_paths = write_external_target_fixture(INSTALLED_EXTERNAL_TARGET_ROOT)
        installed_external_assessment = run_installed_external_assessment(
            cli_cmd=installed_cli,
            env=installed_env,
            governed_root=INSTALLED_FIXTURE_ROOT,
            project_id=INSTALLED_PROJECT_ID,
            external_target_root=INSTALLED_EXTERNAL_TARGET_ROOT,
            expected_dirty_paths=dirty_paths,
        )

        result = {
            "status": "ok",
            "version": project_version(),
            "source_bootstrap": source_host,
            "installed_cli": installed_cli[0],
            "installed_help_contains_expected_commands": True,
            "installed_public_surface": public_surface_summary,
            "installed_config_runtime": installed_config_runtime,
            "installed_bootstrap": installed_host,
            "installed_onboarding": workflow_setup,
            "installed_external_target_assessment": installed_external_assessment,
        }
    finally:
        for path in cleanup_targets:
            cleanup_path(path)

    print(json.dumps(result, ensure_ascii=True, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
