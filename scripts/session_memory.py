#!/usr/bin/env python3
from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
SCRIPTS = ROOT / "scripts"
KERNEL_CLI = "kernel.cli"

KERNEL_COMMANDS = {
    "activate-exception-contract",
    "adjudicate-control-state",
    "audit-control-state",
    "audit-task-contracts",
    "build-index",
    "capture-handoff",
    "check-index",
    "close-objective",
    "compile-adjudication-executor-plan",
    "compile-role-context",
    "create-snapshot",
    "describe-config",
    "open-objective",
    "open-round",
    "open-task-contract",
    "query",
    "record-hard-pivot",
    "record-soft-pivot",
    "reconcile-control-state",
    "refresh-current-task-anchor",
    "refresh-round-scope",
    "render-live-workspace",
    "retire-exception-contract",
    "rewrite-open-round",
    "rewrite-open-task-contract",
    "set-phase",
    "update-round-status",
    "update-task-contract-status",
    "invalidate-exception-contract",
    "list-transition-registry",
    "execute-adjudication-followups",
}

REPO_COMMAND_MAP = {
    "smoke": SCRIPTS / "smoke_repo_acceptance.py",
    "smoke-kernel-bootstrap": SCRIPTS / "smoke_kernel_bootstrap.py",
    "verify-release-publication": SCRIPTS / "verify_release_publication.py",
    "smoke-brooks-semantic-research-snapshot-adoption": SCRIPTS / "smoke_brooks_semantic_research_snapshot_adoption.py",
    "smoke-wind-agent-snapshot-bootstrap": SCRIPTS / "smoke_wind_agent_snapshot_bootstrap.py",
    "smoke-wind-agent-snapshot-adoption": SCRIPTS / "smoke_wind_agent_snapshot_adoption.py",
    "run-smoke-suite": SCRIPTS / "run_smoke_suite.py",
    "eval-wind-agent": SCRIPTS / "run_wind_agent_eval.py",
    "enforce-worktree": SCRIPTS / "enforce_worktree.py",
    "install-hooks": SCRIPTS / "install_hooks.py",
    "prepare-role-eval": SCRIPTS / "prepare_role_eval_bundle.py",
}


def main() -> int:
    parser = argparse.ArgumentParser(description="Unified CLI for session-memory repo workflows.")
    parser.add_argument("command", choices=sorted(KERNEL_COMMANDS | set(REPO_COMMAND_MAP)))
    parser.add_argument("args", nargs=argparse.REMAINDER)
    parsed = parser.parse_args()

    if parsed.command in KERNEL_COMMANDS:
        cmd = [sys.executable, "-m", KERNEL_CLI, parsed.command, *parsed.args]
    else:
        script_path = REPO_COMMAND_MAP[parsed.command]
        cmd = [sys.executable, str(script_path), *parsed.args]
    completed = subprocess.run(cmd, cwd=str(ROOT))
    return completed.returncode


if __name__ == "__main__":
    raise SystemExit(main())
