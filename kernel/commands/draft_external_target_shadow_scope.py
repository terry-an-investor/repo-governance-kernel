#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path

from kernel.host_adoption import (
    adoption_scope_draft_path,
    draft_contract,
    inspect_workspace_changed_paths,
    render_external_target_shadow_scope_draft,
    suggest_scope_paths_from_dirty_paths,
    to_json,
)
from kernel.round_control import (
    assert_anchor_maintenance_command_contract,
    find_task_contracts,
    project_dir,
    resolve_active_objective_record,
    select_open_round_record,
)
from kernel.runtime_paths import resolve_repo_root


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Draft the smallest honest external-target shadow scope before running assess-host-adoption."
    )
    parser.add_argument("--project-id", required=True)
    parser.add_argument("--workspace-root", required=True)
    parser.add_argument("--source-repo", default="")
    parser.add_argument("--output", default="")
    return parser.parse_args()


def _resolve_draft_path(project_id: str, output: str) -> Path:
    if output.strip():
        output_path = Path(output)
        if not output_path.is_absolute():
            output_path = Path.cwd() / output_path
        return output_path
    return adoption_scope_draft_path(project_id)


def main() -> int:
    args = parse_args()
    governance_root = resolve_repo_root()
    governance_project_root = project_dir(args.project_id)
    objective_path, _objective_meta, _objective_sections, objective_id = resolve_active_objective_record(args.project_id)
    round_record, round_issues = select_open_round_record(args.project_id)
    if round_record is None:
        details = "; ".join(round_issues) if round_issues else "no open round exists"
        raise SystemExit(f"external-target shadow drafting requires one open round: {details}")
    round_path, round_meta, _round_sections = round_record
    round_id = str(round_meta.get("id") or round_path.stem).strip()
    current_round_scope_paths = [str(item).strip() for item in round_meta.get("paths", []) if str(item).strip()]

    active_task_contracts = find_task_contracts(args.project_id, round_id=round_id, statuses={"active"})
    if not active_task_contracts:
        raise SystemExit(
            f"external-target shadow drafting requires at least one active task contract beneath round `{round_id}`"
        )
    if len(active_task_contracts) > 1:
        raise SystemExit(
            f"external-target shadow drafting currently requires one active task contract for round `{round_id}`; found {len(active_task_contracts)}"
        )
    task_contract_path, task_contract_meta, _task_contract_sections = active_task_contracts[0]
    task_contract_id = str(task_contract_meta.get("id") or task_contract_path.stem).strip()
    current_task_paths = [str(item).strip() for item in task_contract_meta.get("paths", []) if str(item).strip()]

    workspace_root = args.workspace_root.strip()
    source_repo = args.source_repo.strip() or workspace_root
    draft_path = _resolve_draft_path(args.project_id, args.output)
    contract_payload = draft_contract(
        governance_root=str(governance_root),
        governance_project_root=str(governance_project_root),
        workspace_root=workspace_root,
        draft_path=str(draft_path),
        requested_mode="external-target-shadow",
    )
    live_workspace, dirty_paths = inspect_workspace_changed_paths(workspace_root)
    suggested_scope_paths = suggest_scope_paths_from_dirty_paths(dirty_paths)
    repo_label = Path(workspace_root).name or "external target"

    suggested_round_scope_items = [
        f"Assess the current `{repo_label}` dirty worktree in external-target shadow mode before any stronger host adoption claim.",
        "Keep the adopted boundary equal to the observed dirty paths so the first assessment verdict reflects real source-repo scope.",
    ]
    suggested_round_deliverable = (
        "A bounded external-target shadow assessment setup whose round/task paths match the observed dirty repo scope."
    )
    suggested_round_validation_plan = (
        "Refresh the current-task anchor to the external workspace, then run assess-host-adoption and inspect whether remaining blockers are real scope gaps."
    )
    suggested_task_intent = (
        f"Author the smallest honest task boundary for the current `{repo_label}` dirty paths so assess-host-adoption can judge the repo without hand-authored ambiguity."
    )
    suggested_task_summary = (
        f"One bounded external-target shadow assessment path for the current `{repo_label}` dirty worktree."
    )
    suggested_task_allowed_changes = [
        "Rewrite the active round and task-contract so their paths match the observed external target dirty paths.",
        "Refresh the current-task anchor to the external workspace and run assess-host-adoption in external-target-shadow mode.",
    ]
    suggested_task_forbidden_changes = [
        "Do not mutate the external source repository.",
        "Do not claim broader live-host rewrite or continuous monitoring authority.",
    ]
    suggested_task_completion_criteria = [
        "The active round and task-contract paths match the observed external target dirty paths.",
        "The assessment report exists and its verdict reflects the rewritten external target scope.",
    ]

    command_sequence = [
        "uv run python -m kernel.cli rewrite-open-round --project-id "
        + args.project_id
        + " --round-id "
        + round_id
        + " --reason \"Align the round boundary to the observed external target dirty paths before running assess-host-adoption.\""
        + "".join(f" --scope-path \"{path}\"" for path in suggested_scope_paths)
        + " --replace-scope-paths"
        + "".join(f" --scope-item \"{item}\"" for item in suggested_round_scope_items),
        "uv run python -m kernel.cli rewrite-open-task-contract --project-id "
        + args.project_id
        + " --task-contract-id "
        + task_contract_id
        + " --reason \"Align the task boundary to the observed external target dirty paths before running assess-host-adoption.\""
        + "".join(f" --path \"{path}\"" for path in suggested_scope_paths)
        + " --replace-paths",
        "uv run python -m kernel.cli refresh-current-task-anchor --project-id "
        + args.project_id
        + f" --workspace-root \"{workspace_root}\"",
        "uv run python -m kernel.cli assess-host-adoption --project-id "
        + args.project_id
        + f" --workspace-root \"{workspace_root}\" --source-repo \"{source_repo}\" --mode external-target-shadow",
    ]

    current_control_state_lines = [
        f"open round `{round_id}` already exists and must be rewritten, not replaced, if the external target boundary changes",
        f"active task contract `{task_contract_id}` already exists and must stay inside the rewritten round scope",
        f"draft output path resolves to `{draft_path}`",
    ]

    draft_text = render_external_target_shadow_scope_draft(
        project_id=args.project_id,
        source_repo=source_repo,
        workspace_root=workspace_root,
        objective_id=objective_id,
        suggested_round_title=str(round_meta.get("title") or round_id),
        suggested_round_scope_items=suggested_round_scope_items,
        suggested_round_scope_paths=suggested_scope_paths,
        suggested_round_deliverable=suggested_round_deliverable,
        suggested_round_validation_plan=suggested_round_validation_plan,
        suggested_task_title=str(task_contract_meta.get("title") or task_contract_id),
        suggested_task_summary=suggested_task_summary,
        suggested_task_intent=suggested_task_intent,
        suggested_task_paths=suggested_scope_paths,
        suggested_task_allowed_changes=suggested_task_allowed_changes,
        suggested_task_forbidden_changes=suggested_task_forbidden_changes,
        suggested_task_completion_criteria=suggested_task_completion_criteria,
        draft_contract_payload=contract_payload,
        live_workspace=live_workspace,
        dirty_paths=dirty_paths,
        command_sequence=command_sequence,
        current_control_state_lines=current_control_state_lines,
    )

    draft_path.parent.mkdir(parents=True, exist_ok=True)
    draft_path.write_text(draft_text, encoding="utf-8", newline="\n")

    assert_anchor_maintenance_command_contract(
        "draft-external-target-shadow-scope",
        provided_inputs={"project_id", "workspace_root"},
    )

    print(
        to_json(
            {
                "project_id": args.project_id,
                "governance_root": str(governance_root),
                "governance_project_root": str(governance_project_root),
                "objective_id": objective_id,
                "objective_path": str(objective_path),
                "round_id": round_id,
                "round_path": str(round_path),
                "task_contract_id": task_contract_id,
                "task_contract_path": str(task_contract_path),
                "current_round_scope_paths": current_round_scope_paths,
                "current_task_paths": current_task_paths,
                "workspace_root": workspace_root,
                "source_repo": source_repo,
                "draft_path": str(draft_path),
                "draft_contract": contract_payload,
                "dirty_paths": dirty_paths,
                "suggested_round_scope_items": suggested_round_scope_items,
                "suggested_round_scope_paths": suggested_scope_paths,
                "suggested_round_deliverable": suggested_round_deliverable,
                "suggested_round_validation_plan": suggested_round_validation_plan,
                "suggested_task_summary": suggested_task_summary,
                "suggested_task_paths": suggested_scope_paths,
                "suggested_task_intent": suggested_task_intent,
                "suggested_task_allowed_changes": suggested_task_allowed_changes,
                "suggested_task_forbidden_changes": suggested_task_forbidden_changes,
                "suggested_task_completion_criteria": suggested_task_completion_criteria,
                "command_sequence": command_sequence,
                "wrote_draft": True,
            }
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
