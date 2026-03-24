#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class GuardSpec:
    code: str
    template: str
    context_keys: tuple[str, ...] = ()
    fallback_template: str = ""

    def render(self, context: dict[str, str] | None = None) -> str:
        render_context = {
            key: str(value).strip()
            for key, value in (context or {}).items()
            if str(value).strip()
        }
        if self.context_keys and not all(render_context.get(key) for key in self.context_keys):
            if self.fallback_template:
                return self.fallback_template
            missing = ", ".join(f"`{key}`" for key in self.context_keys)
            raise SystemExit(f"guard `{self.code}` requires render context keys: {missing}")
        return self.template.format(**render_context)

    def to_dict(self) -> dict[str, object]:
        return {
            "code": self.code,
            "template": self.template,
            "context_keys": list(self.context_keys),
            "fallback_template": self.fallback_template,
        }


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
    durable_owners: tuple[str, ...] = ()
    projection_owners: tuple[str, ...] = ()
    artifact_owners: tuple[str, ...] = ()
    live_inspection_owners: tuple[str, ...] = ()
    emits_transition_event: bool = True

    def has_owner_layer_contract(self) -> bool:
        return bool(self.durable_owners or self.projection_owners or self.artifact_owners or self.live_inspection_owners)

    def has_semantic_contract(self) -> bool:
        return bool(
            self.required_inputs
            and self.guard_codes
            and self.write_targets
            and self.side_effect_codes
            and self.has_owner_layer_contract()
        )

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
            "durable_owners": list(self.durable_owners),
            "projection_owners": list(self.projection_owners),
            "artifact_owners": list(self.artifact_owners),
            "live_inspection_owners": list(self.live_inspection_owners),
            "emits_transition_event": self.emits_transition_event,
        }


SUPPORTED_DURABLE_OWNER_LABELS = {
    "memory:objective",
    "memory:pivot",
    "memory:round",
    "memory:exception-contract",
    "current:current-task",
}

SUPPORTED_PROJECTION_OWNER_LABELS = {
    "control:active-objective",
    "control:pivot-log",
    "control:active-round",
    "control:exception-ledger",
}

SUPPORTED_ARTIFACT_OWNER_LABELS = {
    "artifact:live-workspace-projection",
    "snapshot:historical",
}

SUPPORTED_LIVE_INSPECTION_OWNER_LABELS = {
    "workspace:git-status",
}


GUARD_SPECS: tuple[GuardSpec, ...] = (
    GuardSpec("linked_objective_is_active", "objective `{objective_id}` exists and is active", ("objective_id",), "linked objective exists and is active"),
    GuardSpec("linked_objective_is_execution", "objective phase is `execution`"),
    GuardSpec("scope_present", "scope items are present"),
    GuardSpec("validation_plan_present", "validation plan is present"),
    GuardSpec("no_conflicting_open_round", "no conflicting active round remains open"),
    GuardSpec("target_round_is_open", "round `{round_id}` exists and remains open", ("round_id",), "target round exists and remains open"),
    GuardSpec("refresh_reason_present", "scope refresh reason is explicit"),
    GuardSpec("resulting_scope_paths_non_empty", "resulting scope path set remains non-empty"),
    GuardSpec("scope_change_backed_by_evidence", "scope refresh is backed by live dirty paths or explicit path edits"),
    GuardSpec("scope_change_produces_material_change", "scope refresh produces a material scope-path change"),
    GuardSpec("round_exists", "round `{round_id}` exists", ("round_id",), "round exists"),
    GuardSpec(
        "status_transition_legal",
        "transition `{previous_status} -> {next_status}` is legal",
        ("previous_status", "next_status"),
        "status transition is legal",
    ),
    GuardSpec("promotion_passes_enforcement_when_required", "captured or closed promotion passes worktree enforcement when required"),
    GuardSpec("captured_has_validation_record", "captured status includes at least one validation record when capture is requested"),
    GuardSpec("round_remains_open", "round `{round_id}` exists and remains open", ("round_id",), "round exists and remains open"),
    GuardSpec("rewrite_reason_present", "rewrite reason is explicit"),
    GuardSpec("rewritten_round_contract_stays_complete", "rewritten round still has scope, deliverable, validation plan, and scope paths"),
    GuardSpec("round_identity_preserved", "round identity is preserved while contract content is rewritten"),
    GuardSpec("rewrite_produces_material_change", "rewrite produces at least one material round-contract change"),
    GuardSpec("objective_fields_present", "problem, success criteria, non-goals, and phase are present"),
    GuardSpec("active_objective_phase_valid", "initial objective phase is supported"),
    GuardSpec("no_other_active_objective", "no control or durable active objective already exists"),
    GuardSpec(
        "target_matches_active_objective",
        "objective `{objective_id}` matches both control and durable active truth",
        ("objective_id",),
        "target objective matches both control and durable active truth",
    ),
    GuardSpec(
        "closing_status_supported",
        "closing status `{closing_status}` is supported",
        ("closing_status",),
        "closing status is supported",
    ),
    GuardSpec("no_open_rounds_for_objective", "no durable open round remains attached to the objective"),
    GuardSpec("no_active_exception_contracts_for_objective", "no active exception contract remains attached to the objective"),
    GuardSpec("material_objective_change_present", "soft pivot produces at least one material objective change"),
    GuardSpec("resulting_objective_fields_present", "resulting objective problem, success criteria, non-goals, and phase remain present"),
    GuardSpec("execution_phase_round_alignment_preserved", "execution-phase objective state keeps one aligned durable open round when required"),
    GuardSpec("round_review_path_explicit_when_objective_shape_changes", "open-round review path is explicit when the objective shape changes"),
    GuardSpec(
        "previous_objective_is_active",
        "objective `{previous_objective_id}` exists and is active",
        ("previous_objective_id",),
        "previous objective exists and is active",
    ),
    GuardSpec("new_objective_fields_present", "new objective problem, success criteria, non-goals, and phase are present"),
    GuardSpec("previous_objective_matches_control_truth", "previous objective matches both control and durable active truth"),
    GuardSpec("no_open_rounds_on_previous_objective", "no durable still-open round remains tied to the previous objective"),
    GuardSpec("phase_supported", "phase `{next_phase}` is supported", ("next_phase",), "target phase is supported"),
    GuardSpec(
        "phase_transition_prerequisites_met",
        "phase transition `{previous_phase} -> {next_phase}` satisfies its prerequisites",
        ("previous_phase", "next_phase"),
        "phase transition prerequisites are met",
    ),
    GuardSpec("execution_phase_has_or_bootstraps_round", "execution phase has one bounded round or bootstraps one in the same guarded transition"),
    GuardSpec(
        "active_objective_available",
        "objective `{objective_id}` exists and is active",
        ("objective_id",),
        "one active objective exists",
    ),
    GuardSpec("exception_contract_required_fields_present", "summary, reason, temporary behavior, risk, exit condition, and owner scope are present"),
    GuardSpec(
        "exception_contract_exists",
        "exception contract `{exception_contract_id}` exists",
        ("exception_contract_id",),
        "exception contract exists",
    ),
    GuardSpec(
        "exception_contract_is_active",
        "exception contract `{exception_contract_id}` is `active`",
        ("exception_contract_id",),
        "exception contract is `active`",
    ),
    GuardSpec(
        "pivot_exists_when_supplied",
        "pivot `{pivot_id}` exists",
        ("pivot_id",),
        "no pivot id was supplied, so no pivot lookup was required",
    ),
    GuardSpec("current_task_anchor_exists", "current-task anchor exists and is readable"),
    GuardSpec("live_workspace_available", "live workspace inspection is available"),
    GuardSpec("workspace_locator_available", "workspace locator is present in current-task anchor"),
    GuardSpec("project_control_state_available", "project control state required for snapshot capture is available"),
    GuardSpec("workspace_anchor_available", "workspace anchor is available from current-task or latest snapshot context"),
)


@dataclass(frozen=True)
class AdjudicationPayloadBindingSpec:
    target_key: str
    resolver: str
    source_keys: tuple[str, ...] = ()
    required: bool = False
    fanout: bool = False

    def to_dict(self) -> dict[str, object]:
        return {
            "target_key": self.target_key,
            "resolver": self.resolver,
            "source_keys": list(self.source_keys),
            "required": self.required,
            "fanout": self.fanout,
        }


@dataclass(frozen=True)
class AdjudicationPayloadTemplateSpec:
    command_name: str
    static_scalar_fields: tuple[tuple[str, str], ...] = ()
    static_bool_fields: tuple[tuple[str, bool], ...] = ()
    bindings: tuple[AdjudicationPayloadBindingSpec, ...] = ()

    def to_dict(self) -> dict[str, object]:
        return {
            "command_name": self.command_name,
            "static_scalar_fields": [{"key": key, "value": value} for key, value in self.static_scalar_fields],
            "static_bool_fields": [{"key": key, "value": value} for key, value in self.static_bool_fields],
            "bindings": [binding.to_dict() for binding in self.bindings],
        }


@dataclass(frozen=True)
class AdjudicationPlanSpec:
    plan_type: str
    compiled_commands: tuple[str, ...]
    implementation_status: str = "implemented"
    requires_adjudication_fields: tuple[str, ...] = ()
    target_resolution: str = ""
    side_effect_codes: tuple[str, ...] = ()
    payload_templates: tuple[AdjudicationPayloadTemplateSpec, ...] = ()

    def has_semantic_contract(self) -> bool:
        return bool(self.compiled_commands and self.target_resolution and self.side_effect_codes and self.payload_templates)

    def to_dict(self) -> dict[str, object]:
        return {
            "plan_type": self.plan_type,
            "compiled_commands": list(self.compiled_commands),
            "implementation_status": self.implementation_status,
            "requires_adjudication_fields": list(self.requires_adjudication_fields),
            "target_resolution": self.target_resolution,
            "side_effect_codes": list(self.side_effect_codes),
            "payload_templates": [template.to_dict() for template in self.payload_templates],
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
        durable_owners=("memory:objective",),
        projection_owners=("control:active-objective", "control:pivot-log"),
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
        durable_owners=("memory:objective",),
        projection_owners=("control:active-objective", "control:pivot-log"),
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
        durable_owners=("memory:objective", "memory:pivot"),
        projection_owners=("control:active-objective", "control:pivot-log"),
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
        durable_owners=("memory:objective", "memory:pivot"),
        projection_owners=("control:active-objective", "control:pivot-log"),
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
        durable_owners=("memory:objective",),
        projection_owners=("control:active-objective", "control:active-round"),
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
        durable_owners=("memory:round",),
        projection_owners=("control:active-round",),
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
        durable_owners=("memory:round",),
        projection_owners=("control:active-round",),
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
        durable_owners=("memory:round",),
        projection_owners=("control:active-round",),
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
        durable_owners=("memory:round",),
        projection_owners=("control:active-round",),
    ),
    TransitionCommandSpec(
        "activate-exception-contract",
        "exception-contract",
        implementation_status="implemented",
        required_inputs=("project_id", "title", "summary", "reason", "temporary_behavior", "risk", "owner_scope", "exit_condition"),
        guard_codes=("active_objective_available", "exception_contract_required_fields_present"),
        write_targets=("durable:exception-contract", "control:exception-ledger", "memory:transition-event"),
        side_effect_codes=("record_active_exception_contract", "refresh_exception_ledger_projection"),
        durable_owners=("memory:exception-contract",),
        projection_owners=("control:exception-ledger",),
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
        durable_owners=("memory:exception-contract",),
        projection_owners=("control:exception-ledger",),
    ),
    TransitionCommandSpec(
        "invalidate-exception-contract",
        "exception-contract",
        executor_supported=True,
        implementation_status="implemented",
        required_inputs=("project_id", "exception_contract_id", "reason"),
        guard_codes=("exception_contract_exists", "exception_contract_is_active", "pivot_exists_when_supplied"),
        write_targets=("durable:exception-contract", "control:exception-ledger", "memory:transition-event"),
        side_effect_codes=("invalidate_exception_contract", "refresh_exception_ledger_projection"),
        durable_owners=("memory:exception-contract",),
        projection_owners=("control:exception-ledger",),
    ),
    TransitionCommandSpec(
        "refresh-anchor",
        "anchor-maintenance",
        implementation_status="partial",
        required_inputs=("project_id",),
        guard_codes=("current_task_anchor_exists", "live_workspace_available"),
        write_targets=("current:current-task",),
        side_effect_codes=("refresh_current_task_control_locator",),
        durable_owners=("current:current-task",),
        live_inspection_owners=("workspace:git-status",),
        emits_transition_event=False,
    ),
    TransitionCommandSpec(
        "render-live-workspace",
        "anchor-maintenance",
        implementation_status="implemented",
        required_inputs=("project_id",),
        guard_codes=("workspace_locator_available", "live_workspace_available"),
        write_targets=("artifact:live-workspace-projection",),
        side_effect_codes=("render_live_workspace_projection",),
        artifact_owners=("artifact:live-workspace-projection",),
        live_inspection_owners=("workspace:git-status",),
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
        artifact_owners=("snapshot:historical",),
        live_inspection_owners=("workspace:git-status",),
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
        payload_templates=(
            AdjudicationPayloadTemplateSpec(
                command_name="rewrite-open-round",
                bindings=(
                    AdjudicationPayloadBindingSpec("round_id", "contract_scalar", ("round_id",), required=True),
                    AdjudicationPayloadBindingSpec("reason", "contract_scalar", ("rewrite_reason",), required=True),
                    AdjudicationPayloadBindingSpec("title", "contract_scalar", ("title",)),
                    AdjudicationPayloadBindingSpec("summary", "contract_scalar", ("summary",)),
                    AdjudicationPayloadBindingSpec("deliverable", "contract_scalar", ("deliverable",)),
                    AdjudicationPayloadBindingSpec("validation_plan", "contract_scalar", ("validation_plan",)),
                    AdjudicationPayloadBindingSpec("scope_item", "contract_list", ("scope_item",)),
                    AdjudicationPayloadBindingSpec("scope_path", "contract_list", ("scope_path",)),
                    AdjudicationPayloadBindingSpec("risk", "contract_list", ("risk",)),
                    AdjudicationPayloadBindingSpec("blocker", "contract_list", ("blocker",)),
                    AdjudicationPayloadBindingSpec("status_note", "contract_list", ("status_note",)),
                    AdjudicationPayloadBindingSpec("replace_scope_items", "contract_bool", ("replace_scope_items",)),
                    AdjudicationPayloadBindingSpec("replace_scope_paths", "contract_bool", ("replace_scope_paths",)),
                    AdjudicationPayloadBindingSpec("replace_risks", "contract_bool", ("replace_risks",)),
                    AdjudicationPayloadBindingSpec("replace_blockers", "contract_bool", ("replace_blockers",)),
                ),
            ),
            AdjudicationPayloadTemplateSpec(
                command_name="round-close-chain",
                bindings=(
                    AdjudicationPayloadBindingSpec("round_id", "contract_scalar", ("round_id",), required=True),
                    AdjudicationPayloadBindingSpec(
                        "validation_pending_reason",
                        "contract_scalar",
                        ("validation_pending_reason",),
                        required=True,
                    ),
                    AdjudicationPayloadBindingSpec("captured_reason", "contract_scalar", ("captured_reason",), required=True),
                    AdjudicationPayloadBindingSpec("closed_reason", "contract_scalar", ("closed_reason",), required=True),
                    AdjudicationPayloadBindingSpec("validated_by", "round_validated_by_list", ("validated_by",)),
                    AdjudicationPayloadBindingSpec("clear_blockers", "contract_bool", ("clear_blockers",)),
                    AdjudicationPayloadBindingSpec("blocker", "contract_list", ("close_chain_blocker",)),
                    AdjudicationPayloadBindingSpec("risk", "contract_list", ("close_chain_risk",)),
                ),
            ),
        ),
    ),
    AdjudicationPlanSpec(
        plan_type="retire-invalidated-exception-contracts",
        compiled_commands=("retire-exception-contract",),
        requires_adjudication_fields=("Objects Invalidated", "reason"),
        target_resolution="resolve_active_exception_contracts_from_invalidated_objects",
        side_effect_codes=("retire_active_exception_contracts",),
        payload_templates=(
            AdjudicationPayloadTemplateSpec(
                command_name="retire-exception-contract",
                bindings=(
                    AdjudicationPayloadBindingSpec(
                        "exception_contract_id",
                        "exception_contract_target_ids",
                        ("exception_contract_id", "exception_contract_ids"),
                        required=True,
                        fanout=True,
                    ),
                    AdjudicationPayloadBindingSpec("reason", "contract_scalar", ("reason",), required=True),
                    AdjudicationPayloadBindingSpec("evidence", "contract_list", ("evidence",)),
                ),
            ),
        ),
    ),
    AdjudicationPlanSpec(
        plan_type="invalidate-invalidated-exception-contracts",
        compiled_commands=("invalidate-exception-contract",),
        requires_adjudication_fields=("Objects Invalidated", "reason"),
        target_resolution="resolve_active_exception_contracts_from_invalidated_objects",
        side_effect_codes=("invalidate_active_exception_contracts",),
        payload_templates=(
            AdjudicationPayloadTemplateSpec(
                command_name="invalidate-exception-contract",
                bindings=(
                    AdjudicationPayloadBindingSpec(
                        "exception_contract_id",
                        "exception_contract_target_ids",
                        ("exception_contract_id", "exception_contract_ids"),
                        required=True,
                        fanout=True,
                    ),
                    AdjudicationPayloadBindingSpec("reason", "contract_scalar", ("reason",), required=True),
                    AdjudicationPayloadBindingSpec("evidence", "contract_list", ("evidence",)),
                    AdjudicationPayloadBindingSpec("pivot_id", "contract_scalar", ("pivot_id",)),
                ),
            ),
        ),
    ),
    AdjudicationPlanSpec(
        plan_type="enter-execution-with-round-bootstrap",
        compiled_commands=("set-phase",),
        requires_adjudication_fields=("reason", "round_title", "round_scope_items", "round_deliverable", "round_validation_plan"),
        target_resolution="explicit_or_adjudication_objective",
        side_effect_codes=("enter_execution_phase", "bootstrap_bounded_round"),
        payload_templates=(
            AdjudicationPayloadTemplateSpec(
                command_name="set-phase",
                static_scalar_fields=(("phase", "execution"),),
                static_bool_fields=(("auto_open_round", True),),
                bindings=(
                    AdjudicationPayloadBindingSpec("objective_id", "contract_or_meta_scalar", ("objective_id",)),
                    AdjudicationPayloadBindingSpec("reason", "contract_scalar", ("reason",), required=True),
                    AdjudicationPayloadBindingSpec("round_title", "contract_or_meta_scalar", ("round_title",), required=True),
                    AdjudicationPayloadBindingSpec(
                        "round_deliverable",
                        "contract_or_meta_scalar",
                        ("round_deliverable",),
                        required=True,
                    ),
                    AdjudicationPayloadBindingSpec(
                        "round_validation_plan",
                        "contract_or_meta_scalar",
                        ("round_validation_plan",),
                        required=True,
                    ),
                    AdjudicationPayloadBindingSpec(
                        "round_scope_item",
                        "contract_or_meta_list",
                        ("round_scope_item", "round_scope_items"),
                        required=True,
                    ),
                    AdjudicationPayloadBindingSpec(
                        "round_scope_path",
                        "contract_or_meta_list",
                        ("round_scope_path", "round_scope_paths"),
                    ),
                    AdjudicationPayloadBindingSpec("round_summary", "contract_scalar", ("round_summary",)),
                    AdjudicationPayloadBindingSpec(
                        "round_risk",
                        "contract_or_meta_list",
                        ("round_risk", "round_risks"),
                    ),
                    AdjudicationPayloadBindingSpec(
                        "round_blocker",
                        "contract_or_meta_list",
                        ("round_blocker", "round_blockers"),
                    ),
                    AdjudicationPayloadBindingSpec(
                        "round_status_note",
                        "contract_or_meta_scalar",
                        ("round_status_note",),
                    ),
                    AdjudicationPayloadBindingSpec("evidence", "contract_list", ("evidence",)),
                    AdjudicationPayloadBindingSpec(
                        "scope_review_note",
                        "contract_list",
                        ("scope_review_note",),
                    ),
                ),
            ),
        ),
    ),
)


GUARD_SPEC_BY_CODE = {spec.code: spec for spec in GUARD_SPECS}
COMMAND_SPEC_BY_NAME = {spec.name: spec for spec in TRANSITION_COMMAND_SPECS}
PLAN_SPEC_BY_TYPE = {spec.plan_type: spec for spec in ADJUDICATION_PLAN_SPECS}


def validate_transition_specs() -> None:
    valid_implementation_statuses = {"implemented", "partial", "planned"}
    owner_label_sets = {
        "durable": SUPPORTED_DURABLE_OWNER_LABELS,
        "projection": SUPPORTED_PROJECTION_OWNER_LABELS,
        "artifact": SUPPORTED_ARTIFACT_OWNER_LABELS,
        "live inspection": SUPPORTED_LIVE_INSPECTION_OWNER_LABELS,
    }
    if len(GUARD_SPEC_BY_CODE) != len(GUARD_SPECS):
        raise SystemExit("duplicate guard codes found in transition registry")
    if len(COMMAND_SPEC_BY_NAME) != len(TRANSITION_COMMAND_SPECS):
        raise SystemExit("duplicate transition command names found in transition registry")
    if len(PLAN_SPEC_BY_TYPE) != len(ADJUDICATION_PLAN_SPECS):
        raise SystemExit("duplicate adjudication plan types found in transition registry")

    for spec in TRANSITION_COMMAND_SPECS:
        if spec.implementation_status not in valid_implementation_statuses:
            raise SystemExit(f"transition command `{spec.name}` uses unsupported implementation status `{spec.implementation_status}`")
        if spec.implementation_status in {"implemented", "partial"} and not spec.has_semantic_contract():
            raise SystemExit(f"transition command `{spec.name}` is {spec.implementation_status} but lacks semantic registry coverage")
        for owner_kind, allowed_labels, declared_labels in [
            ("durable", owner_label_sets["durable"], set(spec.durable_owners)),
            ("projection", owner_label_sets["projection"], set(spec.projection_owners)),
            ("artifact", owner_label_sets["artifact"], set(spec.artifact_owners)),
            ("live inspection", owner_label_sets["live inspection"], set(spec.live_inspection_owners)),
        ]:
            unsupported_labels = sorted(declared_labels - allowed_labels)
            if unsupported_labels:
                raise SystemExit(
                    f"transition command `{spec.name}` declares unsupported {owner_kind} owner labels: {', '.join(unsupported_labels)}"
                )
        unknown_guard_codes = sorted(set(spec.guard_codes) - set(GUARD_SPEC_BY_CODE))
        if unknown_guard_codes:
            raise SystemExit(
                f"transition command `{spec.name}` declares unknown guard codes: {', '.join(unknown_guard_codes)}"
            )
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
        declared_compiled_commands = set(plan_spec.compiled_commands)
        for template in plan_spec.payload_templates:
            if template.command_name not in declared_compiled_commands:
                raise SystemExit(
                    f"adjudication plan `{plan_spec.plan_type}` declares payload template for undeclared command `{template.command_name}`"
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


def transition_command_specs_for_domains(
    domains: set[str],
) -> list[TransitionCommandSpec]:
    validate_transition_specs()
    expected_domains = {domain.strip() for domain in domains if domain.strip()}
    return [spec for spec in TRANSITION_COMMAND_SPECS if spec.domain in expected_domains]


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


def guard_spec(code: str) -> GuardSpec:
    validate_transition_specs()
    spec = GUARD_SPEC_BY_CODE.get(code.strip())
    if spec is None:
        raise SystemExit(f"unknown transition guard `{code}`")
    return spec


def render_guard_text(code: str, context: dict[str, str] | None = None) -> str:
    return guard_spec(code).render(context)


def semantic_adjudication_plan_types() -> list[str]:
    validate_transition_specs()
    return [spec.plan_type for spec in ADJUDICATION_PLAN_SPECS if spec.has_semantic_contract()]


def export_transition_registry() -> dict[str, object]:
    validate_transition_specs()
    return {
        "guard_semantics": [spec.to_dict() for spec in GUARD_SPECS],
        "transition_commands": [spec.to_dict() for spec in TRANSITION_COMMAND_SPECS],
        "adjudication_plan_families": [spec.to_dict() for spec in ADJUDICATION_PLAN_SPECS],
    }
