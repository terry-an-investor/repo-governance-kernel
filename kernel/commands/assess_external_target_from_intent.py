#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re

from kernel.executor_runtime import run_cli_command_json


WINDOWS_PATH_RE = re.compile(r"([A-Za-z]:[\\/][^\s\"`]+)")
POSIX_PATH_RE = re.compile(r"(/[^\s\"`]+)")

ASSESSMENT_KEYWORDS = (
    "assess",
    "assessment",
    "evaluate",
    "evaluation",
    "check",
    "inspect",
    "review",
    "评估",
    "检查",
    "看一下",
    "看看",
    "结论",
)
MONITORING_KEYWORDS = (
    "continuous monitoring",
    "monitoring",
    "monitor",
    "持续监控",
    "实时监控",
    "监控",
)
NEGATED_MONITORING_PHRASES = (
    "不要监控",
    "不做监控",
    "no monitoring",
    "not monitoring",
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Interpret one bounded natural-language intent and run the governed external-target assessment workflow."
    )
    parser.add_argument("--project-id", required=True)
    parser.add_argument("--request", required=True)
    parser.add_argument("--workspace-root", default="")
    parser.add_argument("--source-repo", default="")
    parser.add_argument("--draft-output", default="")
    parser.add_argument("--report-output", default="")
    return parser.parse_args()


def _extract_workspace_root(request: str) -> str:
    for pattern in (WINDOWS_PATH_RE, POSIX_PATH_RE):
        match = pattern.search(request)
        if match:
            return str(match.group(1)).replace("\\", "/")
    return ""


def _contains_any(text: str, needles: tuple[str, ...]) -> bool:
    return any(needle in text for needle in needles)


def main() -> int:
    args = parse_args()
    request = args.request.strip()
    if not request:
        raise SystemExit("bounded intent assessment requires a non-empty request")

    normalized_request = request.lower()
    if _contains_any(normalized_request, MONITORING_KEYWORDS) and not _contains_any(
        normalized_request,
        NEGATED_MONITORING_PHRASES,
    ):
        raise SystemExit(
            "bounded intent assessment only supports one-time external-target evaluation; continuous monitoring intents are out of scope"
        )
    if not _contains_any(normalized_request, ASSESSMENT_KEYWORDS):
        raise SystemExit(
            "bounded intent assessment requires an assessment-style request such as assess/evaluate/check or 评估/检查"
        )

    workspace_root = args.workspace_root.strip() or _extract_workspace_root(request)
    if not workspace_root:
        raise SystemExit("bounded intent assessment requires `--workspace-root` or one explicit workspace path in the request")
    source_repo = args.source_repo.strip() or workspace_root

    workflow = run_cli_command_json(
        "assess-external-target-once",
        [
            "--project-id",
            args.project_id,
            "--workspace-root",
            workspace_root,
            "--source-repo",
            source_repo,
            *(["--draft-output", args.draft_output.strip()] if args.draft_output.strip() else []),
            *(["--report-output", args.report_output.strip()] if args.report_output.strip() else []),
        ],
        failure_message="bounded intent assessment workflow failed",
    )

    print(
        json.dumps(
            {
                "status": "ok",
                "compiled_intent": {
                    "intent_class": "external-target-single-assessment",
                    "request": request,
                    "workspace_root": workspace_root,
                    "source_repo": source_repo,
                    "scope_strategy": "dirty-path-derived",
                    "execution_surface": "governed-bundle-backed-workflow",
                    "bundle_name": "assess-external-target-once",
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
