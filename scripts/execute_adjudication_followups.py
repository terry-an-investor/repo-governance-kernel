#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

from audit_control_state import audit_project_control_state
from compile_adjudication_executor_plan import compile_plan_contracts
from round_control import (
    load_all_adjudications,
    load_round_file,
    locate_round_file,
    parse_bullet_list,
    project_dir,
    select_open_round_record,
)


ROOT = Path(__file__).resolve().parent.parent
SCRIPTS = ROOT / "scripts"
SUPPORTED_EXECUTOR_COMMANDS = {
    "close-objective",
    "refresh-round-scope",
    "rewrite-open-round",
    "round-close-chain",
    "set-phase",
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


def parse_executor_followup_payload(payload_text: str, *, source_label: str) -> dict[str, object]:
    if not payload_text.strip():
        raise SystemExit(f"executor follow-up is missing JSON payload: {source_label}")
    try:
        payload = json.loads(payload_text)
    except json.JSONDecodeError as exc:
        raise SystemExit(f"invalid executor follow-up JSON {source_label}: {exc}") from exc
    if not isinstance(payload, dict):
        raise SystemExit(f"executor follow-up payload must be a JSON object: {source_label}")
    command_name = str(payload.get("command") or "").strip()
    if not command_name:
        raise SystemExit(f"executor follow-up is missing `command`: {source_label}")
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


def require_payload_text(payload: dict[str, object], field_name: str) -> str:
    value = str(payload.get(field_name) or "").strip()
    if not value:
        raise SystemExit(f"executor {payload.get('command')} requires `{field_name}`")
    return value


def build_update_round_status_command(
    project_id: str,
    *,
    round_id: str,
    status: str,
    reason: str,
    validated_by: list[str] | None = None,
    blockers: list[str] | None = None,
    risks: list[str] | None = None,
    clear_blockers: bool = False,
) -> list[str]:
    cmd = [
        sys.executable,
        str(SCRIPTS / "update_round_status.py"),
        "--project-id",
        project_id,
        "--round-id",
        round_id,
        "--status",
        status,
        "--reason",
        reason,
    ]
    for item in validated_by or []:
        if item.strip():
            cmd.extend(["--validated-by", item.strip()])
    for item in blockers or []:
        if item.strip():
            cmd.extend(["--blocker", item.strip()])
    for item in risks or []:
        if item.strip():
            cmd.extend(["--risk", item.strip()])
    if clear_blockers:
        cmd.append("--clear-blockers")
    return cmd


def run_executor_command(cmd: list[str]) -> tuple[bool, str]:
    completed = subprocess.run(
        cmd,
        cwd=str(ROOT),
        capture_output=True,
        text=True,
        check=False,
    )
    if completed.returncode != 0:
        return False, completed.stderr.strip() or completed.stdout.strip() or "executor follow-up failed"
    return True, completed.stdout.strip()


def build_round_close_chain_commands(project_id: str, payload: dict[str, object]) -> tuple[str, list[tuple[str, list[str]]]]:
    round_id = require_payload_text(payload, "round_id")
    round_path = locate_round_file(project_id, round_id)
    if round_path is None:
        raise SystemExit(f"executor round-close-chain could not find round `{round_id}`")

    round_meta, _sections = load_round_file(round_path)
    current_status = str(round_meta.get("status") or "").strip()
    if not current_status:
        raise SystemExit(f"executor round-close-chain found round `{round_id}` without a status")

    validated_by = _string_list(payload.get("validated_by"))
    blockers = _string_list(payload.get("blocker"))
    risks = _string_list(payload.get("risk"))
    clear_blockers = bool(payload.get("clear_blockers"))

    if current_status == "closed":
        return round_id, []
    if current_status == "captured":
        return round_id, [
            (
                "captured -> closed",
                build_update_round_status_command(
                    project_id,
                    round_id=round_id,
                    status="closed",
                    reason=require_payload_text(payload, "closed_reason"),
                ),
            )
        ]
    if current_status == "validation_pending":
        if not validated_by:
            raise SystemExit("executor round-close-chain requires `validated_by` when round is not yet captured")
        return round_id, [
            (
                "validation_pending -> captured",
                build_update_round_status_command(
                    project_id,
                    round_id=round_id,
                    status="captured",
                    reason=require_payload_text(payload, "captured_reason"),
                    validated_by=validated_by,
                    blockers=blockers,
                    risks=risks,
                    clear_blockers=clear_blockers,
                ),
            ),
            (
                "captured -> closed",
                build_update_round_status_command(
                    project_id,
                    round_id=round_id,
                    status="closed",
                    reason=require_payload_text(payload, "closed_reason"),
                ),
            ),
        ]
    if current_status == "active":
        if not validated_by:
            raise SystemExit("executor round-close-chain requires `validated_by` when round is not yet captured")
        return round_id, [
            (
                "active -> validation_pending",
                build_update_round_status_command(
                    project_id,
                    round_id=round_id,
                    status="validation_pending",
                    reason=require_payload_text(payload, "validation_pending_reason"),
                ),
            ),
            (
                "validation_pending -> captured",
                build_update_round_status_command(
                    project_id,
                    round_id=round_id,
                    status="captured",
                    reason=require_payload_text(payload, "captured_reason"),
                    validated_by=validated_by,
                    blockers=blockers,
                    risks=risks,
                    clear_blockers=clear_blockers,
                ),
            ),
            (
                "captured -> closed",
                build_update_round_status_command(
                    project_id,
                    round_id=round_id,
                    status="closed",
                    reason=require_payload_text(payload, "closed_reason"),
                ),
            ),
        ]
    raise SystemExit(
        f"executor round-close-chain only supports rounds currently in `active`, `validation_pending`, `captured`, or `closed`; found `{current_status}`"
    )


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

    if command_name == "refresh-round-scope":
        round_id = str(payload.get("round_id") or "").strip()
        reason = str(payload.get("reason") or "").strip()
        if not reason:
            raise SystemExit("executor refresh-round-scope requires `reason`")
        if round_id:
            cmd.extend(["--round-id", round_id])
        cmd.extend(["--reason", reason])
        for item in _string_list(payload.get("evidence")):
            cmd.extend(["--evidence", item])
        for item in _string_list(payload.get("add_scope_path")):
            cmd.extend(["--add-scope-path", item])
        for item in _string_list(payload.get("drop_scope_path")):
            cmd.extend(["--drop-scope-path", item])
        if bool(payload.get("no_live_dirty_paths")):
            cmd.append("--no-live-dirty-paths")
        return cmd

    if command_name == "rewrite-open-round":
        reason = str(payload.get("reason") or "").strip()
        if not reason:
            raise SystemExit("executor rewrite-open-round requires `reason`")
        round_id = str(payload.get("round_id") or "").strip()
        if round_id:
            cmd.extend(["--round-id", round_id])
        cmd.extend(["--reason", reason])
        title = str(payload.get("title") or "").strip()
        if title:
            cmd.extend(["--title", title])
        summary = str(payload.get("summary") or "").strip()
        if summary:
            cmd.extend(["--summary", summary])
        deliverable = str(payload.get("deliverable") or "").strip()
        if deliverable:
            cmd.extend(["--deliverable", deliverable])
        validation_plan = str(payload.get("validation_plan") or "").strip()
        if validation_plan:
            cmd.extend(["--validation-plan", validation_plan])
        for item in _string_list(payload.get("scope_item")):
            cmd.extend(["--scope-item", item])
        for item in _string_list(payload.get("scope_path")):
            cmd.extend(["--scope-path", item])
        for item in _string_list(payload.get("risk")):
            cmd.extend(["--risk", item])
        for item in _string_list(payload.get("blocker")):
            cmd.extend(["--blocker", item])
        for item in _string_list(payload.get("status_note")):
            cmd.extend(["--status-note", item])
        if bool(payload.get("replace_scope_items")):
            cmd.append("--replace-scope-items")
        if bool(payload.get("replace_risks")):
            cmd.append("--replace-risks")
        if bool(payload.get("replace_blockers")):
            cmd.append("--replace-blockers")
        if bool(payload.get("replace_scope_paths")):
            cmd.append("--replace-scope-paths")
        return cmd

    if command_name == "set-phase":
        phase = str(payload.get("phase") or "").strip()
        reason = str(payload.get("reason") or "").strip()
        if not phase or not reason:
            raise SystemExit("executor set-phase requires `phase` and `reason`")
        objective_id = str(payload.get("objective_id") or "").strip()
        if objective_id:
            cmd.extend(["--objective-id", objective_id])
        cmd.extend(["--phase", phase, "--reason", reason])
        for item in _string_list(payload.get("evidence")):
            cmd.extend(["--evidence", item])
        for item in _string_list(payload.get("scope_review_note")):
            cmd.extend(["--scope-review-note", item])
        if bool(payload.get("auto_open_round")):
            cmd.append("--auto-open-round")
        round_title = str(payload.get("round_title") or "").strip()
        if round_title:
            cmd.extend(["--round-title", round_title])
        round_summary = str(payload.get("round_summary") or "").strip()
        if round_summary:
            cmd.extend(["--round-summary", round_summary])
        for item in _string_list(payload.get("round_scope_item")):
            cmd.extend(["--round-scope-item", item])
        for item in _string_list(payload.get("round_scope_path")):
            cmd.extend(["--round-scope-path", item])
        round_deliverable = str(payload.get("round_deliverable") or "").strip()
        if round_deliverable:
            cmd.extend(["--round-deliverable", round_deliverable])
        round_validation_plan = str(payload.get("round_validation_plan") or "").strip()
        if round_validation_plan:
            cmd.extend(["--round-validation-plan", round_validation_plan])
        for item in _string_list(payload.get("round_risk")):
            cmd.extend(["--round-risk", item])
        for item in _string_list(payload.get("round_blocker")):
            cmd.extend(["--round-blocker", item])
        round_status_note = str(payload.get("round_status_note") or "").strip()
        if round_status_note:
            cmd.extend(["--round-status-note", round_status_note])
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


def maybe_execute_structured_payload(project_id: str, payload_text: str) -> tuple[bool, str]:
    payload = parse_executor_followup_payload(payload_text, source_label="from adjudication frontmatter `executor_followups`")
    command_name = str(payload.get("command") or "").strip()
    if command_name == "round-close-chain":
        round_id, commands = build_round_close_chain_commands(project_id, payload)
        if not commands:
            return True, f"round `{round_id}` already closed"
        executed_steps: list[str] = []
        for step_label, cmd in commands:
            success, detail = run_executor_command(cmd)
            if not success:
                return False, f"round `{round_id}` {step_label} failed: {detail}"
            executed_steps.append(step_label)
        return True, f"executed round-close-chain for `{round_id}` ({', '.join(executed_steps)})"

    success, detail = run_executor_command(build_executor_command(project_id, payload))
    if not success:
        return False, detail
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
    executed_payloads: set[str] = set()

    plan_contracts = [str(item).strip() for item in adjudication_meta.get("executor_plan_contracts", []) if str(item).strip()]
    compiled_plan_followups: list[str] = []
    if plan_contracts:
        compiled_plan_followups = compile_plan_contracts(
            args.project_id,
            plan_contracts,
            adjudication_meta=adjudication_meta,
            adjudication_sections=adjudication_sections,
        )

    for payload_text in compiled_plan_followups:
        normalized_payload = payload_text.strip()
        if not normalized_payload or normalized_payload in executed_payloads:
            continue
        executed_payloads.add(normalized_payload)
        success, detail = maybe_execute_structured_payload(args.project_id, payload_text)
        if success:
            applied.append(f"`executor plan` -> {detail}")
        else:
            blocked.append(f"`executor plan` -> {detail}")

    for payload_text in [str(item).strip() for item in adjudication_meta.get("executor_followups", []) if str(item).strip()]:
        normalized_payload = payload_text.strip()
        if not normalized_payload or normalized_payload in executed_payloads:
            noop.append("`executor payload` -> skipped duplicate compiled followup")
            continue
        executed_payloads.add(normalized_payload)
        success, detail = maybe_execute_structured_payload(args.project_id, payload_text)
        if success:
            applied.append(f"`executor payload` -> {detail}")
        else:
            blocked.append(f"`executor payload` -> {detail}")

    for followup in followups:
        normalized = " ".join(followup.strip().lower().split())
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
