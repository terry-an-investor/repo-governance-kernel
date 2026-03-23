#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

from smoke_fixture_lib import parse_last_json_object
from smoke_manifest import ROOT, SmokeSpec, select_smoke_specs


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run registered smoke scripts under one harness-law suite runner.")
    parser.add_argument("--smoke", action="append", default=[], help="one registered smoke name; repeatable")
    parser.add_argument("--list", action="store_true", help="print the registered smoke manifest and exit")
    return parser.parse_args()


def _fixture_paths_exist(spec: SmokeSpec) -> list[str]:
    leaked: list[str] = []
    for fixture_path in spec.fixture_paths:
        if fixture_path.exists():
            leaked.append(str(fixture_path.relative_to(ROOT).as_posix()))
    return leaked


def _run_smoke(spec: SmokeSpec) -> dict[str, object]:
    leaked_before = _fixture_paths_exist(spec)
    if leaked_before:
        raise SystemExit(
            json.dumps(
                {
                    "smoke": spec.name,
                    "error": "fixture_leak_before_run",
                    "fixture_paths": leaked_before,
                },
                ensure_ascii=True,
                indent=2,
            )
        )

    completed = subprocess.run(
        [sys.executable, str(spec.script_path)],
        cwd=str(ROOT),
        capture_output=True,
        text=True,
        check=False,
    )
    if completed.returncode != 0:
        raise SystemExit(
            json.dumps(
                {
                    "smoke": spec.name,
                    "error": "smoke_failed",
                    "returncode": completed.returncode,
                    "stdout": completed.stdout,
                    "stderr": completed.stderr,
                },
                ensure_ascii=True,
                indent=2,
            )
        )

    leaked_after = _fixture_paths_exist(spec)
    if leaked_after:
        raise SystemExit(
            json.dumps(
                {
                    "smoke": spec.name,
                    "error": "fixture_leak_after_run",
                    "fixture_paths": leaked_after,
                },
                ensure_ascii=True,
                indent=2,
            )
        )

    try:
        payload = parse_last_json_object(completed.stdout)
    except json.JSONDecodeError as exc:
        raise SystemExit(
            json.dumps(
                {
                    "smoke": spec.name,
                    "error": "invalid_smoke_output",
                    "stdout": completed.stdout,
                    "stderr": completed.stderr,
                    "decode_error": str(exc),
                },
                ensure_ascii=True,
                indent=2,
            )
        )
    return {
        "name": spec.name,
        "script": spec.script_name,
        "parallel_safe": spec.parallel_safe,
        "fixture_project_ids": list(spec.fixture_project_ids),
        "result": payload,
    }


def main() -> int:
    args = parse_args()
    selected = select_smoke_specs(args.smoke)
    if args.list:
        print(json.dumps([spec.to_dict() for spec in selected], ensure_ascii=True, indent=2))
        return 0

    if any(spec.parallel_safe for spec in selected):
        raise SystemExit("parallel-safe smoke execution is not implemented yet; suite runner currently executes all selected smokes serially")

    results: list[dict[str, object]] = []
    for spec in selected:
        results.append(_run_smoke(spec))

    print(
        json.dumps(
            {
                "status": "ok",
                "smokes": results,
            },
            ensure_ascii=True,
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
