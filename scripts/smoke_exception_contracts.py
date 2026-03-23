#!/usr/bin/env python3
from __future__ import annotations

import json
import shutil
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
SCRIPTS = ROOT / "scripts"
FIXTURE_PROJECT_ID = "__exception_contract_smoke__"
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


def write_fixture_current_task() -> None:
    current_task_path = FIXTURE_PROJECT_DIR / "current" / "current-task.md"
    current_task_path.parent.mkdir(parents=True, exist_ok=True)
    current_task_path.write_text(
        "\n".join(
            [
                "# Current Task",
                "",
                "## Goal",
                "",
                "Validate exception-contract transition commands on a disposable fixture project.",
                "",
                "## Current State",
                "",
                f"- Project: `{FIXTURE_PROJECT_ID}`",
                f"- Workspace id: `ws-exception-smoke`",
                f"- Workspace root: `{ROOT.as_posix()}`",
                "- Branch: `master`",
                "- HEAD anchor: `smoke-fixture`",
                "",
                "## Validated Facts",
                "",
                "- Fixture project is disposable and may be deleted after validation.",
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
                "- Run objective and exception-contract transition commands.",
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
                "- This project exists only to validate exception-contract command mechanics on a disposable fixture.",
                "",
                "## Architecture Invariants",
                "",
                "- Durable exception-contract records must project into the exception ledger.",
                "",
                "## Quality Bar",
                "",
                "- Command validation must exercise real file writes, not dry-run stubs.",
                "",
                "## Validation Rules",
                "",
                "- The fixture must prove activate, retire, and invalidate against durable files.",
                "",
                "## Forbidden Shortcuts",
                "",
                "- Do not keep the fixture after validation finishes.",
                "",
            ]
        )
        + "\n",
        encoding="utf-8",
    )


def patch_fixture_objective_anchor(objective_id: str) -> None:
    current_task_path = FIXTURE_PROJECT_DIR / "current" / "current-task.md"
    text = current_task_path.read_text(encoding="utf-8")
    anchor = "- Project: `__exception_contract_smoke__`\n"
    if "- Objective id:" in text:
        return
    text = text.replace(anchor, anchor + f"- Objective id: `{objective_id}`\n", 1)
    current_task_path.write_text(text, encoding="utf-8")


def main() -> None:
    if FIXTURE_PROJECT_DIR.exists():
        shutil.rmtree(FIXTURE_PROJECT_DIR)

    try:
        write_fixture_current_task()

        objective_result = run_json(
            "open_objective.py",
            "--project-id",
            FIXTURE_PROJECT_ID,
            "--title",
            "Disposable exception contract smoke objective",
            "--problem",
            "Validate exception-contract transitions end to end on a disposable project fixture.",
            "--success-criterion",
            "activate-exception-contract writes a durable active contract and projects the ledger",
            "--success-criterion",
            "retire-exception-contract moves the contract into the retired ledger section",
            "--success-criterion",
            "invalidate-exception-contract moves the contract into the invalidated ledger section",
            "--non-goal",
            "Preserve the fixture after validation",
            "--why-now",
            "The exception-contract command slice needs executable coverage before it can be trusted as a control primitive.",
            "--phase",
            "exploration",
            "--path",
            "current/current-task.md",
        )
        objective_id = str(objective_result["objective_id"])
        patch_fixture_objective_anchor(objective_id)

        first_contract = run_json(
            "activate_exception_contract.py",
            "--project-id",
            FIXTURE_PROJECT_ID,
            "--title",
            "Disposable retired exception contract",
            "--summary",
            "Exercise retirement of a real durable exception contract record on a disposable fixture.",
            "--reason",
            "The smoke fixture needs one temporary deviation that will be resolved in the same validation run.",
            "--temporary-behavior",
            "The fixture keeps one exception contract active only until the retire command is executed.",
            "--risk",
            "If retirement fails, the ledger projection will not represent historical exception debt honestly.",
            "--exit-condition",
            "The retire-exception-contract command moves the contract into the retired ledger section.",
            "--owner-scope",
            "projects/__exception_contract_smoke__/control/exception-ledger.md",
            "--path",
            "projects/__exception_contract_smoke__/control/exception-ledger.md",
        )
        first_contract_id = str(first_contract["exception_contract_id"])

        retired_result = run_json(
            "retire_exception_contract.py",
            "--project-id",
            FIXTURE_PROJECT_ID,
            "--exception-contract-id",
            first_contract_id,
            "--reason",
            "retire command executed successfully inside the disposable fixture",
            "--evidence",
            "fixture smoke path",
        )

        second_contract = run_json(
            "activate_exception_contract.py",
            "--project-id",
            FIXTURE_PROJECT_ID,
            "--title",
            "Disposable invalidated exception contract",
            "--summary",
            "Exercise invalidation of a durable exception contract record on a disposable fixture.",
            "--reason",
            "The smoke fixture needs one active exception contract that can be invalidated without relying on a project pivot.",
            "--temporary-behavior",
            "The fixture keeps one exception contract active only until the invalidate command is executed.",
            "--risk",
            "If invalidation fails, the ledger projection will blur resolved and invalidated control debt.",
            "--exit-condition",
            "The invalidate-exception-contract command moves the contract into the invalidated ledger section.",
            "--owner-scope",
            "projects/__exception_contract_smoke__/control/exception-ledger.md",
            "--path",
            "projects/__exception_contract_smoke__/control/exception-ledger.md",
        )
        second_contract_id = str(second_contract["exception_contract_id"])

        invalidated_result = run_json(
            "invalidate_exception_contract.py",
            "--project-id",
            FIXTURE_PROJECT_ID,
            "--exception-contract-id",
            second_contract_id,
            "--reason",
            "invalidate command executed successfully inside the disposable fixture",
            "--evidence",
            "fixture smoke path",
        )

        ledger_text = (FIXTURE_PROJECT_DIR / "control" / "exception-ledger.md").read_text(encoding="utf-8")
        if first_contract_id not in ledger_text:
            raise SystemExit("retired exception contract missing from fixture ledger")
        if second_contract_id not in ledger_text:
            raise SystemExit("invalidated exception contract missing from fixture ledger")
        if "## Retired" not in ledger_text or "## Invalidated" not in ledger_text:
            raise SystemExit("fixture ledger missing expected sections")

        fixture_audit = run_json("audit_control_state.py", "--project-id", FIXTURE_PROJECT_ID)
        if fixture_audit["summary"]["errors"] != 0:
            raise SystemExit("fixture control audit reported errors")

        print(
            json.dumps(
                {
                    "project_id": FIXTURE_PROJECT_ID,
                    "objective_id": objective_id,
                    "retired_contract_id": retired_result["exception_contract_id"],
                    "invalidated_contract_id": invalidated_result["exception_contract_id"],
                    "fixture_audit": fixture_audit["status"],
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
