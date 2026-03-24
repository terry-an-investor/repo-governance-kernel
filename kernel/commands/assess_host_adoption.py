#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path

from kernel.audit_control_state import audit_project_control_state
from kernel.control_enforcement import evaluate_worktree_enforcement
from kernel.host_adoption import (
    adoption_report_path,
    assessment_contract,
    assessment_payload,
    make_shadow_adoption_report,
    to_json,
)
from kernel.round_control import (
    assert_anchor_maintenance_command_contract,
    current_task_path,
    find_task_contracts,
    project_dir,
    resolve_active_objective_record,
    resolve_anchor,
    select_open_round_record,
)
from kernel.runtime_paths import resolve_repo_root


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Assess a governed host repository for shadow-mode adoption and write a readable report."
    )
    parser.add_argument("--project-id", required=True)
    parser.add_argument("--workspace-root", default="")
    parser.add_argument("--source-repo", default="")
    parser.add_argument(
        "--mode",
        choices=("auto", "governed-host-shadow", "external-target-shadow"),
        default="auto",
    )
    parser.add_argument("--output", default="")
    return parser.parse_args()


def _resolve_report_path(project_id: str, output: str) -> Path:
    if output.strip():
        output_path = Path(output)
        if not output_path.is_absolute():
            output_path = Path.cwd() / output_path
        return output_path
    return adoption_report_path(project_id)


def main() -> int:
    args = parse_args()
    governance_root = resolve_repo_root()
    governance_project_root = project_dir(args.project_id)
    objective_path, _objective_meta, _objective_sections, objective_id = resolve_active_objective_record(args.project_id)
    round_record, round_issues = select_open_round_record(args.project_id)
    if round_record is None:
        details = "; ".join(round_issues) if round_issues else "no open round exists"
        raise SystemExit(f"host adoption assessment requires one open round: {details}")
    round_path, round_meta, _round_sections = round_record
    round_id = str(round_meta.get("id") or round_path.stem).strip()
    round_scope_paths = [str(item).strip() for item in round_meta.get("paths", []) if str(item).strip()]

    active_task_contracts = find_task_contracts(args.project_id, round_id=round_id, statuses={"active"})
    if not active_task_contracts:
        raise SystemExit(
            f"host adoption assessment requires at least one active task contract beneath round `{round_id}`"
        )
    if len(active_task_contracts) > 1:
        raise SystemExit(
            f"host adoption assessment currently requires one active task contract for round `{round_id}`; found {len(active_task_contracts)}"
        )
    task_contract_path, task_contract_meta, _task_contract_sections = active_task_contracts[0]
    task_contract_id = str(task_contract_meta.get("id") or task_contract_path.stem).strip()
    task_contract_paths = [str(item).strip() for item in task_contract_meta.get("paths", []) if str(item).strip()]

    anchor = resolve_anchor(args.project_id)
    if args.workspace_root.strip():
        anchor["workspace_root"] = args.workspace_root.strip()
    workspace_root = str(anchor.get("workspace_root") or "").strip()
    if not workspace_root:
        raise SystemExit(
            f"host adoption assessment requires a workspace root in `{current_task_path(args.project_id)}` or via --workspace-root"
        )

    assert_anchor_maintenance_command_contract(
        "assess-host-adoption",
        provided_inputs={"project_id"},
    )
    final_audit = audit_project_control_state(args.project_id)
    final_enforce = evaluate_worktree_enforcement(args.project_id, workspace_root=workspace_root)

    source_repo = args.source_repo.strip() or workspace_root
    report_path = _resolve_report_path(args.project_id, args.output)
    contract_payload = assessment_contract(
        governance_root=str(governance_root),
        governance_project_root=str(governance_project_root),
        workspace_root=workspace_root,
        report_path=str(report_path),
        requested_mode=args.mode,
    )
    report_text, blocker_classification, remaining_blocked_paths = make_shadow_adoption_report(
        project_id=args.project_id,
        source_repo=source_repo,
        workspace_root=workspace_root,
        objective_id=objective_id,
        round_id=round_id,
        task_contract_id=task_contract_id,
        assessment_contract_payload=contract_payload,
        round_scope_paths=round_scope_paths,
        task_contract_paths=task_contract_paths,
        final_audit_status=str(final_audit.get("status") or ""),
        final_enforce=final_enforce,
        report_title="Host Shadow Adoption Assessment Report",
        meaning_lines=[
            "The governed host now has one explicit active objective, round, and task contract for shadow-mode assessment.",
            "This report is an owner-layer assessment artifact for observing host adoption readiness, not a claim of general live-host automatic rewrite.",
            "Any remaining blocked enforcement state now reflects real scope law or explicit host-support noise rather than missing adoption objects.",
        ],
        next_step_lines=[
            "Use remaining repo-scope gaps to narrow or broaden the adopted round honestly before any stronger live-host claim.",
            "Keep live-host rollout in shadow mode first: observe verdicts and reports before promoting any enforcement trigger into developer flow.",
            "Separate host bootstrap/support path policy from real source-repo scope so future live-host reports stay readable.",
        ],
    )

    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(report_text, encoding="utf-8", newline="\n")

    print(
        to_json(
            assessment_payload(
                project_id=args.project_id,
                governance_root=str(governance_root),
                governance_project_root=str(governance_project_root),
                objective_id=objective_id,
                round_id=round_id,
                task_contract_id=task_contract_id,
                source_repo=source_repo,
                workspace_root=workspace_root,
                report_path=str(report_path),
                assessment_contract_payload=contract_payload,
                final_audit=final_audit,
                final_enforce=final_enforce,
                blocker_classification=blocker_classification,
                remaining_blocked_paths=remaining_blocked_paths,
            )
            | {
                "objective_path": str(objective_path),
                "round_path": str(round_path),
                "task_contract_path": str(task_contract_path),
                "round_scope_paths": round_scope_paths,
                "task_contract_paths": task_contract_paths,
                "wrote_report": True,
            }
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
