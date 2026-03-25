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
from git_exec import GIT_EXE


ROOT = Path(__file__).resolve().parent.parent
SOURCE_REPO = ROOT.parent / "wind-agent"
FIXTURE_ROOT = ROOT / "artifacts" / "fixtures" / "wind-agent-bootstrap-host"
PROJECT_ID = "wind-agent-bootstrap"
OPTIONAL_EXCLUDE_NAMES = {
    ".cache",
    "node_modules",
    "outputs",
    "artifacts",
}
OPTIONAL_EXCLUDE_FILES = {
    ".env",
}


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

    audit = run(
        [
            sys.executable,
            "-m",
            "kernel.cli",
            "--repo-root",
            str(FIXTURE_ROOT),
            "audit-control-state",
            "--project-id",
            PROJECT_ID,
        ],
        cwd=ROOT,
    )
    audit_payload = json.loads(audit.stdout)
    if audit_payload.get("status") == "blocked":
        raise SystemExit(
            json.dumps(
                {
                    "message": "wind-agent frozen snapshot bootstrap remains blocked",
                    "audit": audit_payload,
                },
                ensure_ascii=True,
                indent=2,
            )
        )

    enforce = subprocess.run(
        [
            sys.executable,
            "-m",
            "kernel.cli",
            "--repo-root",
            str(FIXTURE_ROOT),
            "enforce-worktree",
            "--project-id",
            PROJECT_ID,
        ],
        cwd=str(ROOT),
        capture_output=True,
        text=True,
        check=False,
    )
    enforce_payload = json.loads(enforce.stdout)
    if enforce_payload.get("status") != "blocked":
        raise SystemExit(
            json.dumps(
                {
                    "message": "wind-agent frozen snapshot enforcement should remain blocked before any round adoption",
                    "enforce": enforce_payload,
                },
                ensure_ascii=True,
                indent=2,
            )
        )
    blocked_codes = [str(issue.get("code") or "").strip() for issue in enforce_payload.get("issues", [])]
    if "dirty_worktree_without_scope_round" not in blocked_codes:
        raise SystemExit(
            json.dumps(
                {
                    "message": "wind-agent frozen snapshot enforcement blocked for an unexpected reason",
                    "enforce": enforce_payload,
                },
                ensure_ascii=True,
                indent=2,
            )
        )

    report_path = FIXTURE_ROOT / "state" / PROJECT_ID / "current" / "adoption-report.md"
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(
        "\n".join(
            [
                "# Frozen Wind-Agent Host Adoption Report",
                "",
                f"- Source repo: `{SOURCE_REPO}`",
                f"- Snapshot fixture: `{FIXTURE_ROOT}`",
                f"- Bootstrap project id: `{PROJECT_ID}`",
                f"- Bootstrap status: `{bootstrap_payload.get('status', '')}`",
                f"- Host control audit: `{audit_payload.get('status', '')}`",
                f"- Host worktree enforcement: `{enforce_payload.get('status', '')}`",
                "",
                "## Current Meaning",
                "",
                "- The copied working-tree snapshot can host the kernel control surface without touching the live wind-agent repo.",
                "- The host-side control audit is already honest enough to pass immediately after bootstrap.",
                "- Worktree enforcement correctly remains blocked because the copied wind-agent worktree is dirty and no active round has been adopted yet.",
                "",
                "## Blocked Reasons",
                "",
                *[
                    f"- `{str(issue.get('code') or '').strip()}`: {str(issue.get('message') or '').strip()}"
                    for issue in enforce_payload.get("issues", [])
                    if str(issue.get("code") or "").strip()
                ],
                "",
                "## Next Steps",
                "",
                "- Adopt one explicit active objective and one explicit active round for the frozen host snapshot.",
                "- Rewrite the round scope so it honestly covers the dirty wind-agent paths that should be governed in shadow mode.",
                "- Re-run host enforcement after round adoption before attempting any live-host shadow integration.",
                "",
            ]
        ),
        encoding="utf-8",
        newline="\n",
    )

    hooks_path = run(
        [GIT_EXE, "config", "--get", "core.hooksPath"],
        cwd=FIXTURE_ROOT,
    ).stdout.strip().replace("\\", "/")

    print(
        json.dumps(
            {
                "status": "ok",
                "source_repo": str(SOURCE_REPO),
                "fixture_root": str(FIXTURE_ROOT),
                "project_id": PROJECT_ID,
                "snapshot": snapshot_meta,
                "bootstrap": bootstrap_payload,
                "audit": audit_payload,
                "enforce": enforce_payload,
                "report_path": str(report_path),
                "hooks_path": hooks_path,
            },
            ensure_ascii=True,
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
