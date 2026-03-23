#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

from round_control import (
    OPEN_ROUND_STATUSES,
    active_objective_path,
    apply_transition_transaction,
    assert_objective_phase_command_contract,
    find_exception_contracts,
    find_rounds,
    objective_record_payload,
    render_active_objective_file,
    render_objective_phase_guard_lines,
    render_objective_file,
    resolve_active_objective_record,
    resolve_anchor,
    timestamp_now,
)


ALLOWED_PHASES = {"exploration", "execution", "paused"}
SCRIPTS_DIR = Path(__file__).resolve().parent


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Change the active objective phase explicitly.")
    parser.add_argument("--project-id", required=True)
    parser.add_argument("--objective-id")
    parser.add_argument("--phase", required=True, choices=sorted(ALLOWED_PHASES))
    parser.add_argument("--reason", required=True)
    parser.add_argument("--evidence", action="append", default=[])
    parser.add_argument("--scope-review-note", action="append", default=[])
    parser.add_argument("--rewrite-open-round", action="store_true")
    parser.add_argument("--round-title", default="")
    parser.add_argument("--round-summary", default="")
    parser.add_argument("--round-scope-item", action="append", default=[])
    parser.add_argument("--round-scope-path", action="append", default=[])
    parser.add_argument("--round-deliverable", default="")
    parser.add_argument("--round-validation-plan", default="")
    parser.add_argument("--round-risk", action="append", default=[])
    parser.add_argument("--round-blocker", action="append", default=[])
    parser.add_argument("--round-status-note", default="")
    parser.add_argument("--replace-round-scope-items", action="store_true")
    parser.add_argument("--replace-round-scope-paths", action="store_true")
    parser.add_argument("--replace-round-risks", action="store_true")
    parser.add_argument("--replace-round-blockers", action="store_true")
    parser.add_argument("--auto-open-round", action="store_true")
    return parser.parse_args()


def _clean_list(values: list[str]) -> list[str]:
    return [value.strip() for value in values if value.strip()]


def _run_open_round(args: argparse.Namespace) -> dict[str, object]:
    cmd = [
        sys.executable,
        str(SCRIPTS_DIR / "open_round.py"),
        "--project-id",
        args.project_id,
        "--title",
        args.round_title.strip(),
        "--deliverable",
        args.round_deliverable.strip(),
        "--validation-plan",
        args.round_validation_plan.strip(),
    ]
    for item in _clean_list(args.round_scope_item):
        cmd.extend(["--scope-item", item])
    for item in _clean_list(args.round_scope_path):
        cmd.extend(["--scope-path", item])
    for item in _clean_list(args.round_risk):
        cmd.extend(["--risk", item])
    for item in _clean_list(args.round_blocker):
        cmd.extend(["--blocker", item])
    if args.round_status_note.strip():
        cmd.extend(["--status-note", args.round_status_note.strip()])
    completed = subprocess.run(
        cmd,
        cwd=str(SCRIPTS_DIR.parent),
        capture_output=True,
        text=True,
        check=False,
    )
    if completed.returncode != 0:
        raise SystemExit(completed.stderr.strip() or completed.stdout.strip() or "auto-open-round failed")
    try:
        return json.loads(completed.stdout)
    except json.JSONDecodeError as exc:
        raise SystemExit(f"auto-open-round returned invalid json: {exc}") from exc


def _run_rewrite_open_round(args: argparse.Namespace, round_id: str) -> dict[str, object]:
    cmd = [
        sys.executable,
        str(SCRIPTS_DIR / "rewrite_open_round.py"),
        "--project-id",
        args.project_id,
        "--round-id",
        round_id,
        "--reason",
        args.reason.strip(),
    ]
    if args.round_title.strip():
        cmd.extend(["--title", args.round_title.strip()])
    if args.round_summary.strip():
        cmd.extend(["--summary", args.round_summary.strip()])
    if args.round_deliverable.strip():
        cmd.extend(["--deliverable", args.round_deliverable.strip()])
    if args.round_validation_plan.strip():
        cmd.extend(["--validation-plan", args.round_validation_plan.strip()])
    for item in _clean_list(args.round_scope_item):
        cmd.extend(["--scope-item", item])
    for item in _clean_list(args.round_scope_path):
        cmd.extend(["--scope-path", item])
    for item in _clean_list(args.round_risk):
        cmd.extend(["--risk", item])
    for item in _clean_list(args.round_blocker):
        cmd.extend(["--blocker", item])
    if args.round_status_note.strip():
        cmd.extend(["--status-note", args.round_status_note.strip()])
    if args.replace_round_scope_items:
        cmd.append("--replace-scope-items")
    if args.replace_round_scope_paths:
        cmd.append("--replace-scope-paths")
    if args.replace_round_risks:
        cmd.append("--replace-risks")
    if args.replace_round_blockers:
        cmd.append("--replace-blockers")
    completed = subprocess.run(
        cmd,
        cwd=str(SCRIPTS_DIR.parent),
        capture_output=True,
        text=True,
        check=False,
    )
    if completed.returncode != 0:
        raise SystemExit(completed.stderr.strip() or completed.stdout.strip() or "rewrite-open-round failed")
    try:
        return json.loads(completed.stdout)
    except json.JSONDecodeError as exc:
        raise SystemExit(f"rewrite-open-round returned invalid json: {exc}") from exc


def main() -> int:
    args = parse_args()
    objective_path, meta, sections, objective_id = resolve_active_objective_record(
        args.project_id,
        objective_id=args.objective_id or "",
    )
    payload = objective_record_payload(meta, sections)

    current_phase = str(payload["phase"]).strip()
    next_phase = args.phase.strip()
    if not current_phase:
        raise SystemExit("active objective is missing phase")
    if current_phase == next_phase:
        raise SystemExit(f"objective `{objective_id}` is already in phase `{next_phase}`")

    open_rounds = find_rounds(args.project_id, objective_id=objective_id, statuses=OPEN_ROUND_STATUSES)
    active_contracts = find_exception_contracts(args.project_id, objective_id=objective_id, statuses={"active"})

    if next_phase == "execution":
        if not list(payload["non_goals"]):
            raise SystemExit("exploration -> execution requires at least one non-goal")
        validation_plan = args.round_validation_plan.strip()
        scope_items = _clean_list(args.round_scope_item)
        if not open_rounds and not args.auto_open_round:
            raise SystemExit(
                "moving into `execution` requires one bounded open round; pass --auto-open-round with round bootstrap inputs"
            )
        if args.auto_open_round:
            required = [
                args.round_title.strip(),
                args.round_deliverable.strip(),
                validation_plan,
            ]
            if not all(required) or not scope_items:
                raise SystemExit(
                    "--auto-open-round requires --round-title, at least one --round-scope-item, "
                    "--round-deliverable, and --round-validation-plan"
                )
            if open_rounds:
                raise SystemExit("cannot auto-open round because one durable open round already exists")

    if current_phase == "execution" and next_phase == "exploration":
        if not args.reason.strip():
            raise SystemExit("execution -> exploration requires an explicit reason")
        if open_rounds and not (_clean_list(args.scope_review_note) or args.rewrite_open_round):
            raise SystemExit(
                "execution -> exploration with open rounds requires either --rewrite-open-round or at least one --scope-review-note"
            )

    if current_phase == "execution" and next_phase == "paused":
        if open_rounds and not (_clean_list(args.scope_review_note) or args.rewrite_open_round):
            raise SystemExit(
                "execution -> paused with open rounds requires either --rewrite-open-round or at least one --scope-review-note"
            )

    if current_phase == "paused" and next_phase == "execution":
        if not open_rounds and not args.auto_open_round:
            raise SystemExit(
                "paused -> execution requires one durable open round or --auto-open-round bootstrap inputs"
            )
        if args.auto_open_round:
            required = [
                args.round_title.strip(),
                args.round_deliverable.strip(),
                args.round_validation_plan.strip(),
            ]
            if not all(required) or not _clean_list(args.round_scope_item):
                raise SystemExit(
                    "--auto-open-round requires --round-title, at least one --round-scope-item, "
                    "--round-deliverable, and --round-validation-plan"
                )
            if open_rounds:
                raise SystemExit("cannot auto-open round because one durable open round already exists")

    if current_phase == "paused" and next_phase == "exploration" and active_contracts and not _clean_list(args.scope_review_note):
        raise SystemExit(
            "paused -> exploration with active exception contracts requires at least one --scope-review-note covering temporary-deviation review"
        )

    anchor = resolve_anchor(args.project_id)
    objective_text = render_objective_file(
        objective_id=objective_id,
        title=str(payload["title"]),
        status="active",
        project_id=args.project_id,
        anchor=anchor,
        paths=list(payload["paths"]),
        created_at=str(payload["created_at"]) or timestamp_now().isoformat(timespec="seconds"),
        evidence_refs=list(payload["evidence_refs"]),
        tags=list(payload["tags"]),
        confidence=str(payload["confidence"]),
        phase=next_phase,
        supersedes=list(payload["supersedes"]),
        superseded_by=list(payload["superseded_by"]),
        summary=str(payload["summary"]),
        problem=str(payload["problem"]),
        success_criteria=list(payload["success_criteria"]),
        non_goals=list(payload["non_goals"]),
        why_now=str(payload["why_now"]),
        current_risks=list(payload["current_risks"]),
        supersession_notes="\n\n".join(
            part
            for part in [
                str(payload["supersession_notes"]),
                f"Phase changed from `{current_phase}` to `{next_phase}` because {args.reason.strip()}",
                *[f"Scope review: {item}" for item in _clean_list(args.scope_review_note)],
            ]
            if part
        ),
    )
    active_objective_text = render_active_objective_file(
        objective_id=objective_id,
        phase=next_phase,
        status="active",
        problem=str(payload["problem"]),
        success_criteria=list(payload["success_criteria"]),
        non_goals=list(payload["non_goals"]),
        why_now=str(payload["why_now"]),
        current_risks=list(payload["current_risks"]),
    )

    timestamp = timestamp_now().strftime("%Y-%m-%d-%H%M%S")
    assert_objective_phase_command_contract(
        "set-phase",
        provided_inputs={"project_id", "phase", "reason"},
        satisfied_guard_codes={
            "phase_supported",
            "phase_transition_prerequisites_met",
            "execution_phase_has_or_bootstraps_round",
        },
        write_targets={
            "durable:objective",
            "control:active-objective",
            "control:active-round",
            "memory:transition-event",
        },
        durable_owners={"memory:objective"},
        projection_owners={"control:active-objective", "control:active-round"},
        artifact_owners=set(),
        live_inspection_owners=set(),
    )
    _side_effects, event_id, event_path = apply_transition_transaction(
        project_id=args.project_id,
        writes=[
            {"path": objective_path, "text": objective_text, "label": "durable objective"},
            {"path": active_objective_path(args.project_id), "text": active_objective_text, "label": "active objective projection"},
        ],
        command_name="set-phase",
        title=f"Changed objective {objective_id} phase to {next_phase}",
        anchor=anchor,
        previous_state=f"objective `{objective_id}` was active in phase `{current_phase}`",
        next_state=f"objective `{objective_id}` remains active in phase `{next_phase}`",
        guards=render_objective_phase_guard_lines(
            "set-phase",
            context={"previous_phase": current_phase, "next_phase": next_phase},
        ),
        evidence=[args.reason.strip()] + _clean_list(args.evidence) + _clean_list(args.scope_review_note),
        target_ids=[objective_id],
        event_file_stem=f"{timestamp}-{objective_id}-set-phase-{next_phase}",
    )

    auto_round_result: dict[str, object] | None = None
    rewritten_rounds: list[dict[str, object]] = []
    if args.auto_open_round:
        auto_round_result = _run_open_round(args)
    elif args.rewrite_open_round:
        for round_path, round_meta, _round_sections in open_rounds:
            round_id = str(round_meta.get("id") or round_path.stem).strip()
            rewritten_rounds.append(_run_rewrite_open_round(args, round_id))

    print(
        json.dumps(
            {
                "project_id": args.project_id,
                "objective_id": objective_id,
                "previous_phase": current_phase,
                "phase": next_phase,
                "objective_path": str(objective_path),
                "active_objective_path": str(active_objective_path(args.project_id)),
                "transition_event_id": event_id,
                "transition_event_path": str(event_path),
                "auto_open_round": auto_round_result,
                "rewritten_rounds": rewritten_rounds,
            },
            ensure_ascii=True,
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
