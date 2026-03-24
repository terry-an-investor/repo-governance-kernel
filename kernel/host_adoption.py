#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

from kernel.assemble_context import inspect_live_workspace
from kernel.audit_control_state import parse_changed_paths, relativize_changed_paths
from kernel.round_control import current_task_path


def classify_host_adoption_blockers(project_id: str, blocked_paths: list[str]) -> dict[str, object]:
    normalized_paths: list[str] = []
    for path in blocked_paths:
        rendered = str(path).replace("\\", "/").strip()
        if not rendered:
            continue
        while rendered.startswith("./"):
            rendered = rendered[2:]
        normalized_paths.append(rendered)
    bootstrap_control_prefix = f"projects/{project_id}/"

    bucket_order = (
        "hook_installation_paths",
        "host_governance_paths",
        "host_support_paths",
        "repo_scope_paths",
    )
    buckets: dict[str, list[str]] = {key: [] for key in bucket_order}

    for path in normalized_paths:
        if path in {".githooks/pre-commit", ".githooks/pre-push", "githooks/pre-commit", "githooks/pre-push"}:
            buckets["hook_installation_paths"].append(path)
            continue
        if path.startswith(bootstrap_control_prefix):
            buckets["host_governance_paths"].append(path)
            continue
        if (
            path.startswith(".claude/")
            or path.startswith("claude/")
            or path.startswith("cross-project/")
            or path.startswith("index/")
        ):
            buckets["host_support_paths"].append(path)
            continue
        buckets["repo_scope_paths"].append(path)

    meanings = {
        "hook_installation_paths": "repo-local hook installation side effects created by kernel bootstrap or hook refresh",
        "host_governance_paths": "host-governance projected or support files created under the adopted project namespace",
        "host_support_paths": "host-side support surfaces not yet covered by the adopted round/task boundary",
        "repo_scope_paths": "real source-repo dirty paths that remain outside the adopted round/task boundary",
    }

    return {
        "counts": {key: len(value) for key, value in buckets.items()},
        "buckets": buckets,
        "meanings": meanings,
        "has_repo_scope_gap": bool(buckets["repo_scope_paths"]),
    }


def adoption_report_path(project_id: str) -> Path:
    return current_task_path(project_id).parent / "shadow-adoption-report.md"


def adoption_scope_draft_path(project_id: str) -> Path:
    return current_task_path(project_id).parent / "external-target-shadow-scope-draft.md"


def _resolve_path(value: str | Path) -> Path:
    return Path(value).expanduser().resolve()


def _path_within(candidate: Path, parent: Path) -> bool:
    try:
        candidate.relative_to(parent)
        return True
    except ValueError:
        return False


def assessment_contract(
    *,
    governance_root: str,
    governance_project_root: str,
    workspace_root: str,
    report_path: str,
    requested_mode: str = "auto",
) -> dict[str, object]:
    governance_root_path = _resolve_path(governance_root)
    governance_project_root_path = _resolve_path(governance_project_root)
    workspace_root_path = _resolve_path(workspace_root)
    report_path_obj = _resolve_path(report_path)

    workspace_binding = (
        "governed-host-workspace"
        if _path_within(workspace_root_path, governance_root_path)
        else "external-target-workspace"
    )
    resolved_mode = "governed-host-shadow" if workspace_binding == "governed-host-workspace" else "external-target-shadow"
    normalized_requested_mode = requested_mode.strip() or "auto"
    if normalized_requested_mode != "auto" and normalized_requested_mode != resolved_mode:
        raise SystemExit(
            f"requested assessment mode `{normalized_requested_mode}` does not match the resolved workspace binding `{resolved_mode}`"
        )

    report_delivery = (
        "governance-repo-artifact"
        if _path_within(report_path_obj, governance_root_path)
        else "explicit-output-artifact"
    )
    report_location = "governed-project-current" if _path_within(report_path_obj, governance_project_root_path) else "external-output-path"

    if resolved_mode == "governed-host-shadow":
        mode_meaning = (
            "control state and live workspace inspection both run against the governed host repository rooted at the governance repo"
        )
    else:
        mode_meaning = (
            "control state stays in the governance repo while live workspace inspection targets one external workspace in shadow mode"
        )
    scope_path_basis = "workspace-root-relative"
    if resolved_mode == "governed-host-shadow":
        scope_path_basis_meaning = (
            "active round and task-contract paths are matched against dirty paths relative to the governed host workspace root"
        )
    else:
        scope_path_basis_meaning = (
            "active round and task-contract paths stay in governance control state, but assessment matches them against dirty paths relative to the external target workspace root"
        )

    return {
        "mode": resolved_mode,
        "workspace_binding": workspace_binding,
        "mode_meaning": mode_meaning,
        "governance_root": str(governance_root_path),
        "governance_project_root": str(governance_project_root_path),
        "workspace_root": str(workspace_root_path),
        "report_delivery": report_delivery,
        "report_location": report_location,
        "writes_into_governance_repo": report_delivery == "governance-repo-artifact",
        "writes_into_governed_project_current": report_location == "governed-project-current",
        "target_repo_mutation_allowed": False,
        "continuous_monitoring_in_scope": False,
        "requires_governed_control_state": True,
        "scope_path_basis": scope_path_basis,
        "scope_path_basis_meaning": scope_path_basis_meaning,
        "dirty_path_reference_root": str(workspace_root_path),
        "default_report_write_behavior": "always-write-resolved-report-path",
    }


def draft_contract(
    *,
    governance_root: str,
    governance_project_root: str,
    workspace_root: str,
    draft_path: str,
    requested_mode: str = "external-target-shadow",
) -> dict[str, object]:
    governance_root_path = _resolve_path(governance_root)
    governance_project_root_path = _resolve_path(governance_project_root)
    workspace_root_path = _resolve_path(workspace_root)
    draft_path_obj = _resolve_path(draft_path)

    workspace_binding = (
        "governed-host-workspace"
        if _path_within(workspace_root_path, governance_root_path)
        else "external-target-workspace"
    )
    resolved_mode = "governed-host-shadow" if workspace_binding == "governed-host-workspace" else "external-target-shadow"
    normalized_requested_mode = requested_mode.strip() or "external-target-shadow"
    if normalized_requested_mode != resolved_mode:
        raise SystemExit(
            f"requested draft mode `{normalized_requested_mode}` does not match the resolved workspace binding `{resolved_mode}`"
        )

    draft_delivery = (
        "governance-repo-artifact"
        if _path_within(draft_path_obj, governance_root_path)
        else "explicit-output-artifact"
    )
    draft_location = "governed-project-current" if _path_within(draft_path_obj, governance_project_root_path) else "external-output-path"

    return {
        "mode": resolved_mode,
        "workspace_binding": workspace_binding,
        "mode_meaning": "control state stays in the governance repo while live workspace inspection targets one external workspace in shadow mode",
        "draft_delivery": draft_delivery,
        "draft_location": draft_location,
        "governance_root": str(governance_root_path),
        "governance_project_root": str(governance_project_root_path),
        "workspace_root": str(workspace_root_path),
        "target_repo_mutation_allowed": False,
        "continuous_monitoring_in_scope": False,
        "requires_governed_control_state": True,
        "scope_path_basis": "workspace-root-relative",
        "scope_path_basis_meaning": (
            "the suggested round and task-contract paths are expressed against dirty paths relative to the external target workspace root"
        ),
        "dirty_path_reference_root": str(workspace_root_path),
        "draft_purpose": "author the smallest honest round/task boundary before running assess-host-adoption",
        "default_draft_write_behavior": "always-write-resolved-draft-path",
    }


def inspect_workspace_changed_paths(workspace_root: str) -> tuple[dict[str, str], list[str]]:
    live_workspace = inspect_live_workspace({"workspace_root": workspace_root})
    if live_workspace.get("status") != "available":
        details = str(live_workspace.get("error") or live_workspace.get("status") or "workspace unavailable").strip()
        raise SystemExit(f"host adoption drafting requires one live accessible workspace: {details}")
    changed_paths = relativize_changed_paths(
        parse_changed_paths(str(live_workspace.get("status_short") or "")),
        workspace_root=str(live_workspace.get("workspace_root") or ""),
    )
    unique_paths: list[str] = []
    for path in changed_paths:
        normalized = str(path).replace("\\", "/").strip().lstrip("./")
        if normalized and normalized not in unique_paths:
            unique_paths.append(normalized)
    return live_workspace, unique_paths


def suggest_scope_paths_from_dirty_paths(dirty_paths: list[str]) -> list[str]:
    return [str(path).replace("\\", "/").strip().lstrip("./") for path in dirty_paths if str(path).strip()]


def render_external_target_shadow_scope_draft(
    *,
    project_id: str,
    source_repo: str,
    workspace_root: str,
    objective_id: str,
    suggested_round_title: str,
    suggested_round_scope_items: list[str],
    suggested_round_scope_paths: list[str],
    suggested_round_deliverable: str,
    suggested_round_validation_plan: str,
    suggested_task_title: str,
    suggested_task_intent: str,
    suggested_task_paths: list[str],
    draft_contract_payload: dict[str, object],
    live_workspace: dict[str, str],
    dirty_paths: list[str],
    command_sequence: list[str],
    current_control_state_lines: list[str],
) -> str:
    repo_name = Path(workspace_root).name or workspace_root
    lines = [
        "# External Target Shadow Scope Draft",
        "",
        f"- Project id: `{project_id}`",
        f"- Objective id: `{objective_id}`",
        f"- Source repo: `{source_repo}`",
        f"- External workspace root: `{workspace_root}`",
        f"- Repo label: `{repo_name}`",
        f"- Draft mode: `{draft_contract_payload['mode']}`",
        f"- Scope path basis: `{draft_contract_payload['scope_path_basis']}`",
        f"- Dirty path count: `{len(dirty_paths)}`",
        "",
        "## Meaning",
        "",
        f"- {draft_contract_payload['mode_meaning']}",
        f"- {draft_contract_payload['scope_path_basis_meaning']}",
        "- This draft narrows authoring ambiguity before the real assessment command runs.",
        "- This draft does not mutate the external target repo and does not open or rewrite control objects automatically.",
        "",
        "## Current Control State",
        "",
    ]
    lines.extend(f"- {line}" for line in current_control_state_lines)
    lines.extend(
        [
            "",
            "## Observed Dirty Paths",
            "",
        ]
    )
    if dirty_paths:
        lines.extend(f"- `{path}`" for path in dirty_paths)
    else:
        lines.append("- none")
    lines.extend(
        [
            "",
            "## Suggested Round Authoring",
            "",
            f"- Title: `{suggested_round_title}`",
            f"- Deliverable: {suggested_round_deliverable}",
            f"- Validation plan: {suggested_round_validation_plan}",
            "",
            "### Scope Items",
            "",
        ]
    )
    lines.extend(f"- {item}" for item in suggested_round_scope_items)
    lines.extend(
        [
            "",
            "### Scope Paths",
            "",
        ]
    )
    lines.extend(f"- `{path}`" for path in suggested_round_scope_paths)
    lines.extend(
        [
            "",
            "## Suggested Task-Contract Authoring",
            "",
            f"- Title: `{suggested_task_title}`",
            f"- Intent: {suggested_task_intent}",
            "",
            "### Task Paths",
            "",
        ]
    )
    lines.extend(f"- `{path}`" for path in suggested_task_paths)
    lines.extend(
        [
            "",
            "## Suggested Command Sequence",
            "",
        ]
    )
    lines.extend(f"- `{command}`" for command in command_sequence)
    lines.extend(
        [
            "",
            "## Live Workspace Snapshot",
            "",
            f"- Branch: `{live_workspace.get('branch', '')}`",
            f"- HEAD: `{live_workspace.get('git_sha', '')}`",
            f"- Worktree state: `{live_workspace.get('worktree_state', '')}`",
            f"- Changed path count: `{live_workspace.get('changed_path_count', '')}`",
            "",
        ]
    )
    return "\n".join(lines)


def collect_remaining_blocked_paths(enforcement_result: dict[str, object]) -> list[str]:
    remaining_blocked_paths: list[str] = []
    for issue in enforcement_result.get("issues", []):
        if str(issue.get("code") or "").strip() not in {
            "dirty_paths_outside_scope_round",
            "dirty_paths_outside_active_task_contracts",
        }:
            continue
        for path in issue.get("evidence", []):
            normalized = str(path).replace("\\", "/").strip()
            while normalized.startswith("./"):
                normalized = normalized[2:]
            if normalized and normalized not in remaining_blocked_paths:
                remaining_blocked_paths.append(normalized)
    return remaining_blocked_paths


def make_shadow_adoption_report(
    *,
    project_id: str,
    source_repo: str,
    workspace_root: str,
    objective_id: str,
    round_id: str,
    task_contract_id: str,
    assessment_contract_payload: dict[str, object],
    round_scope_paths: list[str],
    task_contract_paths: list[str],
    initial_audit_status: str = "",
    initial_enforce: dict[str, object] | None = None,
    final_audit_status: str = "",
    final_enforce: dict[str, object],
    report_title: str,
    meaning_lines: list[str],
    next_step_lines: list[str],
) -> tuple[str, dict[str, object], list[str]]:
    remaining_blocked_paths = collect_remaining_blocked_paths(final_enforce)
    blocker_classification = classify_host_adoption_blockers(project_id, remaining_blocked_paths)

    report_lines = [
        f"# {report_title}",
        "",
        f"- Source repo: `{source_repo}`",
        f"- Workspace root: `{workspace_root}`",
        f"- Project id: `{project_id}`",
        f"- Objective id: `{objective_id}`",
        f"- Round id: `{round_id}`",
        f"- Task contract id: `{task_contract_id}`",
        f"- Assessment mode: `{assessment_contract_payload['mode']}`",
        f"- Scope path basis: `{assessment_contract_payload['scope_path_basis']}`",
    ]
    if initial_audit_status:
        report_lines.append(f"- Initial audit: `{initial_audit_status}`")
    if initial_enforce is not None:
        report_lines.append(f"- Initial enforcement: `{initial_enforce.get('status', '')}`")
    if final_audit_status:
        report_lines.append(f"- Final audit: `{final_audit_status}`")
    report_lines.append(f"- Final enforcement: `{final_enforce.get('status', '')}`")
    report_lines.extend(
        [
            "",
            "## Scope Interpretation",
            "",
            f"- {assessment_contract_payload['mode_meaning']}",
            f"- {assessment_contract_payload['scope_path_basis_meaning']}",
            f"- Dirty path reference root: `{assessment_contract_payload['dirty_path_reference_root']}`",
            "",
            "### Active Round Paths",
            "",
        ]
    )
    if round_scope_paths:
        report_lines.extend(f"- `{path}`" for path in round_scope_paths)
    else:
        report_lines.append("- none")
    report_lines.extend(
        [
            "",
            "### Active Task-Contract Paths",
            "",
        ]
    )
    if task_contract_paths:
        report_lines.extend(f"- `{path}`" for path in task_contract_paths)
    else:
        report_lines.append("- none")
    report_lines.extend(
        [
            "",
            "## Current Meaning",
            "",
        ]
    )
    report_lines.extend(f"- {line}" for line in meaning_lines)
    report_lines.extend(
        [
            "",
            "## Enforcement Issues",
            "",
        ]
    )
    final_issues = final_enforce.get("issues", [])
    if final_issues:
        for issue in final_issues:
            report_lines.append(f"- `{issue.get('code', '')}`: {issue.get('message', '')}")
    else:
        report_lines.append("- No remaining enforcement blockers on the host.")
    report_lines.extend(
        [
            "",
            "## Blocker Classification",
            "",
            f"- Hook installation paths: `{blocker_classification['counts']['hook_installation_paths']}`",
            f"- Host governance paths: `{blocker_classification['counts']['host_governance_paths']}`",
            f"- Host support paths: `{blocker_classification['counts']['host_support_paths']}`",
            f"- Repo scope paths: `{blocker_classification['counts']['repo_scope_paths']}`",
            "",
            "These buckets separate bootstrap/control-plane noise from real source-repo scope gaps.",
            "",
        ]
    )
    for bucket in (
        "hook_installation_paths",
        "host_governance_paths",
        "host_support_paths",
        "repo_scope_paths",
    ):
        report_lines.append(f"### `{bucket}`")
        report_lines.append("")
        report_lines.append(f"- Meaning: {blocker_classification['meanings'][bucket]}")
        bucket_paths = blocker_classification["buckets"][bucket]
        if bucket_paths:
            for path in bucket_paths:
                report_lines.append(f"- `{path}`")
        else:
            report_lines.append("- none")
        report_lines.append("")
    report_lines.extend(
        [
            "## Next Steps",
            "",
        ]
    )
    report_lines.extend(f"- {line}" for line in next_step_lines)
    report_lines.append("")
    return "\n".join(report_lines), blocker_classification, remaining_blocked_paths


def assessment_payload(
    *,
    project_id: str,
    governance_root: str,
    governance_project_root: str,
    objective_id: str,
    round_id: str,
    task_contract_id: str,
    source_repo: str,
    workspace_root: str,
    report_path: str,
    assessment_contract_payload: dict[str, object],
    final_audit: dict[str, object],
    final_enforce: dict[str, object],
    blocker_classification: dict[str, object],
    remaining_blocked_paths: list[str],
) -> dict[str, object]:
    return {
        "project_id": project_id,
        "governance_root": governance_root,
        "governance_project_root": governance_project_root,
        "objective_id": objective_id,
        "round_id": round_id,
        "task_contract_id": task_contract_id,
        "source_repo": source_repo,
        "workspace_root": workspace_root,
        "report_path": report_path,
        "assessment_contract": assessment_contract_payload,
        "final_audit": final_audit,
        "final_enforce": final_enforce,
        "remaining_blocked_paths": remaining_blocked_paths,
        "blocker_classification": blocker_classification,
    }


def to_json(payload: dict[str, object]) -> str:
    return json.dumps(payload, ensure_ascii=True, indent=2)
