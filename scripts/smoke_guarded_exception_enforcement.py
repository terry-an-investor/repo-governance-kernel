#!/usr/bin/env python3
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

from smoke_fixture_lib import (
    ROOT,
    init_fixture_repo,
    on_rm_error,
    reset_fixture_repo,
    run_json,
    run_plain,
    run_git,
)


FIXTURE_PROJECT_ID = "__guarded_exception_enforcement_smoke__"
FIXTURE_PROJECT_DIR = ROOT / "projects" / FIXTURE_PROJECT_ID
FIXTURE_GUARDED_FILE = FIXTURE_PROJECT_DIR / "src" / "guarded-runtime.txt"


def run_python_snippet(code: str) -> str:
    completed = subprocess.run(
        [sys.executable, "-c", code],
        cwd=str(ROOT),
        capture_output=True,
        text=True,
        check=False,
    )
    if completed.returncode != 0:
        raise SystemExit(
            json.dumps(
                {
                    "snippet": code,
                    "returncode": completed.returncode,
                    "stdout": completed.stdout,
                    "stderr": completed.stderr,
                },
                ensure_ascii=True,
                indent=2,
            )
        )
    return completed.stdout


def write_fixture_files() -> None:
    current_dir = FIXTURE_PROJECT_DIR / "current"
    control_dir = FIXTURE_PROJECT_DIR / "control"
    source_dir = FIXTURE_PROJECT_DIR / "src"
    current_dir.mkdir(parents=True, exist_ok=True)
    control_dir.mkdir(parents=True, exist_ok=True)
    source_dir.mkdir(parents=True, exist_ok=True)

    (current_dir / "current-task.md").write_text(
        "\n".join(
            [
                "# Current Task",
                "",
                "## Goal",
                "",
                "Validate guarded exception path enforcement on a disposable fixture project.",
                "",
                "## Current State",
                "",
                f"- Project: `{FIXTURE_PROJECT_ID}`",
                "- Workspace id: `ws-guarded-exception-smoke`",
                f"- Workspace root: `{FIXTURE_PROJECT_DIR.as_posix()}`",
                "- Branch: `master`",
                "- HEAD anchor: `smoke-fixture`",
                "",
                "## Validated Facts",
                "",
                "- This fixture exists only to prove guarded exception enforcement.",
                "",
                "## Important Files",
                "",
                f"- `{(control_dir / 'constitution.md').as_posix()}`",
                f"- `{FIXTURE_GUARDED_FILE.as_posix()}`",
                "",
                "## Active Risks",
                "",
                "- None recorded yet.",
                "",
                "## Next Steps",
                "",
                "- Prove that guarded path changes are blocked without an exception contract and allowed with one.",
                "",
            ]
        )
        + "\n",
        encoding="utf-8",
    )
    (current_dir / "blockers.md").write_text(
        "# Blockers\n\n## Active\n\n- None recorded yet.\n\n## Waiting\n\n- None recorded yet.\n\n## Cleared\n\n- None recorded yet.\n",
        encoding="utf-8",
    )
    (control_dir / "constitution.md").write_text(
        "\n".join(
            [
                "# Constitution",
                "",
                "## Product Boundaries",
                "",
                "- This fixture exists only to validate guarded exception path enforcement.",
                "",
                "## Architecture Invariants",
                "",
                "- Guarded path changes must stay explicit temporary deviation debt.",
                "",
                "## Quality Bar",
                "",
                "- Enforcement claims must be proven through executable fixture behavior.",
                "",
                "## Validation Rules",
                "",
                "- The fixture must prove both blocked and allowed paths.",
                "",
                "## Forbidden Shortcuts",
                "",
                "- Do not let guarded-path changes proceed without an active exception contract.",
                "",
                "## Guarded Exception Paths",
                "",
                "- src/",
                "",
                "## Audit Hooks",
                "",
                "- current_task_mentions_active_objective",
                "- current_task_mentions_active_round",
                "- guarded_exception_paths_require_active_contract",
                "",
            ]
        )
        + "\n",
        encoding="utf-8",
    )
    FIXTURE_GUARDED_FILE.write_text("guarded fixture baseline\n", encoding="utf-8")
    init_fixture_repo(FIXTURE_PROJECT_DIR, commit_message="Initialize guarded exception enforcement fixture")


def patch_fixture_current_task(objective_id: str, round_id: str) -> None:
    current_task_path = FIXTURE_PROJECT_DIR / "current" / "current-task.md"
    text = current_task_path.read_text(encoding="utf-8")
    if "- Objective id:" not in text:
        text = text.replace(f"- Project: `{FIXTURE_PROJECT_ID}`\n", f"- Project: `{FIXTURE_PROJECT_ID}`\n- Objective id: `{objective_id}`\n", 1)
    if "- Active round id:" not in text:
        text = text.replace("- HEAD anchor: `smoke-fixture`\n", f"- HEAD anchor: `smoke-fixture`\n- Active round id: `{round_id}`\n- Phase: `execution`\n", 1)
    current_task_path.write_text(text, encoding="utf-8")


def main() -> None:
    reset_fixture_repo(FIXTURE_PROJECT_DIR)

    try:
        write_fixture_files()

        objective_result = run_json(
            "open_objective.py",
            "--project-id",
            FIXTURE_PROJECT_ID,
            "--title",
            "Guarded exception enforcement fixture objective",
            "--problem",
            "Prove that guarded exception paths require an active exception contract.",
            "--success-criterion",
            "guarded dirty paths block enforcement without an active exception contract",
            "--success-criterion",
            "the same guarded dirty paths pass enforcement once an active exception contract covers them",
            "--non-goal",
            "Keep this disposable fixture after validation",
            "--why-now",
            "The second enforcement slice must prove durable exception coverage, not only scope drift.",
            "--phase",
            "execution",
            "--path",
            f"projects/{FIXTURE_PROJECT_ID}/control/constitution.md",
        )
        objective_id = str(objective_result["objective_id"])

        round_result = run_json(
            "open_round.py",
            "--project-id",
            FIXTURE_PROJECT_ID,
            "--title",
            "Validate guarded exception enforcement",
            "--objective-id",
            objective_id,
            "--scope-item",
            "Exercise one guarded path under enforcement.",
            "--scope-path",
            "src/",
            "--scope-path",
            "current/",
            "--scope-path",
            "control/",
            "--scope-path",
            "memory/",
            "--deliverable",
            "A disposable fixture proving the guarded exception enforcement slice.",
            "--validation-plan",
            "Run enforcement before and after activating one covering exception contract.",
        )
        round_id = str(round_result["round_id"])
        patch_fixture_current_task(objective_id, round_id)

        FIXTURE_GUARDED_FILE.write_text("guarded fixture dirty change\n", encoding="utf-8")

        blocked_result = run_json(
            "enforce_worktree.py",
            "--project-id",
            FIXTURE_PROJECT_ID,
            expect_failure=True,
        )
        blocked_issue_codes = {str(issue.get("code") or "").strip() for issue in blocked_result.get("issues", [])}
        if "guarded_exception_paths_without_active_contract" not in blocked_issue_codes:
            raise SystemExit("expected guarded exception enforcement block did not occur")

        contract_result = run_json(
            "activate_exception_contract.py",
            "--project-id",
            FIXTURE_PROJECT_ID,
            "--title",
            "Disposable guarded path exception contract",
            "--summary",
            "Cover the guarded fixture path while this smoke proves enforcement behavior.",
            "--reason",
            "The guarded fixture path is intentionally dirty during this validation run.",
            "--temporary-behavior",
            "Allow one guarded source path to stay dirty while enforcement is being proven.",
            "--risk",
            "Without explicit coverage, the fixture would silently normalize guarded-path debt.",
            "--exit-condition",
            "Retire the contract after guarded-path enforcement has been validated.",
            "--owner-scope",
            "src/",
            "--path",
            "src/",
        )
        contract_id = str(contract_result["exception_contract_id"])

        debug_contracts = run_python_snippet(
            "\n".join(
                [
                    "import json, sys",
                    "sys.path.append('scripts')",
                    "from round_control import find_exception_contracts",
                    f"records = find_exception_contracts('{FIXTURE_PROJECT_ID}', statuses={{'active'}})",
                    "payload = []",
                    "for path, meta, sections in records:",
                    "    payload.append({",
                    "        'path': str(path),",
                    "        'objective_id': meta.get('objective_id'),",
                    "        'paths': meta.get('paths'),",
                    "        'owner_scope': sections.get('Owner Scope', ''),",
                    "    })",
                    "print(json.dumps(payload, ensure_ascii=True, indent=2))",
                ]
            )
        )

        allowed_result = run_json(
            "enforce_worktree.py",
            "--project-id",
            FIXTURE_PROJECT_ID,
        )
        if str(allowed_result.get("status") or "") != "ok":
            raise SystemExit(
                json.dumps(
                    {
                        "message": "guarded path enforcement should pass once active contract coverage exists",
                        "allowed_result": allowed_result,
                        "contract_result": contract_result,
                        "debug_contracts": debug_contracts,
                    },
                    ensure_ascii=True,
                    indent=2,
                )
            )

        run_plain(
            "update_round_status.py",
            "--project-id",
            FIXTURE_PROJECT_ID,
            "--round-id",
            round_id,
            "--status",
            "validation_pending",
            "--reason",
            "Guarded exception enforcement fixture completed behavioral validation.",
        )
        run_plain(
            "update_round_status.py",
            "--project-id",
            FIXTURE_PROJECT_ID,
            "--round-id",
            round_id,
            "--status",
            "captured",
            "--reason",
            "Guarded exception enforcement fixture validated and captured.",
            "--validated-by",
            "uv run python scripts/smoke_guarded_exception_enforcement.py",
        )
        run_plain(
            "update_round_status.py",
            "--project-id",
            FIXTURE_PROJECT_ID,
            "--round-id",
            round_id,
            "--status",
            "closed",
            "--reason",
            "Guarded exception enforcement fixture closed after validation.",
        )

        retire_result = run_json(
            "retire_exception_contract.py",
            "--project-id",
            FIXTURE_PROJECT_ID,
            "--exception-contract-id",
            contract_id,
            "--reason",
            "The guarded enforcement smoke finished and no temporary deviation remains.",
            "--evidence",
            "guarded exception enforcement smoke",
        )

        final_audit = run_json("audit_control_state.py", "--project-id", FIXTURE_PROJECT_ID)
        if int(final_audit["summary"]["errors"]) != 0:
            raise SystemExit("guarded exception enforcement fixture audit reported errors")

        print(
            json.dumps(
                {
                    "project_id": FIXTURE_PROJECT_ID,
                    "objective_id": objective_id,
                    "round_id": round_id,
                    "blocked_status": blocked_result["status"],
                    "allowed_status": allowed_result["status"],
                    "retired_contract_id": retire_result["exception_contract_id"],
                    "fixture_audit": final_audit["status"],
                },
                ensure_ascii=True,
                indent=2,
            )
        )
    finally:
        if FIXTURE_PROJECT_DIR.exists():
            reset_fixture_repo(FIXTURE_PROJECT_DIR)


if __name__ == "__main__":
    main()
