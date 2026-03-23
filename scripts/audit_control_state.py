#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path

from round_control import (
    active_objective_path,
    active_round_path,
    load_all_rounds,
    parse_bullet_list,
    pivot_log_path,
    project_dir,
    render_active_objective_file,
    render_active_round_file,
    render_pivot_log_file,
    select_active_objective_record,
    select_open_round_record,
)


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


def main() -> int:
    args = parse_args()
    project_path = project_dir(args.project_id)
    if not project_path.exists():
        raise SystemExit(f"project directory not found: {project_path}")

    issues: list[dict[str, object]] = []
    checks: list[str] = []

    active_objective_record, objective_issues = select_active_objective_record(args.project_id)
    for issue in objective_issues:
        add_issue(
            issues,
            severity="error",
            domain="objective-line",
            code="durable_objective_ambiguity",
            message=issue,
        )
    checks.append("durable objective-line selection")

    open_round_record, round_issues = select_open_round_record(args.project_id)
    for issue in round_issues:
        add_issue(
            issues,
            severity="error",
            domain="round-control",
            code="durable_round_ambiguity",
            message=issue,
        )
    checks.append("durable round selection")

    objective_control_path = active_objective_path(args.project_id)
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

    round_control_path = active_round_path(args.project_id)
    if open_round_record is None:
        if load_all_rounds(args.project_id) and round_control_path.exists():
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

    pivot_control_path = pivot_log_path(args.project_id)
    expected_pivot_log = render_pivot_log_file(args.project_id).strip()
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

    exception_ledger_path = project_path / "control" / "exception-ledger.md"
    if not exception_ledger_path.exists():
        add_issue(
            issues,
            severity="warning",
            domain="exception-contract",
            code="missing_exception_ledger",
            message="control/exception-ledger.md is missing, so temporary deviations have no canonical active ledger",
            evidence=[str(exception_ledger_path)],
        )
    checks.append("constitution and exception-contract control presence")

    error_count = sum(1 for issue in issues if issue["severity"] == "error")
    warning_count = sum(1 for issue in issues if issue["severity"] == "warning")

    if error_count:
        status = "blocked"
    elif warning_count:
        status = "warn"
    else:
        status = "ok"

    print(
        json.dumps(
            {
                "project_id": args.project_id,
                "status": status,
                "summary": {
                    "errors": error_count,
                    "warnings": warning_count,
                    "checks": checks,
                },
                "issues": issues,
            },
            ensure_ascii=True,
            indent=2,
        )
    )
    if error_count:
        return 1
    if args.strict_warnings and warning_count:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
