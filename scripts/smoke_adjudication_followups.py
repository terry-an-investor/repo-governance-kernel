#!/usr/bin/env python3
from __future__ import annotations

import json
import shutil
import subprocess
import sys
from pathlib import Path

from round_control import active_round_path, exception_ledger_path, load_active_round


ROOT = Path(__file__).resolve().parent.parent
SCRIPTS = ROOT / "scripts"
FIXTURE_PROJECT_ID = "__adjudication_followups_smoke__"
FIXTURE_PROJECT_DIR = ROOT / "projects" / FIXTURE_PROJECT_ID


def run_json(script_name: str, *args: str) -> dict:
    cmd = [sys.executable, str(SCRIPTS / script_name), *args]
    completed = subprocess.run(
        cmd,
        cwd=str(ROOT),
        capture_output=True,
        text=True,
        check=False,
    )
    if completed.returncode != 0:
        raise SystemExit(
            json.dumps(
                {
                    "script": script_name,
                    "args": list(args),
                    "returncode": completed.returncode,
                    "stdout": completed.stdout,
                    "stderr": completed.stderr,
                },
                ensure_ascii=True,
                indent=2,
            )
        )
    return json.loads(completed.stdout)


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
                "Validate adjudication follow-up execution on a disposable fixture project.",
                "",
                "## Current State",
                "",
                f"- Project: `{FIXTURE_PROJECT_ID}`",
                "- Workspace id: `ws-adjudication-followups-smoke`",
                f"- Workspace root: `{ROOT.as_posix()}`",
                "- Branch: `master`",
                "- HEAD anchor: `adjudication-followups-smoke`",
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
                "- Execute adjudication follow-ups against disposable durable control objects.",
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
                "- This fixture exists only to validate adjudication follow-up execution on disposable state.",
                "",
                "## Architecture Invariants",
                "",
                "- Adjudication should execute explicit follow-up contracts instead of guessing mutations.",
                "",
                "## Quality Bar",
                "",
                "- Follow-up execution must prove durable object rewrites, not just adjudication prose.",
                "",
                "## Validation Rules",
                "",
                "- The fixture must retire one exception contract, abandon one round, and open one successor round.",
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
    if FIXTURE_PROJECT_DIR.exists():
        shutil.rmtree(FIXTURE_PROJECT_DIR)

    try:
        write_fixture_files()
        objective_result = run_json(
            "open_objective.py",
            "--project-id",
            FIXTURE_PROJECT_ID,
            "--title",
            "Disposable adjudication follow-up smoke objective",
            "--problem",
            "Validate that adjudication can execute explicit durable control rewrites on a disposable project.",
            "--success-criterion",
            "structured follow-ups can abandon an existing round and retire an existing exception contract",
            "--success-criterion",
            "a successor round can be opened from adjudication bootstrap fields after those rewrites",
            "--non-goal",
            "Preserve any disposable fixture governance object after validation",
            "--why-now",
            "Adjudication is not real until it can drive durable object rewrites instead of only recording verdicts.",
            "--phase",
            "execution",
            "--path",
            "current/current-task.md",
        )
        objective_id = str(objective_result["objective_id"])
        patch_current_task(objective_id=objective_id)

        round_result = run_json(
            "open_round.py",
            "--project-id",
            FIXTURE_PROJECT_ID,
            "--title",
            "Disposable pre-adjudication round",
            "--scope-item",
            "Simulate an execution slice that adjudication will replace with a narrower successor round.",
            "--deliverable",
            "A disposable round that can be abandoned by adjudication follow-up execution.",
            "--validation-plan",
            "Record adjudication and execute its follow-up contract.",
            "--scope-path",
            "projects/__adjudication_followups_smoke__/",
        )
        initial_round_id = str(round_result["round_id"])
        patch_current_task(objective_id=objective_id, round_id=initial_round_id)

        exception_result = run_json(
            "activate_exception_contract.py",
            "--project-id",
            FIXTURE_PROJECT_ID,
            "--title",
            "Disposable adjudication exception contract",
            "--summary",
            "Temporary debt that adjudication should retire before the successor round starts.",
            "--reason",
            "The fixture needs one active exception contract so adjudication can execute a real retirement rewrite.",
            "--temporary-behavior",
            "Carry a disposable control workaround while the first round is still active.",
            "--risk",
            "Leaving the workaround active after adjudication would make the fixture dishonest.",
            "--exit-condition",
            "Retire the exception contract as part of adjudication follow-up execution.",
            "--owner-scope",
            "projects/__adjudication_followups_smoke__/",
            "--path",
            "projects/__adjudication_followups_smoke__/",
        )
        exception_contract_id = str(exception_result["exception_contract_id"])

        round_followup = "executor: " + json.dumps(
            {
                "command": "update-round-status",
                "round_id": initial_round_id,
                "status": "abandoned",
                "reason": "Adjudication selected a narrower successor round and retired the broader disposable slice.",
            },
            ensure_ascii=True,
        )
        exception_followup = "executor: " + json.dumps(
            {
                "command": "retire-exception-contract",
                "exception_contract_id": exception_contract_id,
                "reason": "Adjudication retired the disposable workaround before opening the successor round.",
            },
            ensure_ascii=True,
        )

        adjudication_result = run_json(
            "adjudicate_control_state.py",
            "--project-id",
            FIXTURE_PROJECT_ID,
            "--allow-clean",
            "--title",
            "Disposable adjudication follow-up execution smoke",
            "--question",
            "Can adjudication execute explicit durable rewrites instead of only recording a verdict?",
            "--verdict",
            "Abandon the broad pre-adjudication round, retire the temporary exception contract, and open a narrower successor round on the same objective.",
            "--retain-id",
            objective_id,
            "--invalidate-id",
            initial_round_id,
            "--invalidate-id",
            exception_contract_id,
            "--follow-up",
            round_followup,
            "--follow-up",
            exception_followup,
            "--follow-up",
            "open one bounded round for the adjudicated objective line",
            "--follow-up",
            "rerun audit-control-state",
            "--round-title",
            "Disposable successor round after adjudication",
            "--round-scope-item",
            "Validate that execute-adjudication-followups can open a successor round after durable rewrites.",
            "--round-scope-item",
            "Keep the same objective but replace the broader abandoned round with a narrower contract.",
            "--round-scope-path",
            "projects/__adjudication_followups_smoke__/",
            "--round-deliverable",
            "A successor round opened by adjudication follow-up execution.",
            "--round-validation-plan",
            "Run follow-up execution, patch current-task to the new active round, then rerun audit.",
            "--round-status-note",
            "Opened from adjudication bootstrap fields after abandoning the predecessor round.",
        )

        execute_result = run_json(
            "execute_adjudication_followups.py",
            "--project-id",
            FIXTURE_PROJECT_ID,
            "--adjudication-id",
            str(adjudication_result["adjudication_id"]),
        )
        if execute_result["blocked"]:
            raise SystemExit(f"adjudication follow-up execution reported blocked steps: {execute_result['blocked']}")

        new_round_preface, _new_round_sections = load_active_round(FIXTURE_PROJECT_ID)
        successor_round_id = str(new_round_preface.get("round id", "")).strip()
        if not successor_round_id:
            raise SystemExit("adjudication follow-up execution did not leave an active successor round")
        if successor_round_id == initial_round_id:
            raise SystemExit("adjudication follow-up execution left the abandoned round active")
        patch_current_task(objective_id=objective_id, round_id=successor_round_id)

        final_audit = run_json("audit_control_state.py", "--project-id", FIXTURE_PROJECT_ID)
        if final_audit["summary"]["errors"] != 0:
            raise SystemExit("adjudication follow-up fixture audit reported errors")

        ledger_text = exception_ledger_path(FIXTURE_PROJECT_ID).read_text(encoding="utf-8")
        if exception_contract_id not in ledger_text or "Retired" not in ledger_text:
            raise SystemExit("exception ledger did not reflect the retired contract after adjudication execution")
        if not active_round_path(FIXTURE_PROJECT_ID).exists():
            raise SystemExit("successor active-round projection missing after adjudication execution")

        print(
            json.dumps(
                {
                    "project_id": FIXTURE_PROJECT_ID,
                    "objective_id": objective_id,
                    "initial_round_id": initial_round_id,
                    "successor_round_id": successor_round_id,
                    "exception_contract_id": exception_contract_id,
                    "adjudication_id": str(adjudication_result["adjudication_id"]),
                    "applied": execute_result["applied"],
                    "fixture_audit": final_audit["status"],
                },
                ensure_ascii=True,
                indent=2,
            )
        )
    finally:
        if FIXTURE_PROJECT_DIR.exists():
            shutil.rmtree(FIXTURE_PROJECT_DIR)


if __name__ == "__main__":
    main()
