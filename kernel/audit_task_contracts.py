#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path

from kernel.round_control import (
    OPEN_TASK_CONTRACT_STATUSES,
    TASK_CONTRACT_EXECUTION_GATE_ROUND_STATUSES,
    load_all_task_contracts,
    load_round_file,
    locate_round_file,
    parse_bullet_list,
    project_dir,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Audit task-contract durability and alignment.")
    parser.add_argument("--project-id", required=True)
    parser.add_argument("--strict-warnings", action="store_true")
    return parser.parse_args()


def add_issue(
    issues: list[dict[str, object]],
    *,
    severity: str,
    code: str,
    message: str,
    evidence: list[str] | None = None,
) -> None:
    issues.append(
        {
            "severity": severity,
            "code": code,
            "message": message,
            "evidence": evidence or [],
        }
    )


def path_is_covered(path: str, scope_paths: list[str]) -> bool:
    normalized_path = path.replace("\\", "/").strip().lstrip("./")
    for raw_scope in scope_paths:
        scope = raw_scope.replace("\\", "/").strip().lstrip("./").rstrip("/")
        if not scope:
            continue
        if normalized_path == scope or normalized_path.startswith(scope + "/"):
            return True
    return False


def section_present(value: str) -> bool:
    normalized = value.strip()
    return normalized not in {"", "_none recorded_"}


def audit_task_contracts(project_id: str) -> dict[str, object]:
    project_path = project_dir(project_id)
    if not project_path.exists():
        raise SystemExit(f"project directory not found: {project_path}")

    issues: list[dict[str, object]] = []
    checks: list[str] = []
    seen_ids: set[str] = set()
    records = load_all_task_contracts(project_id)

    for path, meta, sections in records:
        task_contract_id = str(meta.get("id") or path.stem).strip()
        if task_contract_id in seen_ids:
            add_issue(
                issues,
                severity="error",
                code="duplicate_task_contract_id",
                message="duplicate durable task-contract id detected",
                evidence=[task_contract_id, str(path)],
            )
        seen_ids.add(task_contract_id)

        round_id = str(meta.get("round_id") or "").strip()
        objective_id = str(meta.get("objective_id") or "").strip()
        status = str(meta.get("status") or "").strip()
        task_paths = [str(item).strip() for item in meta.get("paths", []) if str(item).strip()]

        if not round_id:
            add_issue(
                issues,
                severity="error",
                code="missing_round_id",
                message="task contract is missing required round linkage",
                evidence=[task_contract_id, str(path)],
            )
            continue

        round_path = locate_round_file(project_id, round_id)
        if round_path is None:
            add_issue(
                issues,
                severity="error",
                code="missing_round_record",
                message="task contract references a round that does not exist",
                evidence=[task_contract_id, round_id],
            )
            continue

        round_meta, _round_sections = load_round_file(round_path)
        round_objective_id = str(round_meta.get("objective_id") or "").strip()
        round_status = str(round_meta.get("status") or "").strip()
        round_scope_paths = [str(item).strip() for item in round_meta.get("paths", []) if str(item).strip()]

        if objective_id != round_objective_id:
            add_issue(
                issues,
                severity="error",
                code="task_contract_objective_mismatch",
                message="task contract objective linkage does not match its round objective",
                evidence=[task_contract_id, f"task objective: {objective_id}", f"round objective: {round_objective_id}"],
            )

        if status in OPEN_TASK_CONTRACT_STATUSES and round_status not in TASK_CONTRACT_EXECUTION_GATE_ROUND_STATUSES:
            add_issue(
                issues,
                severity="error",
                code="unresolved_task_contract_on_non_execution_round",
                message="draft or active task contract is attached to a round that is no longer eligible for unresolved execution work",
                evidence=[
                    task_contract_id,
                    round_id,
                    f"task status: {status}",
                    f"round status: {round_status}",
                ],
            )

        if not task_paths:
            add_issue(
                issues,
                severity="error",
                code="missing_task_paths",
                message="task contract does not declare any path scope",
                evidence=[task_contract_id, str(path)],
            )
        else:
            uncovered_paths = [task_path for task_path in task_paths if not path_is_covered(task_path, round_scope_paths)]
            if uncovered_paths:
                add_issue(
                    issues,
                    severity="error",
                    code="task_paths_outside_round_scope",
                    message="task contract paths escape the referenced round scope",
                    evidence=[task_contract_id, *uncovered_paths],
                )

        if status == "active":
            if not section_present(str(sections.get("Intent", ""))):
                add_issue(
                    issues,
                    severity="error",
                    code="missing_intent",
                    message="active task contract is missing an Intent section",
                    evidence=[task_contract_id, str(path)],
                )
            if not parse_bullet_list(str(sections.get("Allowed Changes", ""))):
                add_issue(
                    issues,
                    severity="error",
                    code="missing_allowed_changes",
                    message="active task contract is missing allowed changes",
                    evidence=[task_contract_id, str(path)],
                )
            if not parse_bullet_list(str(sections.get("Forbidden Changes", ""))):
                add_issue(
                    issues,
                    severity="error",
                    code="missing_forbidden_changes",
                    message="active task contract is missing forbidden changes",
                    evidence=[task_contract_id, str(path)],
                )
            if not parse_bullet_list(str(sections.get("Completion Criteria", ""))):
                add_issue(
                    issues,
                    severity="error",
                    code="missing_completion_criteria",
                    message="active task contract is missing completion criteria",
                    evidence=[task_contract_id, str(path)],
                )
        if status == "completed" and not parse_bullet_list(str(sections.get("Resolution", ""))):
            add_issue(
                issues,
                severity="error",
                code="completed_task_contract_missing_resolution",
                message="completed task contract is missing Resolution entries",
                evidence=[task_contract_id, str(path)],
            )

    checks.append("task-contract id uniqueness")
    checks.append("task-contract round linkage")
    checks.append("task-contract objective alignment")
    checks.append("task-contract path scope within round scope")
    checks.append("task-contract required active sections")
    checks.append("completed task-contract resolution history")

    error_count = sum(1 for issue in issues if issue["severity"] == "error")
    warning_count = sum(1 for issue in issues if issue["severity"] == "warning")
    status = "blocked" if error_count else ("warn" if warning_count else "ok")
    return {
        "project_id": project_id,
        "status": status,
        "summary": {
            "errors": error_count,
            "warnings": warning_count,
            "checks": checks,
            "task_contract_count": len(records),
        },
        "issues": issues,
    }


def main() -> int:
    args = parse_args()
    result = audit_task_contracts(args.project_id)
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

