#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re

from kernel.executor_runtime import run_cli_command
from kernel.host_adoption import external_target_assessment_next_actions
from kernel.public_flow_contracts import parse_json_dict, reframe_public_flow_payload, render_public_flow_payload


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
    intent_compilation = {
        "intent_class": "external-target-single-assessment",
        "request": request,
        "workspace_root": "",
        "source_repo": "",
        "scope_strategy": "dirty-path-derived",
        "execution_surface": "governed-bundle-backed-workflow",
        "bundle_name": "assess-external-target-once",
    }
    if not request:
        raise SystemExit(
            render_public_flow_payload(
                status="blocked",
                flow_name="external-target-single-assessment",
                entrypoint="assess-external-target-from-intent",
                entry_kind="intent-wrapper",
                project_id=args.project_id,
                intent_compilation=intent_compilation,
                next_actions=[
                    "Provide one explicit assessment request instead of an empty prompt.",
                    "Include one workspace path or pass `--workspace-root` directly.",
                ],
                blocked={
                    "stage": "intent-compilation",
                    "code": "empty_request",
                    "message": "bounded intent assessment requires a non-empty request",
                    "meaning": "the intent wrapper can only compile one explicit external-target assessment request",
                    "suggested_next_actions": [
                        "Provide one explicit assessment request instead of an empty prompt.",
                        "Include one workspace path or pass `--workspace-root` directly.",
                    ],
                },
            )
        )

    normalized_request = request.lower()
    if _contains_any(normalized_request, MONITORING_KEYWORDS) and not _contains_any(
        normalized_request,
        NEGATED_MONITORING_PHRASES,
    ):
        raise SystemExit(
            render_public_flow_payload(
                status="blocked",
                flow_name="external-target-single-assessment",
                entrypoint="assess-external-target-from-intent",
                entry_kind="intent-wrapper",
                project_id=args.project_id,
                intent_compilation=intent_compilation,
                next_actions=[
                    "Keep this wrapper scoped to one-time assessment requests.",
                    "Do not ask this surface for continuous monitoring or background services.",
                ],
                blocked={
                    "stage": "intent-compilation",
                    "code": "unsupported_request_scope",
                    "message": "bounded intent assessment only supports one-time external-target evaluation; continuous monitoring intents are out of scope",
                    "meaning": "the assessment wrapper is intentionally bounded to one-time evaluation and does not compile monitoring requests",
                    "suggested_next_actions": [
                        "Keep this wrapper scoped to one-time assessment requests.",
                        "Do not ask this surface for continuous monitoring or background services.",
                    ],
                },
            )
        )
    if not _contains_any(normalized_request, ASSESSMENT_KEYWORDS):
        raise SystemExit(
            render_public_flow_payload(
                status="blocked",
                flow_name="external-target-single-assessment",
                entrypoint="assess-external-target-from-intent",
                entry_kind="intent-wrapper",
                project_id=args.project_id,
                intent_compilation=intent_compilation,
                next_actions=[
                    "Ask for an assessment explicitly with wording like assess/evaluate/check or 评估/检查.",
                ],
                blocked={
                    "stage": "intent-compilation",
                    "code": "assessment_intent_not_detected",
                    "message": "bounded intent assessment requires an assessment-style request such as assess/evaluate/check or 评估/检查",
                    "meaning": "the wrapper only compiles one-time assessment requests into the external-target workflow",
                    "suggested_next_actions": [
                        "Ask for an assessment explicitly with wording like assess/evaluate/check or 评估/检查.",
                    ],
                },
            )
        )

    workspace_root = args.workspace_root.strip() or _extract_workspace_root(request)
    if not workspace_root:
        raise SystemExit(
            render_public_flow_payload(
                status="blocked",
                flow_name="external-target-single-assessment",
                entrypoint="assess-external-target-from-intent",
                entry_kind="intent-wrapper",
                project_id=args.project_id,
                intent_compilation=intent_compilation,
                next_actions=[
                    "Pass `--workspace-root` directly or include one explicit repo path in the request.",
                ],
                blocked={
                    "stage": "intent-compilation",
                    "code": "workspace_root_not_detected",
                    "message": "bounded intent assessment requires `--workspace-root` or one explicit workspace path in the request",
                    "meaning": "the wrapper cannot bind the assessment to a target repo until one explicit workspace path is available",
                    "suggested_next_actions": [
                        "Pass `--workspace-root` directly or include one explicit repo path in the request.",
                    ],
                },
            )
        )
    source_repo = args.source_repo.strip() or workspace_root
    intent_compilation["workspace_root"] = workspace_root
    intent_compilation["source_repo"] = source_repo

    success, detail = run_cli_command(
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
    payload = parse_json_dict(detail)
    if payload is None:
        next_actions = external_target_assessment_next_actions(
            project_id=args.project_id,
            workspace_root=workspace_root,
        )
        raise SystemExit(
            render_public_flow_payload(
                status="blocked",
                flow_name="external-target-single-assessment",
                entrypoint="assess-external-target-from-intent",
                entry_kind="intent-wrapper",
                project_id=args.project_id,
                workspace_root=workspace_root,
                source_repo=source_repo,
                intent_compilation=intent_compilation,
                next_actions=next_actions,
                blocked={
                    "stage": "workflow-execution",
                    "code": "workflow_response_invalid",
                    "message": detail or "bounded intent assessment workflow failed",
                    "meaning": "the wrapper expected one structured assessment payload from the public workflow but received invalid output",
                    "suggested_next_actions": next_actions,
                },
            )
        )

    reframed = reframe_public_flow_payload(
        payload,
        entrypoint="assess-external-target-from-intent",
        entry_kind="intent-wrapper",
        intent_compilation=intent_compilation,
    )
    if success and str(reframed.get("status") or "") == "ok":
        print(json.dumps(reframed, ensure_ascii=True, indent=2))
        return 0
    raise SystemExit(json.dumps(reframed, ensure_ascii=True, indent=2))


if __name__ == "__main__":
    raise SystemExit(main())
