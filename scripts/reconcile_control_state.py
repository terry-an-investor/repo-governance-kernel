#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json

from round_control import (
    active_objective_path,
    active_round_path,
    exception_ledger_path,
    load_all_rounds,
    parse_bullet_list,
    project_dir,
    render_exception_ledger_file,
    render_active_objective_file,
    render_active_round_file,
    render_pivot_log_file,
    select_active_objective_record,
    select_open_round_record,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Rebuild control files from durable memory truth.")
    parser.add_argument("--project-id", required=True)
    parser.add_argument("--check", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    project_path = project_dir(args.project_id)
    if not project_path.exists():
        raise SystemExit(f"project directory not found: {project_path}")

    actions: list[str] = []
    issues: list[str] = []

    active_objective_record, objective_issues = select_active_objective_record(args.project_id)
    issues.extend(objective_issues)

    open_round_record, round_issues = select_open_round_record(args.project_id)
    issues.extend(round_issues)

    active_objective_text: str | None = None
    if active_objective_record is not None:
        _objective_path, objective_meta, objective_sections = active_objective_record
        active_objective_id = str(objective_meta.get("id") or "").strip()
        active_objective_text = render_active_objective_file(
            objective_id=active_objective_id,
            phase=str(objective_meta.get("phase") or "").strip(),
            status=str(objective_meta.get("status") or "").strip() or "active",
            problem=str(objective_sections.get("Problem", "")).strip(),
            success_criteria=parse_bullet_list(str(objective_sections.get("Success Criteria", ""))),
            non_goals=parse_bullet_list(str(objective_sections.get("Non-Goals", ""))),
            why_now=str(objective_sections.get("Why Now", "")).strip(),
            current_risks=parse_bullet_list(str(objective_sections.get("Active Risks", ""))),
        )
        actions.append(f"rebuild `{active_objective_path(args.project_id).relative_to(project_path.parent).as_posix()}` from durable objective `{active_objective_id}`")

    pivot_log_text = render_pivot_log_file(args.project_id)
    actions.append(f"rebuild `state/{args.project_id}/control/pivot-log.md` from durable pivot and objective records")
    exception_ledger_text = render_exception_ledger_file(args.project_id)

    active_round_text: str | None = None
    active_round_record = open_round_record
    if active_round_record is not None:
        _round_path, round_meta, round_sections = active_round_record
        round_objective_id = str(round_meta.get("objective_id") or "").strip()
        if active_objective_record is None:
            issues.append(
                f"open durable round `{round_meta.get('id', '')}` exists but no unambiguous active objective can be projected"
            )
        elif round_objective_id != str(active_objective_record[1].get("id") or "").strip():
            issues.append(
                f"open durable round `{round_meta.get('id', '')}` points to objective `{round_objective_id}`, "
                f"but durable active objective is `{active_objective_record[1].get('id', '')}`"
            )
        else:
            active_round_text = render_active_round_file(
                round_id=str(round_meta.get("id") or "").strip(),
                objective_id=round_objective_id,
                status=str(round_meta.get("status") or "").strip(),
                scope_items=parse_bullet_list(str(round_sections.get("Scope", ""))),
                deliverable=str(round_sections.get("Deliverable", "")).strip(),
                validation_plan=str(round_sections.get("Validation Plan", "")).strip(),
                risks=parse_bullet_list(str(round_sections.get("Active Risks", ""))),
                blockers=parse_bullet_list(str(round_sections.get("Blockers", ""))),
            )
            actions.append(
                f"rebuild `{active_round_path(args.project_id).relative_to(project_path.parent).as_posix()}` from durable open round `{round_meta.get('id', '')}`"
            )
    else:
        if load_all_rounds(args.project_id):
            actions.append(
                f"remove stale `{active_round_path(args.project_id).relative_to(project_path.parent).as_posix()}` because no durable open round exists"
            )

    ledger_path = exception_ledger_path(args.project_id)
    if ledger_path.exists():
        actions.append(
            f"rebuild `{ledger_path.relative_to(project_path.parent).as_posix()}` from durable exception-contract records"
        )

    if issues:
        print(
            json.dumps(
                {
                    "project_id": args.project_id,
                    "status": "blocked",
                    "issues": issues,
                    "planned_actions": actions,
                },
                ensure_ascii=True,
                indent=2,
            )
        )
        return 1

    if not args.check:
        control_objective_path = active_objective_path(args.project_id)
        control_objective_path.parent.mkdir(parents=True, exist_ok=True)
        if active_objective_text is not None:
            control_objective_path.write_text(active_objective_text, encoding="utf-8")
        elif control_objective_path.exists():
            control_objective_path.unlink()

        control_pivot_log_path = project_path / "control" / "pivot-log.md"
        control_pivot_log_path.parent.mkdir(parents=True, exist_ok=True)
        control_pivot_log_path.write_text(pivot_log_text, encoding="utf-8")

        control_round_path = active_round_path(args.project_id)
        control_round_path.parent.mkdir(parents=True, exist_ok=True)
        if active_round_text is not None:
            control_round_path.write_text(active_round_text, encoding="utf-8")
        elif control_round_path.exists():
            control_round_path.unlink()

        if ledger_path.exists():
            ledger_path.write_text(exception_ledger_text, encoding="utf-8")

    print(
        json.dumps(
            {
                "project_id": args.project_id,
                "status": "ok",
                "mode": "check" if args.check else "apply",
                "actions": actions,
            },
            ensure_ascii=True,
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
