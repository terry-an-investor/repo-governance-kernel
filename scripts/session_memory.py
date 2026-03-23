#!/usr/bin/env python3
from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
SCRIPTS = ROOT / "scripts"


COMMAND_MAP = {
    "build-index": SCRIPTS / "build_index.py",
    "check-index": SCRIPTS / "check_index.py",
    "query": SCRIPTS / "query_index.py",
    "assemble": SCRIPTS / "assemble_context.py",
    "capture-handoff": SCRIPTS / "capture_handoff.py",
    "create-snapshot": SCRIPTS / "create_snapshot.py",
    "refresh-current-task-anchor": SCRIPTS / "refresh_current_task_anchor.py",
    "smoke": SCRIPTS / "smoke_phase1.py",
    "eval-wind-agent": SCRIPTS / "run_wind_agent_eval.py",
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
