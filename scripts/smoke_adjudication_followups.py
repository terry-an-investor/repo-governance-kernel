#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

from round_control import (
    active_round_path,
    exception_ledger_path,
    load_active_round,
    load_exception_contract_file,
    load_objective_file,
    load_round_file,
    load_task_contract_file,
    find_rounds,
    locate_exception_contract_file,
    locate_round_file,
    locate_task_contract_file,
    parse_bullet_list,
)
from smoke_fixture_lib import ROOT, init_fixture_repo, reset_fixture_repo, run_json


FIXTURE_PROJECT_ID = "__adjudication_followups_smoke__"
FIXTURE_PROJECT_DIR = ROOT / "projects" / FIXTURE_PROJECT_ID
PHASE_BUNDLE_FIXTURE_PROJECT_ID = "__adjudication_phase_bundle_smoke__"
PHASE_BUNDLE_FIXTURE_PROJECT_DIR = ROOT / "projects" / PHASE_BUNDLE_FIXTURE_PROJECT_ID


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
                f"- Workspace root: `{FIXTURE_PROJECT_DIR.as_posix()}`",
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
                "- The fixture must retire one exception contract, close one round through a structured close chain, and open one successor round.",
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


def write_phase_bundle_fixture_files() -> None:
    current_task_path = PHASE_BUNDLE_FIXTURE_PROJECT_DIR / "current" / "current-task.md"
    current_task_path.parent.mkdir(parents=True, exist_ok=True)
    current_task_path.write_text(
        "\n".join(
            [
                "# Current Task",
                "",
                "## Goal",
                "",
                "Validate adjudication-driven execution bootstrap on a disposable fixture project.",
                "",
                "## Current State",
                "",
                f"- Project: `{PHASE_BUNDLE_FIXTURE_PROJECT_ID}`",
                "- Workspace id: `ws-adjudication-phase-bundle-smoke`",
                f"- Workspace root: `{PHASE_BUNDLE_FIXTURE_PROJECT_DIR.as_posix()}`",
                "- Branch: `master`",
                "- HEAD anchor: `adjudication-phase-bundle-smoke`",
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
                "- Use adjudication to enter execution and bootstrap one bounded round through the plan compiler.",
                "",
            ]
        )
        + "\n",
        encoding="utf-8",
    )
    blockers_path = PHASE_BUNDLE_FIXTURE_PROJECT_DIR / "current" / "blockers.md"
    blockers_path.parent.mkdir(parents=True, exist_ok=True)
    blockers_path.write_text(
        "# Blockers\n\n## Active\n\n- None recorded yet.\n\n## Waiting\n\n- None recorded yet.\n\n## Cleared\n\n- None recorded yet.\n",
        encoding="utf-8",
    )
    constitution_path = PHASE_BUNDLE_FIXTURE_PROJECT_DIR / "control" / "constitution.md"
    constitution_path.parent.mkdir(parents=True, exist_ok=True)
    constitution_path.write_text(
        "\n".join(
            [
                "# Constitution",
                "",
                "## Product Boundaries",
                "",
                "- This fixture exists only to validate adjudication-driven phase-side-effect bundles.",
                "",
                "## Architecture Invariants",
                "",
                "- Execution bootstrap should reuse existing set-phase and round bootstrap contracts.",
                "",
                "## Quality Bar",
                "",
                "- Adjudication must compile phase-side effects from durable truth instead of hand-authored payload JSON.",
                "",
                "## Validation Rules",
                "",
                "- The fixture must enter execution and open one bounded round through the bounded plan compiler path.",
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
    ledger_path = PHASE_BUNDLE_FIXTURE_PROJECT_DIR / "control" / "exception-ledger.md"
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
    reset_fixture_repo(FIXTURE_PROJECT_DIR)

    try:
        write_fixture_files()
        init_fixture_repo(FIXTURE_PROJECT_DIR, commit_message="Initialize adjudication followups fixture")
        objective_result = run_json(
            "open_objective.py",
            "--project-id",
            FIXTURE_PROJECT_ID,
            "--title",
            "Disposable adjudication follow-up smoke objective",
            "--problem",
            "Validate that adjudication can execute explicit durable control rewrites on a disposable project.",
            "--success-criterion",
            "structured follow-ups can close an existing round through a governed close chain and retire an existing exception contract",
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
            "A disposable round that can be closed by adjudication follow-up execution.",
            "--validation-plan",
            "Record adjudication and execute its follow-up contract.",
            "--scope-path",
            "current/",
            "--scope-path",
            "control/",
            "--scope-path",
            "memory/",
        )
        initial_round_id = str(round_result["round_id"])
        patch_current_task(objective_id=objective_id, round_id=initial_round_id)

        first_task_contract_result = run_json(
            "open_task_contract.py",
            "--project-id",
            FIXTURE_PROJECT_ID,
            "--round-id",
            initial_round_id,
            "--title",
            "Disposable first pre-close task contract",
            "--summary",
            "Disposable task contract that adjudication should invalidate before closing the predecessor round.",
            "--intent",
            "Prove that adjudication can invalidate open task contracts through the bounded plan compiler path.",
            "--path",
            "current/current-task.md",
            "--allowed-change",
            "Rewrite durable control files needed to validate adjudication follow-up execution.",
            "--forbidden-change",
            "Leave the predecessor round open after adjudication closes it.",
            "--completion-criterion",
            "The contract is invalidated before the predecessor round leaves open status.",
            "--risk",
            "If the contract stays open, round close-chain enforcement should block honestly.",
        )
        first_task_contract_id = str(first_task_contract_result["task_contract_id"])

        second_task_contract_result = run_json(
            "open_task_contract.py",
            "--project-id",
            FIXTURE_PROJECT_ID,
            "--round-id",
            initial_round_id,
            "--title",
            "Disposable second pre-close task contract",
            "--summary",
            "Second disposable task contract used to prove multi-object task-contract invalidation fanout.",
            "--intent",
            "Prove that one adjudication plan family can fan out across multiple open task contracts.",
            "--path",
            "control/constitution.md",
            "--allowed-change",
            "Rewrite durable control contracts needed for adjudication smoke coverage.",
            "--forbidden-change",
            "Carry private executor semantics outside the registry.",
            "--completion-criterion",
            "The contract is invalidated through the same plan family as the first contract.",
            "--risk",
            "If only one contract invalidates, the plan family fanout is not real.",
        )
        second_task_contract_id = str(second_task_contract_result["task_contract_id"])

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
            "current/",
            "--path",
            "current/",
        )
        exception_contract_id = str(exception_result["exception_contract_id"])

        rewrite_then_close_plan = json.dumps(
            {
                "plan_type": "rewrite-open-round-then-close-chain",
                "rewrite_reason": "Adjudication narrows the active round before it is closed so the durable round contract matches the verdict.",
                "title": "Disposable predecessor round rewritten by adjudication",
                "summary": "Adjudication narrows the predecessor round to one explicit validation slice before closure.",
                "scope_item": [
                    "Prove that registry-owned rewrite field semantics can replace the predecessor round scope before close-chain execution.",
                ],
                "scope_path": [
                    "current/",
                    "control/",
                    "memory/",
                    "memory/transition-events/",
                ],
                "deliverable": "A narrowed predecessor round that was rewritten by adjudication before closure.",
                "validation_plan": "Rewrite the predecessor round, then close it through the governed close chain.",
                "risk": [
                    "Leaving the predecessor round broad would make the adjudication close-chain claim dishonest.",
                ],
                "blocker": [
                    "The predecessor round must close before the successor adjudicated round opens.",
                ],
                "replace_scope_items": True,
                "replace_scope_paths": True,
                "replace_risks": True,
                "replace_blockers": True,
                "validation_pending_reason": "Adjudication accepted the disposable slice for final validation before closing it.",
                "captured_reason": "Adjudication confirmed the disposable slice was validated and can be captured before closure.",
                "closed_reason": "Adjudication closed the predecessor round before opening the narrower successor slice.",
                "validated_by": [
                    "Disposable adjudication fixture close-chain validation",
                ],
                "clear_blockers": True,
                "status_note": [
                    "Adjudication rewrote the predecessor round before closure.",
                ],
            },
            ensure_ascii=True,
            sort_keys=True,
        )
        invalidate_task_contract_plan = json.dumps(
            {
                "plan_type": "invalidate-invalidated-task-contracts",
                "reason": "Adjudication invalidated open task contracts before closing the predecessor round.",
                "risk": [
                    "If open task contracts survive, the round close-chain should stay blocked.",
                ],
                "status_note": [
                    "Invalidated through adjudication plan fanout before round close-chain execution.",
                ],
            },
            ensure_ascii=True,
            sort_keys=True,
        )
        retire_exception_plan = json.dumps(
            {
                "plan_type": "retire-invalidated-exception-contracts",
                "reason": "Adjudication retired the disposable workaround before opening the successor round.",
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
            "Disposable adjudication follow-up execution smoke",
            "--question",
            "Can adjudication execute explicit durable rewrites instead of only recording a verdict?",
            "--verdict",
            "Close the broad pre-adjudication round through an explicit close chain, retire the temporary exception contract, and open a narrower successor round on the same objective.",
            "--retain-id",
            objective_id,
            "--invalidate-id",
            first_task_contract_id,
            "--invalidate-id",
            second_task_contract_id,
            "--invalidate-id",
            initial_round_id,
            "--invalidate-id",
            exception_contract_id,
            "--executor-plan-json",
            invalidate_task_contract_plan,
            "--executor-plan-json",
            rewrite_then_close_plan,
            "--executor-plan-json",
            retire_exception_plan,
            "--follow-up",
            "open one bounded round for the adjudicated objective line",
            "--follow-up",
            "rerun audit-control-state",
            "--round-title",
            "Disposable successor round after adjudication",
            "--round-scope-item",
            "Validate that execute-adjudication-followups can open a successor round after durable rewrites.",
            "--round-scope-item",
            "Keep the same objective but replace the broader closed round with a narrower contract.",
            "--round-scope-path",
            "current/",
            "--round-scope-path",
            "control/",
            "--round-scope-path",
            "memory/",
            "--round-deliverable",
            "A successor round opened by adjudication follow-up execution.",
            "--round-validation-plan",
            "Run follow-up execution, patch current-task to the new active round, then rerun audit.",
            "--round-status-note",
            "Opened from adjudication bootstrap fields after closing the predecessor round.",
        )
        compile_result = run_json(
            "compile_adjudication_executor_plan.py",
            "--project-id",
            FIXTURE_PROJECT_ID,
            "--adjudication-id",
            str(adjudication_result["adjudication_id"]),
            "--in-place",
        )
        if int(compile_result["compiled_followup_count"]) != 5:
            raise SystemExit("adjudication executor plan compiler did not emit the expected bounded followups")

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
            raise SystemExit("adjudication follow-up execution left the predecessor round active")
        patch_current_task(objective_id=objective_id, round_id=successor_round_id)

        predecessor_round_path = locate_round_file(FIXTURE_PROJECT_ID, initial_round_id)
        if predecessor_round_path is None:
            raise SystemExit("predecessor round disappeared after adjudication execution")
        predecessor_meta, predecessor_sections = load_round_file(predecessor_round_path)
        if str(predecessor_meta.get("status") or "").strip() != "closed":
            raise SystemExit("round-close-chain did not close the predecessor round")
        if str(predecessor_meta.get("title") or "").strip() != "Disposable predecessor round rewritten by adjudication":
            raise SystemExit("adjudication did not rewrite the predecessor round title before closure")
        if [str(item).strip() for item in predecessor_meta.get("paths", []) if str(item).strip()] != [
            "current/",
            "control/",
            "memory/",
            "memory/transition-events/",
        ]:
            raise SystemExit("adjudication did not replace the predecessor round scope paths before closure")
        if parse_bullet_list(str(predecessor_sections.get("Scope", ""))) != [
            "Prove that registry-owned rewrite field semantics can replace the predecessor round scope before close-chain execution.",
        ]:
            raise SystemExit("adjudication did not replace the predecessor round scope items before closure")
        if str(predecessor_sections.get("Summary", "")).strip() != (
            "Adjudication narrows the predecessor round to one explicit validation slice before closure."
        ):
            raise SystemExit("adjudication did not rewrite the predecessor round summary before closure")
        if "rewritten by adjudication before closure" not in str(predecessor_sections.get("Deliverable", "")):
            raise SystemExit("adjudication did not rewrite the predecessor round before closing it")
        validation_plan_text = str(predecessor_sections.get("Validation Plan", "")).strip()
        if "Rewrite the predecessor round, then close it through the governed close chain." not in validation_plan_text:
            raise SystemExit("adjudication did not rewrite the predecessor round validation plan before closure")
        if "Disposable adjudication fixture close-chain validation" not in validation_plan_text:
            raise SystemExit("adjudication close-chain did not preserve the captured validation record")
        if parse_bullet_list(str(predecessor_sections.get("Active Risks", ""))) != [
            "Leaving the predecessor round broad would make the adjudication close-chain claim dishonest.",
        ]:
            raise SystemExit("adjudication did not replace the predecessor round risks before closure")
        if parse_bullet_list(str(predecessor_sections.get("Blockers", ""))):
            raise SystemExit("adjudication close-chain did not clear predecessor blockers before closure")
        if "Adjudication rewrote the predecessor round before closure." not in str(predecessor_sections.get("Status Notes", "")):
            raise SystemExit("adjudication did not append the predecessor round rewrite status note before closure")

        final_audit = run_json("audit_control_state.py", "--project-id", FIXTURE_PROJECT_ID)
        if final_audit["summary"]["errors"] != 0:
            raise SystemExit("adjudication follow-up fixture audit reported errors")

        ledger_text = exception_ledger_path(FIXTURE_PROJECT_ID).read_text(encoding="utf-8")
        if exception_contract_id not in ledger_text or "Retired" not in ledger_text:
            raise SystemExit("exception ledger did not reflect the retired contract after adjudication execution")
        if not active_round_path(FIXTURE_PROJECT_ID).exists():
            raise SystemExit("successor active-round projection missing after adjudication execution")

        for task_contract_id in (first_task_contract_id, second_task_contract_id):
            task_contract_path = locate_task_contract_file(FIXTURE_PROJECT_ID, task_contract_id)
            if task_contract_path is None:
                raise SystemExit(f"task-contract `{task_contract_id}` disappeared after adjudication execution")
            task_contract_meta, task_contract_sections = load_task_contract_file(task_contract_path)
            if str(task_contract_meta.get("status") or "").strip() != "invalidated":
                raise SystemExit(f"task-contract plan did not invalidate `{task_contract_id}`")
            if "Invalidated through adjudication plan fanout before round close-chain execution." not in str(
                task_contract_sections.get("Status Notes", "")
            ):
                raise SystemExit(f"task-contract plan did not append the adjudication status note for `{task_contract_id}`")

        blocked_exception_result = run_json(
            "activate_exception_contract.py",
            "--project-id",
            FIXTURE_PROJECT_ID,
            "--title",
            "Disposable prose-only adjudication exception contract",
            "--summary",
            "Temporary debt used to prove that prose-only adjudication follow-ups stay blocked.",
            "--reason",
            "The fixture needs one second active exception contract so the blocked boundary is exercised explicitly.",
            "--temporary-behavior",
            "Carry a disposable workaround that should not be retired from prose alone.",
            "--risk",
            "If prose-only follow-ups execute automatically, adjudication stops being rule-bound.",
            "--exit-condition",
            "Retire this contract only through a structured follow-up contract.",
            "--owner-scope",
            "current/",
            "--path",
            "current/",
        )
        blocked_exception_id = str(blocked_exception_result["exception_contract_id"])

        blocked_adjudication_result = run_json(
            "adjudicate_control_state.py",
            "--project-id",
            FIXTURE_PROJECT_ID,
            "--allow-clean",
            "--title",
            "Disposable blocked adjudication follow-up boundary",
            "--question",
            "Will the executor refuse prose-only follow-up requests that lack a structured contract?",
            "--verdict",
            "The prose requests retirement of the temporary contract, but the system must block because no structured executor follow-up was recorded.",
            "--retain-id",
            objective_id,
            "--invalidate-id",
            blocked_exception_id,
            "--follow-up",
            f"retire exception contract `{blocked_exception_id}` because the workaround should end now",
            "--follow-up",
            "rerun audit-control-state",
        )
        blocked_execute_result = run_json(
            "execute_adjudication_followups.py",
            "--project-id",
            FIXTURE_PROJECT_ID,
            "--adjudication-id",
            str(blocked_adjudication_result["adjudication_id"]),
        )
        if not blocked_execute_result["blocked"]:
            raise SystemExit("prose-only adjudication follow-up unexpectedly executed instead of blocking")
        if blocked_execute_result["applied"]:
            raise SystemExit("blocked adjudication unexpectedly applied a prose-only durable rewrite")

        blocked_contract_path = locate_exception_contract_file(FIXTURE_PROJECT_ID, blocked_exception_id)
        if blocked_contract_path is None:
            raise SystemExit("blocked-boundary exception contract disappeared")
        blocked_meta, _blocked_sections = load_exception_contract_file(blocked_contract_path)
        if str(blocked_meta.get("status") or "").strip() != "active":
            raise SystemExit("prose-only blocked boundary mutated exception contract status")

        boundary_audit = run_json("audit_control_state.py", "--project-id", FIXTURE_PROJECT_ID)
        if boundary_audit["summary"]["errors"] != 0:
            raise SystemExit("adjudication blocked-boundary fixture audit reported errors")

        invalidated_exception_result = run_json(
            "activate_exception_contract.py",
            "--project-id",
            FIXTURE_PROJECT_ID,
            "--title",
            "Disposable invalidation adjudication exception contract",
            "--summary",
            "Temporary debt used to prove that plan-driven adjudication can invalidate an exception contract.",
            "--reason",
            "The fixture needs one third active exception contract so invalidation also runs through the bounded executor-plan path.",
            "--temporary-behavior",
            "Carry a disposable workaround that should be invalidated instead of retired.",
            "--risk",
            "If invalidation still requires a hand-authored payload, adjudication durable truth remains only half-compiled.",
            "--exit-condition",
            "Invalidate this contract through an exception plan contract compiled from adjudication durable truth.",
            "--owner-scope",
            "current/",
            "--path",
            "current/",
        )
        invalidated_exception_id = str(invalidated_exception_result["exception_contract_id"])

        invalidate_exception_plan = json.dumps(
            {
                "plan_type": "invalidate-invalidated-exception-contracts",
                "reason": "Adjudication invalidated the disposable workaround after proving the bounded exception-plan path.",
            },
            ensure_ascii=True,
            sort_keys=True,
        )
        invalidating_adjudication_result = run_json(
            "adjudicate_control_state.py",
            "--project-id",
            FIXTURE_PROJECT_ID,
            "--allow-clean",
            "--title",
            "Disposable invalidating adjudication follow-up execution smoke",
            "--question",
            "Can adjudication invalidate an exception contract through the bounded plan compiler instead of a hand-authored payload?",
            "--verdict",
            "Invalidate the disposable exception contract through a bounded exception-contract plan compiled from the adjudication object set.",
            "--retain-id",
            objective_id,
            "--invalidate-id",
            invalidated_exception_id,
            "--executor-plan-json",
            invalidate_exception_plan,
            "--follow-up",
            "rerun audit-control-state",
        )
        invalidating_execute_result = run_json(
            "execute_adjudication_followups.py",
            "--project-id",
            FIXTURE_PROJECT_ID,
            "--adjudication-id",
            str(invalidating_adjudication_result["adjudication_id"]),
        )
        if invalidating_execute_result["blocked"]:
            raise SystemExit(
                f"exception invalidation plan execution reported blocked steps: {invalidating_execute_result['blocked']}"
            )

        invalidated_contract_path = locate_exception_contract_file(FIXTURE_PROJECT_ID, invalidated_exception_id)
        if invalidated_contract_path is None:
            raise SystemExit("invalidated-plan exception contract disappeared")
        invalidated_meta, _invalidated_sections = load_exception_contract_file(invalidated_contract_path)
        if str(invalidated_meta.get("status") or "").strip() != "invalidated":
            raise SystemExit("exception invalidation plan did not invalidate the target contract")

        final_boundary_audit = run_json("audit_control_state.py", "--project-id", FIXTURE_PROJECT_ID)
        if final_boundary_audit["summary"]["errors"] != 0:
            raise SystemExit("final adjudication follow-up fixture audit reported errors after invalidation plan execution")

        reset_fixture_repo(PHASE_BUNDLE_FIXTURE_PROJECT_DIR)
        write_phase_bundle_fixture_files()
        init_fixture_repo(PHASE_BUNDLE_FIXTURE_PROJECT_DIR, commit_message="Initialize adjudication phase-bundle fixture")

        execution_bootstrap_objective_result = run_json(
            "open_objective.py",
            "--project-id",
            PHASE_BUNDLE_FIXTURE_PROJECT_ID,
            "--title",
            "Disposable adjudication execution-bootstrap objective",
            "--problem",
            "Validate that adjudication can compile execution bootstrap into set-phase plus auto-open-round from durable round bootstrap fields.",
            "--success-criterion",
            "Adjudication phase-side-effect planning can move an exploration objective into execution.",
            "--success-criterion",
            "The same plan contract can auto-open one bounded round from adjudication bootstrap fields.",
            "--non-goal",
            "Hand-author a low-level set-phase executor payload for the fixture",
            "--why-now",
            "Phase-side-effect bundling should run through the same bounded plan compiler path as other adjudication rewrites.",
            "--phase",
            "exploration",
            "--path",
            "current/current-task.md",
        )
        execution_bootstrap_objective_id = str(execution_bootstrap_objective_result["objective_id"])

        enter_execution_plan = json.dumps(
            {
                "plan_type": "enter-execution-with-round-bootstrap",
                "reason": "Adjudication promotes the fixture objective into execution and boots one bounded round from durable round bootstrap fields.",
            },
            ensure_ascii=True,
            sort_keys=True,
        )
        execution_bootstrap_adjudication_result = run_json(
            "adjudicate_control_state.py",
            "--project-id",
            PHASE_BUNDLE_FIXTURE_PROJECT_ID,
            "--allow-clean",
            "--title",
            "Disposable execution bootstrap adjudication follow-up execution smoke",
            "--question",
            "Can adjudication compile execution bootstrap into set-phase plus auto-open-round from durable bootstrap fields?",
            "--verdict",
            "Enter execution for the new fixture objective and open one bounded round through the bounded phase-side-effect plan compiler path.",
            "--retain-id",
            execution_bootstrap_objective_id,
            "--executor-plan-json",
            enter_execution_plan,
            "--round-title",
            "Disposable adjudicated execution bootstrap round",
            "--round-scope-item",
            "Validate adjudication-driven execution bootstrap through the bounded plan compiler.",
            "--round-scope-item",
            "Reuse adjudication durable round bootstrap fields instead of hand-authored set-phase executor payloads.",
            "--round-scope-path",
            "current/",
            "--round-scope-path",
            "control/",
            "--round-scope-path",
            "memory/",
            "--round-deliverable",
            "A bounded round opened by adjudication-driven execution bootstrap.",
            "--round-validation-plan",
            "Execute adjudication followups, verify execution phase, and verify the opened round contract.",
            "--round-status-note",
            "Opened through the adjudication phase-side-effect plan bundle.",
            "--follow-up",
            "rerun audit-control-state",
        )
        execution_bootstrap_compile_result = run_json(
            "compile_adjudication_executor_plan.py",
            "--project-id",
            PHASE_BUNDLE_FIXTURE_PROJECT_ID,
            "--adjudication-id",
            str(execution_bootstrap_adjudication_result["adjudication_id"]),
        )
        if int(execution_bootstrap_compile_result["compiled_followup_count"]) != 1:
            raise SystemExit("execution bootstrap plan compiler did not emit the expected set-phase bundle")

        execution_bootstrap_execute_result = run_json(
            "execute_adjudication_followups.py",
            "--project-id",
            PHASE_BUNDLE_FIXTURE_PROJECT_ID,
            "--adjudication-id",
            str(execution_bootstrap_adjudication_result["adjudication_id"]),
        )
        if execution_bootstrap_execute_result["blocked"]:
            raise SystemExit(
                f"phase-side-effect plan execution reported blocked steps: {execution_bootstrap_execute_result['blocked']}"
            )

        execution_objective_path = None
        for candidate in (PHASE_BUNDLE_FIXTURE_PROJECT_DIR / "memory" / "objectives").glob("*.md"):
            candidate_meta, _candidate_sections = load_objective_file(candidate)
            if str(candidate_meta.get("id") or "").strip() == execution_bootstrap_objective_id:
                execution_objective_path = candidate
                if str(candidate_meta.get("phase") or "").strip() != "execution":
                    raise SystemExit("phase-side-effect plan did not move the objective into execution")
                break
        if execution_objective_path is None:
            raise SystemExit("execution-bootstrap objective durable file disappeared")

        execution_bootstrap_rounds = find_rounds(
            PHASE_BUNDLE_FIXTURE_PROJECT_ID,
            objective_id=execution_bootstrap_objective_id,
            statuses={"draft", "active", "blocked", "validation_pending"},
        )
        if len(execution_bootstrap_rounds) != 1:
            raise SystemExit("phase-side-effect plan did not leave exactly one open round for the bootstrap objective")
        _bootstrap_round_path, bootstrap_round_meta, _bootstrap_round_sections = execution_bootstrap_rounds[0]
        execution_bootstrap_round_id = str(bootstrap_round_meta.get("id") or "").strip()
        if not execution_bootstrap_round_id:
            raise SystemExit("phase-side-effect plan opened a round without an id")

        print(
            json.dumps(
                {
                    "project_id": FIXTURE_PROJECT_ID,
                    "objective_id": objective_id,
                    "initial_round_id": initial_round_id,
                    "successor_round_id": successor_round_id,
                    "exception_contract_id": exception_contract_id,
                    "first_task_contract_id": first_task_contract_id,
                    "second_task_contract_id": second_task_contract_id,
                    "blocked_exception_contract_id": blocked_exception_id,
                    "invalidated_exception_contract_id": invalidated_exception_id,
                    "execution_bootstrap_objective_id": execution_bootstrap_objective_id,
                    "execution_bootstrap_round_id": execution_bootstrap_round_id,
                    "adjudication_id": str(adjudication_result["adjudication_id"]),
                    "compiled_followup_count": int(compile_result["compiled_followup_count"]),
                    "applied": execute_result["applied"],
                    "invalidated_applied": invalidating_execute_result["applied"],
                    "execution_bootstrap_applied": execution_bootstrap_execute_result["applied"],
                    "blocked": blocked_execute_result["blocked"],
                    "fixture_audit": final_boundary_audit["status"],
                },
                ensure_ascii=True,
                indent=2,
            )
        )
    finally:
        reset_fixture_repo(FIXTURE_PROJECT_DIR)
        reset_fixture_repo(PHASE_BUNDLE_FIXTURE_PROJECT_DIR)


if __name__ == "__main__":
    main()
