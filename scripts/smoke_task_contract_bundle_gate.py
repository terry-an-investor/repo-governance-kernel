#!/usr/bin/env python3
from __future__ import annotations

import json

from round_control import load_round_file, locate_round_file
from smoke_fixture_lib import ROOT, init_fixture_repo, reset_fixture_repo, run_json


FIXTURE_PROJECT_ID = "__task_contract_bundle_gate_smoke__"
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
                "Validate governed bundle task-contract gating on a disposable fixture project.",
                "",
                "## Current State",
                "",
                f"- Project: `{FIXTURE_PROJECT_ID}`",
                "- Workspace id: `ws-task-contract-bundle-gate-smoke`",
                f"- Workspace root: `{FIXTURE_PROJECT_DIR.as_posix()}`",
                "- Branch: `master`",
                "- HEAD anchor: `task-contract-bundle-gate-smoke`",
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
                "- Prove bundle-backed adjudication close-chain execution fails closed until the task contract is resolved.",
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
                "- This fixture exists only to validate governed bundle task-contract hard gating.",
                "",
                "## Architecture Invariants",
                "",
                "- A governed close bundle must not bypass the same unresolved task-contract gate used by direct round promotion commands.",
                "- Adjudication follow-ups may execute only bounded bundle contracts, not special-case private rewrite logic.",
                "",
                "## Quality Bar",
                "",
                "- The fixture must prove one blocked bundle-backed close-chain attempt before task resolution and one successful close-chain after resolution.",
                "",
                "## Validation Rules",
                "",
                "- execute-adjudication-followups must surface the blocked task-contract reason instead of silently skipping or partially closing the round.",
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


def main() -> None:
    reset_fixture_repo(FIXTURE_PROJECT_DIR)
    try:
        write_fixture_files()
        init_fixture_repo(FIXTURE_PROJECT_DIR, commit_message="Initialize task-contract bundle-gate fixture")

        objective_result = run_json(
            "open_objective.py",
            "--project-id",
            FIXTURE_PROJECT_ID,
            "--title",
            "Disposable bundle-backed task-contract gate objective",
            "--problem",
            "Validate that governed bundle close chains do not bypass unresolved task contracts.",
            "--success-criterion",
            "execute-adjudication-followups blocks the governed close chain while the attached task contract is unresolved",
            "--success-criterion",
            "the same close chain succeeds after the task contract is completed",
            "--non-goal",
            "Preserve the disposable bundle-gate fixture after validation",
            "--why-now",
            "The high-level adjudication and bundle surfaces must inherit the same task-contract hard gate as the direct transition commands.",
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
            "The fixture needs one bounded execution round before it can prove bundle-backed task-contract gating honestly.",
            "--auto-open-round",
            "--round-title",
            "Disposable bundle-backed task-contract gate round",
            "--round-scope-item",
            "Prove execute-adjudication-followups plus round-close-chain fails closed until the attached task contract is resolved.",
            "--round-deliverable",
            "One disposable round that demonstrates governed close bundles inherit the task-contract hard gate.",
            "--round-validation-plan",
            "Execute one close-chain followup while the task is unresolved, then complete the task contract and rerun the same followup.",
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
            raise SystemExit("set-phase did not open the bundle-gate fixture round")
        patch_current_task(objective_id=objective_id, round_id=round_id)

        task_result = run_json(
            "open_task_contract.py",
            "--project-id",
            FIXTURE_PROJECT_ID,
            "--round-id",
            round_id,
            "--title",
            "Disposable bundle-gate task contract",
            "--summary",
            "One disposable task contract used to prove bundle-backed close chains do not bypass unresolved task authority.",
            "--intent",
            "Keep one unresolved execution contract attached so the governed close bundle must fail until the task contract is completed.",
            "--path",
            "src/",
            "--allowed-change",
            "Attempt one blocked execute-adjudication-followups close-chain before task resolution.",
            "--allowed-change",
            "Complete the task contract and rerun the same governed close-chain followup.",
            "--forbidden-change",
            "Do not bypass task resolution with direct durable rewrites or adjudication-only special cases.",
            "--completion-criterion",
            "The governed close-chain is blocked before task resolution and succeeds after the task contract is completed.",
        )
        task_contract_id = str(task_result["task_contract_id"])

        close_chain_payload = json.dumps(
            {
                "command": "round-close-chain",
                "round_id": round_id,
                "validation_pending_reason": "The disposable bundle-gate fixture is entering validation_pending through the governed close-chain bundle.",
                "captured_reason": "The governed close-chain fixture validated the round after the task contract was resolved.",
                "closed_reason": "The governed close-chain fixture finished and may close cleanly.",
                "validated_by": ["task-contract bundle-gate disposable smoke"],
            },
            ensure_ascii=True,
            sort_keys=True,
        )
        adjudication_result = run_json(
            "adjudicate_control_state.py",
            "--project-id",
            FIXTURE_PROJECT_ID,
            "--allow-clean",
            "--title",
            "Disposable bundle-backed task-contract gate adjudication",
            "--question",
            "Can execute-adjudication-followups run the governed round close chain honestly while one attached task contract is still unresolved?",
            "--verdict",
            "Run the bounded round-close-chain executor payload and keep the blocked result explicit until the task contract is resolved.",
            "--executor-followup-json",
            close_chain_payload,
            "--follow-up",
            "rerun audit-control-state",
        )
        adjudication_id = str(adjudication_result["adjudication_id"])

        blocked_execute = run_json(
            "execute_adjudication_followups.py",
            "--project-id",
            FIXTURE_PROJECT_ID,
            "--adjudication-id",
            adjudication_id,
        )
        blocked_entries = [str(item) for item in blocked_execute.get("blocked", [])]
        if len(blocked_entries) != 1:
            raise SystemExit("governed bundle close-chain did not produce exactly one blocked followup before task resolution")
        blocked_text = blocked_entries[0]
        if "unresolved draft or active task contracts remain attached" not in blocked_text:
            raise SystemExit("blocked governed bundle did not surface the unresolved task-contract reason")
        if task_contract_id not in blocked_text:
            raise SystemExit("blocked governed bundle output did not identify the unresolved task contract")

        blocked_round_path = locate_round_file(FIXTURE_PROJECT_ID, round_id)
        if blocked_round_path is None:
            raise SystemExit("bundle-gate fixture lost the round before task resolution")
        blocked_round_meta, _blocked_round_sections = load_round_file(blocked_round_path)
        if str(blocked_round_meta.get("status") or "").strip() != "active":
            raise SystemExit("blocked governed bundle changed the round status before task resolution")

        completed_task = run_json(
            "update_task_contract_status.py",
            "--project-id",
            FIXTURE_PROJECT_ID,
            "--task-contract-id",
            task_contract_id,
            "--status",
            "completed",
            "--reason",
            "The disposable bundle-gate proof finished the only attached execution contract.",
            "--resolution",
            "The governed close-chain was blocked until this task contract was completed.",
        )
        if str(completed_task.get("status") or "") != "completed":
            raise SystemExit("task contract did not move to completed")

        applied_execute = run_json(
            "execute_adjudication_followups.py",
            "--project-id",
            FIXTURE_PROJECT_ID,
            "--adjudication-id",
            adjudication_id,
        )
        if applied_execute.get("blocked"):
            raise SystemExit(f"governed bundle remained blocked after task resolution: {applied_execute['blocked']}")
        applied_entries = [str(item) for item in applied_execute.get("applied", [])]
        if not any("executed round-close-chain" in item for item in applied_entries):
            raise SystemExit("post-resolution execute-adjudication-followups did not execute the governed close-chain")

        closed_round_path = locate_round_file(FIXTURE_PROJECT_ID, round_id)
        if closed_round_path is None:
            raise SystemExit("bundle-gate fixture lost the round after task resolution")
        closed_round_meta, _closed_round_sections = load_round_file(closed_round_path)
        if str(closed_round_meta.get("status") or "").strip() != "closed":
            raise SystemExit("governed close-chain did not leave the round closed after task resolution")

        close_objective = run_json(
            "close_objective.py",
            "--project-id",
            FIXTURE_PROJECT_ID,
            "--objective-id",
            objective_id,
            "--closing-status",
            "closed",
            "--reason",
            "The disposable bundle-gate proof is complete and leaves no active objective behind.",
        )
        patch_current_task()

        final_audit = run_json("audit_control_state.py", "--project-id", FIXTURE_PROJECT_ID)
        if final_audit["summary"]["errors"] != 0:
            raise SystemExit("task-contract bundle-gate fixture audit reported errors")

        print(
            json.dumps(
                {
                    "project_id": FIXTURE_PROJECT_ID,
                    "objective_id": objective_id,
                    "round_id": round_id,
                    "task_contract_id": task_contract_id,
                    "adjudication_id": adjudication_id,
                    "blocked_bundle": "round-close-chain",
                    "blocked_message_contains_task_contract": task_contract_id in blocked_text,
                    "post_resolution_round_status": str(closed_round_meta.get("status") or ""),
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
