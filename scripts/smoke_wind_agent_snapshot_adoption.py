#!/usr/bin/env python3
from __future__ import annotations

import json
import os
import shutil
import stat
import subprocess
import sys
from pathlib import Path

from evaluation_bundle import copy_repo_snapshot, resolve_snapshot_exclusions


ROOT = Path(__file__).resolve().parent.parent
SOURCE_REPO = ROOT.parent / "wind-agent"
FIXTURE_ROOT = ROOT / "artifacts" / "fixtures" / "wind-agent-adoption-host"
PROJECT_ID = "wind-agent-adoption"
OPTIONAL_EXCLUDE_NAMES = {
    ".cache",
    "node_modules",
    "outputs",
    "artifacts",
}
OPTIONAL_EXCLUDE_FILES = {
    ".env",
}
ROUND_SCOPE_PATHS = [
    "docs",
    "native",
    "src",
    "tests",
    "package.json",
    "package-lock.json",
]
TASK_SCOPE_PATHS = [
    "docs",
    "native",
    "src",
    "tests",
    "package.json",
    "package-lock.json",
]


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


def kernel_json(repo_root: Path, command: str, *args: str, expect_success: bool = True) -> dict[str, object]:
    completed = run(
        [
            sys.executable,
            "-m",
            "kernel.cli",
            "--repo-root",
            str(repo_root),
            command,
            *args,
        ],
        cwd=ROOT,
        expect_success=expect_success,
    )
    payload = completed.stdout if completed.stdout.strip() else completed.stderr
    return json.loads(payload)


def main() -> int:
    if not SOURCE_REPO.exists():
        raise SystemExit(f"wind-agent source repo not found: {SOURCE_REPO}")
    if FIXTURE_ROOT.exists():
        shutil.rmtree(FIXTURE_ROOT, onerror=on_rm_error)

    excluded_names, excluded_files = resolve_snapshot_exclusions(
        SOURCE_REPO,
        optional_excluded_names=OPTIONAL_EXCLUDE_NAMES,
        optional_excluded_files=OPTIONAL_EXCLUDE_FILES,
    )
    snapshot_meta = copy_repo_snapshot(
        SOURCE_REPO,
        FIXTURE_ROOT,
        excluded_names=excluded_names,
        excluded_file_names=excluded_files,
    )

    bootstrap_payload = kernel_json(
        FIXTURE_ROOT,
        "bootstrap-repo",
        "--project-id",
        PROJECT_ID,
    )
    initial_enforce = kernel_json(
        FIXTURE_ROOT,
        "enforce-worktree",
        "--project-id",
        PROJECT_ID,
        expect_success=False,
    )
    initial_codes = [str(issue.get("code") or "").strip() for issue in initial_enforce.get("issues", [])]
    if "dirty_worktree_without_scope_round" not in initial_codes:
        raise SystemExit(
            json.dumps(
                {
                    "message": "initial frozen host enforcement did not fail for the expected no-round reason",
                    "enforce": initial_enforce,
                },
                ensure_ascii=True,
                indent=2,
            )
        )

    objective_payload = kernel_json(
        FIXTURE_ROOT,
        "open-objective",
        "--project-id",
        PROJECT_ID,
        "--title",
        "Adopt frozen wind-agent snapshot into governed shadow mode",
        "--summary",
        "Capture the current frozen wind-agent worktree inside one honest objective and round before live shadow mode.",
        "--problem",
        "The frozen wind-agent snapshot is dirty and cannot pass enforcement until one explicit owner-layer objective and round adopt the real worktree.",
        "--success-criterion",
        "The frozen host has one active objective and one active round that honestly cover the intended dirty worktree slice.",
        "--success-criterion",
        "Host-side enforcement no longer fails for missing round authority.",
        "--non-goal",
        "Do not mutate the live wind-agent repository.",
        "--non-goal",
        "Do not claim validation closure for the frozen host.",
        "--why-now",
        "Frozen-host adoption is the lowest-risk path to prove real project onboarding before any live shadow-mode rollout.",
        "--phase",
        "exploration",
        "--risk",
        "The first adopted round could still over-cover unrelated dirty paths if the shadow boundary is too broad.",
        "--path",
        "docs",
        "--path",
        "native",
        "--path",
        "src",
        "--path",
        "tests",
        "--path",
        "package.json",
        "--path",
        "package-lock.json",
    )

    set_phase_payload = kernel_json(
        FIXTURE_ROOT,
        "set-phase",
        "--project-id",
        PROJECT_ID,
        "--phase",
        "execution",
        "--reason",
        "Frozen host adoption now needs one real bounded round so enforcement can judge scope honestly.",
        "--auto-open-round",
        "--round-title",
        "Adopt broadened wind-agent dirty slice into one bounded round",
        "--round-scope-item",
        "Adopt the current frozen wind-agent dirty worktree into one explicit governed round.",
        "--round-scope-item",
        "Cover the broadened docs/native/src/tests plus package boundary before live shadow mode.",
        "--round-scope-path",
        "docs",
        "--round-scope-path",
        "native",
        "--round-scope-path",
        "src",
        "--round-scope-path",
        "tests",
        "--round-scope-path",
        "package.json",
        "--round-scope-path",
        "package-lock.json",
        "--round-deliverable",
        "A frozen-host adopted round whose scope honestly covers the intended dirty wind-agent slice.",
        "--round-validation-plan",
        "Re-run frozen-host enforcement and audit, then prepare live-host shadow adoption without touching the live repo.",
        "--round-risk",
        "The adopted round may still need narrower task contracts before any code-changing shadow work.",
    )

    round_id = str((set_phase_payload.get("auto_open_round") or {}).get("round_id") or "").strip()
    if not round_id:
        raise SystemExit("set-phase auto-open-round did not return a round_id")

    task_payload = kernel_json(
        FIXTURE_ROOT,
        "open-task-contract",
        "--project-id",
        PROJECT_ID,
        "--round-id",
        round_id,
        "--title",
        "Prepare frozen wind-agent shadow-mode adoption boundary",
        "--summary",
        "Make the frozen host control boundary explicit enough for shadow-mode preparation.",
        "--intent",
        "Use the adopted round to govern the existing dirty worktree and explain what still blocks live shadow mode.",
        "--path",
        "docs",
        "--path",
        "native",
        "--path",
        "src",
        "--path",
        "tests",
        "--path",
        "package.json",
        "--path",
        "package-lock.json",
        "--allowed-change",
        "Open the minimum honest objective/round/task control objects for the frozen host.",
        "--allowed-change",
        "Use enforcement output to explain the remaining adoption boundary without claiming live rollout.",
        "--forbidden-change",
        "Do not mutate the live wind-agent repository.",
        "--forbidden-change",
        "Do not claim captured or closed status for the adopted round.",
        "--completion-criterion",
        "Frozen-host enforcement no longer reports missing round authority.",
        "--completion-criterion",
        "The frozen host has one readable adoption report that explains remaining blockers.",
    )

    refresh_completed = run(
        [
            sys.executable,
            "-m",
            "kernel.cli",
            "--repo-root",
            str(FIXTURE_ROOT),
            "refresh-current-task-anchor",
            "--project-id",
            PROJECT_ID,
            "--workspace-root",
            str(FIXTURE_ROOT).replace("\\", "/"),
        ],
        cwd=ROOT,
    )

    final_audit = kernel_json(
        FIXTURE_ROOT,
        "audit-control-state",
        "--project-id",
        PROJECT_ID,
    )
    if final_audit.get("status") != "ok":
        raise SystemExit(
            json.dumps(
                {
                    "message": "frozen host audit should remain ok after adopted objective/round/task landing",
                    "audit": final_audit,
                },
                ensure_ascii=True,
                indent=2,
            )
        )

    final_enforce = kernel_json(
        FIXTURE_ROOT,
        "enforce-worktree",
        "--project-id",
        PROJECT_ID,
        expect_success=False,
    )
    final_codes = [str(issue.get("code") or "").strip() for issue in final_enforce.get("issues", [])]
    if "dirty_worktree_without_scope_round" in final_codes:
        raise SystemExit(
            json.dumps(
                {
                    "message": "frozen host enforcement should no longer fail for missing round authority after adoption",
                    "enforce": final_enforce,
                },
                ensure_ascii=True,
                indent=2,
            )
        )

    assessment_payload = kernel_json(
        FIXTURE_ROOT,
        "assess-host-adoption",
        "--project-id",
        PROJECT_ID,
        "--workspace-root",
        str(FIXTURE_ROOT).replace("\\", "/"),
        "--source-repo",
        str(SOURCE_REPO).replace("\\", "/"),
        "--write-report",
    )
    blocker_classification = assessment_payload["blocker_classification"]
    report_path = Path(str(assessment_payload["report_path"]))

    print(
        json.dumps(
            {
                "status": "ok",
                "source_repo": str(SOURCE_REPO),
                "fixture_root": str(FIXTURE_ROOT),
                "project_id": PROJECT_ID,
                "snapshot": snapshot_meta,
                "bootstrap": bootstrap_payload,
                "objective": objective_payload,
                "set_phase": set_phase_payload,
                "task_contract": task_payload,
                "refresh_current_task_anchor_stdout": refresh_completed.stdout,
                "initial_enforce": initial_enforce,
                "final_audit": final_audit,
                "final_enforce": final_enforce,
                "assessment": assessment_payload,
                "blocker_classification": blocker_classification,
                "report_path": str(report_path),
            },
            ensure_ascii=True,
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
