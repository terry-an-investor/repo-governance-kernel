#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

from audit_control_state import audit_project_control_state
from round_control import load_all_adjudications, parse_bullet_list, project_dir, select_open_round_record


ROOT = Path(__file__).resolve().parent.parent
SCRIPTS = ROOT / "scripts"
SUPPORTED_EXECUTOR_COMMANDS = {
    "close-objective",
    "update-round-status",
    "retire-exception-contract",
    "invalidate-exception-contract",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Execute the safe automatic portion of adjudication follow-ups.")
    parser.add_argument("--project-id", required=True)
    parser.add_argument("--adjudication-id")
    parser.add_argument("--round-title")
    parser.add_argument("--round-scope-item", action="append", default=[])
    parser.add_argument("--round-scope-path", action="append", default=[])
    parser.add_argument("--round-deliverable")
    parser.add_argument("--round-validation-plan")
    parser.add_argument("--round-risk", action="append", default=[])
    parser.add_argument("--round-blocker", action="append", default=[])
    parser.add_argument("--round-status-note", default="")
    return parser.parse_args()


def select_adjudication_record(project_id: str, adjudication_id: str | None) -> tuple[Path, dict[str, object], dict[str, str]]:
    records = load_all_adjudications(project_id)
    if not records:
        raise SystemExit(f"no adjudication records found for project `{project_id}`")
    if adjudication_id:
        for record in records:
            _path, meta, _sections = record
            if str(meta.get("id") or "").strip() == adjudication_id.strip():
                return record
        raise SystemExit(f"adjudication `{adjudication_id}` not found for project `{project_id}`")
    return records[0]


def scaffold_constitution(path: Path, adjudication_id: str) -> None:
    text = "\n".join(
        [
            "# Constitution",
            "",
            f"Scaffolded from adjudication `{adjudication_id}`.",
            "Replace placeholders with real project law before treating this file as authoritative governance.",
            "",
            "## Product Boundaries",
            "",
            "_pending authoring_",
            "",
            "## Architecture Invariants",
            "",
            "_pending authoring_",
            "",
            "## Quality Bar",
            "",
            "_pending authoring_",
            "",
            "## Validation Rules",
            "",
            "_pending authoring_",
            "",
            "## Forbidden Shortcuts",
            "",
            "_pending authoring_",
            "",
        ]
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def scaffold_exception_ledger(path: Path) -> None:
    text = "\n".join(
        [
            "# Exception Ledger",
            "",
            "## Active",
            "",
            "- None recorded yet.",
            "",
            "## Retired",
            "",
            "- None recorded yet.",
            "",
            "## Invalidated",
            "",
            "- None recorded yet.",
            "",
        ]
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def resolve_round_bootstrap(
    args: argparse.Namespace,
    adjudication_meta: dict[str, object],
) -> dict[str, object]:
    cli_scope_items = [item.strip() for item in args.round_scope_item if item.strip()]
    cli_scope_paths = [item.strip() for item in args.round_scope_path if item.strip()]
    cli_risks = [item.strip() for item in args.round_risk if item.strip()]
    cli_blockers = [item.strip() for item in args.round_blocker if item.strip()]
    return {
        "title": (args.round_title or "").strip() or str(adjudication_meta.get("round_title") or "").strip(),
        "scope_items": cli_scope_items or [str(item).strip() for item in adjudication_meta.get("round_scope_items", []) if str(item).strip()],
        "scope_paths": cli_scope_paths or [str(item).strip() for item in adjudication_meta.get("round_scope_paths", []) if str(item).strip()],
        "deliverable": (args.round_deliverable or "").strip() or str(adjudication_meta.get("round_deliverable") or "").strip(),
        "validation_plan": (args.round_validation_plan or "").strip() or str(adjudication_meta.get("round_validation_plan") or "").strip(),
        "risks": cli_risks or [str(item).strip() for item in adjudication_meta.get("round_risks", []) if str(item).strip()],
        "blockers": cli_blockers or [str(item).strip() for item in adjudication_meta.get("round_blockers", []) if str(item).strip()],
        "status_note": (args.round_status_note or "").strip() or str(adjudication_meta.get("round_status_note") or "").strip(),
    }


def parse_executor_followup(followup: str) -> dict[str, object] | None:
    stripped = followup.strip()
    if not stripped.lower().startswith("executor:"):
        return None
    payload_text = stripped[len("executor:") :].strip()
    if not payload_text:
        raise SystemExit(f"executor follow-up is missing JSON payload: `{followup}`")
    try:
        payload = json.loads(payload_text)
    except json.JSONDecodeError as exc:
        raise SystemExit(f"invalid executor follow-up JSON `{followup}`: {exc}") from exc
    if not isinstance(payload, dict):
        raise SystemExit(f"executor follow-up payload must be a JSON object: `{followup}`")
    command_name = str(payload.get("command") or "").strip()
    if not command_name:
        raise SystemExit(f"executor follow-up is missing `command`: `{followup}`")
    if command_name not in SUPPORTED_EXECUTOR_COMMANDS:
        raise SystemExit(
            f"executor follow-up command `{command_name}` is not supported; "
            f"supported commands: {', '.join(sorted(SUPPORTED_EXECUTOR_COMMANDS))}"
        )
    return payload


def _string_list(value: object) -> list[str]:
    if isinstance(value, list):
        return [str(item).strip() for item in value if str(item).strip()]
    if isinstance(value, str) and value.strip():
        return [value.strip()]
    return []


def build_executor_command(project_id: str, payload: dict[str, object]) -> list[str]:
    command_name = str(payload.get("command") or "").strip()
    cmd = [sys.executable, str(SCRIPTS / f"{command_name.replace('-', '_')}.py"), "--project-id", project_id]

    if command_name == "close-objective":
        objective_id = str(payload.get("objective_id") or "").strip()
        closing_status = str(payload.get("closing_status") or "").strip()
        reason = str(payload.get("reason") or "").strip()
        if not closing_status or not reason:
            raise SystemExit("executor close-objective requires `closing_status` and `reason`")
        if objective_id:
            cmd.extend(["--objective-id", objective_id])
        cmd.extend(["--closing-status", closing_status, "--reason", reason])
        for item in _string_list(payload.get("evidence")):
            cmd.extend(["--evidence", item])
        supersession_note = str(payload.get("supersession_note") or "").strip()
        if supersession_note:
            cmd.extend(["--supersession-note", supersession_note])
        return cmd

    if command_name == "update-round-status":
        round_id = str(payload.get("round_id") or "").strip()
        status = str(payload.get("status") or "").strip()
        reason = str(payload.get("reason") or "").strip()
        if not round_id or not status or not reason:
            raise SystemExit("executor update-round-status requires `round_id`, `status`, and `reason`")
        cmd.extend(["--round-id", round_id, "--status", status, "--reason", reason])
        for item in _string_list(payload.get("validated_by")):
            cmd.extend(["--validated-by", item])
        for item in _string_list(payload.get("blocker")):
            cmd.extend(["--blocker", item])
        for item in _string_list(payload.get("risk")):
            cmd.extend(["--risk", item])
        if bool(payload.get("clear_blockers")):
            cmd.append("--clear-blockers")
        return cmd

    if command_name == "retire-exception-contract":
        contract_id = str(payload.get("exception_contract_id") or "").strip()
        reason = str(payload.get("reason") or "").strip()
        if not contract_id or not reason:
            raise SystemExit("executor retire-exception-contract requires `exception_contract_id` and `reason`")
        cmd.extend(["--exception-contract-id", contract_id, "--reason", reason])
        for item in _string_list(payload.get("evidence")):
            cmd.extend(["--evidence", item])
        return cmd

    if command_name == "invalidate-exception-contract":
        contract_id = str(payload.get("exception_contract_id") or "").strip()
        reason = str(payload.get("reason") or "").strip()
        if not contract_id or not reason:
            raise SystemExit("executor invalidate-exception-contract requires `exception_contract_id` and `reason`")
        cmd.extend(["--exception-contract-id", contract_id, "--reason", reason])
        pivot_id = str(payload.get("pivot_id") or "").strip()
        if pivot_id:
            cmd.extend(["--pivot-id", pivot_id])
        for item in _string_list(payload.get("evidence")):
            cmd.extend(["--evidence", item])
        return cmd

    raise SystemExit(f"unsupported executor command `{command_name}`")


def maybe_execute_structured_followup(project_id: str, followup: str) -> tuple[bool, str]:
    payload = parse_executor_followup(followup)
    if payload is None:
        return False, ""
    completed = subprocess.run(
        build_executor_command(project_id, payload),
        cwd=str(ROOT),
        capture_output=True,
        text=True,
        check=False,
    )
    if completed.returncode != 0:
        return False, completed.stderr.strip() or completed.stdout.strip() or "executor follow-up failed"
    command_name = str(payload.get("command") or "").strip()
    return True, f"executed {command_name}"


def maybe_execute_open_round(args: argparse.Namespace, adjudication_meta: dict[str, object]) -> tuple[bool, str]:
    bootstrap = resolve_round_bootstrap(args, adjudication_meta)
    open_round_record, open_round_issues = select_open_round_record(args.project_id)
    if open_round_issues:
        return False, "; ".join(open_round_issues)
    if open_round_record is not None:
        _path, round_meta, _sections = open_round_record
        open_round_id = str(round_meta.get("id") or "").strip()
        open_round_objective_id = str(round_meta.get("objective_id") or "").strip()
        adjudication_objective_id = str(adjudication_meta.get("objective_id") or "").strip()
        if adjudication_objective_id and open_round_objective_id == adjudication_objective_id:
            return True, f"open round `{open_round_id}` already exists for objective `{adjudication_objective_id}`"
        return False, f"open round `{open_round_id}` already exists for a different objective `{open_round_objective_id}`"

    required_present = all(
        [
            str(bootstrap["title"]).strip(),
            bool([item for item in bootstrap["scope_items"] if str(item).strip()]),
            str(bootstrap["deliverable"]).strip(),
            str(bootstrap["validation_plan"]).strip(),
        ]
    )
    if not required_present:
        return False, "missing structured round bootstrap inputs in adjudication or CLI"

    cmd = [
        sys.executable,
        str(SCRIPTS / "open_round.py"),
        "--project-id",
        args.project_id,
        "--title",
        str(bootstrap["title"]).strip(),
        "--deliverable",
        str(bootstrap["deliverable"]).strip(),
        "--validation-plan",
        str(bootstrap["validation_plan"]).strip(),
    ]
    for item in bootstrap["scope_items"]:
        if str(item).strip():
            cmd.extend(["--scope-item", str(item).strip()])
    for item in bootstrap["scope_paths"]:
        if str(item).strip():
            cmd.extend(["--scope-path", str(item).strip()])
    for item in bootstrap["risks"]:
        if str(item).strip():
            cmd.extend(["--risk", str(item).strip()])
    for item in bootstrap["blockers"]:
        if str(item).strip():
            cmd.extend(["--blocker", str(item).strip()])
    if str(bootstrap["status_note"]).strip():
        cmd.extend(["--status-note", str(bootstrap["status_note"]).strip()])

    completed = subprocess.run(
        cmd,
        cwd=str(ROOT),
        capture_output=True,
        text=True,
        check=False,
    )
    if completed.returncode != 0:
        return False, completed.stderr.strip() or completed.stdout.strip() or "open-round failed"
    return True, completed.stdout.strip()


def main() -> int:
    args = parse_args()
    project_path = project_dir(args.project_id)
    if not project_path.exists():
        raise SystemExit(f"project directory not found: {project_path}")

    adjudication_path, adjudication_meta, adjudication_sections = select_adjudication_record(args.project_id, args.adjudication_id)
    adjudication_id = str(adjudication_meta.get("id") or adjudication_path.stem).strip()
    followups = parse_bullet_list(adjudication_sections.get("Required Follow-Up Transitions", ""))
    if not followups:
        raise SystemExit(f"adjudication `{adjudication_id}` has no follow-up transitions")

    applied: list[str] = []
    noop: list[str] = []
    blocked: list[str] = []

    for followup in followups:
        normalized = " ".join(followup.strip().lower().split())
        structured_success, structured_detail = maybe_execute_structured_followup(args.project_id, followup)
        if structured_success:
            applied.append(f"`{followup}` -> {structured_detail}")
            continue
        if followup.strip().lower().startswith("executor:") and structured_detail:
            blocked.append(f"`{followup}` -> {structured_detail}")
            continue

        if "control/constitution.md" in normalized:
            constitution_path = project_path / "control" / "constitution.md"
            if constitution_path.exists():
                noop.append(f"`{followup}` -> constitution already exists")
            else:
                scaffold_constitution(constitution_path, adjudication_id)
                applied.append(f"`{followup}` -> created `{constitution_path.relative_to(ROOT).as_posix()}`")
            continue

        if "control/exception-ledger.md" in normalized:
            ledger_path = project_path / "control" / "exception-ledger.md"
            if ledger_path.exists():
                noop.append(f"`{followup}` -> exception ledger already exists")
            else:
                scaffold_exception_ledger(ledger_path)
                applied.append(f"`{followup}` -> created `{ledger_path.relative_to(ROOT).as_posix()}`")
            continue

        if "open one bounded round" in normalized or "open a bounded round" in normalized:
            success, detail = maybe_execute_open_round(args, adjudication_meta)
            if success:
                if "already exists" in detail:
                    noop.append(f"`{followup}` -> {detail}")
                else:
                    applied.append(f"`{followup}` -> executed open-round")
            else:
                blocked.append(f"`{followup}` -> {detail}")
            continue

        if "rerun audit-control-state" in normalized:
            continue

        blocked.append(f"`{followup}` -> no automatic executor is defined for this follow-up")

    audit_after = audit_project_control_state(args.project_id)
    print(
        json.dumps(
            {
                "project_id": args.project_id,
                "adjudication_id": adjudication_id,
                "adjudication_path": str(adjudication_path),
                "applied": applied,
                "noop": noop,
                "blocked": blocked,
                "audit_after": audit_after,
            },
            ensure_ascii=True,
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
