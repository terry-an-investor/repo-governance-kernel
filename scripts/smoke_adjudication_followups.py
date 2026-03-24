#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

from round_control import (
    active_objective_path,
    active_round_path,
    exception_ledger_path,
    load_active_round,
    load_exception_contract_file,
    load_objective_file,
    load_pivot_file,
    load_round_file,
    load_task_contract_file,
    find_rounds,
    locate_exception_contract_file,
    locate_round_file,
    locate_task_contract_file,
    pivot_log_path,
    parse_bullet_list,
)
from smoke_fixture_lib import ROOT, init_fixture_repo, reset_fixture_repo, run_json


FIXTURE_PROJECT_ID = "__adjudication_followups_smoke__"
FIXTURE_PROJECT_DIR = ROOT / "state" / FIXTURE_PROJECT_ID
PHASE_BUNDLE_FIXTURE_PROJECT_ID = "__adjudication_phase_bundle_smoke__"
PHASE_BUNDLE_FIXTURE_PROJECT_DIR = ROOT / "state" / PHASE_BUNDLE_FIXTURE_PROJECT_ID
PHASE_FALLBACK_FIXTURE_PROJECT_ID = "__adjudication_phase_fallback_smoke__"
PHASE_FALLBACK_FIXTURE_PROJECT_DIR = ROOT / "state" / PHASE_FALLBACK_FIXTURE_PROJECT_ID
HARD_PIVOT_FIXTURE_PROJECT_ID = "__adjudication_hard_pivot_smoke__"
HARD_PIVOT_FIXTURE_PROJECT_DIR = ROOT / "state" / HARD_PIVOT_FIXTURE_PROJECT_ID


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


def write_phase_fallback_fixture_files() -> None:
    current_task_path = PHASE_FALLBACK_FIXTURE_PROJECT_DIR / "current" / "current-task.md"
    current_task_path.parent.mkdir(parents=True, exist_ok=True)
    current_task_path.write_text(
        "\n".join(
            [
                "# Current Task",
                "",
                "## Goal",
                "",
                "Validate adjudication-driven phase fallback with bounded open-round rewrite on a disposable fixture project.",
                "",
                "## Current State",
                "",
                f"- Project: `{PHASE_FALLBACK_FIXTURE_PROJECT_ID}`",
                "- Workspace id: `ws-adjudication-phase-fallback-smoke`",
                f"- Workspace root: `{PHASE_FALLBACK_FIXTURE_PROJECT_DIR.as_posix()}`",
                "- Branch: `master`",
                "- HEAD anchor: `adjudication-phase-fallback-smoke`",
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
                "- Use adjudication to leave execution and rewrite the still-open round through the bounded phase primitive.",
                "",
            ]
        )
        + "\n",
        encoding="utf-8",
    )
    blockers_path = PHASE_FALLBACK_FIXTURE_PROJECT_DIR / "current" / "blockers.md"
    blockers_path.parent.mkdir(parents=True, exist_ok=True)
    blockers_path.write_text(
        "# Blockers\n\n## Active\n\n- None recorded yet.\n\n## Waiting\n\n- None recorded yet.\n\n## Cleared\n\n- None recorded yet.\n",
        encoding="utf-8",
    )
    constitution_path = PHASE_FALLBACK_FIXTURE_PROJECT_DIR / "control" / "constitution.md"
    constitution_path.parent.mkdir(parents=True, exist_ok=True)
    constitution_path.write_text(
        "\n".join(
            [
                "# Constitution",
                "",
                "## Product Boundaries",
                "",
                "- This fixture exists only to validate adjudication-driven phase fallback bundles.",
                "",
                "## Architecture Invariants",
                "",
                "- Leaving execution should reuse existing set-phase and rewrite-open-round contracts.",
                "",
                "## Quality Bar",
                "",
                "- Adjudication must compile phase fallback from durable truth instead of hand-authored payload JSON.",
                "",
                "## Validation Rules",
                "",
                "- The fixture must leave execution and rewrite the still-open round through the bounded plan compiler path.",
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
    ledger_path = PHASE_FALLBACK_FIXTURE_PROJECT_DIR / "control" / "exception-ledger.md"
    ledger_path.parent.mkdir(parents=True, exist_ok=True)
    ledger_path.write_text(
        "# Exception Ledger\n\n## Active\n\n- None recorded yet.\n\n## Retired\n\n- None recorded yet.\n\n## Invalidated\n\n- None recorded yet.\n",
        encoding="utf-8",
    )


def write_hard_pivot_fixture_files() -> None:
    current_task_path = HARD_PIVOT_FIXTURE_PROJECT_DIR / "current" / "current-task.md"
    current_task_path.parent.mkdir(parents=True, exist_ok=True)
    current_task_path.write_text(
        "\n".join(
            [
                "# Current Task",
                "",
                "## Goal",
                "",
                "Validate adjudication-driven hard pivot after governed predecessor-round closure on a disposable fixture project.",
                "",
                "## Current State",
                "",
                f"- Project: `{HARD_PIVOT_FIXTURE_PROJECT_ID}`",
                "- Workspace id: `ws-adjudication-hard-pivot-smoke`",
                f"- Workspace root: `{HARD_PIVOT_FIXTURE_PROJECT_DIR.as_posix()}`",
                "- Branch: `master`",
                "- HEAD anchor: `adjudication-hard-pivot-smoke`",
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
                "- Use adjudication to close the predecessor round and then record a hard pivot through one governed bundle family.",
                "",
            ]
        )
        + "\n",
        encoding="utf-8",
    )
    blockers_path = HARD_PIVOT_FIXTURE_PROJECT_DIR / "current" / "blockers.md"
    blockers_path.parent.mkdir(parents=True, exist_ok=True)
    blockers_path.write_text(
        "# Blockers\n\n## Active\n\n- None recorded yet.\n\n## Waiting\n\n- None recorded yet.\n\n## Cleared\n\n- None recorded yet.\n",
        encoding="utf-8",
    )
    constitution_path = HARD_PIVOT_FIXTURE_PROJECT_DIR / "control" / "constitution.md"
    constitution_path.parent.mkdir(parents=True, exist_ok=True)
    constitution_path.write_text(
        "\n".join(
            [
                "# Constitution",
                "",
                "## Product Boundaries",
                "",
                "- This fixture exists only to validate adjudication-driven hard-pivot replacement bundles.",
                "",
                "## Architecture Invariants",
                "",
                "- Hard pivot replacement should reuse existing round-close and record-hard-pivot contracts.",
                "",
                "## Quality Bar",
                "",
                "- Adjudication must compile hard pivot replacement from durable truth instead of hand-authored nested payload JSON.",
                "",
                "## Validation Rules",
                "",
                "- The fixture must close the predecessor round and then record the hard pivot through the bounded plan compiler path.",
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
    ledger_path = HARD_PIVOT_FIXTURE_PROJECT_DIR / "control" / "exception-ledger.md"
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
        rewrite_task_contract_plan = json.dumps(
            {
                "plan_type": "rewrite-open-task-contracts",
                "task_contract_ids": [
                    first_task_contract_id,
                    second_task_contract_id,
                ],
                "rewrite_reason": "Adjudication narrows the surviving task-contract intent before lifecycle closure so the durable task contracts reflect the verdict.",
                "summary": "Adjudication rewrote this disposable task contract before status transition.",
                "risk": [
                    "If task-contract rewrite still requires private executor code paths, owner-layer semantics remain fragmented.",
                ],
                "status_note": [
                    "Rewritten through adjudication plan fanout before task-contract invalidation.",
                ],
                "allowed_change": [
                    "Prove that adjudication can compile shared task-contract rewrite semantics through the registry.",
                ],
                "replace_allowed_changes": True,
                "replace_risks": True,
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
            rewrite_task_contract_plan,
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
        if int(compile_result["compiled_followup_count"]) != 7:
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
            if str(task_contract_sections.get("Summary", "")).strip() != (
                "Adjudication rewrote this disposable task contract before status transition."
            ):
                raise SystemExit(f"task-contract rewrite plan did not rewrite summary for `{task_contract_id}`")
            if parse_bullet_list(str(task_contract_sections.get("Allowed Changes", ""))) != [
                "Prove that adjudication can compile shared task-contract rewrite semantics through the registry.",
            ]:
                raise SystemExit(f"task-contract rewrite plan did not replace allowed changes for `{task_contract_id}`")
            if parse_bullet_list(str(task_contract_sections.get("Active Risks", ""))) != [
                "If task-contract rewrite still requires private executor code paths, owner-layer semantics remain fragmented.",
                "If open task contracts survive, the round close-chain should stay blocked.",
            ]:
                raise SystemExit(f"task-contract plans did not preserve rewrite risk plus invalidation risk for `{task_contract_id}`")
            if "Rewritten through adjudication plan fanout before task-contract invalidation." not in str(
                task_contract_sections.get("Status Notes", "")
            ):
                raise SystemExit(f"task-contract rewrite plan did not append the adjudication rewrite note for `{task_contract_id}`")
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

        reset_fixture_repo(PHASE_FALLBACK_FIXTURE_PROJECT_DIR)
        write_phase_fallback_fixture_files()
        init_fixture_repo(PHASE_FALLBACK_FIXTURE_PROJECT_DIR, commit_message="Initialize adjudication phase-fallback fixture")

        phase_fallback_objective_result = run_json(
            "open_objective.py",
            "--project-id",
            PHASE_FALLBACK_FIXTURE_PROJECT_ID,
            "--title",
            "Disposable adjudication phase fallback objective",
            "--problem",
            "Validate that adjudication can leave execution while rewriting the still-open round through the bounded phase primitive.",
            "--success-criterion",
            "Adjudication can compile a bounded phase fallback plan into set-phase with rewrite-open-round.",
            "--success-criterion",
            "The same plan can rewrite the still-open round contract while the objective leaves execution.",
            "--non-goal",
            "Hand-author a low-level set-phase rewrite payload for the fixture.",
            "--why-now",
            "Phase fallback semantics should be consumable through the same owner-layer adjudication path as execution bootstrap.",
            "--phase",
            "execution",
            "--path",
            "current/current-task.md",
        )
        phase_fallback_objective_id = str(phase_fallback_objective_result["objective_id"])

        phase_fallback_round_result = run_json(
            "open_round.py",
            "--project-id",
            PHASE_FALLBACK_FIXTURE_PROJECT_ID,
            "--title",
            "Disposable phase fallback predecessor round",
            "--scope-item",
            "Prove that adjudication phase fallback can rewrite the still-open round through governed set-phase semantics.",
            "--deliverable",
            "A disposable round that will be rewritten by the phase fallback adjudication plan.",
            "--validation-plan",
            "Compile and execute the phase fallback plan, then inspect durable objective and round truth.",
            "--scope-path",
            "current/",
            "--scope-path",
            "control/",
            "--scope-path",
            "memory/",
        )
        phase_fallback_round_id = str(phase_fallback_round_result["round_id"])

        leave_execution_plan = json.dumps(
            {
                "plan_type": "leave-execution-with-round-rewrite",
                "phase": "paused",
                "reason": "Adjudication pauses the fixture objective and rewrites the still-open round so the bounded contract stays honest outside active execution.",
                "scope_review_note": [
                    "The open round remains durable but its contract is rewritten to reflect paused execution."
                ],
                "round_title": "Disposable paused phase fallback round",
                "round_summary": "Rewritten through adjudication-driven phase fallback.",
                "round_scope_item": [
                    "Preserve bounded round truth while objective execution is paused."
                ],
                "round_scope_path": [
                    "current/",
                    "control/",
                ],
                "round_deliverable": "A rewritten round contract aligned with paused execution.",
                "round_validation_plan": "Inspect durable objective and round truth after the bounded phase fallback execution.",
                "round_risk": [
                    "Paused execution still requires an honest bounded round contract."
                ],
                "round_status_note": "Rewritten through the adjudication phase fallback plan bundle.",
                "replace_round_scope_items": True,
                "replace_round_scope_paths": True,
                "replace_round_risks": True,
            },
            ensure_ascii=True,
            sort_keys=True,
        )
        phase_fallback_adjudication_result = run_json(
            "adjudicate_control_state.py",
            "--project-id",
            PHASE_FALLBACK_FIXTURE_PROJECT_ID,
            "--allow-clean",
            "--title",
            "Disposable phase fallback adjudication follow-up execution smoke",
            "--question",
            "Can adjudication compile leaving execution plus open-round rewrite into the bounded phase primitive?",
            "--verdict",
            "Pause the fixture objective and rewrite the still-open round through the bounded phase fallback plan compiler path.",
            "--retain-id",
            phase_fallback_objective_id,
            "--executor-plan-json",
            leave_execution_plan,
            "--follow-up",
            "rerun audit-control-state",
        )
        phase_fallback_compile_result = run_json(
            "compile_adjudication_executor_plan.py",
            "--project-id",
            PHASE_FALLBACK_FIXTURE_PROJECT_ID,
            "--adjudication-id",
            str(phase_fallback_adjudication_result["adjudication_id"]),
        )
        if int(phase_fallback_compile_result["compiled_followup_count"]) != 1:
            raise SystemExit("phase fallback plan compiler did not emit the expected set-phase bundle")
        compiled_phase_fallback_payloads = phase_fallback_compile_result.get("compiled_followups") or []
        if not compiled_phase_fallback_payloads:
            raise SystemExit("phase fallback plan compiler emitted no payloads")
        compiled_phase_fallback_payload = compiled_phase_fallback_payloads[0]
        if compiled_phase_fallback_payload.get("command") != "set-phase":
            raise SystemExit("phase fallback plan compiler did not compile through set-phase")
        if compiled_phase_fallback_payload.get("phase") != "paused":
            raise SystemExit("phase fallback plan compiler did not target the expected phase")
        if not compiled_phase_fallback_payload.get("rewrite_open_round"):
            raise SystemExit("phase fallback plan compiler did not request bounded open-round rewrite")

        phase_fallback_execute_result = run_json(
            "execute_adjudication_followups.py",
            "--project-id",
            PHASE_FALLBACK_FIXTURE_PROJECT_ID,
            "--adjudication-id",
            str(phase_fallback_adjudication_result["adjudication_id"]),
        )
        if phase_fallback_execute_result["blocked"]:
            raise SystemExit(
                f"phase fallback plan execution reported blocked steps: {phase_fallback_execute_result['blocked']}"
            )

        phase_fallback_objective_path = None
        for candidate in (PHASE_FALLBACK_FIXTURE_PROJECT_DIR / "memory" / "objectives").glob("*.md"):
            candidate_meta, _candidate_sections = load_objective_file(candidate)
            if str(candidate_meta.get("id") or "").strip() == phase_fallback_objective_id:
                phase_fallback_objective_path = candidate
                if str(candidate_meta.get("phase") or "").strip() != "paused":
                    raise SystemExit("phase fallback plan did not move the objective into paused")
                break
        if phase_fallback_objective_path is None:
            raise SystemExit("phase-fallback objective durable file disappeared")

        phase_fallback_round_path = locate_round_file(PHASE_FALLBACK_FIXTURE_PROJECT_ID, phase_fallback_round_id)
        if phase_fallback_round_path is None:
            raise SystemExit("phase fallback target round durable file disappeared")
        phase_fallback_round_meta, phase_fallback_round_sections = load_round_file(phase_fallback_round_path)
        if str(phase_fallback_round_meta.get("title") or "").strip() != "Disposable paused phase fallback round":
            raise SystemExit("phase fallback plan did not rewrite the round title")
        rewritten_scope_items = parse_bullet_list(phase_fallback_round_sections.get("Scope", ""))
        if rewritten_scope_items != ["Preserve bounded round truth while objective execution is paused."]:
            raise SystemExit("phase fallback plan did not replace the round scope items")
        rewritten_scope_paths = [str(item).strip() for item in phase_fallback_round_meta.get("paths", []) if str(item).strip()]
        if rewritten_scope_paths != ["current/", "control/"]:
            raise SystemExit("phase fallback plan did not replace the round scope paths")

        phase_fallback_audit = run_json("audit_control_state.py", "--project-id", PHASE_FALLBACK_FIXTURE_PROJECT_ID)
        if phase_fallback_audit["summary"]["errors"] != 0:
            raise SystemExit("phase fallback fixture audit reported errors")

        reset_fixture_repo(HARD_PIVOT_FIXTURE_PROJECT_DIR)
        write_hard_pivot_fixture_files()
        init_fixture_repo(HARD_PIVOT_FIXTURE_PROJECT_DIR, commit_message="Initialize adjudication hard-pivot fixture")

        hard_pivot_objective_result = run_json(
            "open_objective.py",
            "--project-id",
            HARD_PIVOT_FIXTURE_PROJECT_ID,
            "--title",
            "Disposable adjudication hard pivot predecessor objective",
            "--problem",
            "Validate that adjudication can close the predecessor round and then record a hard pivot through the bounded bundle family.",
            "--success-criterion",
            "Adjudication can compile predecessor-round closure plus hard pivot into one governed bundle payload.",
            "--success-criterion",
            "The same plan can leave the previous objective superseded and the successor objective active.",
            "--non-goal",
            "Hand-author a nested hard-pivot replacement executor payload.",
            "--why-now",
            "Hard-pivot replacement semantics should reuse the same governed round and objective primitives instead of inventing private bundle logic.",
            "--phase",
            "execution",
            "--path",
            "current/current-task.md",
        )
        hard_pivot_previous_objective_id = str(hard_pivot_objective_result["objective_id"])

        hard_pivot_round_result = run_json(
            "open_round.py",
            "--project-id",
            HARD_PIVOT_FIXTURE_PROJECT_ID,
            "--title",
            "Disposable hard pivot predecessor round",
            "--scope-item",
            "Prove that hard-pivot adjudication can close the predecessor round before replacing the objective line.",
            "--deliverable",
            "A disposable predecessor round that will be closed by the hard-pivot bundle.",
            "--validation-plan",
            "Drive the round through a governed close chain and then confirm the hard pivot durable state.",
            "--scope-path",
            "current/",
            "--scope-path",
            "control/",
            "--scope-path",
            "memory/",
        )
        hard_pivot_round_id = str(hard_pivot_round_result["round_id"])

        run_json(
            "update_round_status.py",
            "--project-id",
            HARD_PIVOT_FIXTURE_PROJECT_ID,
            "--round-id",
            hard_pivot_round_id,
            "--status",
            "blocked",
            "--reason",
            "The predecessor round is intentionally paused until adjudication decides whether to replace the objective line.",
            "--blocker",
            "Need governed close-chain plus hard-pivot bundle validation before replacement.",
        )

        hard_pivot_plan = json.dumps(
            {
                "plan_type": "close-round-and-record-hard-pivot",
                "previous_objective_id": hard_pivot_previous_objective_id,
                "reactivation_reason": "Adjudication resumes the predecessor round only to close it honestly before the hard pivot.",
                "validation_pending_reason": "The predecessor round is ready for final validation before the objective line is replaced.",
                "captured_reason": "The predecessor round was validated and can be captured before hard pivot replacement.",
                "closed_reason": "The predecessor round must close before the objective line is superseded.",
                "close_chain_risk": [
                    "Objective replacement should not strand a predecessor round in open status."
                ],
                "clear_blockers": True,
                "title": "Disposable adjudication hard pivot successor objective",
                "summary": "A successor objective opened through the bounded hard-pivot adjudication bundle.",
                "problem": "Replace the predecessor objective after its execution slice is durably closed.",
                "success_criterion": [
                    "The predecessor round is durably closed before the hard pivot executes.",
                    "The successor objective becomes the active objective after the hard pivot.",
                ],
                "non_goal": [
                    "Leave the predecessor objective active after replacement."
                ],
                "why_now": "The predecessor framing is done and the project needs a new objective line.",
                "phase": "exploration",
                "trigger": "The predecessor objective finished its bounded slice and a replacement objective is now required.",
                "pivot_title": "Disposable governed hard pivot after predecessor-round closure",
                "retained_decision": [
                    "Keep the durable record that the predecessor round was completed before replacement."
                ],
                "invalidated_assumption": [
                    "The predecessor objective should continue as the active mainline."
                ],
                "next_control_change": [
                    "Open a new bounded round only after the successor objective is active."
                ],
                "risk": [
                    "If bundle semantics drift, hard pivot could outrun predecessor-round closure."
                ],
                "path": [
                    "current/current-task.md"
                ],
                "supersession_notes": "Recorded through the bounded hard-pivot adjudication bundle.",
            },
            ensure_ascii=True,
            sort_keys=True,
        )
        hard_pivot_adjudication_result = run_json(
            "adjudicate_control_state.py",
            "--project-id",
            HARD_PIVOT_FIXTURE_PROJECT_ID,
            "--allow-clean",
            "--title",
            "Disposable hard pivot adjudication follow-up execution smoke",
            "--question",
            "Can adjudication close the predecessor round and then record a hard pivot through one governed bundle family?",
            "--verdict",
            "Close the predecessor round and then record the hard pivot through the bounded hard-pivot replacement plan compiler path.",
            "--retain-id",
            hard_pivot_previous_objective_id,
            "--invalidate-id",
            hard_pivot_round_id,
            "--executor-plan-json",
            hard_pivot_plan,
            "--follow-up",
            "rerun audit-control-state",
        )
        hard_pivot_compile_result = run_json(
            "compile_adjudication_executor_plan.py",
            "--project-id",
            HARD_PIVOT_FIXTURE_PROJECT_ID,
            "--adjudication-id",
            str(hard_pivot_adjudication_result["adjudication_id"]),
        )
        if int(hard_pivot_compile_result["compiled_followup_count"]) != 1:
            raise SystemExit("hard-pivot plan compiler did not emit the expected governed bundle payload")
        compiled_hard_pivot_payloads = hard_pivot_compile_result.get("compiled_followups") or []
        if not compiled_hard_pivot_payloads:
            raise SystemExit("hard-pivot plan compiler emitted no payloads")
        compiled_hard_pivot_payload = compiled_hard_pivot_payloads[0]
        if compiled_hard_pivot_payload.get("command") != "round-close-chain-then-hard-pivot":
            raise SystemExit("hard-pivot plan compiler did not compile through the governed bundle")
        if compiled_hard_pivot_payload.get("previous_objective_id") != hard_pivot_previous_objective_id:
            raise SystemExit("hard-pivot plan compiler lost the previous objective target")

        hard_pivot_execute_result = run_json(
            "execute_adjudication_followups.py",
            "--project-id",
            HARD_PIVOT_FIXTURE_PROJECT_ID,
            "--adjudication-id",
            str(hard_pivot_adjudication_result["adjudication_id"]),
        )
        if hard_pivot_execute_result["blocked"]:
            raise SystemExit(
                f"hard-pivot plan execution reported blocked steps: {hard_pivot_execute_result['blocked']}"
            )

        hard_pivot_previous_objective_path = None
        hard_pivot_successor_objective_path = None
        hard_pivot_successor_objective_id = ""
        for candidate in (HARD_PIVOT_FIXTURE_PROJECT_DIR / "memory" / "objectives").glob("*.md"):
            candidate_meta, _candidate_sections = load_objective_file(candidate)
            candidate_id = str(candidate_meta.get("id") or "").strip()
            candidate_status = str(candidate_meta.get("status") or "").strip()
            if candidate_id == hard_pivot_previous_objective_id:
                hard_pivot_previous_objective_path = candidate
                if candidate_status != "superseded":
                    raise SystemExit("hard-pivot plan did not supersede the previous objective")
            elif candidate_status == "active":
                hard_pivot_successor_objective_path = candidate
                hard_pivot_successor_objective_id = candidate_id
        if hard_pivot_previous_objective_path is None:
            raise SystemExit("hard-pivot plan lost the previous objective durable file")
        if hard_pivot_successor_objective_path is None or not hard_pivot_successor_objective_id:
            raise SystemExit("hard-pivot plan did not leave one active successor objective")

        hard_pivot_round_path = locate_round_file(HARD_PIVOT_FIXTURE_PROJECT_ID, hard_pivot_round_id)
        if hard_pivot_round_path is None:
            raise SystemExit("hard-pivot predecessor round durable file disappeared")
        hard_pivot_round_meta, _hard_pivot_round_sections = load_round_file(hard_pivot_round_path)
        if str(hard_pivot_round_meta.get("status") or "").strip() != "closed":
            raise SystemExit("hard-pivot plan did not close the predecessor round")

        hard_pivot_pivots = list((HARD_PIVOT_FIXTURE_PROJECT_DIR / "memory" / "pivots").glob("*.md"))
        if len(hard_pivot_pivots) != 1:
            raise SystemExit("hard-pivot plan did not leave exactly one pivot record")
        hard_pivot_pivot_meta, _hard_pivot_pivot_sections = load_pivot_file(hard_pivot_pivots[0])
        if str(hard_pivot_pivot_meta.get("objective_id") or "").strip() != hard_pivot_successor_objective_id:
            raise SystemExit("hard-pivot plan pivot record does not point at the successor objective")

        hard_pivot_audit = run_json("audit_control_state.py", "--project-id", HARD_PIVOT_FIXTURE_PROJECT_ID)
        if hard_pivot_audit["summary"]["errors"] != 0:
            raise SystemExit("hard-pivot fixture audit reported errors")

        reset_fixture_repo(FIXTURE_PROJECT_DIR)
        write_fixture_files()
        init_fixture_repo(FIXTURE_PROJECT_DIR, commit_message="Initialize adjudication objective-rewrite fixture")

        objective_rewrite_objective_result = run_json(
            "open_objective.py",
            "--project-id",
            FIXTURE_PROJECT_ID,
            "--title",
            "Disposable adjudication objective rewrite smoke objective",
            "--problem",
            "Validate that adjudication can rewrite the active objective line through the bounded soft-pivot plan path.",
            "--success-criterion",
            "Adjudication can compile a bounded objective rewrite plan into record-soft-pivot.",
            "--success-criterion",
            "The same plan can rewrite the active round to stay aligned with the rewritten objective.",
            "--non-goal",
            "Branch to a new objective id.",
            "--why-now",
            "Objective rewrite semantics should be consumable through the same owner-layer adjudication path as round and task rewrites.",
            "--phase",
            "execution",
            "--path",
            "current/current-task.md",
        )
        objective_rewrite_objective_id = str(objective_rewrite_objective_result["objective_id"])
        patch_current_task(objective_id=objective_rewrite_objective_id)

        objective_rewrite_round_result = run_json(
            "open_round.py",
            "--project-id",
            FIXTURE_PROJECT_ID,
            "--title",
            "Disposable objective rewrite predecessor round",
            "--scope-item",
            "Prove that objective rewrite adjudication can keep the open round aligned through governed rewrite semantics.",
            "--deliverable",
            "A disposable round that will be rewritten by objective adjudication.",
            "--validation-plan",
            "Compile and execute the objective rewrite adjudication plan, then inspect durable objective and round truth.",
            "--scope-path",
            "current/",
            "--scope-path",
            "control/",
            "--scope-path",
            "memory/",
        )
        objective_rewrite_round_id = str(objective_rewrite_round_result["round_id"])
        patch_current_task(objective_id=objective_rewrite_objective_id, round_id=objective_rewrite_round_id)

        objective_rewrite_plan = json.dumps(
            {
                "plan_type": "rewrite-active-objective-via-soft-pivot",
                "trigger": "The active objective needs a tighter execution framing without changing objective identity.",
                "change_summary": "Refine the active objective around adjudication-driven rewrite semantics while preserving the same objective line.",
                "identity_rationale": "The user problem and owner line remain the same; only the execution framing and rewrite discipline are being tightened.",
                "title": "Disposable adjudication objective rewrite smoke objective in execution",
                "summary": "Keep the same objective id while rewriting the active objective through adjudication.",
                "why_now": "The fixture now proves bounded objective rewrite semantics through the same adjudication path as other governed rewrites.",
                "risk": [
                    "If objective rewrite still bypasses the registry-owned executor path, M3 remains incomplete.",
                ],
                "next_control_change": [
                    "Keep the existing open round aligned by rewriting it in the same soft-pivot command.",
                ],
                "rewrite_open_round": True,
                "round_deliverable": "A disposable round rewritten through objective adjudication so round and objective truth stay aligned.",
                "round_validation_plan": "Execute adjudication followups and inspect durable objective plus round rewrite results.",
                "round_status_note": [
                    "Rewritten during objective adjudication so round and objective framing stay aligned.",
                ],
                "evidence": [
                    "The same objective id still owns the work after the rewrite.",
                ],
            },
            ensure_ascii=True,
            sort_keys=True,
        )
        objective_rewrite_adjudication_result = run_json(
            "adjudicate_control_state.py",
            "--project-id",
            FIXTURE_PROJECT_ID,
            "--allow-clean",
            "--title",
            "Disposable objective rewrite adjudication follow-up execution smoke",
            "--question",
            "Can adjudication rewrite the active objective line through the bounded soft-pivot plan path?",
            "--verdict",
            "Rewrite the active objective through a bounded soft pivot and rewrite the still-open round in the same owner-layer transition.",
            "--retain-id",
            objective_rewrite_objective_id,
            "--executor-plan-json",
            objective_rewrite_plan,
            "--follow-up",
            "rerun audit-control-state",
        )
        objective_rewrite_compile_result = run_json(
            "compile_adjudication_executor_plan.py",
            "--project-id",
            FIXTURE_PROJECT_ID,
            "--adjudication-id",
            str(objective_rewrite_adjudication_result["adjudication_id"]),
        )
        if int(objective_rewrite_compile_result["compiled_followup_count"]) != 1:
            raise SystemExit("objective rewrite adjudication plan compiler did not emit the expected bounded followup")

        objective_rewrite_execute_result = run_json(
            "execute_adjudication_followups.py",
            "--project-id",
            FIXTURE_PROJECT_ID,
            "--adjudication-id",
            str(objective_rewrite_adjudication_result["adjudication_id"]),
        )
        if objective_rewrite_execute_result["blocked"]:
            raise SystemExit(
                f"objective rewrite adjudication execution reported blocked steps: {objective_rewrite_execute_result['blocked']}"
            )

        rewritten_objective_path = None
        for candidate in (FIXTURE_PROJECT_DIR / "memory" / "objectives").glob("*.md"):
            candidate_meta, candidate_sections = load_objective_file(candidate)
            if str(candidate_meta.get("id") or "").strip() == objective_rewrite_objective_id:
                rewritten_objective_path = candidate
                if "bounded objective rewrite semantics" not in str(candidate_sections.get("Why Now", "")):
                    raise SystemExit("objective rewrite adjudication did not rewrite durable objective why-now")
                break
        if rewritten_objective_path is None:
            raise SystemExit("objective rewrite adjudication lost the durable objective file")

        rewritten_round_path = locate_round_file(FIXTURE_PROJECT_ID, objective_rewrite_round_id)
        if rewritten_round_path is None:
            raise SystemExit("objective rewrite adjudication lost the open round")
        _rewritten_round_meta, rewritten_round_sections = load_round_file(rewritten_round_path)
        if "rewritten through objective adjudication" not in str(rewritten_round_sections.get("Deliverable", "")):
            raise SystemExit("objective rewrite adjudication did not rewrite the open round deliverable")

        rewritten_pivots = list((FIXTURE_PROJECT_DIR / "memory" / "pivots").glob("*.md"))
        if len(rewritten_pivots) != 1:
            raise SystemExit("objective rewrite adjudication did not leave exactly one pivot record")
        rewritten_pivot_meta, _rewritten_pivot_sections = load_pivot_file(rewritten_pivots[0])
        if str(rewritten_pivot_meta.get("objective_id") or "").strip() != objective_rewrite_objective_id:
            raise SystemExit("objective rewrite adjudication pivot does not point at the preserved objective id")
        if not active_objective_path(FIXTURE_PROJECT_ID).exists():
            raise SystemExit("objective rewrite adjudication removed the active objective projection")
        if objective_rewrite_objective_id not in pivot_log_path(FIXTURE_PROJECT_ID).read_text(encoding="utf-8"):
            raise SystemExit("objective rewrite adjudication did not refresh pivot log projection")

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
                    "phase_fallback_objective_id": phase_fallback_objective_id,
                    "phase_fallback_round_id": phase_fallback_round_id,
                    "hard_pivot_previous_objective_id": hard_pivot_previous_objective_id,
                    "hard_pivot_successor_objective_id": hard_pivot_successor_objective_id,
                    "hard_pivot_round_id": hard_pivot_round_id,
                    "objective_rewrite_objective_id": objective_rewrite_objective_id,
                    "objective_rewrite_round_id": objective_rewrite_round_id,
                    "adjudication_id": str(adjudication_result["adjudication_id"]),
                    "compiled_followup_count": int(compile_result["compiled_followup_count"]),
                    "applied": execute_result["applied"],
                    "invalidated_applied": invalidating_execute_result["applied"],
                    "execution_bootstrap_applied": execution_bootstrap_execute_result["applied"],
                    "phase_fallback_applied": phase_fallback_execute_result["applied"],
                    "hard_pivot_applied": hard_pivot_execute_result["applied"],
                    "objective_rewrite_applied": objective_rewrite_execute_result["applied"],
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
        reset_fixture_repo(PHASE_FALLBACK_FIXTURE_PROJECT_DIR)
        reset_fixture_repo(HARD_PIVOT_FIXTURE_PROJECT_DIR)


if __name__ == "__main__":
    main()
