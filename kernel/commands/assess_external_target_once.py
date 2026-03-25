#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json

from kernel.executor_runtime import run_cli_command_json
from kernel.governed_bundle_runtime import execute_governed_bundle
from kernel.host_adoption import external_target_assessment_flow_contract, external_target_assessment_next_actions
from kernel.public_flow_contracts import render_public_flow_payload
from kernel.round_control import project_dir


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run one bounded external-target shadow workflow: draft scope, rewrite control, refresh anchor, and assess."
    )
    parser.add_argument("--project-id", required=True)
    parser.add_argument("--workspace-root", required=True)
    parser.add_argument("--source-repo", default="")
    parser.add_argument("--draft-output", default="")
    parser.add_argument("--report-output", default="")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    workspace_root = args.workspace_root.strip()
    source_repo = args.source_repo.strip() or workspace_root
    flow_contract = (
        external_target_assessment_flow_contract(
            project_id=args.project_id,
            workspace_root=workspace_root,
            source_repo=source_repo,
        )
        if workspace_root
        else None
    )
    if not project_dir(args.project_id).exists():
        raise SystemExit(
            render_public_flow_payload(
                status="blocked",
                flow_name="external-target-single-assessment",
                entrypoint="assess-external-target-once",
                entry_kind="direct-command",
                project_id=args.project_id,
                workspace_root=workspace_root,
                source_repo=source_repo,
                flow_contract=flow_contract,
                next_actions=[
                    "Bootstrap or onboard the governed host project before running external-target assessment.",
                    "Then rerun `assess-external-target-once` against the intended external workspace.",
                ],
                blocked={
                    "stage": "preflight",
                    "code": "project_control_state_not_found",
                    "message": f"project directory not found: {project_dir(args.project_id)}",
                    "meaning": "the external-target assessment flow requires one existing governed project because it rewrites active round and task-contract scope before assessing",
                    "suggested_next_actions": [
                        "Bootstrap or onboard the governed host project before running external-target assessment.",
                        "Then rerun `assess-external-target-once` against the intended external workspace.",
                    ],
                },
            )
        )

    try:
        draft = run_cli_command_json(
            "draft-external-target-shadow-scope",
            [
                "--project-id",
                args.project_id,
                "--workspace-root",
                workspace_root,
                "--source-repo",
                source_repo,
                *(["--output", args.draft_output.strip()] if args.draft_output.strip() else []),
            ],
            failure_message="external-target shadow drafting failed",
        )
    except SystemExit as exc:
        raise SystemExit(
            render_public_flow_payload(
                status="blocked",
                flow_name="external-target-single-assessment",
                entrypoint="assess-external-target-once",
                entry_kind="direct-command",
                project_id=args.project_id,
                workspace_root=workspace_root,
                source_repo=source_repo,
                flow_contract=flow_contract,
                next_actions=[
                    "Make sure the governed host already has one active objective, open round, and active task contract before running this workflow.",
                    "Make sure the target workspace path exists and is accessible from the current machine.",
                ],
                blocked={
                    "stage": "drafting",
                    "code": "draft_scope_failed",
                    "message": str(exc),
                    "meaning": "the workflow could not produce one draft scope from the target repo's current dirty paths, so it cannot honestly rewrite the governed boundary yet",
                    "suggested_next_actions": [
                        "Make sure the governed host already has one active objective, open round, and active task contract before running this workflow.",
                        "Make sure the target workspace path exists and is accessible from the current machine.",
                    ],
                },
            )
        ) from exc

    suggested_round_scope_paths = [str(item).strip() for item in draft.get("suggested_round_scope_paths", []) if str(item).strip()]
    suggested_round_scope_items = [str(item).strip() for item in draft.get("suggested_round_scope_items", []) if str(item).strip()]
    suggested_task_paths = [str(item).strip() for item in draft.get("suggested_task_paths", []) if str(item).strip()]
    current_round_scope_paths = [str(item).strip() for item in draft.get("current_round_scope_paths", []) if str(item).strip()]
    current_task_paths = [str(item).strip() for item in draft.get("current_task_paths", []) if str(item).strip()]
    suggested_task_allowed_changes = [
        str(item).strip() for item in draft.get("suggested_task_allowed_changes", []) if str(item).strip()
    ]
    suggested_task_forbidden_changes = [
        str(item).strip() for item in draft.get("suggested_task_forbidden_changes", []) if str(item).strip()
    ]
    suggested_task_completion_criteria = [
        str(item).strip() for item in draft.get("suggested_task_completion_criteria", []) if str(item).strip()
    ]
    if not suggested_round_scope_paths or not suggested_task_paths:
        raise SystemExit(
            render_public_flow_payload(
                status="blocked",
                flow_name="external-target-single-assessment",
                entrypoint="assess-external-target-once",
                entry_kind="direct-command",
                project_id=args.project_id,
                workspace_root=workspace_root,
                source_repo=source_repo,
                flow_contract=flow_contract,
                execution={
                    "draft": draft,
                },
                next_actions=[
                    "Point the workflow at a repo with current dirty paths, or make one bounded change before requesting a shadow assessment.",
                    "If you only need a report on the currently adopted governed host, use the lower-layer assessment surface instead of this external-target workflow.",
                ],
                blocked={
                    "stage": "drafting",
                    "code": "no_dirty_paths_observed",
                    "message": "external-target assessment workflow requires at least one observed dirty path before it can rewrite scope",
                    "meaning": "this one-task workflow derives the new governed boundary from the external repo's current dirty paths, so it cannot continue when the target repo is clean",
                    "suggested_next_actions": [
                        "Point the workflow at a repo with current dirty paths, or make one bounded change before requesting a shadow assessment.",
                        "If you only need a report on the currently adopted governed host, use the lower-layer assessment surface instead of this external-target workflow.",
                    ],
                },
            )
        )

    interim_round_scope_paths: list[str] = []
    for path in [*current_round_scope_paths, *current_task_paths, *suggested_round_scope_paths]:
        if path and path not in interim_round_scope_paths:
            interim_round_scope_paths.append(path)

    bundle_payload = {
        "command": "assess-external-target-once",
        "workspace_root": workspace_root,
        "source_repo": source_repo,
        "draft_output": args.draft_output.strip(),
        "report_output": args.report_output.strip(),
        "round_id": str(draft.get("round_id") or "").strip(),
        "task_contract_id": str(draft.get("task_contract_id") or "").strip(),
        "expand_round_scope_path": interim_round_scope_paths,
        "round_scope_item": suggested_round_scope_items,
        "round_scope_path": suggested_round_scope_paths,
        "round_deliverable": str(draft.get("suggested_round_deliverable") or "").strip(),
        "round_validation_plan": str(draft.get("suggested_round_validation_plan") or "").strip(),
        "task_summary": str(draft.get("suggested_task_summary") or "").strip(),
        "task_intent": str(draft.get("suggested_task_intent") or "").strip(),
        "task_path": suggested_task_paths,
        "task_allowed_change": suggested_task_allowed_changes,
        "task_forbidden_change": suggested_task_forbidden_changes,
        "task_completion_criterion": suggested_task_completion_criteria,
    }
    bundle_success, bundle_detail = execute_governed_bundle(
        args.project_id,
        bundle_payload,
        "assess-external-target-once",
    )
    if not bundle_success:
        raise SystemExit(
            render_public_flow_payload(
                status="blocked",
                flow_name="external-target-single-assessment",
                entrypoint="assess-external-target-once",
                entry_kind="direct-command",
                project_id=args.project_id,
                workspace_root=workspace_root,
                source_repo=source_repo,
                flow_contract=flow_contract,
                execution={
                    "draft": draft,
                    "bundle_name": "assess-external-target-once",
                    "bundle_detail": bundle_detail,
                    "compiled_bundle": bundle_payload,
                },
                next_actions=[
                    "Inspect the bundle execution detail and repair the lower-layer blocked step before retrying the workflow.",
                ],
                blocked={
                    "stage": "bundle-execution",
                    "code": "bundle_execution_failed",
                    "message": bundle_detail,
                    "meaning": "the workflow could draft scope, but one governed rewrite or anchor-maintenance step blocked before the final assessment could run",
                    "suggested_next_actions": [
                        "Inspect the bundle execution detail and repair the lower-layer blocked step before retrying the workflow.",
                    ],
                },
            )
        )

    try:
        assessment = run_cli_command_json(
            "assess-host-adoption",
            [
                "--project-id",
                args.project_id,
                "--workspace-root",
                workspace_root,
                "--source-repo",
                source_repo,
                "--mode",
                "external-target-shadow",
                *(["--output", args.report_output.strip()] if args.report_output.strip() else []),
            ],
            failure_message="assess-host-adoption failed during external-target workflow",
        )
    except SystemExit as exc:
        raise SystemExit(
            render_public_flow_payload(
                status="blocked",
                flow_name="external-target-single-assessment",
                entrypoint="assess-external-target-once",
                entry_kind="direct-command",
                project_id=args.project_id,
                workspace_root=workspace_root,
                source_repo=source_repo,
                flow_contract=flow_contract,
                execution={
                    "draft": draft,
                    "bundle_name": "assess-external-target-once",
                    "bundle_detail": bundle_detail,
                    "compiled_bundle": bundle_payload,
                },
                next_actions=[
                    "Inspect the lower-layer assess-host-adoption failure detail and repair the governed control state before retrying the public workflow.",
                ],
                blocked={
                    "stage": "assessment",
                    "code": "assessment_execution_failed",
                    "message": str(exc),
                    "meaning": "the workflow rewrote scope successfully but the lower-layer assessment command still could not produce a stable assessment payload",
                    "suggested_next_actions": [
                        "Inspect the lower-layer assess-host-adoption failure detail and repair the governed control state before retrying the public workflow.",
                    ],
                },
            )
        ) from exc

    postconditions = {
        "audit_status": str((assessment.get("final_audit") or {}).get("status") or ""),
        "enforce_status": str((assessment.get("final_enforce") or {}).get("status") or ""),
        "audit": assessment.get("final_audit"),
        "enforce": assessment.get("final_enforce"),
    }
    outcome = {
        "draft": draft,
        "assessment": assessment,
        "adopted_round_scope_paths": suggested_round_scope_paths,
        "adopted_task_paths": suggested_task_paths,
    }
    next_actions = external_target_assessment_next_actions(
        project_id=args.project_id,
        workspace_root=workspace_root,
        blocker_classification=assessment.get("blocker_classification") if isinstance(assessment, dict) else None,
        report_path=str(assessment.get("report_path") or ""),
    )

    if postconditions["audit_status"] != "ok" or postconditions["enforce_status"] != "ok":
        raise SystemExit(
            render_public_flow_payload(
                status="blocked",
                flow_name="external-target-single-assessment",
                entrypoint="assess-external-target-once",
                entry_kind="direct-command",
                project_id=args.project_id,
                workspace_root=workspace_root,
                source_repo=source_repo,
                flow_contract=flow_contract,
                execution={
                    "bundle_name": "assess-external-target-once",
                    "bundle_detail": bundle_detail,
                    "compiled_bundle": bundle_payload,
                },
                outcome=outcome,
                postconditions=postconditions,
                next_actions=next_actions,
                blocked={
                    "stage": "postconditions",
                    "code": "assessment_postconditions_blocked",
                    "message": "assess-external-target-once finished with remaining audit or enforcement blockers",
                    "meaning": "the workflow completed its one-task path, but the governed boundary or host-side support state still blocks a clean final verdict",
                    "suggested_next_actions": next_actions,
                    "details": {
                        "audit_status": postconditions["audit_status"],
                        "enforce_status": postconditions["enforce_status"],
                        "blocker_classification": assessment.get("blocker_classification"),
                        "remaining_blocked_paths": assessment.get("remaining_blocked_paths"),
                    },
                },
            )
        )

    print(
        render_public_flow_payload(
            status="ok",
            flow_name="external-target-single-assessment",
            entrypoint="assess-external-target-once",
            entry_kind="direct-command",
            project_id=args.project_id,
            workspace_root=workspace_root,
            source_repo=source_repo,
            flow_contract=flow_contract,
            execution={
                "bundle_name": "assess-external-target-once",
                "bundle_detail": bundle_detail,
                "compiled_bundle": bundle_payload,
            },
            outcome=outcome,
            postconditions=postconditions,
            next_actions=next_actions,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
