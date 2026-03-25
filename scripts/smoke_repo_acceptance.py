#!/usr/bin/env python3
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

from smoke_fixture_lib import parse_last_json_object

ROOT = Path(__file__).resolve().parent.parent
SCRIPTS = ROOT / "scripts"
WIND_ARTIFACT_PATH = ROOT / "artifacts" / "wind-agent" / "session-context-smoke.md"
SELF_ARTIFACT_PATH = ROOT / "artifacts" / "session-memory" / "session-context-smoke.md"
ROLE_ARTIFACT_PATH = ROOT / "artifacts" / "session-memory" / "reviewer-context-smoke.md"


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
    return parse_last_json_object(completed.stdout)


def run_plain(script_name: str, *args: str) -> None:
    cmd = [sys.executable, str(SCRIPTS / script_name), *args]
    subprocess.run(cmd, cwd=str(ROOT), check=True)


def run_smoke_suite(*smoke_names: str) -> dict:
    return run_json("run_smoke_suite.py", *[item for name in smoke_names for item in ("--smoke", name)])


def main() -> None:
    session_memory_audit = run_json("audit_control_state.py", "--project-id", "session-memory")
    wind_agent_audit = run_json("audit_control_state.py", "--project-id", "wind-agent")
    smoke_suite_result = run_smoke_suite(
        "adjudication_followups",
        "config_runtime",
        "exception_contracts",
        "guarded_exception_enforcement",
        "repo_onboarding",
        "objective_line",
        "phase_scope_controls",
        "task_contract_bundle_gate",
        "task_contract_hard_gate",
        "transition_engine",
    )
    smoke_results = {str(item["name"]): item["result"] for item in smoke_suite_result.get("smokes", []) if isinstance(item, dict)}
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
    self_query_result = run_json(
        "query_index.py",
        "--project-id",
        "session-memory",
        "--text",
        "workspace",
        "--limit",
        "10",
    )
    run_plain(
        "assemble_context.py",
        "--project-id",
        "wind-agent",
        "--output",
        str(WIND_ARTIFACT_PATH),
    )
    run_plain(
        "assemble_context.py",
        "--project-id",
        "session-memory",
        "--output",
        str(SELF_ARTIFACT_PATH),
    )
    run_plain(
        "compile_role_context.py",
        "--project-id",
        "session-memory",
        "--role",
        "reviewer",
        "--output",
        str(ROLE_ARTIFACT_PATH),
    )

    if build_result["memory_items"] < 1:
        raise SystemExit("memory_items is empty")
    if check_result["memory_fts"] < 1:
        raise SystemExit("memory_fts is empty")
    if build_result["memory_links"] < 1:
        raise SystemExit("memory_links is empty")
    if check_result["memory_links"] < 1:
        raise SystemExit("check memory_links is empty")
    if query_result["count"] < 1:
        raise SystemExit("wind-agent query returned no rows")
    if self_query_result["count"] < 1:
        raise SystemExit("session-memory query returned no rows")
    if not WIND_ARTIFACT_PATH.exists():
        raise SystemExit("wind-agent assemble output missing")
    if not SELF_ARTIFACT_PATH.exists():
        raise SystemExit("session-memory assemble output missing")
    if not ROLE_ARTIFACT_PATH.exists():
        raise SystemExit("session-memory reviewer context output missing")
    role_context_text = ROLE_ARTIFACT_PATH.read_text(encoding="utf-8")
    if "## Current Control Status" not in role_context_text:
        raise SystemExit("session-memory reviewer context missing control status section")
    if "## Current Control Violations" not in role_context_text:
        raise SystemExit("session-memory reviewer context missing control violations section")
    if session_memory_audit["summary"]["errors"] != 0:
        raise SystemExit("session-memory control audit reported errors")
    if wind_agent_audit["summary"]["errors"] != 0:
        raise SystemExit("wind-agent control audit reported errors")

    print(
        json.dumps(
            {
                "audit": {
                    "session-memory": session_memory_audit["status"],
                    "wind-agent": wind_agent_audit["status"],
                },
                "smoke_suite": smoke_suite_result["status"],
                "adjudication_followups": smoke_results["adjudication_followups"],
                "config_runtime": smoke_results["config_runtime"],
                "exception_contracts": smoke_results["exception_contracts"],
                "guarded_exception_enforcement": smoke_results["guarded_exception_enforcement"],
                "repo_onboarding": smoke_results["repo_onboarding"],
                "objective_line": smoke_results["objective_line"],
                "phase_scope_controls": smoke_results["phase_scope_controls"],
                "task_contract_bundle_gate": smoke_results["task_contract_bundle_gate"],
                "task_contract_hard_gate": smoke_results["task_contract_hard_gate"],
                "transition_engine": smoke_results["transition_engine"],
                "build": build_result,
                "check": {
                    "memory_items": check_result["memory_items"],
                    "memory_evidence_refs": check_result["memory_evidence_refs"],
                    "memory_links": check_result["memory_links"],
                    "memory_fts": check_result["memory_fts"],
                },
                "query": {
                    "wind-agent": query_result["count"],
                    "session-memory": self_query_result["count"],
                },
                "artifacts": {
                    "wind-agent": str(WIND_ARTIFACT_PATH),
                    "session-memory": str(SELF_ARTIFACT_PATH),
                    "session-memory-reviewer": str(ROLE_ARTIFACT_PATH),
                },
            },
            ensure_ascii=True,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
