#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class TransitionCommandSpec:
    name: str
    domain: str
    executor_supported: bool = False
    implementation_status: str = "implemented"
    required_inputs: tuple[str, ...] = ()
    guard_codes: tuple[str, ...] = ()
    write_targets: tuple[str, ...] = ()
    side_effect_codes: tuple[str, ...] = ()
    emits_transition_event: bool = True

    def has_semantic_contract(self) -> bool:
        return bool(self.required_inputs and self.guard_codes and self.write_targets and self.side_effect_codes)

    def to_dict(self) -> dict[str, object]:
        return {
            "name": self.name,
            "domain": self.domain,
            "executor_supported": self.executor_supported,
            "implementation_status": self.implementation_status,
            "required_inputs": list(self.required_inputs),
            "guard_codes": list(self.guard_codes),
            "write_targets": list(self.write_targets),
            "side_effect_codes": list(self.side_effect_codes),
            "emits_transition_event": self.emits_transition_event,
        }


@dataclass(frozen=True)
class AdjudicationPlanSpec:
    plan_type: str
    compiled_commands: tuple[str, ...]
    implementation_status: str = "implemented"
    requires_adjudication_fields: tuple[str, ...] = ()
    target_resolution: str = ""
    side_effect_codes: tuple[str, ...] = ()

    def has_semantic_contract(self) -> bool:
        return bool(self.compiled_commands and self.target_resolution and self.side_effect_codes)

    def to_dict(self) -> dict[str, object]:
        return {
            "plan_type": self.plan_type,
            "compiled_commands": list(self.compiled_commands),
            "implementation_status": self.implementation_status,
            "requires_adjudication_fields": list(self.requires_adjudication_fields),
            "target_resolution": self.target_resolution,
            "side_effect_codes": list(self.side_effect_codes),
        }


TRANSITION_COMMAND_SPECS: tuple[TransitionCommandSpec, ...] = (
    TransitionCommandSpec(
        "open-objective",
        "objective-line",
        implementation_status="implemented",
        required_inputs=("project_id", "title", "problem", "success_criteria", "non_goals", "phase"),
        guard_codes=("objective_fields_present", "active_objective_phase_valid", "no_other_active_objective"),
        write_targets=("durable:objective", "control:active-objective", "control:pivot-log", "memory:transition-event"),
        side_effect_codes=("activate_objective_line", "refresh_active_objective_projection", "refresh_pivot_log_projection"),
    ),
    TransitionCommandSpec(
        "close-objective",
        "objective-line",
        executor_supported=True,
        implementation_status="implemented",
        required_inputs=("project_id", "objective_id", "closing_status", "reason"),
        guard_codes=(
            "target_matches_active_objective",
            "closing_status_supported",
            "no_open_rounds_for_objective",
            "no_active_exception_contracts_for_objective",
        ),
        write_targets=("durable:objective", "control:active-objective", "control:pivot-log", "memory:transition-event"),
        side_effect_codes=("close_active_objective", "refresh_active_objective_projection", "refresh_pivot_log_projection"),
    ),
    TransitionCommandSpec(
        "record-soft-pivot",
        "objective-line",
        implementation_status="implemented",
        required_inputs=("project_id", "objective_id", "trigger", "change_summary", "identity_rationale"),
        guard_codes=(
            "target_matches_active_objective",
            "material_objective_change_present",
            "resulting_objective_fields_present",
            "execution_phase_round_alignment_preserved",
            "round_review_path_explicit_when_objective_shape_changes",
        ),
        write_targets=("durable:objective", "durable:pivot", "control:active-objective", "control:pivot-log", "memory:transition-event"),
        side_effect_codes=("rewrite_active_objective_in_place", "record_pivot_lineage", "force_explicit_round_review_path"),
    ),
    TransitionCommandSpec(
        "record-hard-pivot",
        "objective-line",
        implementation_status="implemented",
        required_inputs=("project_id", "previous_objective_id", "title", "problem", "success_criteria", "non_goals", "phase", "trigger"),
        guard_codes=(
            "previous_objective_is_active",
            "new_objective_fields_present",
            "previous_objective_matches_control_truth",
            "no_open_rounds_on_previous_objective",
        ),
        write_targets=("durable:objective", "durable:pivot", "control:active-objective", "control:pivot-log", "memory:transition-event"),
        side_effect_codes=("supersede_previous_objective", "activate_new_objective_line", "review_or_resolve_stale_exception_contracts"),
    ),
    TransitionCommandSpec(
        "set-phase",
        "phase",
        executor_supported=True,
        implementation_status="implemented",
        required_inputs=("project_id", "phase", "reason"),
        guard_codes=("phase_supported", "phase_transition_prerequisites_met", "execution_phase_has_or_bootstraps_round"),
        write_targets=("durable:objective", "control:active-objective", "control:active-round", "memory:transition-event"),
        side_effect_codes=("rewrite_objective_phase", "optionally_bootstrap_execution_round", "optionally_rewrite_open_rounds"),
    ),
    TransitionCommandSpec(
        "open-round",
        "round",
        implementation_status="implemented",
        required_inputs=("project_id", "objective_id", "title", "scope", "deliverable", "validation_plan"),
        guard_codes=(
            "linked_objective_is_active",
            "linked_objective_is_execution",
            "scope_present",
            "validation_plan_present",
            "no_conflicting_open_round",
        ),
        write_targets=("durable:round", "control:active-round", "memory:transition-event"),
        side_effect_codes=("open_bounded_execution_round", "refresh_active_round_projection"),
    ),
    TransitionCommandSpec(
        "refresh-round-scope",
        "round",
        executor_supported=True,
        implementation_status="implemented",
        required_inputs=("project_id", "reason"),
        guard_codes=(
            "target_round_is_open",
            "refresh_reason_present",
            "resulting_scope_paths_non_empty",
            "scope_change_backed_by_evidence",
            "scope_change_produces_material_change",
        ),
        write_targets=("durable:round", "control:active-round", "memory:transition-event"),
        side_effect_codes=("rewrite_round_scope_paths", "preserve_round_identity", "refresh_active_round_projection"),
    ),
    TransitionCommandSpec(
        "update-round-status",
        "round",
        executor_supported=True,
        implementation_status="implemented",
        required_inputs=("project_id", "round_id", "status", "reason"),
        guard_codes=(
            "round_exists",
            "status_transition_legal",
            "promotion_passes_enforcement_when_required",
            "captured_has_validation_record",
        ),
        write_targets=("durable:round", "control:active-round", "memory:transition-event"),
        side_effect_codes=("advance_round_lifecycle_state", "record_blocker_or_validation_history", "refresh_active_round_projection"),
    ),
    TransitionCommandSpec(
        "rewrite-open-round",
        "round",
        executor_supported=True,
        implementation_status="implemented",
        required_inputs=("project_id", "round_id", "reason", "mutable_fields"),
        guard_codes=(
            "round_remains_open",
            "rewrite_reason_present",
            "rewritten_round_contract_stays_complete",
            "round_identity_preserved",
            "rewrite_produces_material_change",
        ),
        write_targets=("durable:round", "control:active-round", "memory:transition-event"),
        side_effect_codes=("rewrite_open_round_contract", "refresh_active_round_projection"),
    ),
    TransitionCommandSpec(
        "activate-exception-contract",
        "exception-contract",
        implementation_status="implemented",
        required_inputs=("project_id", "title", "reason", "risk", "owner_scope", "exit_condition"),
        guard_codes=("exception_contract_required_fields_present",),
        write_targets=("durable:exception-contract", "control:exception-ledger", "memory:transition-event"),
        side_effect_codes=("record_active_exception_contract", "refresh_exception_ledger_projection"),
    ),
    TransitionCommandSpec(
        "retire-exception-contract",
        "exception-contract",
        executor_supported=True,
        implementation_status="implemented",
        required_inputs=("project_id", "exception_contract_id", "reason"),
        guard_codes=("exception_contract_exists", "exception_contract_is_active"),
        write_targets=("durable:exception-contract", "control:exception-ledger", "memory:transition-event"),
        side_effect_codes=("retire_exception_contract", "refresh_exception_ledger_projection"),
    ),
    TransitionCommandSpec(
        "invalidate-exception-contract",
        "exception-contract",
        executor_supported=True,
        implementation_status="implemented",
        required_inputs=("project_id", "exception_contract_id", "reason"),
        guard_codes=("exception_contract_exists", "exception_contract_is_active"),
        write_targets=("durable:exception-contract", "control:exception-ledger", "memory:transition-event"),
        side_effect_codes=("invalidate_exception_contract", "refresh_exception_ledger_projection"),
    ),
    TransitionCommandSpec(
        "refresh-anchor",
        "anchor-maintenance",
        implementation_status="partial",
        required_inputs=("project_id",),
        guard_codes=("current_task_anchor_exists", "live_workspace_available"),
        write_targets=("current:current-task",),
        side_effect_codes=("refresh_live_workspace_anchor",),
        emits_transition_event=False,
    ),
    TransitionCommandSpec(
        "capture-snapshot",
        "anchor-maintenance",
        implementation_status="partial",
        required_inputs=("project_id", "slug"),
        guard_codes=("project_control_state_available", "workspace_anchor_available"),
        write_targets=("snapshot:historical",),
        side_effect_codes=("capture_phase_or_handoff_snapshot",),
        emits_transition_event=False,
    ),
)


ADJUDICATION_PLAN_SPECS: tuple[AdjudicationPlanSpec, ...] = (
    AdjudicationPlanSpec(
        plan_type="rewrite-open-round-then-close-chain",
        compiled_commands=("rewrite-open-round", "round-close-chain"),
        requires_adjudication_fields=("round_id", "rewrite_reason", "validation_pending_reason", "captured_reason", "closed_reason"),
        target_resolution="explicit_round_id",
        side_effect_codes=("rewrite_round_contract", "advance_round_to_closed"),
    ),
    AdjudicationPlanSpec(
        plan_type="retire-invalidated-exception-contracts",
        compiled_commands=("retire-exception-contract",),
        requires_adjudication_fields=("Objects Invalidated", "reason"),
        target_resolution="resolve_active_exception_contracts_from_invalidated_objects",
        side_effect_codes=("retire_active_exception_contracts",),
    ),
    AdjudicationPlanSpec(
        plan_type="invalidate-invalidated-exception-contracts",
        compiled_commands=("invalidate-exception-contract",),
        requires_adjudication_fields=("Objects Invalidated", "reason"),
        target_resolution="resolve_active_exception_contracts_from_invalidated_objects",
        side_effect_codes=("invalidate_active_exception_contracts",),
    ),
    AdjudicationPlanSpec(
        plan_type="enter-execution-with-round-bootstrap",
        compiled_commands=("set-phase",),
        requires_adjudication_fields=("reason", "round_title", "round_scope_items", "round_deliverable", "round_validation_plan"),
        target_resolution="explicit_or_adjudication_objective",
        side_effect_codes=("enter_execution_phase", "bootstrap_bounded_round"),
    ),
)


COMMAND_SPEC_BY_NAME = {spec.name: spec for spec in TRANSITION_COMMAND_SPECS}
PLAN_SPEC_BY_TYPE = {spec.plan_type: spec for spec in ADJUDICATION_PLAN_SPECS}


def validate_transition_specs() -> None:
    valid_implementation_statuses = {"implemented", "partial", "planned"}
    if len(COMMAND_SPEC_BY_NAME) != len(TRANSITION_COMMAND_SPECS):
        raise SystemExit("duplicate transition command names found in transition registry")
    if len(PLAN_SPEC_BY_TYPE) != len(ADJUDICATION_PLAN_SPECS):
        raise SystemExit("duplicate adjudication plan types found in transition registry")

    for spec in TRANSITION_COMMAND_SPECS:
        if spec.implementation_status not in valid_implementation_statuses:
            raise SystemExit(f"transition command `{spec.name}` uses unsupported implementation status `{spec.implementation_status}`")
        if spec.implementation_status in {"implemented", "partial"} and not spec.has_semantic_contract():
            raise SystemExit(f"transition command `{spec.name}` is {spec.implementation_status} but lacks semantic registry coverage")
        if spec.emits_transition_event and "memory:transition-event" not in spec.write_targets and spec.implementation_status == "implemented":
            raise SystemExit(f"transition command `{spec.name}` emits transition events but does not declare `memory:transition-event`")
        if not spec.emits_transition_event and "memory:transition-event" in spec.write_targets:
            raise SystemExit(f"transition command `{spec.name}` declares `memory:transition-event` despite `emits_transition_event=False`")

    known_commands = set(COMMAND_SPEC_BY_NAME)
    allowed_bundle_commands = {"round-close-chain"}
    for plan_spec in ADJUDICATION_PLAN_SPECS:
        if plan_spec.implementation_status not in valid_implementation_statuses:
            raise SystemExit(
                f"adjudication plan `{plan_spec.plan_type}` uses unsupported implementation status `{plan_spec.implementation_status}`"
            )
        if plan_spec.implementation_status in {"implemented", "partial"} and not plan_spec.has_semantic_contract():
            raise SystemExit(
                f"adjudication plan `{plan_spec.plan_type}` is {plan_spec.implementation_status} but lacks semantic registry coverage"
            )
        for command_name in plan_spec.compiled_commands:
            if command_name not in known_commands and command_name not in allowed_bundle_commands:
                raise SystemExit(
                    f"adjudication plan `{plan_spec.plan_type}` references unknown compiled command `{command_name}`"
                )


def transition_command_names() -> list[str]:
    validate_transition_specs()
    return [spec.name for spec in TRANSITION_COMMAND_SPECS]


def transition_command_spec(command_name: str) -> TransitionCommandSpec:
    validate_transition_specs()
    spec = COMMAND_SPEC_BY_NAME.get(command_name.strip())
    if spec is None:
        raise SystemExit(f"unknown transition command `{command_name}`")
    return spec


def semantic_transition_command_names() -> list[str]:
    validate_transition_specs()
    return [spec.name for spec in TRANSITION_COMMAND_SPECS if spec.has_semantic_contract()]


def executor_supported_command_names() -> list[str]:
    validate_transition_specs()
    return [spec.name for spec in TRANSITION_COMMAND_SPECS if spec.executor_supported]


def adjudication_plan_types() -> list[str]:
    validate_transition_specs()
    return [spec.plan_type for spec in ADJUDICATION_PLAN_SPECS]


def adjudication_plan_spec(plan_type: str) -> AdjudicationPlanSpec:
    validate_transition_specs()
    spec = PLAN_SPEC_BY_TYPE.get(plan_type.strip())
    if spec is None:
        raise SystemExit(f"unknown adjudication plan type `{plan_type}`")
    return spec


def semantic_adjudication_plan_types() -> list[str]:
    validate_transition_specs()
    return [spec.plan_type for spec in ADJUDICATION_PLAN_SPECS if spec.has_semantic_contract()]


def export_transition_registry() -> dict[str, object]:
    validate_transition_specs()
    return {
        "transition_commands": [spec.to_dict() for spec in TRANSITION_COMMAND_SPECS],
        "adjudication_plan_families": [spec.to_dict() for spec in ADJUDICATION_PLAN_SPECS],
    }
