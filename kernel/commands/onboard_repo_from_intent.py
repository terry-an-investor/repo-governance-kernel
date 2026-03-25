#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json

from kernel.executor_runtime import run_cli_command
from kernel.public_flow_contracts import parse_json_dict, reframe_public_flow_payload, render_public_flow_payload
from kernel.repo_onboarding import onboarding_blocked_next_actions


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
    intent_compilation = {
        "intent_class": "repo-first-host-onboarding",
        "request": request,
        "project_id": args.project_id,
        "execution_surface": "governed-bundle-backed-workflow",
        "bundle_name": "onboard-repo",
        "hook_installation_requested": not bool(args.skip_hooks),
    }
    if not request:
        raise SystemExit(
            render_public_flow_payload(
                status="blocked",
                flow_name="repo-onboarding",
                entrypoint="onboard-repo-from-intent",
                entry_kind="intent-wrapper",
                project_id=args.project_id,
                intent_compilation=intent_compilation,
                next_actions=[
                    "Provide one explicit initialization request instead of an empty prompt.",
                    "Use wording like onboard/bootstrap/init or 初始化/接入 and mention the repo target.",
                ],
                blocked={
                    "stage": "intent-compilation",
                    "code": "empty_request",
                    "message": "bounded onboarding intent requires a non-empty request",
                    "meaning": "the intent wrapper can only compile one explicit onboarding request into the governed onboarding workflow",
                    "suggested_next_actions": [
                        "Provide one explicit initialization request instead of an empty prompt.",
                        "Use wording like onboard/bootstrap/init or 初始化/接入 and mention the repo target.",
                    ],
                },
            )
        )

    normalized_request = request.lower()
    if _contains_any(normalized_request, REJECTED_KEYWORDS) and not _contains_any(normalized_request, NEGATED_REJECTED_PHRASES):
        raise SystemExit(
            render_public_flow_payload(
                status="blocked",
                flow_name="repo-onboarding",
                entrypoint="onboard-repo-from-intent",
                entry_kind="intent-wrapper",
                project_id=args.project_id,
                intent_compilation=intent_compilation,
                next_actions=[
                    "Keep this wrapper scoped to first-control-line onboarding requests.",
                    "Use `assess-external-target-from-intent` for one-time repo assessment instead of asking onboarding to monitor or assess.",
                ],
                blocked={
                    "stage": "intent-compilation",
                    "code": "unsupported_request_scope",
                    "message": "bounded onboarding intent only supports first-control-line repo initialization; monitoring or assessment intents are out of scope",
                    "meaning": "the onboarding wrapper is intentionally narrow and does not compile monitoring or assessment requests",
                    "suggested_next_actions": [
                        "Keep this wrapper scoped to first-control-line onboarding requests.",
                        "Use `assess-external-target-from-intent` for one-time repo assessment instead of asking onboarding to monitor or assess.",
                    ],
                },
            )
        )
    if not _contains_any(normalized_request, ONBOARDING_KEYWORDS):
        raise SystemExit(
            render_public_flow_payload(
                status="blocked",
                flow_name="repo-onboarding",
                entrypoint="onboard-repo-from-intent",
                entry_kind="intent-wrapper",
                project_id=args.project_id,
                intent_compilation=intent_compilation,
                next_actions=[
                    "Ask for onboarding explicitly with wording like onboard/bootstrap/init or 初始化/接入.",
                ],
                blocked={
                    "stage": "intent-compilation",
                    "code": "initialization_intent_not_detected",
                    "message": "bounded onboarding intent requires an initialization-style request such as onboard/bootstrap/init or 初始化/接入",
                    "meaning": "the wrapper only compiles initialization requests into the repo onboarding flow",
                    "suggested_next_actions": [
                        "Ask for onboarding explicitly with wording like onboard/bootstrap/init or 初始化/接入.",
                    ],
                },
            )
        )
    if not _contains_any(normalized_request, REPO_TARGET_KEYWORDS):
        raise SystemExit(
            render_public_flow_payload(
                status="blocked",
                flow_name="repo-onboarding",
                entrypoint="onboard-repo-from-intent",
                entry_kind="intent-wrapper",
                project_id=args.project_id,
                intent_compilation=intent_compilation,
                next_actions=[
                    "Mention the repo target explicitly with repo/repository/codebase or 仓库/项目.",
                ],
                blocked={
                    "stage": "intent-compilation",
                    "code": "repo_target_not_detected",
                    "message": "bounded onboarding intent requires an explicit repo-style target such as repo/repository/codebase or 仓库/项目",
                    "meaning": "the wrapper only compiles repo-first onboarding requests, so the target repo must be explicit in the request",
                    "suggested_next_actions": [
                        "Mention the repo target explicitly with repo/repository/codebase or 仓库/项目.",
                    ],
                },
            )
        )

    success, detail = run_cli_command(
        "onboard-repo",
        [
            "--project-id",
            args.project_id,
            *(["--skip-hooks"] if args.skip_hooks else []),
        ],
        failure_message="bounded onboarding workflow failed",
    )
    payload = parse_json_dict(detail)
    if payload is None:
        raise SystemExit(
            render_public_flow_payload(
                status="blocked",
                flow_name="repo-onboarding",
                entrypoint="onboard-repo-from-intent",
                entry_kind="intent-wrapper",
                project_id=args.project_id,
                intent_compilation=intent_compilation,
                next_actions=onboarding_blocked_next_actions(args.project_id, "", "bundle_execution_failed"),
                blocked={
                    "stage": "workflow-execution",
                    "code": "workflow_response_invalid",
                    "message": detail or "bounded onboarding workflow failed",
                    "meaning": "the wrapper expected one structured onboarding payload from the public workflow but received invalid output",
                    "suggested_next_actions": onboarding_blocked_next_actions(args.project_id, "", "bundle_execution_failed"),
                },
            )
        )

    reframed = reframe_public_flow_payload(
        payload,
        entrypoint="onboard-repo-from-intent",
        entry_kind="intent-wrapper",
        intent_compilation=intent_compilation,
    )
    if success and str(reframed.get("status") or "") == "ok":
        print(json.dumps(reframed, ensure_ascii=True, indent=2))
        return 0
    raise SystemExit(json.dumps(reframed, ensure_ascii=True, indent=2))


if __name__ == "__main__":
    raise SystemExit(main())
