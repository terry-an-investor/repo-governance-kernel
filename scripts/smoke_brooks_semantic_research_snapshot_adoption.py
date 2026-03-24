#!/usr/bin/env python3
from __future__ import annotations

import json
import os
import shutil
import stat
import subprocess
import sys
from pathlib import Path

from evaluation_bundle import (
    classify_host_adoption_blockers,
    copy_repo_snapshot,
    resolve_snapshot_exclusions,
)


ROOT = Path(__file__).resolve().parent.parent
SOURCE_REPO = ROOT.parent / "git_repos" / "brooks-semantic-research"
FIXTURE_ROOT = ROOT / "artifacts" / "bsr-host"
PROJECT_ID = "brooks-semantic-research-adoption"
OPTIONAL_EXCLUDE_NAMES = {
    ".cache",
    "artifacts",
    "outputs",
}
OPTIONAL_EXCLUDE_FILES = {
    ".env",
}
ROUND_SCOPE_PATHS = [
    "AGENTS.md",
    "CLAUDE.md",
    "DEVELOPMENT_OPERATING_PRINCIPLES_v0.md",
    "JUDGMENT_LOG_v0.md",
    "MILESTONE_CONTRACT_TEMPLATE_v0.md",
    "MILESTONE_COURSE_PDF_PARSER_EVAL_v0.md",
    "MILESTONE_COURSE_PDF_PREPROCESSING_BOOTSTRAP_v0.md",
    "MILESTONE_COURSE_PDF_REPAIR_PATH_BAKEOFF_v0.md",
    "MILESTONE_COURSE_PDF_ROUTER_IMPLEMENTATION_v0.md",
    "MILESTONE_DECISION_FIRST_SLICE_v0.md",
    "MILESTONE_DECISION_WORKSPACE_BOOTSTRAP_v0.md",
    "MILESTONE_GOLDEN_SET_BOOTSTRAP_v0.md",
    "PROGRESS_LEDGER_v0.md",
    "PROJECT_CONTROL_PLANE_v0.md",
    "QUALITY_RUBRIC_EVOLUTION_v0.md",
    "README.md",
    "REBUILD_BLUEPRINT_v0.md",
    "pyproject.toml",
    "uv.lock",
    "workspaces",
]
TASK_SCOPE_PATHS = list(ROUND_SCOPE_PATHS)


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
        raise SystemExit(f"source repo not found: {SOURCE_REPO}")
    if FIXTURE_ROOT.exists():
        shutil.rmtree(FIXTURE_ROOT, onexc=on_rm_error)

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
    initial_audit = kernel_json(
        FIXTURE_ROOT,
        "audit-control-state",
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
        "Adopt frozen brooks-semantic-research snapshot into governed shadow mode",
        "--summary",
        "Capture the current frozen brooks-semantic-research dirty worktree inside one honest objective and round before any live-host usage.",
        "--problem",
        "The frozen brooks-semantic-research snapshot is already dirty and cannot pass enforcement until one explicit owner-layer objective and round adopt the real worktree slice.",
        "--success-criterion",
        "The frozen host has one active objective and one active round that honestly cover the intended dirty worktree slice.",
        "--success-criterion",
        "Host-side enforcement no longer fails for missing round authority.",
        "--non-goal",
        "Do not mutate the live brooks-semantic-research repository.",
        "--non-goal",
        "Do not claim validation closure for the frozen host.",
        "--why-now",
        "This is the first real dirty external-worktree adoption pressure test beyond clean bootstrap examples.",
        "--phase",
        "exploration",
        "--risk",
        "The adopted round could still under-cover nested dirty paths inside workspaces or over-cover unrelated future paths.",
        *[item for path in ROUND_SCOPE_PATHS for item in ("--path", path)],
    )

    set_phase_payload = kernel_json(
        FIXTURE_ROOT,
        "set-phase",
        "--project-id",
        PROJECT_ID,
        "--phase",
        "execution",
        "--reason",
        "Frozen host adoption now needs one real bounded round so enforcement can judge the existing dirty worktree honestly.",
        "--auto-open-round",
        "--round-title",
        "Adopt dirty brooks-semantic-research working slice into one bounded round",
        "--round-scope-item",
        "Adopt the current frozen brooks-semantic-research dirty worktree into one explicit governed round.",
        "--round-scope-item",
        "Cover the current root governance documents, dependency files, and workspace tree without touching the live repo.",
        *[item for path in ROUND_SCOPE_PATHS for item in ("--round-scope-path", path)],
        "--round-deliverable",
        "A frozen-host adopted round whose scope honestly covers the intended dirty brooks-semantic-research slice.",
        "--round-validation-plan",
        "Re-run frozen-host enforcement and audit, then inspect whether remaining blockers are real scope gaps or host support noise.",
        "--round-risk",
        "The adopted round may still need narrower task contracts or a refined workspace-specific policy.",
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
        "Govern frozen brooks-semantic-research host adoption surface",
        "--summary",
        "Make the frozen host control boundary explicit enough for dirty-worktree adoption analysis.",
        "--intent",
        "Use the adopted round to govern the existing dirty worktree and explain what still blocks future live shadow mode.",
        *[item for path in TASK_SCOPE_PATHS for item in ("--path", path)],
        "--allowed-change",
        "Open the minimum honest objective, round, and task control objects for the frozen host.",
        "--allowed-change",
        "Use enforcement output to explain whether remaining blockers are true repo-scope gaps or host-adoption noise.",
        "--forbidden-change",
        "Do not mutate the live brooks-semantic-research repository.",
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

    remaining_blocked_paths: list[str] = []
    for issue in final_enforce.get("issues", []):
        if str(issue.get("code") or "").strip() not in {
            "dirty_paths_outside_scope_round",
            "dirty_paths_outside_active_task_contracts",
        }:
            continue
        for path in issue.get("evidence", []):
            normalized = str(path).replace("\\", "/").strip()
            while normalized.startswith("./"):
                normalized = normalized[2:]
            if normalized and normalized not in remaining_blocked_paths:
                remaining_blocked_paths.append(normalized)
    blocker_classification = classify_host_adoption_blockers(PROJECT_ID, remaining_blocked_paths)

    report_lines = [
        "# Frozen Brooks Semantic Research Adopted Shadow-Mode Report",
        "",
        f"- Source repo: `{SOURCE_REPO}`",
        f"- Snapshot fixture: `{FIXTURE_ROOT}`",
        f"- Project id: `{PROJECT_ID}`",
        f"- Objective id: `{objective_payload.get('objective_id', '')}`",
        f"- Round id: `{round_id}`",
        f"- Task contract id: `{task_payload.get('task_contract_id', '')}`",
        f"- Initial audit: `{initial_audit.get('status', '')}`",
        f"- Initial enforcement: `{initial_enforce.get('status', '')}`",
        f"- Final audit: `{final_audit.get('status', '')}`",
        f"- Final enforcement: `{final_enforce.get('status', '')}`",
        "",
        "## Current Meaning",
        "",
        "- The frozen brooks-semantic-research snapshot now has one explicit adopted objective, round, and task contract.",
        "- Enforcement no longer fails for missing round authority; any remaining blocked state is now about real scope law or host adoption policy instead of missing adoption objects.",
        "- This is the current release-grade pressure test for dirty external-worktree adoption.",
        "",
        "## Enforcement Issues",
        "",
    ]
    final_issues = final_enforce.get("issues", [])
    if final_issues:
        for issue in final_issues:
            report_lines.append(f"- `{issue.get('code', '')}`: {issue.get('message', '')}")
    else:
        report_lines.append("- No remaining enforcement blockers on the frozen host.")
    report_lines.extend(
        [
            "",
            "## Blocker Classification",
            "",
            f"- Hook installation paths: `{blocker_classification['counts']['hook_installation_paths']}`",
            f"- Host governance paths: `{blocker_classification['counts']['host_governance_paths']}`",
            f"- Host support paths: `{blocker_classification['counts']['host_support_paths']}`",
            f"- Repo scope paths: `{blocker_classification['counts']['repo_scope_paths']}`",
            "",
            "These buckets separate bootstrap/control-plane noise from real source-repo scope gaps.",
            "",
        ]
    )
    for bucket in (
        "hook_installation_paths",
        "host_governance_paths",
        "host_support_paths",
        "repo_scope_paths",
    ):
        report_lines.append(f"### `{bucket}`")
        report_lines.append("")
        report_lines.append(f"- Meaning: {blocker_classification['meanings'][bucket]}")
        bucket_paths = blocker_classification["buckets"][bucket]
        if bucket_paths:
            for path in bucket_paths:
                report_lines.append(f"- `{path}`")
        else:
            report_lines.append("- none")
        report_lines.append("")
    report_lines.extend(
        [
            "## Next Steps",
            "",
            "- Compare the adopted round boundary with the real root-level and workspace-level dirty paths, then decide whether remaining repo-scope gaps need a wider round or separate task contracts.",
            "- Separate host bootstrap/support path treatment from real research-workspace changes before any live shadow rollout.",
            "- Keep this pressure test frozen; do not mutate the live source repository.",
            "",
        ]
    )
    report_path = FIXTURE_ROOT / "projects" / PROJECT_ID / "current" / "shadow-adoption-report.md"
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text("\n".join(report_lines), encoding="utf-8", newline="\n")

    print(
        json.dumps(
            {
                "status": "ok",
                "source_repo": str(SOURCE_REPO),
                "fixture_root": str(FIXTURE_ROOT),
                "project_id": PROJECT_ID,
                "snapshot": snapshot_meta,
                "bootstrap": bootstrap_payload,
                "initial_audit": initial_audit,
                "objective": objective_payload,
                "set_phase": set_phase_payload,
                "task_contract": task_payload,
                "refresh_current_task_anchor_stdout": refresh_completed.stdout,
                "final_audit": final_audit,
                "final_enforce": final_enforce,
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
