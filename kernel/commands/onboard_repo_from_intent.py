#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json

from kernel.executor_runtime import run_cli_command_json


ONBOARDING_KEYWORDS = (
    "onboard",
    "initialize",
    "initialise",
    "bootstrap",
    "set up",
    "setup",
    "init",
    "attach",
    "接入",
    "初始化",
    "接管",
)
REPO_TARGET_KEYWORDS = (
    "repo",
    "repository",
    "codebase",
    "项目",
    "仓库",
)
REJECTED_KEYWORDS = (
    "monitor",
    "monitoring",
    "continuous",
    "持续监控",
    "实时监控",
    "监控",
    "assess",
    "assessment",
    "评估",
)
NEGATED_REJECTED_PHRASES = (
    "不要监控",
    "不做监控",
    "no monitoring",
    "not monitoring",
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Interpret one bounded natural-language onboarding intent and run the governed repo onboarding workflow."
    )
    parser.add_argument("--project-id", required=True)
    parser.add_argument("--request", required=True)
    parser.add_argument("--skip-hooks", action="store_true")
    return parser.parse_args()


def _contains_any(text: str, needles: tuple[str, ...]) -> bool:
    return any(needle in text for needle in needles)


def main() -> int:
    args = parse_args()
    request = args.request.strip()
    if not request:
        raise SystemExit("bounded onboarding intent requires a non-empty request")

    normalized_request = request.lower()
    if _contains_any(normalized_request, REJECTED_KEYWORDS) and not _contains_any(normalized_request, NEGATED_REJECTED_PHRASES):
        raise SystemExit(
            "bounded onboarding intent only supports first-control-line repo initialization; monitoring or assessment intents are out of scope"
        )
    if not _contains_any(normalized_request, ONBOARDING_KEYWORDS):
        raise SystemExit(
            "bounded onboarding intent requires an initialization-style request such as onboard/bootstrap/init or 初始化/接入"
        )
    if not _contains_any(normalized_request, REPO_TARGET_KEYWORDS):
        raise SystemExit(
            "bounded onboarding intent requires an explicit repo-style target such as repo/repository/codebase or 仓库/项目"
        )

    workflow = run_cli_command_json(
        "onboard-repo",
        [
            "--project-id",
            args.project_id,
            *(["--skip-hooks"] if args.skip_hooks else []),
        ],
        failure_message="bounded onboarding workflow failed",
    )

    print(
        json.dumps(
            {
                "status": "ok",
                "compiled_intent": {
                    "intent_class": "repo-first-host-onboarding",
                    "request": request,
                    "project_id": args.project_id,
                    "execution_surface": "governed-bundle-backed-workflow",
                    "bundle_name": "onboard-repo",
                    "hook_installation_requested": not bool(args.skip_hooks),
                },
                "workflow": workflow,
            },
            ensure_ascii=True,
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
