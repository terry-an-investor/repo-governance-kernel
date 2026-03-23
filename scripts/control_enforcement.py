#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

from assemble_context import inspect_live_workspace
from audit_control_state import audit_project_control_state, parse_changed_paths, path_is_covered, read_if_exists
from round_control import (
    ROOT,
    active_objective_path,
    active_round_path,
    exception_ledger_path,
    load_round_file,
    locate_round_file,
    parse_bullet_list,
    pivot_log_path,
    project_dir,
    render_active_objective_file,
    render_active_round_file,
    render_exception_ledger_file,
    render_pivot_log_file,
    resolve_anchor,
    select_active_objective_record,
    select_open_round_record,
)


def add_issue(
    issues: list[dict[str, object]],
    *,
    severity: str,
    domain: str,
    code: str,
    message: str,
    evidence: list[str] | None = None,
) -> None:
    issues.append(
        {
            "severity": severity,
            "domain": domain,
            "code": code,
            "message": message,
            "evidence": evidence or [],
        }
    )


def normalize_repo_path(value: str | Path) -> str:
    path = value if isinstance(value, Path) else Path(str(value))
    try:
        return path.relative_to(ROOT).as_posix()
    except ValueError:
        return path.as_posix().replace("\\", "/").lstrip("./")


def is_control_plane_path(project_id: str, path: str) -> bool:
    normalized = path.replace("\\", "/").lstrip("./")
    prefix = f"projects/{project_id}/"
    if not normalized.startswith(prefix):
        return False
    suffix = normalized[len(prefix) :]
    return suffix.startswith("control/") or suffix.startswith("memory/")


def expected_projection_texts(project_id: str) -> dict[str, str]:
    expected: dict[str, str] = {}

    objective_record, _objective_issues = select_active_objective_record(project_id)
    objective_path = active_objective_path(project_id)
    if objective_record is None:
        expected[normalize_repo_path(objective_path)] = ""
    else:
        _path, objective_meta, objective_sections = objective_record
        expected[normalize_repo_path(objective_path)] = render_active_objective_file(
            objective_id=str(objective_meta.get("id") or "").strip(),
            phase=str(objective_meta.get("phase") or "").strip(),
            status=str(objective_meta.get("status") or "").strip() or "active",
            problem=str(objective_sections.get("Problem", "")).strip(),
            success_criteria=parse_bullet_list(str(objective_sections.get("Success Criteria", ""))),
            non_goals=parse_bullet_list(str(objective_sections.get("Non-Goals", ""))),
            why_now=str(objective_sections.get("Why Now", "")).strip(),
            current_risks=parse_bullet_list(str(objective_sections.get("Active Risks", ""))),
        ).strip()

    round_record, _round_issues = select_open_round_record(project_id)
    round_path = active_round_path(project_id)
    if round_record is None:
        expected[normalize_repo_path(round_path)] = ""
    else:
        _path, round_meta, round_sections = round_record
        expected[normalize_repo_path(round_path)] = render_active_round_file(
            round_id=str(round_meta.get("id") or "").strip(),
            objective_id=str(round_meta.get("objective_id") or "").strip(),
            status=str(round_meta.get("status") or "").strip(),
            scope_items=parse_bullet_list(str(round_sections.get("Scope", ""))),
            deliverable=str(round_sections.get("Deliverable", "")).strip(),
            validation_plan=str(round_sections.get("Validation Plan", "")).strip(),
            risks=parse_bullet_list(str(round_sections.get("Active Risks", ""))),
            blockers=parse_bullet_list(str(round_sections.get("Blockers", ""))),
        ).strip()

    expected[normalize_repo_path(pivot_log_path(project_id))] = render_pivot_log_file(project_id).strip()
    expected[normalize_repo_path(exception_ledger_path(project_id))] = render_exception_ledger_file(project_id).strip()
    return expected


def resolve_scope_record(
    project_id: str,
    *,
    round_id: str = "",
) -> tuple[tuple[Path, dict[str, object], dict[str, str]] | None, list[str], str]:
    requested_round_id = round_id.strip()
    if requested_round_id:
        round_path = locate_round_file(project_id, requested_round_id)
        if round_path is None:
            return None, [f"scope round `{requested_round_id}` was not found"], requested_round_id
        round_meta, round_sections = load_round_file(round_path)
        return (round_path, round_meta, round_sections), [], requested_round_id

    open_round_record, round_issues = select_open_round_record(project_id)
    resolved_round_id = ""
    if open_round_record is not None:
        resolved_round_id = str(open_round_record[1].get("id") or "").strip()
    return open_round_record, round_issues, resolved_round_id


def evaluate_worktree_enforcement(project_id: str, *, round_id: str = "") -> dict[str, object]:
    project_path = project_dir(project_id)
    if not project_path.exists():
        raise SystemExit(f"project directory not found: {project_path}")

    issues: list[dict[str, object]] = []
    checks: list[str] = []
    live_workspace = inspect_live_workspace(resolve_anchor(project_id))
    changed_paths: list[str] = []

    if live_workspace.get("status") != "available":
        add_issue(
            issues,
            severity="error",
            domain="enforcement",
            code="workspace_unavailable_for_enforcement",
            message="automatic worktree enforcement requires a live accessible workspace",
            evidence=[str(live_workspace.get("workspace_root") or ""), str(live_workspace.get("error") or "")],
        )
    else:
        changed_paths = parse_changed_paths(str(live_workspace.get("status_short") or ""))
    checks.append("live workspace inspection for enforcement")

    scope_record, round_issues, scope_round_id = resolve_scope_record(project_id, round_id=round_id)
    for issue in round_issues:
        add_issue(
            issues,
            severity="error",
            domain="round-control",
            code="durable_round_ambiguity",
            message=issue,
        )

    non_control_dirty_paths = [path for path in changed_paths if not is_control_plane_path(project_id, path)]
    if non_control_dirty_paths and scope_record is None:
        add_issue(
            issues,
            severity="error",
            domain="enforcement",
            code="dirty_worktree_without_scope_round",
            message="the live workspace has dirty non-control paths but no active or explicitly requested round exists to authorize them",
            evidence=non_control_dirty_paths,
        )
    elif scope_record is not None:
        _round_path, round_meta, _round_sections = scope_record
        round_scope_paths = [str(item).strip() for item in round_meta.get("paths", []) if str(item).strip()]
        uncovered_paths = [path for path in non_control_dirty_paths if not path_is_covered(path, round_scope_paths)]
        if uncovered_paths:
            add_issue(
                issues,
                severity="error",
                domain="enforcement",
                code="dirty_paths_outside_scope_round",
                message="the live workspace contains dirty non-control paths that are outside the scope of the active or requested round",
                evidence=uncovered_paths,
            )
    checks.append("scope-round coverage for dirty non-control paths")

    projection_drift_paths: list[str] = []
    for relative_path, expected_text in expected_projection_texts(project_id).items():
        if relative_path not in changed_paths:
            continue
        actual_text = read_if_exists(ROOT / relative_path).strip()
        if actual_text != expected_text:
            projection_drift_paths.append(relative_path)
    if projection_drift_paths:
        add_issue(
            issues,
            severity="error",
            domain="enforcement",
            code="dirty_projection_files_drift_from_durable_truth",
            message="dirty projected control files were edited away from the projection implied by durable truth",
            evidence=projection_drift_paths,
        )
    checks.append("dirty projected control files remain aligned to durable truth")

    audit_result = audit_project_control_state(project_id)
    if int(audit_result["summary"]["errors"]):
        add_issue(
            issues,
            severity="error",
            domain="enforcement",
            code="control_audit_blocked",
            message="control audit is already blocked, so round promotion or closure would ratify dishonest state",
            evidence=[str(issue.get("code") or "").strip() for issue in audit_result["issues"] if str(issue.get("code") or "").strip()],
        )
    checks.append("control audit remains unblocked")

    error_count = sum(1 for issue in issues if issue["severity"] == "error")
    warning_count = sum(1 for issue in issues if issue["severity"] == "warning")
    status = "blocked" if error_count else "warn" if warning_count else "ok"
    return {
        "project_id": project_id,
        "status": status,
        "summary": {
            "errors": error_count,
            "warnings": warning_count,
            "checks": checks,
            "changed_paths": changed_paths,
            "scope_round_id": scope_round_id,
        },
        "issues": issues,
        "live_workspace": live_workspace,
    }


def assert_worktree_enforcement(project_id: str, *, transition_target: str = "", round_id: str = "") -> dict[str, object]:
    result = evaluate_worktree_enforcement(project_id, round_id=round_id)
    if result["status"] == "blocked":
        transition_note = f" before `{transition_target}`" if transition_target.strip() else ""
        raise SystemExit(
            f"automatic worktree enforcement blocked this transition{transition_note}:\n"
            + json.dumps(result, ensure_ascii=True, indent=2)
        )
    return result
