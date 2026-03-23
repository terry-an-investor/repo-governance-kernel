#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

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

        round_result = run_json(
            "open_round.py",
            "--project-id",
            FIXTURE_PROJECT_ID,
            "--title",
            "Fixture round for shared transition engine smoke",
            "--scope-item",
            "Validate shared transition writes on a disposable round.",
            "--deliverable",
            "A disposable round that exercises the shared transition engine through status changes.",
            "--validation-plan",
            "Drive the round through real status transitions before the hard pivot.",
            "--scope-path",
            "current/",
            "--scope-path",
            "control/",
            "--scope-path",
            "memory/",
        )
        round_id = str(round_result["round_id"])
        patch_current_task(objective_id=first_objective_id, round_id=round_id)

        run_json(
            "update_round_status.py",
            "--project-id",
            FIXTURE_PROJECT_ID,
            "--status",
            "blocked",
            "--reason",
            "fixture status transition smoke",
            "--blocker",
            "temporary fixture blocker",
        )
        run_json(
            "update_round_status.py",
            "--project-id",
            FIXTURE_PROJECT_ID,
            "--status",
            "active",
            "--reason",
            "resume fixture round after blocker smoke",
            "--clear-blockers",
        )
        run_json(
            "update_round_status.py",
            "--project-id",
            FIXTURE_PROJECT_ID,
            "--status",
            "validation_pending",
            "--reason",
            "fixture round ready for validation",
        )
        run_json(
            "update_round_status.py",
            "--project-id",
            FIXTURE_PROJECT_ID,
            "--status",
            "captured",
            "--reason",
            "fixture round validated",
            "--validated-by",
            "shared transition engine fixture path",
        )
        run_json(
            "update_round_status.py",
            "--project-id",
            FIXTURE_PROJECT_ID,
            "--status",
            "closed",
            "--reason",
            "fixture round completed before hard pivot",
            "--round-id",
            round_id,
        )

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
