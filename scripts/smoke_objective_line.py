#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

from round_control import active_objective_path, load_objective_file, load_pivot_file, load_round_file, locate_round_file, pivot_log_path
from smoke_fixture_lib import ROOT, init_fixture_repo, reset_fixture_repo, run_json


FIXTURE_PROJECT_ID = "__objective_line_smoke__"
FIXTURE_PROJECT_DIR = ROOT / "state" / FIXTURE_PROJECT_ID


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
                "Validate soft-pivot and close-objective on a disposable fixture project.",
                "",
                "## Current State",
                "",
                f"- Project: `{FIXTURE_PROJECT_ID}`",
                "- Workspace id: `ws-objective-line-smoke`",
                f"- Workspace root: `{FIXTURE_PROJECT_DIR.as_posix()}`",
                "- Branch: `master`",
                "- HEAD anchor: `objective-line-smoke`",
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
                "- Exercise soft-pivot and close-objective on one disposable objective line.",
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
                "- This fixture exists only to validate objective-line control transitions on disposable state.",
                "",
                "## Architecture Invariants",
                "",
                "- A soft pivot must preserve objective identity while updating durable truth and projections together.",
                "- A closed objective must leave no fake active-objective projection behind.",
                "",
                "## Quality Bar",
                "",
                "- Objective-line transitions must be proven by executable state, not prose claims.",
                "",
                "## Validation Rules",
                "",
                "- The fixture must prove open-objective, record-soft-pivot, round closure, and close-objective.",
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
    filtered = []
    for line in text.splitlines():
        if line.startswith("- Objective id:"):
            continue
        if line.startswith("- Active round id:"):
            continue
        filtered.append(line)

    updated: list[str] = []
    for line in filtered:
        updated.append(line)
        if line == f"- Project: `{FIXTURE_PROJECT_ID}`":
            if objective_id:
                updated.append(f"- Objective id: `{objective_id}`")
            if round_id:
                updated.append(f"- Active round id: `{round_id}`")
    current_task_path.write_text("\n".join(updated) + "\n", encoding="utf-8")


def main() -> None:
    reset_fixture_repo(FIXTURE_PROJECT_DIR)

    try:
        write_fixture_files()
        init_fixture_repo(FIXTURE_PROJECT_DIR, commit_message="Initialize objective line fixture")
        objective_result = run_json(
            "open_objective.py",
            "--project-id",
            FIXTURE_PROJECT_ID,
            "--title",
            "Disposable objective-line smoke objective",
            "--problem",
            "Validate remaining objective-line transitions on a disposable project.",
            "--success-criterion",
            "soft pivot preserves the existing objective id",
            "--success-criterion",
            "close-objective removes the active-objective projection cleanly",
            "--non-goal",
            "Preserve any disposable fixture artifacts after validation",
            "--why-now",
            "Remaining objective-line commands must prove honest durable and projected control behavior.",
            "--phase",
            "exploration",
            "--path",
            "current/current-task.md",
        )
        objective_id = str(objective_result["objective_id"])
        patch_current_task(objective_id=objective_id)

        phase_result = run_json(
            "set_phase.py",
            "--project-id",
            FIXTURE_PROJECT_ID,
            "--objective-id",
            objective_id,
            "--phase",
            "execution",
            "--reason",
            "The fixture now needs an execution-phase framing so round and objective alignment rules are exercised honestly.",
            "--auto-open-round",
            "--round-title",
            "Fixture round for objective-line smoke",
            "--round-scope-item",
            "Exercise soft-pivot and close-objective against one disposable objective line.",
            "--round-deliverable",
            "A disposable round that proves objective-line transitions keep durable truth and projections aligned.",
            "--round-validation-plan",
            "Run soft pivot, close the round honestly, then close the objective.",
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
            raise SystemExit("set-phase did not auto-open the fixture round")
        patch_current_task(objective_id=objective_id, round_id=round_id)

        soft_pivot_result = run_json(
            "record_soft_pivot.py",
            "--project-id",
            FIXTURE_PROJECT_ID,
            "--objective-id",
            objective_id,
            "--trigger",
            "The fixture should prove that execution-phase refinement can preserve objective identity.",
            "--change-summary",
            "Refine the disposable objective around execution readiness without branching the objective line.",
            "--identity-rationale",
            "The problem and ownership line remain the same; only the execution framing and validation emphasis are changing.",
            "--title",
            "Disposable objective-line smoke objective in execution",
            "--summary",
            "Keep the same disposable objective id while moving into an execution-ready framing.",
            "--why-now",
            "The fixture now refines the already-executing objective without changing its identity.",
            "--risk",
            "The fixture could accidentally require a hard pivot if identity preservation is not explicit.",
            "--next-control-change",
            "Review the existing open round against the refined execution framing and then close it before objective closeout.",
            "--rewrite-open-round",
            "--round-deliverable",
            "A disposable round that proves objective-line transitions keep durable truth, projections, and round contract rewrites aligned.",
            "--round-validation-plan",
            "Run soft pivot, confirm the open round was rewritten, then close the round honestly before objective closeout.",
            "--round-status-note",
            "Rewritten during soft pivot so the open round stays aligned with the refined objective framing.",
            "--evidence",
            "The same disposable objective id is still the correct owner for the work.",
        )
        if str(soft_pivot_result["objective_id"]) != objective_id:
            raise SystemExit("soft pivot unexpectedly changed objective id")
        if not soft_pivot_result.get("round_rewrite"):
            raise SystemExit("soft pivot did not rewrite the open round")

        objective_meta, objective_sections = load_objective_file(Path(soft_pivot_result["objective_path"]))
        if str(objective_meta.get("id") or "") != objective_id:
            raise SystemExit("durable objective id changed during soft pivot")
        if str(objective_meta.get("phase") or "") != "execution":
            raise SystemExit("soft pivot did not update objective phase to execution")
        if "execution-ready framing" not in str(objective_sections.get("Summary", "")):
            raise SystemExit("soft pivot did not rewrite objective summary")

        pivot_meta, pivot_sections = load_pivot_file(Path(soft_pivot_result["pivot_path"]))
        if str(pivot_meta.get("objective_id") or "") != objective_id:
            raise SystemExit("soft pivot durable pivot does not point at the preserved objective id")
        if "same" not in str(pivot_sections.get("Identity Rationale", "")).lower():
            raise SystemExit("soft pivot pivot record is missing identity rationale content")
        round_path = locate_round_file(FIXTURE_PROJECT_ID, round_id)
        if round_path is None:
            raise SystemExit("fixture round disappeared during soft pivot rewrite")
        round_meta, round_sections = load_round_file(round_path)
        if "round contract rewrites aligned" not in str(round_sections.get("Deliverable", "")):
            raise SystemExit("soft pivot did not rewrite the round deliverable")
        if "confirm the open round was rewritten" not in str(round_sections.get("Validation Plan", "")):
            raise SystemExit("soft pivot did not rewrite the round validation plan")

        interim_audit = run_json("audit_control_state.py", "--project-id", FIXTURE_PROJECT_ID)
        if interim_audit["summary"]["errors"] != 0:
            raise SystemExit("objective-line fixture audit failed after soft pivot")

        run_json(
            "update_round_status.py",
            "--project-id",
            FIXTURE_PROJECT_ID,
            "--status",
            "validation_pending",
            "--reason",
            "fixture round finished after soft-pivot validation",
        )
        run_json(
            "update_round_status.py",
            "--project-id",
            FIXTURE_PROJECT_ID,
            "--status",
            "captured",
            "--reason",
            "objective-line fixture round validated",
            "--validated-by",
            "soft pivot and close-objective disposable smoke",
        )
        run_json(
            "update_round_status.py",
            "--project-id",
            FIXTURE_PROJECT_ID,
            "--status",
            "closed",
            "--reason",
            "fixture round completed before closing the disposable objective",
            "--round-id",
            round_id,
        )
        patch_current_task(objective_id=objective_id)

        close_result = run_json(
            "close_objective.py",
            "--project-id",
            FIXTURE_PROJECT_ID,
            "--objective-id",
            objective_id,
            "--closing-status",
            "closed",
            "--reason",
            "The disposable objective-line smoke finished and should leave no active mainline behind.",
        )
        patch_current_task()

        if active_objective_path(FIXTURE_PROJECT_ID).exists():
            raise SystemExit("close-objective left an active-objective projection behind")

        pivot_log_text = pivot_log_path(FIXTURE_PROJECT_ID).read_text(encoding="utf-8")
        if "_none recorded_" not in pivot_log_text.split("## Active Lineage", 1)[1]:
            raise SystemExit("pivot log still claims an active lineage after closing the objective")
        if objective_id not in pivot_log_text:
            raise SystemExit("pivot log lost the closed objective history")

        closed_meta, _closed_sections = load_objective_file(Path(close_result["objective_path"]))
        if str(closed_meta.get("status") or "") != "closed":
            raise SystemExit("close-objective did not update durable objective status")

        final_audit = run_json("audit_control_state.py", "--project-id", FIXTURE_PROJECT_ID)
        if final_audit["summary"]["errors"] != 0:
            raise SystemExit("objective-line fixture audit failed after objective closeout")

        print(
            json.dumps(
                {
                    "project_id": FIXTURE_PROJECT_ID,
                    "objective_id": objective_id,
                    "round_id": round_id,
                    "soft_pivot_id": str(soft_pivot_result["pivot_id"]),
                    "close_status": str(close_result["closing_status"]),
                    "fixture_audit": final_audit["status"],
                },
                ensure_ascii=True,
                indent=2,
            )
        )
    finally:
        reset_fixture_repo(FIXTURE_PROJECT_DIR)


if __name__ == "__main__":
    main()
