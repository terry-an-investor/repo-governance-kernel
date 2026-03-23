#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json

from round_control import (
    active_objective_path,
    apply_transition_transaction,
    assert_objective_phase_command_contract,
    find_objectives_by_status,
    load_active_objective,
    objectives_dir,
    pivot_log_path,
    project_dir,
    render_objective_phase_guard_lines,
    render_active_objective_file,
    render_objective_file,
    render_pivot_log_file,
    resolve_anchor,
    slugify,
    timestamp_now,
    transition_events_dir,
)


ALLOWED_PHASES = {"exploration", "execution"}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Open a new active objective.")
    parser.add_argument("--project-id", required=True)
    parser.add_argument("--title", required=True)
    parser.add_argument("--summary", default="")
    parser.add_argument("--problem", required=True)
    parser.add_argument("--success-criterion", action="append", required=True)
    parser.add_argument("--non-goal", action="append", required=True)
    parser.add_argument("--why-now", required=True)
    parser.add_argument("--phase", required=True, choices=sorted(ALLOWED_PHASES))
    parser.add_argument("--risk", action="append", default=[])
    parser.add_argument("--path", action="append", default=[])
    parser.add_argument("--supersession-notes", default="")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    project_path = project_dir(args.project_id)
    if not project_path.exists():
        raise SystemExit(f"project directory not found: {project_path}")

    active_objective_preface, _active_objective_sections = load_active_objective(args.project_id)
    existing_objective_id = active_objective_preface.get("objective id", "")
    existing_status = active_objective_preface.get("status", "")
    if existing_objective_id:
        raise SystemExit(
            f"cannot open a new objective while `{existing_objective_id}` is still present in "
            f"`{active_objective_path(args.project_id)}` with status `{existing_status or 'unknown'}`; "
            "use a pivot or explicit close path instead"
        )

    durable_active_objectives = find_objectives_by_status(args.project_id, statuses={"active"})
    if durable_active_objectives:
        durable_ids = ", ".join(
            f"`{str(meta.get('id') or path.stem)}`"
            for path, meta, _sections in durable_active_objectives
        )
        raise SystemExit(
            f"cannot open a new objective because durable active objective records already exist: {durable_ids}; "
            "repair or pivot the active line instead of creating a second active objective"
        )

    timestamp = timestamp_now()
    slug = slugify(args.title)
    objective_id = f"obj-{timestamp.strftime('%Y-%m-%d-%H%M')}-{slug}"
    file_stem = f"{timestamp.strftime('%Y-%m-%d-%H%M')}-{slug}"
    anchor = resolve_anchor(args.project_id)

    summary = args.summary.strip() or args.problem.strip()
    objective_text = render_objective_file(
        objective_id=objective_id,
        title=args.title,
        status="active",
        project_id=args.project_id,
        anchor=anchor,
        paths=args.path,
        created_at=timestamp.isoformat(timespec="seconds"),
        evidence_refs=[],
        tags=["objective", "active"],
        confidence="high",
        phase=args.phase,
        supersedes=[],
        superseded_by=[],
        summary=summary,
        problem=args.problem,
        success_criteria=args.success_criterion,
        non_goals=args.non_goal,
        why_now=args.why_now,
        current_risks=args.risk,
        supersession_notes=args.supersession_notes,
    )
    active_objective_text = render_active_objective_file(
        objective_id=objective_id,
        phase=args.phase,
        status="active",
        problem=args.problem,
        success_criteria=args.success_criterion,
        non_goals=args.non_goal,
        why_now=args.why_now,
        current_risks=args.risk,
    )

    objective_path = objectives_dir(args.project_id) / f"{file_stem}.md"
    active_path = active_objective_path(args.project_id)
    pivot_path = pivot_log_path(args.project_id)
    assert_objective_phase_command_contract(
        "open-objective",
        provided_inputs={"project_id", "title", "problem", "success_criteria", "non_goals", "phase"},
        satisfied_guard_codes={"objective_fields_present", "active_objective_phase_valid", "no_other_active_objective"},
        write_targets={"durable:objective", "control:active-objective", "control:pivot-log", "memory:transition-event"},
        durable_owners={"memory:objective"},
        projection_owners={"control:active-objective", "control:pivot-log"},
        artifact_owners=set(),
        live_inspection_owners=set(),
    )
    _side_effects, event_id, event_path = apply_transition_transaction(
        project_id=args.project_id,
        writes=[
            {"path": objective_path, "text": objective_text, "label": "durable objective"},
            {"path": active_path, "text": active_objective_text, "label": "active objective projection"},
            {"path": pivot_path, "text": lambda: render_pivot_log_file(args.project_id), "label": "pivot-log projection"},
        ],
        command_name="open-objective",
        title=f"Opened objective {objective_id}",
        anchor=anchor,
        previous_state="no active objective was present",
        next_state=f"objective `{objective_id}` is now active in phase `{args.phase}`",
        guards=render_objective_phase_guard_lines("open-objective"),
        evidence=[args.problem, args.why_now],
        target_ids=[objective_id],
        event_file_stem=f"{file_stem}-open-objective",
    )

    print(
        json.dumps(
            {
                "project_id": args.project_id,
                "objective_id": objective_id,
                "objective_path": str(objective_path),
                "active_objective_path": str(active_path),
                "pivot_log_path": str(pivot_path),
                "transition_event_id": event_id,
                "transition_event_path": str(event_path),
            },
            ensure_ascii=True,
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
