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
FIXTURE_ROOT = ROOT / "artifacts" / "fixtures" / "assess-host-adoption"
EXTERNAL_TARGET_ROOT = ROOT / "artifacts" / "fixtures" / "assess-host-adoption-external-target"
PROJECT_ID = "assess-host-adoption"
EXTERNAL_REPORT_PATH = ROOT / "artifacts" / "fixtures" / "assess-host-adoption-external-report.md"
EXTERNAL_DRAFT_PATH = ROOT / "artifacts" / "fixtures" / "assess-host-adoption-external-draft.md"
WORKFLOW_REPORT_PATH = ROOT / "artifacts" / "fixtures" / "assess-host-adoption-workflow-report.md"


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


def init_git_repo(path: Path) -> None:
    run(["C:\\Program Files\\Git\\cmd\\git.exe", "init"], cwd=path)
    run(["C:\\Program Files\\Git\\cmd\\git.exe", "config", "user.email", "fixture@example.com"], cwd=path)
    run(["C:\\Program Files\\Git\\cmd\\git.exe", "config", "user.name", "Fixture Smoke"], cwd=path)


def write_external_target_fixture(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)
    init_git_repo(path)
    (path / "README.md").write_text("external fixture\n", encoding="utf-8", newline="\n")
    baseline_doc = path / "docs" / "baseline.md"
    baseline_doc.parent.mkdir(parents=True, exist_ok=True)
    baseline_doc.write_text("baseline\n", encoding="utf-8", newline="\n")
    run(["C:\\Program Files\\Git\\cmd\\git.exe", "add", "README.md", "docs/baseline.md"], cwd=path)
    run(["C:\\Program Files\\Git\\cmd\\git.exe", "commit", "-m", "Initial external fixture baseline"], cwd=path)

    (path / "docs" / "baseline.md").write_text("baseline changed\n", encoding="utf-8", newline="\n")
    (path / "docs" / "close_reading" / "README.md").parent.mkdir(parents=True, exist_ok=True)
    (path / "docs" / "close_reading" / "README.md").write_text("close reading\n", encoding="utf-8", newline="\n")
    (path / "docs" / "close_reading" / "theme_close_read.md").write_text("theme close read\n", encoding="utf-8", newline="\n")


def main() -> int:
    if FIXTURE_ROOT.exists():
        shutil.rmtree(FIXTURE_ROOT, onexc=on_rm_error)
    if EXTERNAL_TARGET_ROOT.exists():
        shutil.rmtree(EXTERNAL_TARGET_ROOT, onexc=on_rm_error)
    if EXTERNAL_REPORT_PATH.exists():
        EXTERNAL_REPORT_PATH.unlink()
    if EXTERNAL_DRAFT_PATH.exists():
        EXTERNAL_DRAFT_PATH.unlink()
    if WORKFLOW_REPORT_PATH.exists():
        WORKFLOW_REPORT_PATH.unlink()
    FIXTURE_ROOT.mkdir(parents=True, exist_ok=True)
    init_git_repo(FIXTURE_ROOT)
    (FIXTURE_ROOT / "README.md").write_text("fixture\n", encoding="utf-8", newline="\n")
    run(["C:\\Program Files\\Git\\cmd\\git.exe", "add", "README.md"], cwd=FIXTURE_ROOT)
    run(["C:\\Program Files\\Git\\cmd\\git.exe", "commit", "-m", "Initial fixture baseline"], cwd=FIXTURE_ROOT)
    write_external_target_fixture(EXTERNAL_TARGET_ROOT)

    bootstrap = kernel_json(FIXTURE_ROOT, "bootstrap-repo", "--project-id", PROJECT_ID)
    objective = kernel_json(
        FIXTURE_ROOT,
        "open-objective",
        "--project-id",
        PROJECT_ID,
        "--title",
        "Assess governed host adoption surface",
        "--summary",
        "Prepare one bounded host assessment surface for shadow-mode reporting.",
        "--problem",
        "The host needs one explicit objective before a shadow adoption assessment can be honest.",
        "--success-criterion",
        "The host has one active objective and one active round for assessment.",
        "--non-goal",
        "Do not claim live-host mutation authority.",
        "--why-now",
        "A command-level smoke should prove the assessment surface directly.",
        "--phase",
        "exploration",
        "--path",
        "README.md",
    )
    set_phase = kernel_json(
        FIXTURE_ROOT,
        "set-phase",
        "--project-id",
        PROJECT_ID,
        "--phase",
        "execution",
        "--reason",
        "Assessment now needs one real bounded round.",
        "--auto-open-round",
        "--round-title",
        "Assess host shadow adoption boundary",
        "--round-scope-item",
        "Assess the current fixture worktree in shadow mode.",
        "--round-scope-path",
        "README.md",
        "--round-deliverable",
        "A readable host adoption assessment report.",
        "--round-validation-plan",
        "Run assess-host-adoption and inspect the report.",
    )
    round_id = str((set_phase.get("auto_open_round") or {}).get("round_id") or "").strip()
    if not round_id:
        raise SystemExit("set-phase auto-open-round did not return a round_id")

    task_contract = kernel_json(
        FIXTURE_ROOT,
        "open-task-contract",
        "--project-id",
        PROJECT_ID,
        "--round-id",
        round_id,
        "--title",
        "Assess host adoption report generation",
        "--intent",
        "Produce one readable shadow assessment report for the governed host fixture.",
        "--path",
        "README.md",
        "--allowed-change",
        "Run the owner-layer assessment command and inspect its report output.",
        "--forbidden-change",
        "Do not claim broader automation authority.",
        "--completion-criterion",
        "Assessment report exists and is readable.",
    )
    refresh_anchor = run(
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

    assessment = kernel_json(
        FIXTURE_ROOT,
        "assess-host-adoption",
        "--project-id",
        PROJECT_ID,
        "--workspace-root",
        str(FIXTURE_ROOT).replace("\\", "/"),
    )
    report_path = Path(str(assessment["report_path"]))
    if not report_path.exists():
        raise SystemExit(f"assessment report was not written: {report_path}")
    report_text = report_path.read_text(encoding="utf-8")
    if "Host Shadow Adoption Assessment Report" not in report_text:
        raise SystemExit("assessment report missing expected title")
    contract = assessment["assessment_contract"]
    if contract["mode"] != "governed-host-shadow":
        raise SystemExit(f"unexpected assessment mode: {contract['mode']}")
    if contract["scope_path_basis"] != "workspace-root-relative":
        raise SystemExit(f"unexpected scope path basis: {contract['scope_path_basis']}")
    if not contract["writes_into_governance_repo"]:
        raise SystemExit("assessment should write into the governance repo by default")
    if not contract["writes_into_governed_project_current"]:
        raise SystemExit("default report path should target governed project current/")
    if assessment["round_scope_paths"] != ["README.md"]:
        raise SystemExit(f"unexpected round scope paths: {assessment['round_scope_paths']}")
    if assessment["task_contract_paths"] != ["README.md"]:
        raise SystemExit(f"unexpected task contract paths: {assessment['task_contract_paths']}")

    external_draft = kernel_json(
        FIXTURE_ROOT,
        "draft-external-target-shadow-scope",
        "--project-id",
        PROJECT_ID,
        "--workspace-root",
        str(EXTERNAL_TARGET_ROOT).replace("\\", "/"),
        "--source-repo",
        str(EXTERNAL_TARGET_ROOT).replace("\\", "/"),
        "--output",
        str(EXTERNAL_DRAFT_PATH),
    )
    external_draft_contract = external_draft["draft_contract"]
    if external_draft_contract["mode"] != "external-target-shadow":
        raise SystemExit(f"unexpected external draft mode: {external_draft_contract['mode']}")
    if external_draft_contract["scope_path_basis"] != "workspace-root-relative":
        raise SystemExit(f"unexpected external draft scope path basis: {external_draft_contract['scope_path_basis']}")
    if not external_draft["dirty_paths"]:
        raise SystemExit("external target draft should observe at least one dirty path")
    if external_draft["suggested_round_scope_paths"] != external_draft["dirty_paths"]:
        raise SystemExit("external draft should suggest round scope paths from the observed dirty paths")
    if external_draft["suggested_task_paths"] != external_draft["dirty_paths"]:
        raise SystemExit("external draft should suggest task paths from the observed dirty paths")
    if not EXTERNAL_DRAFT_PATH.exists():
        raise SystemExit(f"external scope draft was not written: {EXTERNAL_DRAFT_PATH}")
    draft_text = EXTERNAL_DRAFT_PATH.read_text(encoding="utf-8")
    if "External Target Shadow Scope Draft" not in draft_text:
        raise SystemExit("external scope draft missing expected title")
    if "assess-host-adoption" not in draft_text:
        raise SystemExit("external scope draft should include the next assessment command")

    external_assessment = kernel_json(
        FIXTURE_ROOT,
        "assess-host-adoption",
        "--project-id",
        PROJECT_ID,
        "--workspace-root",
        str(EXTERNAL_TARGET_ROOT).replace("\\", "/"),
        "--source-repo",
        str(EXTERNAL_TARGET_ROOT).replace("\\", "/"),
        "--mode",
        "external-target-shadow",
        "--output",
        str(EXTERNAL_REPORT_PATH),
    )
    external_contract = external_assessment["assessment_contract"]
    if external_contract["mode"] != "external-target-shadow":
        raise SystemExit(f"unexpected external assessment mode: {external_contract['mode']}")
    if external_contract["scope_path_basis"] != "workspace-root-relative":
        raise SystemExit(f"unexpected external scope path basis: {external_contract['scope_path_basis']}")
    if external_contract["writes_into_governance_repo"]:
        raise SystemExit("external assessment output should not be marked as governance-repo artifact")
    if external_contract["writes_into_governed_project_current"]:
        raise SystemExit("external assessment output should not be marked as governed project current artifact")
    if not EXTERNAL_REPORT_PATH.exists():
        raise SystemExit(f"external assessment report was not written: {EXTERNAL_REPORT_PATH}")
    if str(external_assessment["final_enforce"]["status"]) != "blocked":
        raise SystemExit("external assessment should still be blocked before the workflow rewrites scope")

    external_workflow = kernel_json(
        FIXTURE_ROOT,
        "assess-external-target-once",
        "--project-id",
        PROJECT_ID,
        "--workspace-root",
        str(EXTERNAL_TARGET_ROOT).replace("\\", "/"),
        "--source-repo",
        str(EXTERNAL_TARGET_ROOT).replace("\\", "/"),
        "--draft-output",
        str(EXTERNAL_DRAFT_PATH),
        "--report-output",
        str(WORKFLOW_REPORT_PATH),
    )
    workflow_assessment = external_workflow["assessment"]
    if str(workflow_assessment["final_enforce"]["status"]) != "ok":
        raise SystemExit("external workflow should finish with an unblocked assessment after rewriting scope")
    if workflow_assessment["round_scope_paths"] != external_workflow["adopted_round_scope_paths"]:
        raise SystemExit("workflow assessment round scope should match the adopted rewrite scope")
    if workflow_assessment["task_contract_paths"] != external_workflow["adopted_task_paths"]:
        raise SystemExit("workflow assessment task scope should match the adopted rewrite scope")
    if not WORKFLOW_REPORT_PATH.exists():
        raise SystemExit(f"workflow report was not written: {WORKFLOW_REPORT_PATH}")

    print(
        json.dumps(
            {
                "status": "ok",
                "fixture_root": str(FIXTURE_ROOT),
                "project_id": PROJECT_ID,
                "bootstrap": bootstrap,
                "objective": objective,
                "set_phase": set_phase,
                "task_contract": task_contract,
                "refresh_anchor_stdout": refresh_anchor.stdout,
                "assessment": assessment,
                "external_draft": external_draft,
                "external_assessment": external_assessment,
                "external_workflow": external_workflow,
            },
            ensure_ascii=True,
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
