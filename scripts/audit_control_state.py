#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

from assemble_context import clean_section_text, inspect_live_workspace, parse_h2_sections
from round_control import (
    ROOT,
    active_exception_contract_records,
    active_objective_path,
    active_round_path,
    exception_ledger_path,
    load_all_rounds,
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
from transition_specs import adjudication_plan_types, transition_command_names


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Audit whether project control state is honest and aligned.")
    parser.add_argument("--project-id", required=True)
    parser.add_argument("--strict-warnings", action="store_true")
    return parser.parse_args()


def read_if_exists(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8").replace("\r\n", "\n").strip()


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


def is_placeholder_text(text: str) -> bool:
    normalized = " ".join(text.strip().lower().split())
    return normalized in {
        "",
        "_none recorded_",
        "_pending authoring_",
        "pending authoring",
        "none recorded yet.",
        "- none recorded yet.",
    }


def constitution_has_substance(path: Path) -> bool:
    if not path.exists():
        return False
    sections = parse_h2_sections(clean_section_text(path, strip_heading=True, strip_yaml=False))
    for name in [
        "Product Boundaries",
        "Architecture Invariants",
        "Quality Bar",
        "Validation Rules",
        "Forbidden Shortcuts",
    ]:
        if not is_placeholder_text(sections.get(name, "")):
            return True
    return False


def normalize_hook_name(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "_", value.strip().lower()).strip("_")


def load_constitution_sections(path: Path) -> dict[str, str]:
    if not path.exists():
        return {}
    return parse_h2_sections(clean_section_text(path, strip_heading=True, strip_yaml=False))


def constitution_audit_hooks(path: Path) -> set[str]:
    sections = load_constitution_sections(path)
    return {
        normalize_hook_name(item)
        for item in parse_bullet_list(sections.get("Audit Hooks", ""))
        if normalize_hook_name(item)
    }


def constitution_guarded_exception_paths(path: Path) -> list[str]:
    sections = load_constitution_sections(path)
    return [item.strip() for item in parse_bullet_list(sections.get("Guarded Exception Paths", "")) if item.strip()]


def parse_changed_paths(status_short: str) -> list[str]:
    changed_paths: list[str] = []
    for raw_line in status_short.splitlines():
        line = raw_line.rstrip()
        if not line or line.startswith("## "):
            continue
        if len(line) < 4:
            continue
        path_part = line[3:].strip()
        if " -> " in path_part:
            path_part = path_part.split(" -> ", 1)[1].strip()
        normalized = path_part.replace("\\", "/").lstrip("./")
        if normalized:
            changed_paths.append(normalized)
    return changed_paths


def documented_transition_command_names(path: Path) -> set[str]:
    if not path.exists():
        return set()
    text = path.read_text(encoding="utf-8")
    return {
        match.group(1).strip()
        for match in re.finditer(r"^### `([^`]+)`\s*$", text, flags=re.MULTILINE)
        if match.group(1).strip() not in {"audit-control-state", "enforce-worktree", "adjudicate-control-state", "execute-adjudication-followups"}
    }


def documented_plan_family_names(path: Path) -> set[str]:
    if not path.exists():
        return set()
    text = path.read_text(encoding="utf-8")
    capture = False
    plan_names: set[str] = set()
    for raw_line in text.splitlines():
        line = raw_line.rstrip()
        if "current supported plan-contract families include:" in line:
            capture = True
            continue
        if capture and not line.strip():
            break
        if capture:
            match = re.match(r"^\s*-\s+`([^`]+)`\s*$", line)
            if match:
                plan_names.add(match.group(1).strip())
                continue
            if line.startswith("- ") and "`" not in line:
                break
    return plan_names


def relativize_changed_paths(
    changed_paths: list[str],
    *,
    workspace_root: str,
) -> list[str]:
    if not workspace_root.strip():
        return changed_paths
    try:
        workspace_path = Path(workspace_root).resolve()
    except OSError:
        return changed_paths
    try:
        relative_workspace = workspace_path.relative_to(ROOT.resolve()).as_posix().rstrip("/")
    except ValueError:
        return changed_paths
    if not relative_workspace:
        return changed_paths
    relativized: list[str] = []
    for path in changed_paths:
        normalized = path.replace("\\", "/").lstrip("./")
        if normalized == relative_workspace or normalized.startswith(relative_workspace + "/"):
            trimmed = normalized[len(relative_workspace) :].lstrip("/")
            if trimmed:
                relativized.append(trimmed)
            continue
        relativized.append(normalized)
    return relativized


def path_is_covered(path: str, scope_paths: list[str]) -> bool:
    normalized_path = path.replace("\\", "/").strip().lstrip("./")
    for raw_scope in scope_paths:
        scope = raw_scope.replace("\\", "/").strip().lstrip("./").rstrip("/")
        if not scope:
            continue
        if normalized_path == scope or normalized_path.startswith(scope + "/"):
            return True
    return False


def current_task_contains(path: Path, needle: str) -> bool:
    if not needle.strip() or not path.exists():
        return False
    text = path.read_text(encoding="utf-8").replace("\r\n", "\n")
    return needle.strip() in text


def run_hook_round_paths_cover_live_dirty_paths(
    *,
    issues: list[dict[str, object]],
    checks: list[str],
    project_id: str,
    open_round_record: tuple[Path, dict[str, object], dict[str, str]] | None,
    **_: object,
) -> None:
    if open_round_record is None:
        return
    _round_path, round_meta, _round_sections = open_round_record
    round_scope_paths = [str(item).strip() for item in round_meta.get("paths", []) if str(item).strip()]
    live_workspace = inspect_live_workspace(resolve_anchor(project_id))
    if live_workspace.get("status") == "available":
        changed_paths = relativize_changed_paths(
            parse_changed_paths(str(live_workspace.get("status_short") or "")),
            workspace_root=str(live_workspace.get("workspace_root") or ""),
        )
        uncovered_paths = [path for path in changed_paths if not path_is_covered(path, round_scope_paths)]
        if uncovered_paths:
            add_issue(
                issues,
                severity="warning",
                domain="constitution",
                code="round_scope_excludes_live_dirty_paths",
                message="the active round paths do not cover every live dirty path required by constitution audit hooks",
                evidence=uncovered_paths,
            )
    checks.append("constitution-derived live round scope coverage")


def run_hook_current_task_mentions_active_objective(
    *,
    issues: list[dict[str, object]],
    checks: list[str],
    current_task_path: Path,
    active_objective_record: tuple[Path, dict[str, object], dict[str, str]] | None,
    **_: object,
) -> None:
    if active_objective_record is None:
        return
    _objective_path, objective_meta, _objective_sections = active_objective_record
    active_objective_id = str(objective_meta.get("id") or "").strip()
    if active_objective_id and not current_task_contains(current_task_path, active_objective_id):
        add_issue(
            issues,
            severity="warning",
            domain="current-task",
            code="current_task_missing_active_objective",
            message="current/current-task.md does not mention the durable active objective id, so orientation can anchor on stale project direction",
            evidence=[str(current_task_path), active_objective_id],
        )
    checks.append("current-task active objective anchor")


def run_hook_current_task_mentions_active_round(
    *,
    issues: list[dict[str, object]],
    checks: list[str],
    current_task_path: Path,
    open_round_record: tuple[Path, dict[str, object], dict[str, str]] | None,
    **_: object,
) -> None:
    if open_round_record is None:
        return
    _round_path, round_meta, _round_sections = open_round_record
    round_id = str(round_meta.get("id") or "").strip()
    if round_id and not current_task_contains(current_task_path, round_id):
        add_issue(
            issues,
            severity="warning",
            domain="current-task",
            code="current_task_missing_active_round",
            message="current/current-task.md does not mention the durable active round id, so orientation can anchor on stale execution control",
            evidence=[str(current_task_path), round_id],
        )
    checks.append("current-task active round anchor")


def run_hook_guarded_exception_paths_require_active_contract(
    *,
    issues: list[dict[str, object]],
    checks: list[str],
    project_id: str,
    constitution_path: Path,
    active_objective_record: tuple[Path, dict[str, object], dict[str, str]] | None,
    **_: object,
) -> None:
    guarded_paths = constitution_guarded_exception_paths(constitution_path)
    if not guarded_paths:
        return

    live_workspace = inspect_live_workspace(resolve_anchor(project_id))
    if live_workspace.get("status") != "available":
        checks.append("guarded exception paths require active contract coverage")
        return

    changed_paths = parse_changed_paths(str(live_workspace.get("status_short") or ""))
    changed_paths = relativize_changed_paths(
        changed_paths,
        workspace_root=str(live_workspace.get("workspace_root") or ""),
    )
    matching_dirty_paths = [path for path in changed_paths if path_is_covered(path, guarded_paths)]
    if not matching_dirty_paths:
        checks.append("guarded exception paths require active contract coverage")
        return

    objective_id = ""
    if active_objective_record is not None:
        objective_id = str(active_objective_record[1].get("id") or "").strip()

    active_contracts = active_exception_contract_records(project_id, objective_id=objective_id)
    covered_paths: set[str] = set()
    for _contract_path, contract_meta, _contract_sections in active_contracts:
        contract_paths = [str(item).strip() for item in contract_meta.get("paths", []) if str(item).strip()]
        owner_scope_paths = [
            item.strip()
            for item in parse_bullet_list(_contract_sections.get("Owner Scope", ""))
            if item.strip()
        ]
        for dirty_path in matching_dirty_paths:
            if any(path_is_covered(dirty_path, [scope]) for scope in [*contract_paths, *owner_scope_paths]):
                covered_paths.add(dirty_path)

    uncovered_paths = [path for path in matching_dirty_paths if path not in covered_paths]
    if uncovered_paths:
        add_issue(
            issues,
            severity="warning",
            domain="exception-contract",
            code="guarded_exception_paths_without_active_contract",
            message="dirty guarded-exception paths exist without one active exception contract that explicitly covers them",
            evidence=uncovered_paths,
        )
    checks.append("guarded exception paths require active contract coverage")


HOOK_RUNNERS = {
    "round_paths_cover_live_dirty_paths": run_hook_round_paths_cover_live_dirty_paths,
    "current_task_mentions_active_objective": run_hook_current_task_mentions_active_objective,
    "current_task_mentions_active_round": run_hook_current_task_mentions_active_round,
    "guarded_exception_paths_require_active_contract": run_hook_guarded_exception_paths_require_active_contract,
}


def audit_project_control_state(project_id: str) -> dict[str, object]:
    project_path = project_dir(project_id)
    if not project_path.exists():
        raise SystemExit(f"project directory not found: {project_path}")

    issues: list[dict[str, object]] = []
    checks: list[str] = []
    current_task_path = project_path / "current" / "current-task.md"

    active_objective_record, objective_issues = select_active_objective_record(project_id)
    for issue in objective_issues:
        add_issue(
            issues,
            severity="error",
            domain="objective-line",
            code="durable_objective_ambiguity",
            message=issue,
        )
    checks.append("durable objective-line selection")

    open_round_record, round_issues = select_open_round_record(project_id)
    for issue in round_issues:
        add_issue(
            issues,
            severity="error",
            domain="round-control",
            code="durable_round_ambiguity",
            message=issue,
        )
    checks.append("durable round selection")

    objective_control_path = active_objective_path(project_id)
    if active_objective_record is None:
        if objective_control_path.exists():
            add_issue(
                issues,
                severity="error",
                domain="projection",
                code="stale_active_objective_projection",
                message="control/active-objective.md exists, but no unambiguous durable active objective can justify it",
                evidence=[str(objective_control_path)],
            )
    else:
        _objective_path, objective_meta, objective_sections = active_objective_record
        active_objective_id = str(objective_meta.get("id") or "").strip()
        expected_active_objective = render_active_objective_file(
            objective_id=active_objective_id,
            phase=str(objective_meta.get("phase") or "").strip(),
            status=str(objective_meta.get("status") or "").strip() or "active",
            problem=str(objective_sections.get("Problem", "")).strip(),
            success_criteria=parse_bullet_list(str(objective_sections.get("Success Criteria", ""))),
            non_goals=parse_bullet_list(str(objective_sections.get("Non-Goals", ""))),
            why_now=str(objective_sections.get("Why Now", "")).strip(),
            current_risks=parse_bullet_list(str(objective_sections.get("Active Risks", ""))),
        ).strip()
        actual_active_objective = read_if_exists(objective_control_path)
        if not actual_active_objective:
            add_issue(
                issues,
                severity="error",
                domain="projection",
                code="missing_active_objective_projection",
                message="control/active-objective.md is missing even though a durable active objective exists",
                evidence=[str(objective_control_path), active_objective_id],
            )
        elif actual_active_objective != expected_active_objective:
            add_issue(
                issues,
                severity="error",
                domain="projection",
                code="active_objective_projection_drift",
                message="control/active-objective.md does not match the projection implied by durable objective truth",
                evidence=[str(objective_control_path), active_objective_id],
            )

        if str(objective_meta.get("phase") or "").strip() == "execution" and open_round_record is None:
            add_issue(
                issues,
                severity="warning",
                domain="round-control",
                code="execution_without_open_round",
                message="the active objective is in execution phase, but no durable open round is present",
                evidence=[active_objective_id],
            )
    checks.append("active objective projection and execution/round alignment")

    round_control_path = active_round_path(project_id)
    if open_round_record is None:
        if load_all_rounds(project_id) and round_control_path.exists():
            add_issue(
                issues,
                severity="error",
                domain="projection",
                code="stale_active_round_projection",
                message="control/active-round.md exists, but no durable open round can justify it",
                evidence=[str(round_control_path)],
            )
    else:
        _round_path, round_meta, round_sections = open_round_record
        round_id = str(round_meta.get("id") or "").strip()
        round_objective_id = str(round_meta.get("objective_id") or "").strip()
        if active_objective_record is None:
            add_issue(
                issues,
                severity="error",
                domain="round-control",
                code="open_round_without_active_objective",
                message="a durable open round exists but there is no unambiguous durable active objective",
                evidence=[round_id],
            )
        elif round_objective_id != str(active_objective_record[1].get("id") or "").strip():
            add_issue(
                issues,
                severity="error",
                domain="round-control",
                code="round_objective_mismatch",
                message="the durable open round is attached to a different objective than the durable active objective",
                evidence=[round_id, round_objective_id, str(active_objective_record[1].get("id") or "").strip()],
            )

        expected_active_round = render_active_round_file(
            round_id=round_id,
            objective_id=round_objective_id,
            status=str(round_meta.get("status") or "").strip(),
            scope_items=parse_bullet_list(str(round_sections.get("Scope", ""))),
            deliverable=str(round_sections.get("Deliverable", "")).strip(),
            validation_plan=str(round_sections.get("Validation Plan", "")).strip(),
            risks=parse_bullet_list(str(round_sections.get("Active Risks", ""))),
            blockers=parse_bullet_list(str(round_sections.get("Blockers", ""))),
        ).strip()
        actual_active_round = read_if_exists(round_control_path)
        if not actual_active_round:
            add_issue(
                issues,
                severity="error",
                domain="projection",
                code="missing_active_round_projection",
                message="control/active-round.md is missing even though a durable open round exists",
                evidence=[str(round_control_path), round_id],
            )
        elif actual_active_round != expected_active_round:
            add_issue(
                issues,
                severity="error",
                domain="projection",
                code="active_round_projection_drift",
                message="control/active-round.md does not match the projection implied by the durable open round",
                evidence=[str(round_control_path), round_id],
            )

        round_status = str(round_meta.get("status") or "").strip()
        round_blockers = parse_bullet_list(str(round_sections.get("Blockers", "")))
        if round_status == "blocked" and not round_blockers:
            add_issue(
                issues,
                severity="error",
                domain="round-control",
                code="blocked_round_without_blockers",
                message="the durable open round is marked blocked, but it has no blocker entries",
                evidence=[round_id],
            )
    checks.append("active round projection and round honesty")

    run_hook_current_task_mentions_active_objective(
        issues=issues,
        checks=checks,
        current_task_path=current_task_path,
        active_objective_record=active_objective_record,
    )
    run_hook_current_task_mentions_active_round(
        issues=issues,
        checks=checks,
        current_task_path=current_task_path,
        open_round_record=open_round_record,
    )

    pivot_control_path = pivot_log_path(project_id)
    expected_pivot_log = render_pivot_log_file(project_id).strip()
    actual_pivot_log = read_if_exists(pivot_control_path)
    if not actual_pivot_log:
        add_issue(
            issues,
            severity="warning",
            domain="projection",
            code="missing_pivot_log_projection",
            message="control/pivot-log.md is missing",
            evidence=[str(pivot_control_path)],
        )
    elif actual_pivot_log != expected_pivot_log:
        add_issue(
            issues,
            severity="warning",
            domain="projection",
            code="pivot_log_projection_drift",
            message="control/pivot-log.md does not match the current durable pivot/objective history",
            evidence=[str(pivot_control_path)],
        )
    checks.append("pivot lineage projection")

    constitution_path = project_path / "control" / "constitution.md"
    if not constitution_path.exists():
        add_issue(
            issues,
            severity="warning",
            domain="constitution",
            code="missing_constitution_file",
            message="control/constitution.md is missing, so project-specific invariants cannot be compiled explicitly",
            evidence=[str(constitution_path)],
        )
    elif not constitution_has_substance(constitution_path):
        add_issue(
            issues,
            severity="warning",
            domain="constitution",
            code="constitution_placeholder",
            message="control/constitution.md exists, but it is still a placeholder and does not restore real project invariants yet",
            evidence=[str(constitution_path)],
        )

    exception_path = exception_ledger_path(project_id)
    expected_exception_ledger = render_exception_ledger_file(project_id).strip()
    actual_exception_ledger = read_if_exists(exception_path)
    if not exception_path.exists():
        add_issue(
            issues,
            severity="warning",
            domain="exception-contract",
            code="missing_exception_ledger",
            message="control/exception-ledger.md is missing, so temporary deviations have no canonical active ledger",
            evidence=[str(exception_path)],
        )
    elif actual_exception_ledger != expected_exception_ledger:
        add_issue(
            issues,
            severity="error",
            domain="projection",
            code="exception_ledger_projection_drift",
            message="control/exception-ledger.md does not match the durable exception-contract projection",
            evidence=[str(exception_path)],
        )
    checks.append("constitution and exception-contract control presence")

    hooks = constitution_audit_hooks(constitution_path)
    core_hook_names = {"current_task_mentions_active_objective", "current_task_mentions_active_round"}
    for hook_name in sorted(hooks):
        if hook_name in core_hook_names:
            continue
        runner = HOOK_RUNNERS.get(hook_name)
        if runner is None:
            add_issue(
                issues,
                severity="warning",
                domain="constitution",
                code="unknown_constitution_audit_hook",
                message=f"constitution declares unsupported audit hook `{hook_name}`",
                evidence=[str(constitution_path)],
            )
            continue
        runner(
            issues=issues,
            checks=checks,
            project_id=project_id,
            current_task_path=current_task_path,
            constitution_path=constitution_path,
            active_objective_record=active_objective_record,
            open_round_record=open_round_record,
        )

    transition_commands_doc_path = ROOT / "TRANSITION_COMMANDS.md"
    documented_commands = documented_transition_command_names(transition_commands_doc_path)
    registry_commands = set(transition_command_names())
    missing_registry_commands = sorted(documented_commands - registry_commands)
    if missing_registry_commands:
        add_issue(
            issues,
            severity="warning",
            domain="transition-registry",
            code="documented_transition_commands_missing_from_registry",
            message="TRANSITION_COMMANDS.md documents commands that are not present in the machine-readable transition registry",
            evidence=missing_registry_commands,
        )
    documented_plans = documented_plan_family_names(transition_commands_doc_path)
    registry_plans = set(adjudication_plan_types())
    missing_registry_plans = sorted(documented_plans - registry_plans)
    if missing_registry_plans:
        add_issue(
            issues,
            severity="warning",
            domain="transition-registry",
            code="documented_adjudication_plans_missing_from_registry",
            message="TRANSITION_COMMANDS.md documents adjudication plan families that are not present in the machine-readable transition registry",
            evidence=missing_registry_plans,
        )
    checks.append("transition registry coverage against documented command surface")

    error_count = sum(1 for issue in issues if issue["severity"] == "error")
    warning_count = sum(1 for issue in issues if issue["severity"] == "warning")

    if error_count:
        status = "blocked"
    elif warning_count:
        status = "warn"
    else:
        status = "ok"

    return {
        "project_id": project_id,
        "status": status,
        "summary": {
            "errors": error_count,
            "warnings": warning_count,
            "checks": checks,
        },
        "issues": issues,
    }


def main() -> int:
    args = parse_args()
    result = audit_project_control_state(args.project_id)
    print(json.dumps(result, ensure_ascii=True, indent=2))
    error_count = int(result["summary"]["errors"])
    warning_count = int(result["summary"]["warnings"])
    if error_count:
        return 1
    if args.strict_warnings and warning_count:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
