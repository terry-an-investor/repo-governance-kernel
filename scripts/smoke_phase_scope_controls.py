#!/usr/bin/env python3
from __future__ import annotations

import json

from smoke_fixture_lib import ROOT, init_fixture_repo, reset_fixture_repo, run_json


FIXTURE_PROJECT_ID = "__phase_scope_control_smoke__"
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
                "Validate explicit phase transitions and round-scope refresh on a disposable fixture project.",
                "",
                "## Current State",
                "",
                f"- Project: `{FIXTURE_PROJECT_ID}`",
                "- Workspace id: `ws-phase-scope-control-smoke`",
                f"- Workspace root: `{FIXTURE_PROJECT_DIR.as_posix()}`",
                "- Branch: `master`",
                "- HEAD anchor: `phase-scope-control-smoke`",
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
                "- Move the fixture objective into execution with an auto-opened round, then refresh the round scope from live dirty paths.",
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
                "- This fixture exists only to validate explicit phase and scope-control commands.",
                "",
                "## Architecture Invariants",
                "",
                "- Execution phase should not be claimed without one bounded round.",
                "- Round scope refresh must rewrite durable truth instead of relying on manual YAML edits.",
                "",
                "## Quality Bar",
                "",
                "- Control commands must prove real file-state change and audit alignment.",
                "",
                "## Validation Rules",
                "",
                "- The fixture must prove set-phase auto-open behavior and refresh-round-scope durability.",
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


def main() -> None:
    reset_fixture_repo(FIXTURE_PROJECT_DIR)
    try:
        write_fixture_files()
        init_fixture_repo(FIXTURE_PROJECT_DIR, commit_message="Initialize phase/scope control fixture")

        objective_result = run_json(
            "open_objective.py",
            "--project-id",
            FIXTURE_PROJECT_ID,
            "--title",
            "Disposable phase and scope control objective",
            "--problem",
            "Validate explicit phase and round-scope control commands on a disposable project.",
            "--success-criterion",
            "set-phase can enter execution only by establishing one bounded round",
            "--success-criterion",
            "refresh-round-scope rewrites durable round paths to cover live dirty work honestly",
            "--non-goal",
            "Keep the fixture after validation",
            "--why-now",
            "Phase and scope control should be command-owned, not hand-maintained text.",
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
            "The fixture now needs one bounded execution contract before dirty-path scope refresh is exercised.",
            "--auto-open-round",
            "--round-title",
            "Disposable phase/scope control round",
            "--round-scope-item",
            "Validate explicit phase and round-scope control commands.",
            "--round-deliverable",
            "A disposable round proving phase bootstrap and scope refresh behavior.",
            "--round-validation-plan",
            "Dirty one source file, refresh the round scope, and rerun enforcement plus audit.",
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
            raise SystemExit("set-phase did not open a round for the phase/scope control fixture")
        patch_current_task(objective_id=objective_id, round_id=round_id)

        dirty_path = FIXTURE_PROJECT_DIR / "src" / "tracked.txt"
        dirty_path.write_text("dirty after phase bootstrap\n", encoding="utf-8")

        blocked_result = run_json(
            "enforce_worktree.py",
            "--project-id",
            FIXTURE_PROJECT_ID,
            expect_failure=True,
        )
        blocked_codes = {str(issue.get("code") or "").strip() for issue in blocked_result.get("issues", [])}
        if "dirty_paths_outside_scope_round" not in blocked_codes:
            raise SystemExit("expected out-of-scope dirty path block did not occur")

        refresh_result = run_json(
            "refresh_round_scope.py",
            "--project-id",
            FIXTURE_PROJECT_ID,
            "--round-id",
            round_id,
            "--reason",
            "The fixture intentionally dirtied one source file and the round must absorb that live work honestly.",
        )
        if "src/tracked.txt" not in refresh_result.get("paths", []):
            raise SystemExit("refresh-round-scope did not add the live dirty source file")

        allowed_result = run_json(
            "enforce_worktree.py",
            "--project-id",
            FIXTURE_PROJECT_ID,
        )
        if str(allowed_result.get("status") or "") != "ok":
            raise SystemExit("worktree should pass once round scope is refreshed")

        final_audit = run_json("audit_control_state.py", "--project-id", FIXTURE_PROJECT_ID)
        if final_audit["summary"]["errors"] != 0:
            raise SystemExit("phase/scope control fixture audit reported errors")

        print(
            json.dumps(
                {
                    "project_id": FIXTURE_PROJECT_ID,
                    "objective_id": objective_id,
                    "round_id": round_id,
                    "blocked_status": blocked_result["status"],
                    "allowed_status": allowed_result["status"],
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
