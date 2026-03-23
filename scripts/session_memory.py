#!/usr/bin/env python3
from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
SCRIPTS = ROOT / "scripts"


COMMAND_MAP = {
    "adjudicate-control-state": SCRIPTS / "adjudicate_control_state.py",
    "audit-control-state": SCRIPTS / "audit_control_state.py",
    "build-index": SCRIPTS / "build_index.py",
    "check-index": SCRIPTS / "check_index.py",
    "query": SCRIPTS / "query_index.py",
    "assemble": SCRIPTS / "assemble_context.py",
    "compile-role-context": SCRIPTS / "compile_role_context.py",
    "capture-handoff": SCRIPTS / "capture_handoff.py",
    "close-objective": SCRIPTS / "close_objective.py",
    "create-snapshot": SCRIPTS / "create_snapshot.py",
    "open-objective": SCRIPTS / "open_objective.py",
    "prepare-role-eval": SCRIPTS / "prepare_role_eval_bundle.py",
    "open-round": SCRIPTS / "open_round.py",
    "activate-exception-contract": SCRIPTS / "activate_exception_contract.py",
    "record-hard-pivot": SCRIPTS / "record_hard_pivot.py",
    "record-soft-pivot": SCRIPTS / "record_soft_pivot.py",
    "reconcile-control-state": SCRIPTS / "reconcile_control_state.py",
    "retire-exception-contract": SCRIPTS / "retire_exception_contract.py",
    "refresh-current-task-anchor": SCRIPTS / "refresh_current_task_anchor.py",
    "smoke": SCRIPTS / "smoke_phase1.py",
    "update-round-status": SCRIPTS / "update_round_status.py",
    "invalidate-exception-contract": SCRIPTS / "invalidate_exception_contract.py",
    "eval-wind-agent": SCRIPTS / "run_wind_agent_eval.py",
    "execute-adjudication-followups": SCRIPTS / "execute_adjudication_followups.py",
}


def main() -> int:
    parser = argparse.ArgumentParser(description="Unified CLI for session-memory phase-1 workflows.")
    parser.add_argument("command", choices=sorted(COMMAND_MAP))
    parser.add_argument("args", nargs=argparse.REMAINDER)
    parsed = parser.parse_args()

    script_path = COMMAND_MAP[parsed.command]
    cmd = [sys.executable, str(script_path), *parsed.args]
    completed = subprocess.run(cmd, cwd=str(ROOT))
    return completed.returncode


if __name__ == "__main__":
    raise SystemExit(main())
