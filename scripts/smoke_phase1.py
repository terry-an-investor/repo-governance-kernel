#!/usr/bin/env python3
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
SCRIPTS = ROOT / "scripts"
ARTIFACT_PATH = ROOT / "artifacts" / "wind-agent" / "session-context-smoke.md"


def run_json(script_name: str, *args: str) -> dict:
    cmd = [sys.executable, str(SCRIPTS / script_name), *args]
    completed = subprocess.run(
        cmd,
        cwd=str(ROOT),
        capture_output=True,
        text=True,
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


def run_plain(script_name: str, *args: str) -> None:
    cmd = [sys.executable, str(SCRIPTS / script_name), *args]
    subprocess.run(cmd, cwd=str(ROOT), check=True)


def main() -> None:
    build_result = run_json("build_index.py")
    check_result = run_json("check_index.py")
    query_result = run_json(
        "query_index.py",
        "--project-id",
        "wind-agent",
        "--text",
        "contract",
        "--limit",
        "10",
    )
    run_plain(
        "assemble_context.py",
        "--project-id",
        "wind-agent",
        "--output",
        str(ARTIFACT_PATH),
    )

    if build_result["memory_items"] < 1:
        raise SystemExit("memory_items is empty")
    if check_result["memory_fts"] < 1:
        raise SystemExit("memory_fts is empty")
    if query_result["count"] < 1:
        raise SystemExit("query returned no rows")
    if not ARTIFACT_PATH.exists():
        raise SystemExit("assemble output missing")

    print(
        json.dumps(
            {
                "build": build_result,
                "check": {
                    "memory_items": check_result["memory_items"],
                    "memory_evidence_refs": check_result["memory_evidence_refs"],
                    "memory_fts": check_result["memory_fts"],
                },
                "query_count": query_result["count"],
                "artifact": str(ARTIFACT_PATH),
            },
            ensure_ascii=True,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
