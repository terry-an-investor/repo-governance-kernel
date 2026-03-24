#!/usr/bin/env python3
from __future__ import annotations

import argparse
import sqlite3
from pathlib import Path

from audit_control_state import audit_project_control_state
from assemble_context import (
    DB_PATH,
    ROOT,
    append_active_task_contracts,
    clean_section_text,
    latest_snapshot,
    load_active_task_contract_records,
    load_control_sections,
    parse_keyed_bullets,
    parse_h2_sections,
)


ROLE_CHOICES = ("reviewer", "architect", "orchestrator")


def fetch_memory_rows(project_id: str, types: tuple[str, ...], limit: int) -> list[sqlite3.Row]:
    placeholders = ", ".join("?" for _ in types)
    query = f"""
        SELECT id, type, title, summary_text, source_file
        FROM memory_items
        WHERE project_id = ?
          AND type IN ({placeholders})
        ORDER BY updated_at DESC, id ASC
        LIMIT ?
    """
    params = [project_id, *types, limit]
    with sqlite3.connect(DB_PATH) as conn:
        conn.row_factory = sqlite3.Row
        return conn.execute(query, params).fetchall()


def is_placeholder(text: str) -> bool:
    normalized = " ".join(text.strip().lower().split())
    return normalized in {
        "",
        "- none recorded yet.",
        "none recorded yet.",
        "- _none_",
        "_none_",
    }


def append_control_sections(parts: list[str], title: str, preface: str, sections: dict[str, str], names: list[str]) -> None:
    selected: list[str] = []
    preface = preface.strip()
    if preface and not is_placeholder(preface):
        selected.append(preface)
    for name in names:
        body = sections.get(name, "").strip()
        if is_placeholder(body):
            continue
        selected.append(f"### {name}\n\n{body}")
    if not selected:
        return
    parts.append(f"## {title}\n")
    parts.append("\n\n".join(selected))
    parts.append("")


def append_memory(parts: list[str], title: str, rows: list[sqlite3.Row]) -> None:
    if not rows:
        return
    parts.append(f"## {title}\n")
    for row in rows:
        parts.append(f"- `{row['type']}` `{row['id']}`: {row['title']}")
        if row["summary_text"]:
            parts.append(f"  {row['summary_text']}")
        parts.append(f"  Source: `{row['source_file']}`")
    parts.append("")


def append_control_status(parts: list[str], audit_result: dict[str, object]) -> None:
    summary = dict(audit_result.get("summary") or {})
    checks = [str(item).strip() for item in summary.get("checks", []) if str(item).strip()]
    parts.append("## Current Control Status\n")
    parts.append(f"- Audit status: `{audit_result.get('status', 'unknown')}`")
    parts.append(f"- Errors: `{summary.get('errors', 0)}`")
    parts.append(f"- Warnings: `{summary.get('warnings', 0)}`")
    if checks:
        parts.append(f"- Checks: {'; '.join(checks)}")
    parts.append("")


def append_control_violations(parts: list[str], audit_result: dict[str, object]) -> None:
    issues = list(audit_result.get("issues") or [])
    parts.append("## Current Control Violations\n")
    if not issues:
        parts.append("- No active audit violations.")
        parts.append("")
        return

    sorted_issues = sorted(
        issues,
        key=lambda issue: (0 if str(issue.get("severity")) == "error" else 1, str(issue.get("domain") or ""), str(issue.get("code") or "")),
    )
    for issue in sorted_issues:
        severity = str(issue.get("severity") or "warning").strip()
        domain = str(issue.get("domain") or "unknown").strip()
        code = str(issue.get("code") or "unspecified").strip()
        message = str(issue.get("message") or "").strip()
        parts.append(f"- `{severity}` `{domain}` `{code}`: {message}")
        evidence = [str(item).strip() for item in issue.get("evidence", []) if str(item).strip()]
        if evidence:
            parts.append(f"  Evidence: {', '.join(evidence)}")
    parts.append("")


def compile_reviewer_context(project_dir: Path, project_id: str, limit: int) -> str:
    audit_result = audit_project_control_state(project_id)
    constitution_preface, constitution_sections = load_control_sections(project_dir / "control" / "constitution.md")
    objective_preface, objective_sections = load_control_sections(project_dir / "control" / "active-objective.md")
    round_preface, round_sections = load_control_sections(project_dir / "control" / "active-round.md")
    pivot_preface, pivot_sections = load_control_sections(project_dir / "control" / "pivot-log.md")
    exception_preface, exception_sections = load_control_sections(project_dir / "control" / "exception-ledger.md")
    blockers_sections = parse_h2_sections(clean_section_text(project_dir / "current" / "blockers.md", strip_heading=True))
    current_task_sections = parse_h2_sections(clean_section_text(project_dir / "current" / "current-task.md", strip_heading=True))
    review_memory = fetch_memory_rows(project_id, ("decision", "failure", "constraint", "adjudication"), limit)
    active_round_values = {}
    if round_preface.strip():
        active_round_values = parse_keyed_bullets(round_preface)
    active_task_contracts = load_active_task_contract_records(
        project_dir,
        active_round_values.get("round id", ""),
    )

    parts = [f"# Reviewer Context\n", f"Project: `{project_id}`\n"]
    append_control_status(parts, audit_result)
    append_control_violations(parts, audit_result)
    append_control_sections(
        parts,
        "Project Constitution",
        constitution_preface,
        constitution_sections,
        ["Architecture Invariants", "Quality Bar", "Validation Rules", "Forbidden Shortcuts"],
    )
    append_control_sections(
        parts,
        "Active Objective",
        objective_preface,
        objective_sections,
        ["Problem", "Success Criteria", "Non-Goals", "Current Risks"],
    )
    append_control_sections(
        parts,
        "Active Round",
        round_preface,
        round_sections,
        ["Scope", "Deliverable", "Validation Plan", "Active Risks", "Blockers"],
    )
    append_active_task_contracts(parts, active_task_contracts)
    append_control_sections(
        parts,
        "Pivot Lineage",
        pivot_preface,
        pivot_sections,
        ["Active Lineage", "Recent Pivots"],
    )
    append_control_sections(
        parts,
        "Exception Ledger",
        exception_preface,
        exception_sections,
        ["Active", "Invalidated"],
    )
    append_control_sections(
        parts,
        "Current Review Surface",
        "",
        current_task_sections,
        ["Goal", "Current State", "Active Risks", "Next Steps"],
    )
    append_control_sections(parts, "Active Blockers", "", blockers_sections, ["Active", "Waiting"])
    append_memory(parts, "Relevant Durable Memory", review_memory)
    return "\n".join(parts).strip() + "\n"


def compile_architect_context(project_dir: Path, project_id: str, limit: int) -> str:
    audit_result = audit_project_control_state(project_id)
    constitution_preface, constitution_sections = load_control_sections(project_dir / "control" / "constitution.md")
    objective_preface, objective_sections = load_control_sections(project_dir / "control" / "active-objective.md")
    round_preface, round_sections = load_control_sections(project_dir / "control" / "active-round.md")
    pivot_preface, pivot_sections = load_control_sections(project_dir / "control" / "pivot-log.md")
    snapshot_path = latest_snapshot(project_dir)
    snapshot_sections: dict[str, str] = {}
    if snapshot_path:
        snapshot_sections = parse_h2_sections(clean_section_text(snapshot_path, strip_heading=False, strip_yaml=True))
    architecture_memory = fetch_memory_rows(project_id, ("decision", "failure", "constraint", "pattern", "adjudication"), limit)
    active_round_values = {}
    if round_preface.strip():
        active_round_values = parse_keyed_bullets(round_preface)
    active_task_contracts = load_active_task_contract_records(
        project_dir,
        active_round_values.get("round id", ""),
    )

    parts = [f"# Architect Context\n", f"Project: `{project_id}`\n"]
    append_control_status(parts, audit_result)
    append_control_violations(parts, audit_result)
    append_control_sections(
        parts,
        "Project Constitution",
        constitution_preface,
        constitution_sections,
        ["Product Boundaries", "Architecture Invariants", "Quality Bar", "Forbidden Shortcuts"],
    )
    append_control_sections(
        parts,
        "Active Objective",
        objective_preface,
        objective_sections,
        ["Problem", "Success Criteria", "Non-Goals", "Current Risks"],
    )
    append_control_sections(
        parts,
        "Active Round",
        round_preface,
        round_sections,
        ["Scope", "Deliverable", "Validation Plan", "Active Risks", "Blockers"],
    )
    append_active_task_contracts(parts, active_task_contracts)
    append_control_sections(
        parts,
        "Pivot Lineage",
        pivot_preface,
        pivot_sections,
        ["Active Lineage", "Recent Pivots"],
    )
    append_control_sections(
        parts,
        "Latest Snapshot",
        "",
        snapshot_sections,
        ["Goal", "Completed Work", "Validated Facts", "Rejected Approaches", "Blockers", "Next Steps"],
    )
    append_memory(parts, "Relevant Durable Memory", architecture_memory)
    return "\n".join(parts).strip() + "\n"


def compile_orchestrator_context(project_dir: Path, project_id: str, limit: int) -> str:
    audit_result = audit_project_control_state(project_id)
    constitution_preface, constitution_sections = load_control_sections(project_dir / "control" / "constitution.md")
    objective_preface, objective_sections = load_control_sections(project_dir / "control" / "active-objective.md")
    round_preface, round_sections = load_control_sections(project_dir / "control" / "active-round.md")
    pivot_preface, pivot_sections = load_control_sections(project_dir / "control" / "pivot-log.md")
    exception_preface, exception_sections = load_control_sections(project_dir / "control" / "exception-ledger.md")
    current_task_sections = parse_h2_sections(clean_section_text(project_dir / "current" / "current-task.md", strip_heading=True))
    blockers_sections = parse_h2_sections(clean_section_text(project_dir / "current" / "blockers.md", strip_heading=True))
    orchestration_memory = fetch_memory_rows(project_id, ("decision", "failure", "constraint", "pattern", "adjudication"), limit)
    active_round_values = {}
    if round_preface.strip():
        active_round_values = parse_keyed_bullets(round_preface)
    active_task_contracts = load_active_task_contract_records(
        project_dir,
        active_round_values.get("round id", ""),
    )

    parts = [f"# Orchestrator Context\n", f"Project: `{project_id}`\n"]
    append_control_status(parts, audit_result)
    append_control_violations(parts, audit_result)
    append_control_sections(
        parts,
        "Project Constitution",
        constitution_preface,
        constitution_sections,
        ["Product Boundaries", "Architecture Invariants", "Quality Bar", "Validation Rules", "Forbidden Shortcuts"],
    )
    append_control_sections(
        parts,
        "Active Objective",
        objective_preface,
        objective_sections,
        ["Problem", "Success Criteria", "Non-Goals", "Current Risks"],
    )
    append_control_sections(
        parts,
        "Active Round",
        round_preface,
        round_sections,
        ["Scope", "Deliverable", "Validation Plan", "Active Risks", "Blockers"],
    )
    append_active_task_contracts(parts, active_task_contracts)
    append_control_sections(
        parts,
        "Pivot Lineage",
        pivot_preface,
        pivot_sections,
        ["Active Lineage", "Recent Pivots"],
    )
    append_control_sections(
        parts,
        "Current Execution State",
        "",
        current_task_sections,
        ["Goal", "Current State", "Active Risks", "Next Steps"],
    )
    append_control_sections(parts, "Blockers", "", blockers_sections, ["Active", "Waiting"])
    append_control_sections(
        parts,
        "Exception Ledger",
        exception_preface,
        exception_sections,
        ["Active", "Invalidated"],
    )
    append_memory(parts, "Relevant Durable Memory", orchestration_memory)
    return "\n".join(parts).strip() + "\n"


def main() -> None:
    parser = argparse.ArgumentParser(description="Compile role-specific project context from control state.")
    parser.add_argument("--project-id", required=True)
    parser.add_argument("--role", required=True, choices=ROLE_CHOICES)
    parser.add_argument("--memory-limit", type=int, default=6)
    parser.add_argument("--output")
    args = parser.parse_args()

    project_dir = ROOT / "projects" / args.project_id
    if not project_dir.exists():
        raise SystemExit(f"project directory not found: {project_dir}")

    if args.role == "reviewer":
        output = compile_reviewer_context(project_dir, args.project_id, args.memory_limit)
    elif args.role == "architect":
        output = compile_architect_context(project_dir, args.project_id, args.memory_limit)
    else:
        output = compile_orchestrator_context(project_dir, args.project_id, args.memory_limit)

    if args.output:
        output_path = Path(args.output)
        if not output_path.is_absolute():
            output_path = ROOT / output_path
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(output, encoding="utf-8")
    else:
        print(output)


if __name__ == "__main__":
    main()
