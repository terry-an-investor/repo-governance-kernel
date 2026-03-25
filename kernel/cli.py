#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path

from kernel.config_runtime import CONFIG_RESOLUTION_ENV_VAR, PROJECT_ID_ENV_VAR, resolve_runtime_config
from kernel.runtime_paths import REPO_ROOT_ENV_VAR, resolve_repo_root


ROOT = resolve_repo_root()

COMMAND_MODULES = {
    "activate-exception-contract": "kernel.commands.activate_exception_contract",
    "assess-external-target-from-intent": "kernel.commands.assess_external_target_from_intent",
    "assess-external-target-once": "kernel.commands.assess_external_target_once",
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
    "describe-config": "kernel.commands.describe_config",
    "describe-public-alpha-surface": "kernel.commands.describe_public_alpha_surface",
    "draft-external-target-shadow-scope": "kernel.commands.draft_external_target_shadow_scope",
    "enforce-worktree": "kernel.commands.enforce_worktree",
    "execute-adjudication-followups": "kernel.commands.execute_adjudication_followups",
    "invalidate-exception-contract": "kernel.commands.invalidate_exception_contract",
    "install-hooks": "kernel.commands.install_hooks",
    "list-transition-registry": "kernel.commands.list_transition_registry",
    "bootstrap-repo": "kernel.commands.bootstrap_repo",
    "onboard-repo": "kernel.commands.onboard_repo",
    "onboard-repo-from-intent": "kernel.commands.onboard_repo_from_intent",
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

PROJECT_AWARE_PUBLIC_COMMANDS = {
    "audit-control-state",
    "enforce-worktree",
    "bootstrap-repo",
    "onboard-repo",
    "onboard-repo-from-intent",
    "assess-external-target-once",
    "assess-external-target-from-intent",
}


def _extract_option_value(args: list[str], option: str) -> str:
    for index, value in enumerate(args):
        normalized = value.strip()
        if normalized == option and index + 1 < len(args):
            return args[index + 1].strip()
        if normalized.startswith(f"{option}="):
            return normalized.split("=", 1)[1].strip()
    return ""


def main() -> int:
    parser = argparse.ArgumentParser(description="Unified CLI for the reusable governance kernel.")
    parser.add_argument("--repo-root", default="")
    parser.add_argument("command", choices=sorted(COMMAND_MODULES))
    parser.add_argument("args", nargs=argparse.REMAINDER)
    parsed = parser.parse_args()

    env = os.environ.copy()
    repo_root = parsed.repo_root.strip()
    explicit_project_id = _extract_option_value(parsed.args, "--project-id")
    resolved_config = resolve_runtime_config(
        explicit_repo_root=repo_root,
        explicit_project_id=explicit_project_id,
        cwd=Path.cwd(),
        env=env,
    )
    resolved_repo_root = str(resolved_config["resolved"]["repo_root"]).strip()
    resolved_project_id = str(resolved_config["resolved"]["project_id"]).strip()
    if resolved_repo_root:
        env[REPO_ROOT_ENV_VAR] = resolved_repo_root
    if resolved_project_id:
        env[PROJECT_ID_ENV_VAR] = resolved_project_id
    env[CONFIG_RESOLUTION_ENV_VAR] = json.dumps(resolved_config, ensure_ascii=True)

    module_name = COMMAND_MODULES[parsed.command]
    injected_args: list[str] = []
    if parsed.command in PROJECT_AWARE_PUBLIC_COMMANDS and not explicit_project_id and resolved_project_id:
        injected_args.extend(["--project-id", resolved_project_id])
    cmd = [sys.executable, "-m", module_name, *injected_args, *parsed.args]
    completed = subprocess.run(cmd, cwd=str(ROOT), check=False, env=env)
    return completed.returncode


if __name__ == "__main__":
    raise SystemExit(main())
