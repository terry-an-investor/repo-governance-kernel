#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

from executor_runtime import run_registry_command_json
from smoke_fixture_lib import ROOT, init_fixture_repo, reset_fixture_repo, run_json


FIXTURE_PROJECT_ID = "__transition_engine_smoke__"
FIXTURE_PROJECT_DIR = ROOT / "projects" / FIXTURE_PROJECT_ID


def write_fixture_files() -> None:
    current_task_path = FIXTURE_PROJECT_DIR / "current" / "current-task.md"
    current_task_path.parent.mkdir(parents=True, exist_ok=True)
    current_task_path.write_text(
        "\n".join(
            [
                "# Current Task",
                "",
                "## Goal",
                "",
                "Validate shared transition-engine command behavior on a disposable fixture project.",
                "",
                "## Current State",
                "",
                f"- Project: `{FIXTURE_PROJECT_ID}`",
                "- Workspace id: `ws-transition-engine-smoke`",
                f"- Workspace root: `{FIXTURE_PROJECT_DIR.as_posix()}`",
                "- Branch: `master`",
                "- HEAD anchor: `transition-engine-smoke`",
                "",
                "## Validated Facts",
                "",
                "- Fixture project is disposable and should be deleted after validation.",
                "",
                "## Important Files",
                "",
                f"- `{current_task_path.as_posix()}`",
                "",
                "## Active Risks",
                "",
                "- None recorded yet.",
                "",
                "## Next Steps",
                "",
                "- Run objective, round, status, and hard-pivot transitions.",
                "",
            ]
        )
        + "\n",
        encoding="utf-8",
    )

    blockers_path = FIXTURE_PROJECT_DIR / "current" / "blockers.md"
    blockers_path.parent.mkdir(parents=True, exist_ok=True)
    blockers_path.write_text(
        "# Blockers\n\n## Active\n\n- None recorded yet.\n\n## Waiting\n\n- None recorded yet.\n\n## Cleared\n\n- None recorded yet.\n",
        encoding="utf-8",
    )

    constitution_path = FIXTURE_PROJECT_DIR / "control" / "constitution.md"
    constitution_path.parent.mkdir(parents=True, exist_ok=True)
    constitution_path.write_text(
        "\n".join(
            [
                "# Constitution",
                "",
                "## Product Boundaries",
                "",
                "- This fixture exists only to validate the shared transition engine on disposable control objects.",
                "",
                "## Architecture Invariants",
                "",
                "- Objective, round, and pivot projections must follow durable writes honestly.",
                "",
                "## Quality Bar",
                "",
                "- Transition regressions must be caught by executable fixture state, not prose claims.",
                "",
                "## Validation Rules",
                "",
                "- The fixture must prove open-objective, open-round, update-round-status, and record-hard-pivot.",
                "",
                "## Forbidden Shortcuts",
                "",
                "- Do not preserve the fixture after validation.",
                "",
            ]
        )
        + "\n",
        encoding="utf-8",
    )

    ledger_path = FIXTURE_PROJECT_DIR / "control" / "exception-ledger.md"
    ledger_path.parent.mkdir(parents=True, exist_ok=True)
    ledger_path.write_text(
        "# Exception Ledger\n\n## Active\n\n- None recorded yet.\n\n## Retired\n\n- None recorded yet.\n\n## Invalidated\n\n- None recorded yet.\n",
        encoding="utf-8",
    )


def patch_current_task(objective_id: str = "", round_id: str = "") -> None:
    current_task_path = FIXTURE_PROJECT_DIR / "current" / "current-task.md"
    text = current_task_path.read_text(encoding="utf-8")
    lines = text.splitlines()
    filtered: list[str] = []
    for line in lines:
        if line.startswith("- Objective id:"):
            continue
        if line.startswith("- Active round id:"):
            continue
        filtered.append(line)

    inserted: list[str] = []
    for line in filtered:
        inserted.append(line)
        if line == f"- Project: `{FIXTURE_PROJECT_ID}`":
            if objective_id:
                inserted.append(f"- Objective id: `{objective_id}`")
            if round_id:
                inserted.append(f"- Active round id: `{round_id}`")
    current_task_path.write_text("\n".join(inserted) + "\n", encoding="utf-8")


def main() -> None:
    reset_fixture_repo(FIXTURE_PROJECT_DIR)

    try:
        write_fixture_files()
        init_fixture_repo(FIXTURE_PROJECT_DIR, commit_message="Initialize transition engine fixture")
        objective_result = run_json(
            "open_objective.py",
            "--project-id",
            FIXTURE_PROJECT_ID,
            "--title",
            "Initial transition engine smoke objective",
            "--problem",
            "Validate transition transaction behavior on one disposable objective line.",
            "--success-criterion",
            "open-objective and record-hard-pivot keep pivot-log projection aligned",
            "--success-criterion",
            "open-round and update-round-status preserve round projection honesty",
            "--non-goal",
            "Keep any fixture control object after validation",
            "--why-now",
            "Shared transition primitives must prove they preserve projection order and transition events.",
            "--phase",
            "exploration",
            "--path",
            "current/current-task.md",
        )
        first_objective_id = str(objective_result["objective_id"])
        patch_current_task(objective_id=first_objective_id)

        phase_result = run_json(
            "set_phase.py",
            "--project-id",
            FIXTURE_PROJECT_ID,
            "--objective-id",
            first_objective_id,
            "--phase",
            "execution",
            "--reason",
            "The shared transition engine fixture needs a bounded execution contract before round-state transitions are exercised.",
            "--auto-open-round",
            "--round-title",
            "Fixture round for shared transition engine smoke",
            "--round-scope-item",
            "Validate shared transition writes on a disposable round.",
            "--round-deliverable",
            "A disposable round that exercises the shared transition engine through status changes.",
            "--round-validation-plan",
            "Drive the round through real status transitions before the hard pivot.",
            "--round-scope-path",
            "current/",
            "--round-scope-path",
            "control/",
            "--round-scope-path",
            "memory/",
        )
        auto_open_round = phase_result.get("auto_open_round") or {}
        round_id = str(auto_open_round.get("round_id") or "")
        if not round_id:
            raise SystemExit("set-phase did not auto-open the transition-engine fixture round")
        patch_current_task(objective_id=first_objective_id, round_id=round_id)

        blocked_result = run_registry_command_json(
            FIXTURE_PROJECT_ID,
            {
                "round_id": round_id,
                "status": "blocked",
                "reason": "fixture status transition smoke",
                "blocker": ["temporary fixture blocker"],
            },
            "update-round-status",
            failure_message="fixture blocked status transition failed",
        )
        if str(blocked_result.get("status") or "").strip() != "blocked":
            raise SystemExit("shared runtime did not drive the fixture round into blocked status")

        active_result = run_registry_command_json(
            FIXTURE_PROJECT_ID,
            {
                "round_id": round_id,
                "status": "active",
                "reason": "resume fixture round after blocker smoke",
                "clear_blockers": True,
            },
            "update-round-status",
            failure_message="fixture active status transition failed",
        )
        if str(active_result.get("status") or "").strip() != "active":
            raise SystemExit("shared runtime did not resume the fixture round to active status")

        validation_pending_result = run_registry_command_json(
            FIXTURE_PROJECT_ID,
            {
                "round_id": round_id,
                "status": "validation_pending",
                "reason": "fixture round ready for validation",
            },
            "update-round-status",
            failure_message="fixture validation-pending status transition failed",
        )
        if str(validation_pending_result.get("status") or "").strip() != "validation_pending":
            raise SystemExit("shared runtime did not move the fixture round into validation_pending")

        captured_result = run_registry_command_json(
            FIXTURE_PROJECT_ID,
            {
                "round_id": round_id,
                "status": "captured",
                "reason": "fixture round validated",
                "validated_by": ["shared transition engine fixture path"],
            },
            "update-round-status",
            failure_message="fixture captured status transition failed",
        )
        if str(captured_result.get("status") or "").strip() != "captured":
            raise SystemExit("shared runtime did not capture the fixture round")

        closed_result = run_registry_command_json(
            FIXTURE_PROJECT_ID,
            {
                "round_id": round_id,
                "status": "closed",
                "reason": "fixture round completed before hard pivot",
            },
            "update-round-status",
            failure_message="fixture closed status transition failed",
        )
        if str(closed_result.get("status") or "").strip() != "closed":
            raise SystemExit("shared runtime did not close the fixture round")

        pivot_result = run_json(
            "record_hard_pivot.py",
            "--project-id",
            FIXTURE_PROJECT_ID,
            "--title",
            "Post-pivot transition engine smoke objective",
            "--problem",
            "Validate that hard pivots also use the shared transition engine without projection drift.",
            "--success-criterion",
            "durable superseded objective, new objective, and pivot stay projection-aligned",
            "--success-criterion",
            "pivot-log reflects the new active objective after the transaction",
            "--non-goal",
            "Preserve the previous objective as active",
            "--why-now",
            "The shared transition engine should cover remaining objective-line file writes too.",
            "--phase",
            "exploration",
            "--trigger",
            "The fixture needs a second objective line to prove shared transition writes across pivot boundaries.",
            "--path",
            "current/current-task.md",
        )
        patch_current_task(objective_id=str(pivot_result["objective_id"]))

        fixture_audit = run_json("audit_control_state.py", "--project-id", FIXTURE_PROJECT_ID)
        if fixture_audit["summary"]["errors"] != 0:
            raise SystemExit("transition-engine fixture control audit reported errors")

        print(
            json.dumps(
                {
                    "project_id": FIXTURE_PROJECT_ID,
                    "initial_objective_id": first_objective_id,
                    "round_id": round_id,
                    "pivot_objective_id": str(pivot_result["objective_id"]),
                    "pivot_id": str(pivot_result["pivot_id"]),
                    "fixture_audit": fixture_audit["status"],
                },
                ensure_ascii=True,
                indent=2,
            )
        )
    finally:
        reset_fixture_repo(FIXTURE_PROJECT_DIR)


if __name__ == "__main__":
    main()
