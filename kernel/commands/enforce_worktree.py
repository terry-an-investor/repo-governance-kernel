#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json

from kernel.control_enforcement import evaluate_worktree_enforcement


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Block dishonest round promotion from a dirty or drifting worktree.")
    parser.add_argument("--project-id", required=True)
    parser.add_argument("--round-id", default="")
    parser.add_argument("--workspace-root", default="")
    parser.add_argument("--strict-warnings", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    result = evaluate_worktree_enforcement(
        args.project_id,
        round_id=args.round_id,
        workspace_root=args.workspace_root,
    )
    print(json.dumps(result, ensure_ascii=True, indent=2))
    if int(result["summary"]["errors"]):
        return 1
    if args.strict_warnings and int(result["summary"]["warnings"]):
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
