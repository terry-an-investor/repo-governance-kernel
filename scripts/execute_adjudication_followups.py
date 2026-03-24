#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path

from compile_adjudication_executor_plan import compile_plan_contracts
from executor_command_builder import string_list
from executor_runtime import run_registry_command
from resolver_runtime import resolve_round_status_from_round_id
from round_control import (
    load_all_adjudications,
    parse_bullet_list,
    project_dir,
    select_open_round_record,
)
from transition_specs import (
    bundle_governance_names,
    bundle_allowed_payload_keys,
    bundle_field_specs,
    bundle_governance_spec,
    bundle_route_state_spec,
    bundle_step_template_spec,
    executor_supported_command_names,
)


ROOT = Path(__file__).resolve().parent.parent


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
    supported_commands = supported_executor_commands()
    if command_name not in supported_commands:
        raise SystemExit(
            f"executor follow-up command `{command_name}` is not supported; "
            f"supported commands: {', '.join(sorted(supported_commands))}"
        )
    return payload


def _string_list(value: object) -> list[str]:
    return string_list(value)


def require_payload_text(payload: dict[str, object], field_name: str) -> str:
    value = str(payload.get(field_name) or "").strip()
    if not value:
        raise SystemExit(f"executor {payload.get('command')} requires `{field_name}`")
    return value


def _field_value_present(value_kind: str, value: object) -> bool:
    if value_kind == "scalar":
        return bool(str(value or "").strip())
    if value_kind == "list":
        return bool(_string_list(value))
    if value_kind == "bool":
        return bool(value)
    raise SystemExit(f"unsupported executor value kind `{value_kind}`")


def _validate_bundle_payload(payload: dict[str, object], bundle_name: str) -> None:
    unknown_keys = sorted(set(payload) - {"command"} - bundle_allowed_payload_keys(bundle_name))
    if unknown_keys:
        raise SystemExit(
            f"executor {bundle_name} payload carries undeclared private keys: {', '.join(unknown_keys)}"
        )
    for field_spec in bundle_field_specs(bundle_name):
        if field_spec.required and not _field_value_present(field_spec.value_kind, payload.get(field_spec.payload_key)):
            raise SystemExit(f"executor {bundle_name} requires `{field_spec.payload_key}`")


def bundle_executor_handler_names() -> list[str]:
    return sorted(bundle_governance_names())


def validate_bundle_governance_executor_contracts() -> None:
    governed_bundle_names = set(bundle_governance_names())
    executor_bundle_names = set(bundle_executor_handler_names())
    missing_executor_handlers = sorted(governed_bundle_names - executor_bundle_names)
    undocumented_executor_handlers = sorted(executor_bundle_names - governed_bundle_names)
    if missing_executor_handlers or undocumented_executor_handlers:
        details: list[str] = []
        if missing_executor_handlers:
            details.append(
                "missing executor handlers for governed bundle wrappers: "
                + ", ".join(f"`{name}`" for name in missing_executor_handlers)
            )
        if undocumented_executor_handlers:
            details.append(
                "executor exposes ungoverned bundle handlers: "
                + ", ".join(f"`{name}`" for name in undocumented_executor_handlers)
            )
        raise SystemExit("; ".join(details))


def supported_executor_commands() -> set[str]:
    validate_bundle_governance_executor_contracts()
    return set(executor_supported_command_names()) | set(bundle_executor_handler_names())


GOVERNED_BUNDLE_STATE_RESOLVERS = {
    "round_status_from_round_id": resolve_round_status_from_round_id,
}


def _resolve_bundle_current_state(project_id: str, bundle_name: str, payload: dict[str, object]) -> str:
    resolver_name = bundle_governance_spec(bundle_name).state_resolver
    resolver = GOVERNED_BUNDLE_STATE_RESOLVERS.get(resolver_name)
    if resolver is None:
        raise SystemExit(f"unsupported bundle state resolver `{resolver_name}`")
    return str(resolver(project_id, payload)).strip()


def _materialize_bundle_step_payload(
    bundle_name: str,
    bundle_payload: dict[str, object],
    *,
    from_state: str,
) -> tuple[str, str, str, dict[str, object]]:
    step_template = bundle_step_template_spec(bundle_name, from_state)
    command_name = step_template.command_name
    payload: dict[str, object] = {}
    for key, value in step_template.static_scalar_fields:
        payload[key] = value
    for key, value in step_template.static_bool_fields:
        payload[key] = value
    for binding in step_template.bindings:
        raw_value = bundle_payload.get(binding.source_key)
        if binding.value_kind == "scalar":
            value = str(raw_value or "").strip()
            if value:
                payload[binding.target_key] = value
            continue
        if binding.value_kind == "list":
            values = _string_list(raw_value)
            if values:
                payload[binding.target_key] = values
            continue
        if binding.value_kind == "bool":
            if bool(raw_value):
                payload[binding.target_key] = True
            continue
        raise SystemExit(
            f"bundle `{bundle_name}` step template `{step_template.label}` uses unsupported value kind `{binding.value_kind}`"
        )
    return step_template.label, command_name, step_template.to_state, payload


def execute_governed_bundle(project_id: str, payload: dict[str, object], bundle_name: str) -> tuple[bool, str]:
    _validate_bundle_payload(payload, bundle_name)
    current_state = _resolve_bundle_current_state(project_id, bundle_name, payload)
    route_state_spec = bundle_route_state_spec(bundle_name, current_state)
    round_id = str(payload.get("round_id") or "").strip()
    if route_state_spec.terminal:
        target_label = f"round `{round_id}`" if round_id else f"bundle `{bundle_name}` target"
        return True, f"{target_label} already {current_state}"

    missing_required_payloads = [
        key
        for key in route_state_spec.required_payload_keys
        if not _field_value_present(
            next(field.value_kind for field in bundle_field_specs(bundle_name) if field.payload_key == key),
            payload.get(key),
        )
    ]
    if missing_required_payloads:
        raise SystemExit(
            f"executor {bundle_name} requires {', '.join(f'`{key}`' for key in missing_required_payloads)} when target is `{current_state}`"
        )

    executed_steps: list[str] = []
    while True:
        route_state_spec = bundle_route_state_spec(bundle_name, current_state)
        if route_state_spec.terminal:
            break
        step_label, command_name, next_state, step_payload = _materialize_bundle_step_payload(
            bundle_name,
            payload,
            from_state=current_state,
        )
        success, detail = run_registry_command(
            project_id,
            step_payload,
            command_name,
            failure_message="executor follow-up failed",
        )
        if not success:
            target_label = f"round `{round_id}`" if round_id else f"bundle `{bundle_name}` target"
            return False, f"{target_label} {step_label} failed: {detail}"
        executed_steps.append(step_label)
        current_state = next_state

    target_label = f"round `{round_id}`" if round_id else f"bundle `{bundle_name}` target"
    return True, f"executed {bundle_name} for {target_label} ({', '.join(executed_steps)})"


def maybe_execute_structured_payload(project_id: str, payload_text: str) -> tuple[bool, str]:
    payload = parse_executor_followup_payload(payload_text, source_label="from adjudication frontmatter `executor_followups`")
    command_name = str(payload.get("command") or "").strip()
    if command_name in bundle_governance_names():
        return execute_governed_bundle(project_id, payload, command_name)

    if command_name not in executor_supported_command_names():
        raise SystemExit(f"unsupported executor command `{command_name}`")
    success, detail = run_registry_command(
        project_id,
        payload,
        command_name,
        failure_message="executor follow-up failed",
    )
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

    success, detail = run_registry_command(
        args.project_id,
        {
            "command": "open-round",
            "title": str(bootstrap["title"]).strip(),
            "scope_item": [str(item).strip() for item in bootstrap["scope_items"] if str(item).strip()],
            "scope_path": [str(item).strip() for item in bootstrap["scope_paths"] if str(item).strip()],
            "deliverable": str(bootstrap["deliverable"]).strip(),
            "validation_plan": str(bootstrap["validation_plan"]).strip(),
            "risk": [str(item).strip() for item in bootstrap["risks"] if str(item).strip()],
            "blocker": [str(item).strip() for item in bootstrap["blockers"] if str(item).strip()],
            "status_note": str(bootstrap["status_note"]).strip(),
        },
        "open-round",
        failure_message="open-round failed",
    )
    if not success:
        return False, detail
    return True, detail


def main() -> int:
    from audit_control_state import audit_project_control_state

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
