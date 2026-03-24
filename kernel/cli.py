#!/usr/bin/env python3
from __future__ import annotations

import argparse
import os
import subprocess
import sys
from kernel.runtime_paths import REPO_ROOT_ENV_VAR, resolve_repo_root


ROOT = resolve_repo_root()

COMMAND_MODULES = {
    "activate-exception-contract": "kernel.commands.activate_exception_contract",
    "assess-host-adoption": "kernel.commands.assess_host_adoption",
    "adjudicate-control-state": "kernel.commands.adjudicate_control_state",
    "audit-control-state": "kernel.audit_control_state",
    "audit-product-docs": "kernel.commands.audit_product_docs",
    "audit-task-contracts": "kernel.audit_task_contracts",
    "build-index": "kernel.build_index",
    "capture-handoff": "kernel.commands.capture_handoff",
    "check-index": "kernel.commands.check_index",
    "close-objective": "kernel.commands.close_objective",
    "compile-adjudication-executor-plan": "kernel.commands.compile_adjudication_executor_plan",
    "compile-role-context": "kernel.commands.compile_role_context",
    "create-snapshot": "kernel.commands.create_snapshot",
    "draft-external-target-shadow-scope": "kernel.commands.draft_external_target_shadow_scope",
    "enforce-worktree": "kernel.commands.enforce_worktree",
    "execute-adjudication-followups": "kernel.commands.execute_adjudication_followups",
    "invalidate-exception-contract": "kernel.commands.invalidate_exception_contract",
    "install-hooks": "kernel.commands.install_hooks",
    "list-transition-registry": "kernel.commands.list_transition_registry",
    "bootstrap-repo": "kernel.commands.bootstrap_repo",
    "open-objective": "kernel.commands.open_objective",
    "open-round": "kernel.commands.open_round",
    "open-task-contract": "kernel.commands.open_task_contract",
    "query": "kernel.commands.query_index",
    "reconcile-control-state": "kernel.commands.reconcile_control_state",
    "record-hard-pivot": "kernel.commands.record_hard_pivot",
    "record-soft-pivot": "kernel.commands.record_soft_pivot",
    "refresh-current-task-anchor": "kernel.commands.refresh_current_task_anchor",
    "refresh-round-scope": "kernel.commands.refresh_round_scope",
    "render-live-workspace": "kernel.commands.render_live_workspace_projection",
    "retire-exception-contract": "kernel.commands.retire_exception_contract",
    "rewrite-open-round": "kernel.commands.rewrite_open_round",
    "rewrite-open-task-contract": "kernel.commands.rewrite_open_task_contract",
    "set-phase": "kernel.commands.set_phase",
    "update-round-status": "kernel.commands.update_round_status",
    "update-task-contract-status": "kernel.commands.update_task_contract_status",
}


def main() -> int:
    parser = argparse.ArgumentParser(description="Unified CLI for the reusable governance kernel.")
    parser.add_argument("--repo-root", default="")
    parser.add_argument("command", choices=sorted(COMMAND_MODULES))
    parser.add_argument("args", nargs=argparse.REMAINDER)
    parsed = parser.parse_args()

    env = os.environ.copy()
    repo_root = parsed.repo_root.strip()
    if repo_root:
        env[REPO_ROOT_ENV_VAR] = repo_root

    module_name = COMMAND_MODULES[parsed.command]
    cmd = [sys.executable, "-m", module_name, *parsed.args]
    completed = subprocess.run(cmd, cwd=str(ROOT), check=False, env=env)
    return completed.returncode


if __name__ == "__main__":
    raise SystemExit(main())
