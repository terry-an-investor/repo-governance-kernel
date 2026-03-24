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
from transition_specs import (
    command_allowed_executor_payload_keys,
    executor_field_specs_for_command,
    executor_supported_command_names,
    mutable_field_specs_for_command,
)


ROOT = Path(__file__).resolve().parent.parent
SCRIPTS = ROOT / "scripts"
SUPPORTED_EXECUTOR_COMMANDS = set(executor_supported_command_names()) | {"round-close-chain"}


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


def _reject_unknown_payload_keys(command_name: str, payload: dict[str, object], allowed_keys: set[str]) -> None:
    unknown_keys = sorted(set(payload) - {"command"} - allowed_keys)
    if unknown_keys:
        raise SystemExit(
            f"executor {command_name} payload carries undeclared private keys: {', '.join(unknown_keys)}"
        )


def _append_executor_field_specs(cmd: list[str], payload: dict[str, object], command_name: str) -> None:
    _reject_unknown_payload_keys(
        command_name,
        payload,
        command_allowed_executor_payload_keys(command_name),
    )
    for field_spec in executor_field_specs_for_command(command_name):
        cli_flag = f"--{field_spec.cli_flag}"
        if field_spec.value_kind == "scalar":
            value = str(payload.get(field_spec.payload_key) or "").strip()
            if field_spec.required and not value:
                raise SystemExit(f"executor {command_name} requires `{field_spec.payload_key}`")
            if value:
                cmd.extend([cli_flag, value])
            continue
        if field_spec.value_kind == "list":
            values = _string_list(payload.get(field_spec.payload_key))
            if field_spec.required and not values:
                raise SystemExit(f"executor {command_name} requires `{field_spec.payload_key}`")
            for item in values:
                cmd.extend([cli_flag, item])
            continue
        if field_spec.value_kind == "bool":
            if field_spec.required and not bool(payload.get(field_spec.payload_key)):
                raise SystemExit(f"executor {command_name} requires `{field_spec.payload_key}`")
            if bool(payload.get(field_spec.payload_key)):
                cmd.append(cli_flag)
            continue
        raise SystemExit(
            f"executor {command_name} encountered unsupported executor value kind `{field_spec.value_kind}`"
        )


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
        _append_executor_field_specs(cmd, payload, command_name)
        return cmd

    if command_name == "update-round-status":
        _append_executor_field_specs(cmd, payload, command_name)
        return cmd

    if command_name == "refresh-round-scope":
        _append_executor_field_specs(cmd, payload, command_name)
        return cmd

    if command_name == "rewrite-open-round":
        _append_executor_field_specs(cmd, payload, command_name)
        for field_spec in mutable_field_specs_for_command("rewrite-open-round"):
            cli_flag = f"--{field_spec.cli_flag}"
            if field_spec.value_kind == "scalar":
                value = str(payload.get(field_spec.payload_key) or "").strip()
                if value:
                    cmd.extend([cli_flag, value])
            else:
                for item in _string_list(payload.get(field_spec.payload_key)):
                    cmd.extend([cli_flag, item])
            if field_spec.replace_flag and bool(payload.get(field_spec.replace_flag)):
                cmd.append(f"--{field_spec.replace_flag.replace('_', '-')}")
        return cmd

    if command_name == "set-phase":
        _append_executor_field_specs(cmd, payload, command_name)
        return cmd

    if command_name == "retire-exception-contract":
        _append_executor_field_specs(cmd, payload, command_name)
        return cmd

    if command_name == "invalidate-exception-contract":
        _append_executor_field_specs(cmd, payload, command_name)
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
