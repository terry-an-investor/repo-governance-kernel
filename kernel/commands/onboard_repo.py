#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json

from kernel.executor_runtime import run_cli_command_json
from kernel.governed_bundle_runtime import execute_governed_bundle
from kernel.repo_onboarding import (
    assert_onboarding_target_available,
    compile_repo_onboarding_bundle_payload,
    render_onboarding_error,
    render_onboarding_success_payload,
    resolve_onboarding_control_state,
)
from kernel.runtime_paths import resolve_repo_root


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Bootstrap a governed host repo and open the first honest objective, round, and task boundary."
    )
    parser.add_argument("--project-id", required=True)
    parser.add_argument("--skip-hooks", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    repo_root = resolve_repo_root()
    workspace_root = str(repo_root).replace("\\", "/")
    if not (repo_root / ".git").exists():
        raise SystemExit(
            render_onboarding_error(
                stage="preflight",
                code="git_repository_not_found",
                message=f"git repository not found at {workspace_root}",
                project_id=args.project_id,
                workspace_root=workspace_root,
                skip_hooks=bool(args.skip_hooks),
            )
        )

    try:
        assert_onboarding_target_available(args.project_id)
    except SystemExit as exc:
        raise SystemExit(
            render_onboarding_error(
                stage="preflight",
                code="project_history_not_empty",
                message=str(exc),
                project_id=args.project_id,
                workspace_root=workspace_root,
                skip_hooks=bool(args.skip_hooks),
            )
        ) from exc

    onboarding = compile_repo_onboarding_bundle_payload(
        args.project_id,
        workspace_root,
        skip_hooks=args.skip_hooks,
    )
    bundle_payload = {
        "command": "onboard-repo",
        "workspace_root": onboarding["workspace_root"],
        "bootstrap_skip_hooks": onboarding["bootstrap_skip_hooks"],
        "objective_title": onboarding["objective_title"],
        "objective_summary": onboarding["objective_summary"],
        "objective_problem": onboarding["objective_problem"],
        "objective_success_criterion": onboarding["objective_success_criterion"],
        "objective_non_goal": onboarding["objective_non_goal"],
        "objective_why_now": onboarding["objective_why_now"],
        "objective_phase": onboarding["objective_phase"],
        "objective_path": onboarding["objective_path"],
        "round_title": onboarding["round_title"],
        "round_scope_item": onboarding["round_scope_item"],
        "round_scope_path": onboarding["round_scope_path"],
        "round_deliverable": onboarding["round_deliverable"],
        "round_validation_plan": onboarding["round_validation_plan"],
        "task_title": onboarding["task_title"],
        "task_summary": onboarding["task_summary"],
        "task_intent": onboarding["task_intent"],
        "task_path": onboarding["task_path"],
        "task_allowed_change": onboarding["task_allowed_change"],
        "task_forbidden_change": onboarding["task_forbidden_change"],
        "task_completion_criterion": onboarding["task_completion_criterion"],
    }

    bundle_success, bundle_detail = execute_governed_bundle(
        args.project_id,
        bundle_payload,
        "onboard-repo",
    )
    if not bundle_success:
        raise SystemExit(
            render_onboarding_error(
                stage="bundle-execution",
                code="bundle_execution_failed",
                message=bundle_detail,
                project_id=args.project_id,
                workspace_root=workspace_root,
                skip_hooks=bool(args.skip_hooks),
                execution={
                    "bundle_name": "onboard-repo",
                    "bundle_detail": bundle_detail,
                    "compiled_bundle": {
                        "governance_scope_paths": onboarding["governance_scope_paths"],
                        "observed_repo_dirty_paths": onboarding["observed_repo_dirty_paths"],
                        "onboarding_scope_paths": onboarding["onboarding_scope_paths"],
                        "bundle_payload": bundle_payload,
                    },
                },
            )
        )

    audit = run_cli_command_json(
        "audit-control-state",
        ["--project-id", args.project_id],
        failure_message="audit-control-state failed after onboarding",
    )
    enforce = run_cli_command_json(
        "enforce-worktree",
        [
            "--project-id",
            args.project_id,
            "--workspace-root",
            workspace_root,
        ],
        failure_message="enforce-worktree failed after onboarding",
    )

    if str(audit.get("status") or "") != "ok" or str(enforce.get("status") or "") != "ok":
        raise SystemExit(
            render_onboarding_error(
                stage="postconditions",
                code="postconditions_not_clean",
                message="onboard-repo did not finish in an audit-clean enforced state",
                project_id=args.project_id,
                workspace_root=workspace_root,
                skip_hooks=bool(args.skip_hooks),
                execution={
                    "bundle_name": "onboard-repo",
                    "bundle_detail": bundle_detail,
                    "compiled_bundle": {
                        "governance_scope_paths": onboarding["governance_scope_paths"],
                        "observed_repo_dirty_paths": onboarding["observed_repo_dirty_paths"],
                        "onboarding_scope_paths": onboarding["onboarding_scope_paths"],
                        "bundle_payload": bundle_payload,
                    },
                },
                postconditions={
                    "audit_status": str(audit.get("status") or ""),
                    "enforce_status": str(enforce.get("status") or ""),
                    "audit": audit,
                    "enforce": enforce,
                },
                details={"audit": audit, "enforce": enforce},
            )
        )

    control_state = resolve_onboarding_control_state(args.project_id)

    print(json.dumps(
        render_onboarding_success_payload(
            project_id=args.project_id,
            workspace_root=workspace_root,
            skip_hooks=bool(args.skip_hooks),
            bundle_payload=bundle_payload,
            bundle_detail=bundle_detail,
            onboarding_payload=onboarding,
            control_state=control_state,
            audit=audit,
            enforce=enforce,
        ),
        ensure_ascii=True,
        indent=2,
    ))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
