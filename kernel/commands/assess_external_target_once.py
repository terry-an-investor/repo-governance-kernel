#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json

from kernel.executor_runtime import run_cli_command, run_cli_command_json
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


def _append_optional_scalar(args: list[str], flag: str, value: str) -> None:
    normalized = value.strip()
    if normalized:
        args.extend([flag, normalized])


def main() -> int:
    args = parse_args()
    if not project_dir(args.project_id).exists():
        raise SystemExit(f"project directory not found: {project_dir(args.project_id)}")

    workspace_root = args.workspace_root.strip()
    source_repo = args.source_repo.strip() or workspace_root

    draft_args = [
        "--project-id",
        args.project_id,
        "--workspace-root",
        workspace_root,
        "--source-repo",
        source_repo,
    ]
    _append_optional_scalar(draft_args, "--output", args.draft_output)
    draft = run_cli_command_json(
        "draft-external-target-shadow-scope",
        draft_args,
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

    round_expand_args = [
        "--project-id",
        args.project_id,
        "--round-id",
        str(draft.get("round_id") or "").strip(),
        "--reason",
        "Temporarily expand the active round so the task contract can move from its previous scope into the external target dirty paths.",
        "--replace-scope-paths",
    ]
    for path in interim_round_scope_paths:
        round_expand_args.extend(["--scope-path", path])
    round_expand = run_cli_command_json(
        "rewrite-open-round",
        round_expand_args,
        failure_message="initial rewrite-open-round failed during external-target workflow",
    )

    task_rewrite_args = [
        "--project-id",
        args.project_id,
        "--task-contract-id",
        str(draft.get("task_contract_id") or "").strip(),
        "--reason",
        "Align the active task contract to the observed external target dirty paths before running assess-host-adoption.",
        "--summary",
        str(draft.get("suggested_task_summary") or "").strip(),
        "--intent",
        str(draft.get("suggested_task_intent") or "").strip(),
        "--replace-paths",
        "--replace-allowed-changes",
        "--replace-forbidden-changes",
        "--replace-completion-criteria",
    ]
    for path in suggested_task_paths:
        task_rewrite_args.extend(["--path", path])
    for item in suggested_task_allowed_changes:
        task_rewrite_args.extend(["--allowed-change", item])
    for item in suggested_task_forbidden_changes:
        task_rewrite_args.extend(["--forbidden-change", item])
    for item in suggested_task_completion_criteria:
        task_rewrite_args.extend(["--completion-criterion", item])
    task_rewrite = run_cli_command_json(
        "rewrite-open-task-contract",
        task_rewrite_args,
        failure_message="rewrite-open-task-contract failed during external-target workflow",
    )

    round_rewrite_args = [
        "--project-id",
        args.project_id,
        "--round-id",
        str(draft.get("round_id") or "").strip(),
        "--reason",
        "Align the active round to the observed external target dirty paths before running assess-host-adoption.",
        "--deliverable",
        str(draft.get("suggested_round_deliverable") or "").strip(),
        "--validation-plan",
        str(draft.get("suggested_round_validation_plan") or "").strip(),
        "--replace-scope-items",
        "--replace-scope-paths",
    ]
    for item in suggested_round_scope_items:
        round_rewrite_args.extend(["--scope-item", item])
    for path in suggested_round_scope_paths:
        round_rewrite_args.extend(["--scope-path", path])
    round_rewrite = run_cli_command_json(
        "rewrite-open-round",
        round_rewrite_args,
        failure_message="final rewrite-open-round failed during external-target workflow",
    )

    refresh_success, refresh_output = run_cli_command(
        "refresh-current-task-anchor",
        [
            "--project-id",
            args.project_id,
            "--workspace-root",
            workspace_root,
        ],
        failure_message="refresh-current-task-anchor failed during external-target workflow",
    )
    if not refresh_success:
        raise SystemExit(refresh_output)

    assessment_args = [
        "--project-id",
        args.project_id,
        "--workspace-root",
        workspace_root,
        "--source-repo",
        source_repo,
        "--mode",
        "external-target-shadow",
    ]
    _append_optional_scalar(assessment_args, "--output", args.report_output)
    assessment = run_cli_command_json(
        "assess-host-adoption",
        assessment_args,
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
                "round_expand": round_expand,
                "task_rewrite": task_rewrite,
                "round_rewrite": round_rewrite,
                "refresh_anchor_stdout": refresh_output,
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
