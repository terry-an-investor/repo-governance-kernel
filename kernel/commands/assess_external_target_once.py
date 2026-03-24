#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json

from kernel.executor_runtime import run_cli_command_json
from kernel.governed_bundle_runtime import execute_governed_bundle
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
    if not project_dir(args.project_id).exists():
        raise SystemExit(f"project directory not found: {project_dir(args.project_id)}")

    workspace_root = args.workspace_root.strip()
    source_repo = args.source_repo.strip() or workspace_root

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
        raise SystemExit("external-target assessment workflow requires at least one observed dirty path before it can rewrite scope")

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
        raise SystemExit(bundle_detail)

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

    print(
        json.dumps(
            {
                "status": "ok",
                "project_id": args.project_id,
                "workspace_root": workspace_root,
                "source_repo": source_repo,
                "draft": draft,
                "bundle_payload": bundle_payload,
                "bundle_detail": bundle_detail,
                "assessment": assessment,
                "adopted_round_scope_paths": suggested_round_scope_paths,
                "adopted_task_paths": suggested_task_paths,
            },
            ensure_ascii=True,
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
