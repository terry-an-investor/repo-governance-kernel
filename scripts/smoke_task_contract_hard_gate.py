#!/usr/bin/env python3
from __future__ import annotations

import json
import subprocess
import sys

from smoke_fixture_lib import ROOT, SCRIPTS, init_fixture_repo, reset_fixture_repo, run_json


FIXTURE_PROJECT_ID = "__task_contract_hard_gate_smoke__"
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
                "Validate task-contract hard-gate behavior on a disposable fixture project.",
                "",
                "## Current State",
                "",
                f"- Project: `{FIXTURE_PROJECT_ID}`",
                "- Workspace id: `ws-task-contract-hard-gate-smoke`",
                f"- Workspace root: `{FIXTURE_PROJECT_DIR.as_posix()}`",
                "- Branch: `master`",
                "- HEAD anchor: `task-contract-hard-gate-smoke`",
                "",
                "## Validated Facts",
                "",
                "- Fixture project is disposable and should be deleted after validation.",
                "",
                "## Active Risks",
                "",
                "- None recorded yet.",
                "",
                "## Next Steps",
                "",
                "- Prove unresolved task contracts block round promotion until the task is resolved.",
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
                "- This fixture exists only to validate task-contract hard-gate behavior.",
                "",
                "## Architecture Invariants",
                "",
                "- A round must not promote into validation_pending while unresolved task contracts still authorize execution work.",
                "- Closing a round should only happen after the attached task contract is resolved.",
                "",
                "## Quality Bar",
                "",
                "- Promotion and closure claims must be proven by command behavior, not prose.",
                "",
                "## Validation Rules",
                "",
                "- The fixture must prove one blocked promotion attempt before task resolution and one successful close chain after task resolution.",
                "",
                "## Forbidden Shortcuts",
                "",
                "- Do not keep the fixture after validation.",
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
    source_dir = FIXTURE_PROJECT_DIR / "src"
    source_dir.mkdir(parents=True, exist_ok=True)
    (source_dir / "tracked.txt").write_text("baseline\n", encoding="utf-8")


def patch_current_task(objective_id: str = "", round_id: str = "") -> None:
    current_task_path = FIXTURE_PROJECT_DIR / "current" / "current-task.md"
    text = current_task_path.read_text(encoding="utf-8")
    filtered: list[str] = []
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


def run_expected_failure(script_name: str, *args: str) -> str:
    completed = subprocess.run(
        [sys.executable, str(SCRIPTS / script_name), *args],
        cwd=str(ROOT),
        capture_output=True,
        text=True,
        check=False,
    )
    if completed.returncode == 0:
        raise SystemExit(f"{script_name} unexpectedly succeeded")
    payload = (completed.stderr or completed.stdout).strip()
    if not payload:
        raise SystemExit(f"{script_name} failed without any error text")
    return payload


def main() -> None:
    reset_fixture_repo(FIXTURE_PROJECT_DIR)
    try:
        write_fixture_files()
        init_fixture_repo(FIXTURE_PROJECT_DIR, commit_message="Initialize task-contract hard-gate fixture")

        objective_result = run_json(
            "open_objective.py",
            "--project-id",
            FIXTURE_PROJECT_ID,
            "--title",
            "Disposable task-contract hard-gate objective",
            "--problem",
            "Validate that unresolved task contracts block dishonest round promotion.",
            "--success-criterion",
            "validation_pending is blocked while the attached task contract is unresolved",
            "--success-criterion",
            "the close chain succeeds after the task contract is completed",
            "--non-goal",
            "Keep the fixture after validation",
            "--why-now",
            "Task contracts should become a real execution gate rather than a durable note.",
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
            "The fixture needs one bounded execution round before it can prove task-contract promotion gating honestly.",
            "--auto-open-round",
            "--round-title",
            "Disposable task-contract hard-gate round",
            "--round-scope-item",
            "Prove unresolved task contracts block round promotion until resolution.",
            "--round-deliverable",
            "One disposable round that demonstrates task-contract hard-gate behavior across validation_pending and close-chain transitions.",
            "--round-validation-plan",
            "Attempt validation_pending before task resolution, then complete the task contract and rerun the close chain.",
            "--round-scope-path",
            "src/",
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
            raise SystemExit("set-phase did not open the hard-gate fixture round")
        patch_current_task(objective_id=objective_id, round_id=round_id)

        task_result = run_json(
            "open_task_contract.py",
            "--project-id",
            FIXTURE_PROJECT_ID,
            "--round-id",
            round_id,
            "--title",
            "Disposable hard-gate fixture task",
            "--summary",
            "One disposable task contract used to prove round promotion blocks until task resolution.",
            "--intent",
            "Keep one unresolved execution contract attached to the round so validation_pending must fail until the task is completed.",
            "--path",
            "src/",
            "--allowed-change",
            "Attempt one blocked round promotion before completing the task contract.",
            "--allowed-change",
            "Complete the task contract and rerun the honest round close chain.",
            "--forbidden-change",
            "Do not bypass task resolution by rewriting the round or objective dishonestly.",
            "--completion-criterion",
            "validation_pending fails before task resolution and the close chain succeeds after completion.",
        )
        task_contract_id = str(task_result["task_contract_id"])

        blocked_text = run_expected_failure(
            "update_round_status.py",
            "--project-id",
            FIXTURE_PROJECT_ID,
            "--round-id",
            round_id,
            "--status",
            "validation_pending",
            "--reason",
            "This should fail because the attached task contract still authorizes unresolved execution work.",
        )
        if "unresolved draft or active task contracts remain attached" not in blocked_text:
            raise SystemExit("round promotion did not fail for the expected unresolved-task reason")
        if task_contract_id not in blocked_text:
            raise SystemExit("blocked promotion output did not identify the unresolved task contract")

        completed_task = run_json(
            "update_task_contract_status.py",
            "--project-id",
            FIXTURE_PROJECT_ID,
            "--task-contract-id",
            task_contract_id,
            "--status",
            "completed",
            "--reason",
            "The disposable hard-gate proof finished the only attached execution contract.",
            "--resolution",
            "The fixture proved validation_pending was blocked until this task contract was completed.",
        )
        if str(completed_task.get("status") or "") != "completed":
            raise SystemExit("task contract did not move to completed")

        validation_pending = run_json(
            "update_round_status.py",
            "--project-id",
            FIXTURE_PROJECT_ID,
            "--round-id",
            round_id,
            "--status",
            "validation_pending",
            "--reason",
            "The attached task contract is now resolved, so the round may enter validation_pending honestly.",
        )
        captured = run_json(
            "update_round_status.py",
            "--project-id",
            FIXTURE_PROJECT_ID,
            "--round-id",
            round_id,
            "--status",
            "captured",
            "--reason",
            "The disposable hard-gate proof validated the round after task resolution.",
            "--validated-by",
            "task-contract hard-gate disposable smoke",
        )
        closed = run_json(
            "update_round_status.py",
            "--project-id",
            FIXTURE_PROJECT_ID,
            "--round-id",
            round_id,
            "--status",
            "closed",
            "--reason",
            "The disposable hard-gate round is captured and can close cleanly.",
        )
        close_objective = run_json(
            "close_objective.py",
            "--project-id",
            FIXTURE_PROJECT_ID,
            "--objective-id",
            objective_id,
            "--closing-status",
            "closed",
            "--reason",
            "The disposable hard-gate proof is complete and should leave no active objective behind.",
        )
        patch_current_task()

        final_audit = run_json("audit_control_state.py", "--project-id", FIXTURE_PROJECT_ID)
        if final_audit["summary"]["errors"] != 0:
            raise SystemExit("task-contract hard-gate fixture audit reported errors")

        print(
            json.dumps(
                {
                    "project_id": FIXTURE_PROJECT_ID,
                    "objective_id": objective_id,
                    "round_id": round_id,
                    "task_contract_id": task_contract_id,
                    "blocked_transition": "validation_pending",
                    "blocked_message_contains_task_contract": task_contract_id in blocked_text,
                    "post_resolution_statuses": {
                        "validation_pending": str(validation_pending["status"]),
                        "captured": str(captured["status"]),
                        "closed": str(closed["status"]),
                    },
                    "objective_close_status": str(close_objective["closing_status"]),
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
