from __future__ import annotations

import json
from pathlib import Path

from kernel.host_adoption import inspect_workspace_changed_paths
from kernel.round_control import (
    active_task_contract_records,
    load_all_objectives,
    load_all_rounds,
    load_all_task_contracts,
    render_task_contract_record_refs,
    select_active_objective_record,
    select_open_round_record,
)
from kernel.runtime_paths import render_project_state_prefix


def normalize_repo_relative_paths(paths: list[str]) -> list[str]:
    normalized: list[str] = []
    for raw_path in paths:
        candidate = str(raw_path).replace("\\", "/").strip().lstrip("./").rstrip("/")
        if candidate and candidate not in normalized:
            normalized.append(candidate)
    return normalized


def path_is_covered(path: str, scope_paths: list[str]) -> bool:
    normalized_path = str(path).replace("\\", "/").strip().lstrip("./")
    for raw_scope in scope_paths:
        scope = str(raw_scope).replace("\\", "/").strip().lstrip("./").rstrip("/")
        if not scope:
            continue
        if normalized_path == scope or normalized_path.startswith(scope + "/"):
            return True
    return False


def onboarding_governance_scope_paths(project_id: str) -> list[str]:
    return normalize_repo_relative_paths(
        [
            render_project_state_prefix(project_id),
            ".githooks",
            "cross-project",
            "index",
        ]
    )


def observed_repo_dirty_paths(project_id: str, workspace_root: str) -> list[str]:
    _live_workspace, dirty_paths = inspect_workspace_changed_paths(workspace_root)
    governance_scope_paths = onboarding_governance_scope_paths(project_id)
    return [
        path
        for path in normalize_repo_relative_paths(dirty_paths)
        if not path_is_covered(path, governance_scope_paths)
    ]


def onboarding_scope_paths(project_id: str, workspace_root: str) -> tuple[list[str], list[str]]:
    governance_scope_paths = onboarding_governance_scope_paths(project_id)
    repo_dirty_paths = observed_repo_dirty_paths(project_id, workspace_root)
    return governance_scope_paths, normalize_repo_relative_paths([*governance_scope_paths, *repo_dirty_paths])


def compile_repo_onboarding_bundle_payload(
    project_id: str,
    workspace_root: str,
    *,
    skip_hooks: bool = False,
) -> dict[str, object]:
    governance_scope_paths, scope_paths = onboarding_scope_paths(project_id, workspace_root)
    scope_item_lines = [
        f"Bootstrap the governed host control surface for `{project_id}` under `state/{project_id}/` and repo-local support paths.",
        "Carry any pre-existing dirty repo paths into the first honest governance boundary instead of dropping them during onboarding.",
    ]
    return {
        "workspace_root": str(Path(workspace_root).expanduser().resolve()).replace("\\", "/"),
        "bootstrap_skip_hooks": bool(skip_hooks),
        "objective_title": "Establish the first governed repo workflow",
        "objective_summary": "Bootstrap repo-governance-kernel in this host repo and open the first honest execution boundary.",
        "objective_problem": (
            "This host repo does not yet have the first active objective, round, and task contract needed to use repo-governance-kernel without manual control authoring."
        ),
        "objective_success_criterion": [
            "One active objective exists for the governed host.",
            "One open round exists with an honest scope for governance setup and any pre-existing dirty repo paths.",
            "One active task contract exists beneath that round.",
        ],
        "objective_non_goal": [
            "Do not claim continuous monitoring or background control services.",
            "Do not mutate pre-existing repo dirty paths automatically just to make onboarding look complete.",
        ],
        "objective_why_now": "Package-first adoption is not real until a new host repo can enter its first governed execution state without hand-opening every control object.",
        "objective_phase": "exploration",
        "objective_path": scope_paths,
        "round_title": "Bootstrap the first bounded governance setup",
        "round_scope_item": scope_item_lines,
        "round_scope_path": scope_paths,
        "round_deliverable": "One honest first governance setup with an active objective, open round, active task contract, and refreshed anchor.",
        "round_validation_plan": "Run audit-control-state and enforce-worktree after onboarding and confirm both are ok.",
        "task_title": "Complete repo onboarding into the first governed boundary",
        "task_summary": "Create the first honest governed execution setup for this host repo.",
        "task_intent": "Replace manual bootstrap-plus-authoring with one bounded onboarding surface that preserves real repo dirty-path scope.",
        "task_path": scope_paths,
        "task_allowed_change": [
            "Create the initial governed host control surface under the project state tree and repo-local support paths.",
            "Carry any already-dirty repo paths into the first bounded round and task contract without pretending they were clean.",
            "Refresh the current-task anchor to the governed host workspace.",
        ],
        "task_forbidden_change": [
            "Do not invent scope for repo paths that were not already dirty before onboarding.",
            "Do not claim general autonomous rewrite authority or continuous monitoring.",
        ],
        "task_completion_criterion": [
            "The governed host has one active objective, one open round, and one active task contract.",
            "The current-task anchor resolves to the governed host repo root.",
            "audit-control-state and enforce-worktree both return ok after onboarding.",
        ],
        "governance_scope_paths": governance_scope_paths,
        "observed_repo_dirty_paths": [
            path
            for path in scope_paths
            if not path_is_covered(path, governance_scope_paths)
        ],
        "onboarding_scope_paths": scope_paths,
    }


def onboarding_next_commands(project_id: str, workspace_root: str) -> list[str]:
    normalized_root = str(Path(workspace_root).expanduser().resolve()).replace("\\", "/")
    return [
        f"repo-governance-kernel --repo-root {normalized_root} audit-control-state --project-id {project_id}",
        f"repo-governance-kernel --repo-root {normalized_root} enforce-worktree --project-id {project_id} --workspace-root {normalized_root}",
        (
            f"repo-governance-kernel --repo-root {normalized_root} "
            f"assess-external-target-from-intent --project-id {project_id} "
            f'--request "Assess C:/path/to/external/repo current changes, set scope first, then give me the verdict."'
        ),
    ]


def onboarding_contract(project_id: str, workspace_root: str, *, skip_hooks: bool) -> dict[str, object]:
    normalized_root = str(Path(workspace_root).expanduser().resolve()).replace("\\", "/")
    return {
        "intent_class": "repo-first-host-onboarding",
        "execution_surface": "governed-bundle-backed-workflow",
        "bundle_name": "onboard-repo",
        "project_id": project_id,
        "workspace_root": normalized_root,
        "requires_git_repo": True,
        "requires_empty_project_history": True,
        "hook_installation_requested": not bool(skip_hooks),
        "control_plane_mutation_allowed": True,
        "preexisting_repo_dirty_path_mutation_allowed": False,
        "continuous_monitoring_in_scope": False,
        "general_autonomous_rewrite_in_scope": False,
    }


def assert_onboarding_target_available(project_id: str) -> None:
    objective_records = load_all_objectives(project_id)
    round_records = load_all_rounds(project_id)
    task_records = load_all_task_contracts(project_id)
    if objective_records or round_records or task_records:
        raise SystemExit(
            "onboard-repo only supports one project id with no durable objective, round, or task-contract history; "
            f"found {len(objective_records)} objective(s), {len(round_records)} round(s), and {len(task_records)} task-contract(s)"
        )


def resolve_onboarding_control_state(project_id: str) -> dict[str, str]:
    objective_record, objective_issues = select_active_objective_record(project_id)
    if objective_record is None:
        raise SystemExit("onboard-repo did not leave one durable active objective")
    if objective_issues:
        raise SystemExit("; ".join(objective_issues))
    round_record, round_issues = select_open_round_record(project_id)
    if round_record is None:
        raise SystemExit("onboard-repo did not leave one durable open round")
    if round_issues:
        raise SystemExit("; ".join(round_issues))

    round_id = str(round_record[1].get("id") or "").strip()
    active_tasks = active_task_contract_records(project_id, round_id=round_id)
    if len(active_tasks) != 1:
        rendered = render_task_contract_record_refs(active_tasks)
        raise SystemExit(
            "onboard-repo should leave exactly one active task contract beneath the new round; "
            f"found {len(active_tasks)}: {rendered or 'none'}"
        )

    return {
        "objective_id": str(objective_record[1].get("id") or "").strip(),
        "round_id": round_id,
        "task_contract_id": str(active_tasks[0][1].get("id") or "").strip(),
    }


def render_onboarding_success_payload(
    *,
    project_id: str,
    workspace_root: str,
    skip_hooks: bool,
    bundle_payload: dict[str, object],
    bundle_detail: str,
    onboarding_payload: dict[str, object],
    control_state: dict[str, str],
    audit: dict[str, object],
    enforce: dict[str, object],
) -> dict[str, object]:
    normalized_root = str(Path(workspace_root).expanduser().resolve()).replace("\\", "/")
    return {
        "status": "ok",
        "project_id": project_id,
        "workspace_root": normalized_root,
        "onboarding_contract": onboarding_contract(project_id, normalized_root, skip_hooks=skip_hooks),
        "compiled_onboarding": {
            "governance_scope_paths": onboarding_payload["governance_scope_paths"],
            "observed_repo_dirty_paths": onboarding_payload["observed_repo_dirty_paths"],
            "onboarding_scope_paths": onboarding_payload["onboarding_scope_paths"],
            "bundle_payload": bundle_payload,
            "bundle_detail": bundle_detail,
        },
        "created_control_state": control_state,
        "postconditions": {
            "audit_status": str(audit.get("status") or ""),
            "enforce_status": str(enforce.get("status") or ""),
            "audit": audit,
            "enforce": enforce,
        },
        "next_actions": onboarding_next_commands(project_id, normalized_root),
    }


def render_onboarding_error(
    *,
    code: str,
    message: str,
    project_id: str = "",
    workspace_root: str = "",
    details: dict[str, object] | None = None,
) -> str:
    payload = {
        "status": "blocked",
        "error": {
            "code": code,
            "message": message,
        },
    }
    if project_id.strip():
        payload["project_id"] = project_id.strip()
    if workspace_root.strip():
        payload["workspace_root"] = str(Path(workspace_root).expanduser().resolve()).replace("\\", "/")
    if details:
        payload["error"]["details"] = details
    return json.dumps(payload, ensure_ascii=True, indent=2)
