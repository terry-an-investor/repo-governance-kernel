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
class WriteTargetSpec:
    target: str
    surface: str
    owner_bucket: str = "none"
    owner_labels: tuple[str, ...] = ()

    def to_dict(self) -> dict[str, object]:
        return {
            "target": self.target,
            "surface": self.surface,
            "owner_bucket": self.owner_bucket,
            "owner_labels": list(self.owner_labels),
        }


@dataclass(frozen=True)
class TransitionSideEffectSpec:
    code: str
    write_targets: tuple[str, ...] = ()
    durable_owners: tuple[str, ...] = ()
    projection_owners: tuple[str, ...] = ()
    artifact_owners: tuple[str, ...] = ()
    live_inspection_owners: tuple[str, ...] = ()

    def to_dict(self) -> dict[str, object]:
        return {
            "code": self.code,
            "write_targets": list(self.write_targets),
            "durable_owners": list(self.durable_owners),
            "projection_owners": list(self.projection_owners),
            "artifact_owners": list(self.artifact_owners),
            "live_inspection_owners": list(self.live_inspection_owners),
        }


@dataclass(frozen=True)
class CommandMutableFieldSpec:
    command_name: str
    code: str
    payload_key: str
    cli_flag: str
    value_kind: str
    storage_kind: str
    storage_key: str
    mutation_mode: str
    replace_flag: str = ""
    required_after_write: bool = False
    include_reason_note: bool = False
    material_requires_explicit_input: bool = False

    def to_dict(self) -> dict[str, object]:
        return {
            "command_name": self.command_name,
            "code": self.code,
            "payload_key": self.payload_key,
            "cli_flag": self.cli_flag,
            "value_kind": self.value_kind,
            "storage_kind": self.storage_kind,
            "storage_key": self.storage_key,
            "mutation_mode": self.mutation_mode,
            "replace_flag": self.replace_flag,
            "required_after_write": self.required_after_write,
            "include_reason_note": self.include_reason_note,
            "material_requires_explicit_input": self.material_requires_explicit_input,
        }


@dataclass(frozen=True)
class CommandExecutorFieldSpec:
    command_name: str
    payload_key: str
    cli_flag: str
    value_kind: str
    required: bool = False

    def to_dict(self) -> dict[str, object]:
        return {
            "command_name": self.command_name,
            "payload_key": self.payload_key,
            "cli_flag": self.cli_flag,
            "value_kind": self.value_kind,
            "required": self.required,
        }


@dataclass(frozen=True)
class BundleExecutorFieldSpec:
    bundle_name: str
    payload_key: str
    value_kind: str
    required: bool = False

    def to_dict(self) -> dict[str, object]:
        return {
            "bundle_name": self.bundle_name,
            "payload_key": self.payload_key,
            "value_kind": self.value_kind,
            "required": self.required,
        }


@dataclass(frozen=True)
class BundleGovernanceSpec:
    name: str
    bundle_kind: str
    purpose: str
    composed_commands: tuple[str, ...]
    state_resolver: str = ""
    direct_write_forbidden: bool = True
    private_semantics_forbidden: bool = True
    required_validations: tuple[str, ...] = ()

    def to_dict(self) -> dict[str, object]:
        return {
            "name": self.name,
            "bundle_kind": self.bundle_kind,
            "purpose": self.purpose,
            "composed_commands": list(self.composed_commands),
            "state_resolver": self.state_resolver,
            "direct_write_forbidden": self.direct_write_forbidden,
            "private_semantics_forbidden": self.private_semantics_forbidden,
            "required_validations": list(self.required_validations),
        }


@dataclass(frozen=True)
class BundleStateResolverSpec:
    name: str
    description: str

    def to_dict(self) -> dict[str, object]:
        return {
            "name": self.name,
            "description": self.description,
        }


@dataclass(frozen=True)
class BundleRouteStateSpec:
    bundle_name: str
    state: str
    terminal: bool = False
    required_payload_keys: tuple[str, ...] = ()

    def to_dict(self) -> dict[str, object]:
        return {
            "bundle_name": self.bundle_name,
            "state": self.state,
            "terminal": self.terminal,
            "required_payload_keys": list(self.required_payload_keys),
        }


@dataclass(frozen=True)
class BundleStepBindingSpec:
    target_key: str
    source_key: str
    value_kind: str = "scalar"

    def to_dict(self) -> dict[str, object]:
        return {
            "target_key": self.target_key,
            "source_key": self.source_key,
            "value_kind": self.value_kind,
        }


@dataclass(frozen=True)
class BundleStepTemplateSpec:
    bundle_name: str
    from_state: str
    to_state: str
    command_name: str
    label: str
    static_scalar_fields: tuple[tuple[str, str], ...] = ()
    static_bool_fields: tuple[tuple[str, bool], ...] = ()
    bindings: tuple[BundleStepBindingSpec, ...] = ()

    def to_dict(self) -> dict[str, object]:
        return {
            "bundle_name": self.bundle_name,
            "from_state": self.from_state,
            "to_state": self.to_state,
            "command_name": self.command_name,
            "label": self.label,
            "static_scalar_fields": [{"key": key, "value": value} for key, value in self.static_scalar_fields],
            "static_bool_fields": [{"key": key, "value": value} for key, value in self.static_bool_fields],
            "bindings": [binding.to_dict() for binding in self.bindings],
        }


@dataclass(frozen=True)
class AdjudicationTargetResolutionSpec:
    name: str
    description: str

    def to_dict(self) -> dict[str, object]:
        return {
            "name": self.name,
            "description": self.description,
        }


@dataclass(frozen=True)
class AdjudicationBindingResolverSpec:
    name: str
    description: str

    def to_dict(self) -> dict[str, object]:
        return {
            "name": self.name,
            "description": self.description,
        }


@dataclass(frozen=True)
class AdjudicationPlanSideEffectSpec:
    code: str
    description: str

    def to_dict(self) -> dict[str, object]:
        return {
            "code": self.code,
            "description": self.description,
        }


@dataclass(frozen=True)
class TransitionCommandSpec:
    name: str
    domain: str
    executor_supported: bool = False
    implementation_status: str = "implemented"
    required_inputs: tuple[str, ...] = ()
    mutable_field_codes: tuple[str, ...] = ()
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
        mutable_field_contract_present = "mutable_fields" not in self.required_inputs or bool(self.mutable_field_codes)
        return bool(
            self.required_inputs
            and mutable_field_contract_present
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
            "mutable_field_codes": list(self.mutable_field_codes),
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
    "memory:task-contract",
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
    "artifact:shadow-adoption-report",
    "snapshot:historical",
}

SUPPORTED_LIVE_INSPECTION_OWNER_LABELS = {
    "workspace:git-status",
}


WRITE_TARGET_SPECS: tuple[WriteTargetSpec, ...] = (
    WriteTargetSpec("durable:objective", "durable", "durable", ("memory:objective",)),
    WriteTargetSpec("durable:pivot", "durable", "durable", ("memory:pivot",)),
    WriteTargetSpec("durable:round", "durable", "durable", ("memory:round",)),
    WriteTargetSpec("durable:task-contract", "durable", "durable", ("memory:task-contract",)),
    WriteTargetSpec("durable:exception-contract", "durable", "durable", ("memory:exception-contract",)),
    WriteTargetSpec("control:active-objective", "projection", "projection", ("control:active-objective",)),
    WriteTargetSpec("control:pivot-log", "projection", "projection", ("control:pivot-log",)),
    WriteTargetSpec("control:active-round", "projection", "projection", ("control:active-round",)),
    WriteTargetSpec("control:exception-ledger", "projection", "projection", ("control:exception-ledger",)),
    WriteTargetSpec("current:current-task", "current", "durable", ("current:current-task",)),
    WriteTargetSpec("artifact:live-workspace-projection", "artifact", "artifact", ("artifact:live-workspace-projection",)),
    WriteTargetSpec("artifact:shadow-adoption-report", "artifact", "artifact", ("artifact:shadow-adoption-report",)),
    WriteTargetSpec("snapshot:historical", "snapshot", "artifact", ("snapshot:historical",)),
    WriteTargetSpec("memory:transition-event", "event"),
)


TRANSITION_SIDE_EFFECT_SPECS: tuple[TransitionSideEffectSpec, ...] = (
    TransitionSideEffectSpec("activate_objective_line", ("durable:objective",), durable_owners=("memory:objective",)),
    TransitionSideEffectSpec("refresh_active_objective_projection", ("control:active-objective",), projection_owners=("control:active-objective",)),
    TransitionSideEffectSpec("refresh_pivot_log_projection", ("control:pivot-log",), projection_owners=("control:pivot-log",)),
    TransitionSideEffectSpec("close_active_objective", ("durable:objective",), durable_owners=("memory:objective",)),
    TransitionSideEffectSpec("rewrite_active_objective_in_place", ("durable:objective",), durable_owners=("memory:objective",)),
    TransitionSideEffectSpec("record_pivot_lineage", ("durable:pivot",), durable_owners=("memory:pivot",)),
    TransitionSideEffectSpec("force_explicit_round_review_path"),
    TransitionSideEffectSpec("supersede_previous_objective", ("durable:objective",), durable_owners=("memory:objective",)),
    TransitionSideEffectSpec("activate_new_objective_line", ("durable:objective",), durable_owners=("memory:objective",)),
    TransitionSideEffectSpec("review_or_resolve_stale_exception_contracts"),
    TransitionSideEffectSpec("rewrite_objective_phase", ("durable:objective",), durable_owners=("memory:objective",)),
    TransitionSideEffectSpec("optionally_bootstrap_execution_round", ("control:active-round",), projection_owners=("control:active-round",)),
    TransitionSideEffectSpec("optionally_rewrite_open_rounds", ("control:active-round",), projection_owners=("control:active-round",)),
    TransitionSideEffectSpec("open_bounded_execution_round", ("durable:round",), durable_owners=("memory:round",)),
    TransitionSideEffectSpec("refresh_active_round_projection", ("control:active-round",), projection_owners=("control:active-round",)),
    TransitionSideEffectSpec("rewrite_round_scope_paths", ("durable:round",), durable_owners=("memory:round",)),
    TransitionSideEffectSpec("preserve_round_identity"),
    TransitionSideEffectSpec("advance_round_lifecycle_state", ("durable:round",), durable_owners=("memory:round",)),
    TransitionSideEffectSpec("record_blocker_or_validation_history", ("durable:round",), durable_owners=("memory:round",)),
    TransitionSideEffectSpec("rewrite_open_round_contract", ("durable:round",), durable_owners=("memory:round",)),
    TransitionSideEffectSpec("record_task_contract", ("durable:task-contract",), durable_owners=("memory:task-contract",)),
    TransitionSideEffectSpec("preserve_round_task_governance_boundary"),
    TransitionSideEffectSpec("advance_task_contract_lifecycle_state", ("durable:task-contract",), durable_owners=("memory:task-contract",)),
    TransitionSideEffectSpec("record_task_contract_completion_or_resolution", ("durable:task-contract",), durable_owners=("memory:task-contract",)),
    TransitionSideEffectSpec("rewrite_open_task_contract", ("durable:task-contract",), durable_owners=("memory:task-contract",)),
    TransitionSideEffectSpec("record_active_exception_contract", ("durable:exception-contract",), durable_owners=("memory:exception-contract",)),
    TransitionSideEffectSpec("refresh_exception_ledger_projection", ("control:exception-ledger",), projection_owners=("control:exception-ledger",)),
    TransitionSideEffectSpec("retire_exception_contract", ("durable:exception-contract",), durable_owners=("memory:exception-contract",)),
    TransitionSideEffectSpec("invalidate_exception_contract", ("durable:exception-contract",), durable_owners=("memory:exception-contract",)),
    TransitionSideEffectSpec(
        "refresh_current_task_control_locator",
        ("current:current-task",),
        durable_owners=("current:current-task",),
        live_inspection_owners=("workspace:git-status",),
    ),
    TransitionSideEffectSpec(
        "render_live_workspace_projection",
        ("artifact:live-workspace-projection",),
        artifact_owners=("artifact:live-workspace-projection",),
        live_inspection_owners=("workspace:git-status",),
    ),
    TransitionSideEffectSpec(
        "render_shadow_adoption_report",
        ("artifact:shadow-adoption-report",),
        artifact_owners=("artifact:shadow-adoption-report",),
        live_inspection_owners=("workspace:git-status",),
    ),
    TransitionSideEffectSpec(
        "render_external_target_shadow_scope_draft",
        ("artifact:shadow-adoption-report",),
        artifact_owners=("artifact:shadow-adoption-report",),
        live_inspection_owners=("workspace:git-status",),
    ),
    TransitionSideEffectSpec(
        "capture_phase_or_handoff_snapshot",
        ("snapshot:historical",),
        artifact_owners=("snapshot:historical",),
        live_inspection_owners=("workspace:git-status",),
    ),
)


COMMAND_MUTABLE_FIELD_SPECS: tuple[CommandMutableFieldSpec, ...] = (
    CommandMutableFieldSpec(
        command_name="rewrite-open-round",
        code="title",
        payload_key="title",
        cli_flag="title",
        value_kind="scalar",
        storage_kind="meta_scalar",
        storage_key="title",
        mutation_mode="replace_if_present",
    ),
    CommandMutableFieldSpec(
        command_name="rewrite-open-round",
        code="summary",
        payload_key="summary",
        cli_flag="summary",
        value_kind="scalar",
        storage_kind="section_text",
        storage_key="Summary",
        mutation_mode="replace_if_present",
    ),
    CommandMutableFieldSpec(
        command_name="rewrite-open-round",
        code="scope_items",
        payload_key="scope_item",
        cli_flag="scope-item",
        value_kind="list",
        storage_kind="section_bullets",
        storage_key="Scope",
        mutation_mode="merge_unique",
        replace_flag="replace_scope_items",
        required_after_write=True,
    ),
    CommandMutableFieldSpec(
        command_name="rewrite-open-round",
        code="deliverable",
        payload_key="deliverable",
        cli_flag="deliverable",
        value_kind="scalar",
        storage_kind="section_text",
        storage_key="Deliverable",
        mutation_mode="replace_if_present",
        required_after_write=True,
    ),
    CommandMutableFieldSpec(
        command_name="rewrite-open-round",
        code="validation_plan",
        payload_key="validation_plan",
        cli_flag="validation-plan",
        value_kind="scalar",
        storage_kind="section_text",
        storage_key="Validation Plan",
        mutation_mode="replace_if_present",
        required_after_write=True,
    ),
    CommandMutableFieldSpec(
        command_name="rewrite-open-round",
        code="risks",
        payload_key="risk",
        cli_flag="risk",
        value_kind="list",
        storage_kind="section_bullets",
        storage_key="Active Risks",
        mutation_mode="merge_unique",
        replace_flag="replace_risks",
    ),
    CommandMutableFieldSpec(
        command_name="rewrite-open-round",
        code="blockers",
        payload_key="blocker",
        cli_flag="blocker",
        value_kind="list",
        storage_kind="section_bullets",
        storage_key="Blockers",
        mutation_mode="merge_unique",
        replace_flag="replace_blockers",
    ),
    CommandMutableFieldSpec(
        command_name="rewrite-open-round",
        code="status_notes",
        payload_key="status_note",
        cli_flag="status-note",
        value_kind="list",
        storage_kind="section_text",
        storage_key="Status Notes",
        mutation_mode="append_paragraphs",
        include_reason_note=True,
        material_requires_explicit_input=True,
    ),
    CommandMutableFieldSpec(
        command_name="rewrite-open-round",
        code="paths",
        payload_key="scope_path",
        cli_flag="scope-path",
        value_kind="list",
        storage_kind="meta_list",
        storage_key="paths",
        mutation_mode="merge_unique",
        replace_flag="replace_scope_paths",
        required_after_write=True,
    ),
    CommandMutableFieldSpec(
        command_name="rewrite-open-task-contract",
        code="title",
        payload_key="title",
        cli_flag="title",
        value_kind="scalar",
        storage_kind="meta_scalar",
        storage_key="title",
        mutation_mode="replace_if_present",
    ),
    CommandMutableFieldSpec(
        command_name="rewrite-open-task-contract",
        code="summary",
        payload_key="summary",
        cli_flag="summary",
        value_kind="scalar",
        storage_kind="section_text",
        storage_key="Summary",
        mutation_mode="replace_if_present",
    ),
    CommandMutableFieldSpec(
        command_name="rewrite-open-task-contract",
        code="intent",
        payload_key="intent",
        cli_flag="intent",
        value_kind="scalar",
        storage_kind="section_text",
        storage_key="Intent",
        mutation_mode="replace_if_present",
        required_after_write=True,
    ),
    CommandMutableFieldSpec(
        command_name="rewrite-open-task-contract",
        code="allowed_changes",
        payload_key="allowed_change",
        cli_flag="allowed-change",
        value_kind="list",
        storage_kind="section_bullets",
        storage_key="Allowed Changes",
        mutation_mode="merge_unique",
        replace_flag="replace_allowed_changes",
        required_after_write=True,
    ),
    CommandMutableFieldSpec(
        command_name="rewrite-open-task-contract",
        code="forbidden_changes",
        payload_key="forbidden_change",
        cli_flag="forbidden-change",
        value_kind="list",
        storage_kind="section_bullets",
        storage_key="Forbidden Changes",
        mutation_mode="merge_unique",
        replace_flag="replace_forbidden_changes",
        required_after_write=True,
    ),
    CommandMutableFieldSpec(
        command_name="rewrite-open-task-contract",
        code="completion_criteria",
        payload_key="completion_criterion",
        cli_flag="completion-criterion",
        value_kind="list",
        storage_kind="section_bullets",
        storage_key="Completion Criteria",
        mutation_mode="merge_unique",
        replace_flag="replace_completion_criteria",
        required_after_write=True,
    ),
    CommandMutableFieldSpec(
        command_name="rewrite-open-task-contract",
        code="risks",
        payload_key="risk",
        cli_flag="risk",
        value_kind="list",
        storage_kind="section_bullets",
        storage_key="Active Risks",
        mutation_mode="merge_unique",
        replace_flag="replace_risks",
    ),
    CommandMutableFieldSpec(
        command_name="rewrite-open-task-contract",
        code="status_notes",
        payload_key="status_note",
        cli_flag="status-note",
        value_kind="list",
        storage_kind="section_text",
        storage_key="Status Notes",
        mutation_mode="append_paragraphs",
        include_reason_note=True,
        material_requires_explicit_input=True,
    ),
    CommandMutableFieldSpec(
        command_name="rewrite-open-task-contract",
        code="paths",
        payload_key="path",
        cli_flag="path",
        value_kind="list",
        storage_kind="meta_list",
        storage_key="paths",
        mutation_mode="merge_unique",
        replace_flag="replace_paths",
        required_after_write=True,
    ),
)


COMMAND_EXECUTOR_FIELD_SPECS: tuple[CommandExecutorFieldSpec, ...] = (
    CommandExecutorFieldSpec("open-objective", "title", "title", "scalar", required=True),
    CommandExecutorFieldSpec("open-objective", "summary", "summary", "scalar"),
    CommandExecutorFieldSpec("open-objective", "problem", "problem", "scalar", required=True),
    CommandExecutorFieldSpec("open-objective", "success_criterion", "success-criterion", "list", required=True),
    CommandExecutorFieldSpec("open-objective", "non_goal", "non-goal", "list", required=True),
    CommandExecutorFieldSpec("open-objective", "why_now", "why-now", "scalar", required=True),
    CommandExecutorFieldSpec("open-objective", "phase", "phase", "scalar", required=True),
    CommandExecutorFieldSpec("open-objective", "risk", "risk", "list"),
    CommandExecutorFieldSpec("open-objective", "path", "path", "list"),
    CommandExecutorFieldSpec("open-objective", "supersession_notes", "supersession-notes", "scalar"),
    CommandExecutorFieldSpec("close-objective", "objective_id", "objective-id", "scalar"),
    CommandExecutorFieldSpec("close-objective", "closing_status", "closing-status", "scalar", required=True),
    CommandExecutorFieldSpec("close-objective", "reason", "reason", "scalar", required=True),
    CommandExecutorFieldSpec("close-objective", "evidence", "evidence", "list"),
    CommandExecutorFieldSpec("close-objective", "supersession_note", "supersession-note", "scalar"),
    CommandExecutorFieldSpec("open-round", "objective_id", "objective-id", "scalar"),
    CommandExecutorFieldSpec("open-round", "title", "title", "scalar", required=True),
    CommandExecutorFieldSpec("open-round", "scope_item", "scope-item", "list", required=True),
    CommandExecutorFieldSpec("open-round", "scope_path", "scope-path", "list"),
    CommandExecutorFieldSpec("open-round", "deliverable", "deliverable", "scalar", required=True),
    CommandExecutorFieldSpec("open-round", "validation_plan", "validation-plan", "scalar", required=True),
    CommandExecutorFieldSpec("open-round", "risk", "risk", "list"),
    CommandExecutorFieldSpec("open-round", "blocker", "blocker", "list"),
    CommandExecutorFieldSpec("open-round", "status_note", "status-note", "scalar"),
    CommandExecutorFieldSpec("record-soft-pivot", "objective_id", "objective-id", "scalar"),
    CommandExecutorFieldSpec("record-soft-pivot", "trigger", "trigger", "scalar", required=True),
    CommandExecutorFieldSpec("record-soft-pivot", "change_summary", "change-summary", "scalar", required=True),
    CommandExecutorFieldSpec("record-soft-pivot", "identity_rationale", "identity-rationale", "scalar", required=True),
    CommandExecutorFieldSpec("record-soft-pivot", "pivot_title", "pivot-title", "scalar"),
    CommandExecutorFieldSpec("record-soft-pivot", "evidence", "evidence", "list"),
    CommandExecutorFieldSpec("record-soft-pivot", "retained_decision", "retained-decision", "list"),
    CommandExecutorFieldSpec("record-soft-pivot", "invalidated_assumption", "invalidated-assumption", "list"),
    CommandExecutorFieldSpec("record-soft-pivot", "next_control_change", "next-control-change", "list"),
    CommandExecutorFieldSpec("record-soft-pivot", "rewrite_open_round", "rewrite-open-round", "bool"),
    CommandExecutorFieldSpec("record-soft-pivot", "title", "title", "scalar"),
    CommandExecutorFieldSpec("record-soft-pivot", "summary", "summary", "scalar"),
    CommandExecutorFieldSpec("record-soft-pivot", "problem", "problem", "scalar"),
    CommandExecutorFieldSpec("record-soft-pivot", "success_criterion", "success-criterion", "list"),
    CommandExecutorFieldSpec("record-soft-pivot", "non_goal", "non-goal", "list"),
    CommandExecutorFieldSpec("record-soft-pivot", "why_now", "why-now", "scalar"),
    CommandExecutorFieldSpec("record-soft-pivot", "phase", "phase", "scalar"),
    CommandExecutorFieldSpec("record-soft-pivot", "risk", "risk", "list"),
    CommandExecutorFieldSpec("record-soft-pivot", "path", "path", "list"),
    CommandExecutorFieldSpec("record-soft-pivot", "supersession_notes", "supersession-notes", "scalar"),
    CommandExecutorFieldSpec("record-soft-pivot", "round_title", "round-title", "scalar"),
    CommandExecutorFieldSpec("record-soft-pivot", "round_summary", "round-summary", "scalar"),
    CommandExecutorFieldSpec("record-soft-pivot", "round_scope_item", "round-scope-item", "list"),
    CommandExecutorFieldSpec("record-soft-pivot", "round_scope_path", "round-scope-path", "list"),
    CommandExecutorFieldSpec("record-soft-pivot", "round_deliverable", "round-deliverable", "scalar"),
    CommandExecutorFieldSpec("record-soft-pivot", "round_validation_plan", "round-validation-plan", "scalar"),
    CommandExecutorFieldSpec("record-soft-pivot", "round_risk", "round-risk", "list"),
    CommandExecutorFieldSpec("record-soft-pivot", "round_blocker", "round-blocker", "list"),
    CommandExecutorFieldSpec("record-soft-pivot", "round_status_note", "round-status-note", "list"),
    CommandExecutorFieldSpec("record-soft-pivot", "replace_round_scope_items", "replace-round-scope-items", "bool"),
    CommandExecutorFieldSpec("record-soft-pivot", "replace_round_scope_paths", "replace-round-scope-paths", "bool"),
    CommandExecutorFieldSpec("record-soft-pivot", "replace_round_risks", "replace-round-risks", "bool"),
    CommandExecutorFieldSpec("record-soft-pivot", "replace_round_blockers", "replace-round-blockers", "bool"),
    CommandExecutorFieldSpec("record-hard-pivot", "previous_objective_id", "previous-objective-id", "scalar"),
    CommandExecutorFieldSpec("record-hard-pivot", "title", "title", "scalar", required=True),
    CommandExecutorFieldSpec("record-hard-pivot", "summary", "summary", "scalar"),
    CommandExecutorFieldSpec("record-hard-pivot", "problem", "problem", "scalar", required=True),
    CommandExecutorFieldSpec("record-hard-pivot", "success_criterion", "success-criterion", "list", required=True),
    CommandExecutorFieldSpec("record-hard-pivot", "non_goal", "non-goal", "list", required=True),
    CommandExecutorFieldSpec("record-hard-pivot", "why_now", "why-now", "scalar", required=True),
    CommandExecutorFieldSpec("record-hard-pivot", "phase", "phase", "scalar", required=True),
    CommandExecutorFieldSpec("record-hard-pivot", "trigger", "trigger", "scalar", required=True),
    CommandExecutorFieldSpec("record-hard-pivot", "pivot_title", "pivot-title", "scalar"),
    CommandExecutorFieldSpec("record-hard-pivot", "evidence", "evidence", "list"),
    CommandExecutorFieldSpec("record-hard-pivot", "retained_decision", "retained-decision", "list"),
    CommandExecutorFieldSpec("record-hard-pivot", "invalidated_assumption", "invalidated-assumption", "list"),
    CommandExecutorFieldSpec("record-hard-pivot", "next_control_change", "next-control-change", "list"),
    CommandExecutorFieldSpec("record-hard-pivot", "risk", "risk", "list"),
    CommandExecutorFieldSpec("record-hard-pivot", "path", "path", "list"),
    CommandExecutorFieldSpec("record-hard-pivot", "supersession_notes", "supersession-notes", "scalar"),
    CommandExecutorFieldSpec("update-round-status", "round_id", "round-id", "scalar", required=True),
    CommandExecutorFieldSpec("update-round-status", "status", "status", "scalar", required=True),
    CommandExecutorFieldSpec("update-round-status", "reason", "reason", "scalar", required=True),
    CommandExecutorFieldSpec("update-round-status", "validated_by", "validated-by", "list"),
    CommandExecutorFieldSpec("update-round-status", "blocker", "blocker", "list"),
    CommandExecutorFieldSpec("update-round-status", "risk", "risk", "list"),
    CommandExecutorFieldSpec("update-round-status", "clear_blockers", "clear-blockers", "bool"),
    CommandExecutorFieldSpec("refresh-round-scope", "round_id", "round-id", "scalar"),
    CommandExecutorFieldSpec("refresh-round-scope", "reason", "reason", "scalar", required=True),
    CommandExecutorFieldSpec("refresh-round-scope", "evidence", "evidence", "list"),
    CommandExecutorFieldSpec("refresh-round-scope", "add_scope_path", "add-scope-path", "list"),
    CommandExecutorFieldSpec("refresh-round-scope", "drop_scope_path", "drop-scope-path", "list"),
    CommandExecutorFieldSpec("refresh-round-scope", "no_live_dirty_paths", "no-live-dirty-paths", "bool"),
    CommandExecutorFieldSpec("rewrite-open-round", "round_id", "round-id", "scalar"),
    CommandExecutorFieldSpec("rewrite-open-round", "reason", "reason", "scalar", required=True),
    CommandExecutorFieldSpec("open-task-contract", "title", "title", "scalar", required=True),
    CommandExecutorFieldSpec("open-task-contract", "summary", "summary", "scalar"),
    CommandExecutorFieldSpec("open-task-contract", "round_id", "round-id", "scalar"),
    CommandExecutorFieldSpec("open-task-contract", "intent", "intent", "scalar", required=True),
    CommandExecutorFieldSpec("open-task-contract", "path", "path", "list", required=True),
    CommandExecutorFieldSpec("open-task-contract", "allowed_change", "allowed-change", "list", required=True),
    CommandExecutorFieldSpec("open-task-contract", "forbidden_change", "forbidden-change", "list", required=True),
    CommandExecutorFieldSpec("open-task-contract", "completion_criterion", "completion-criterion", "list", required=True),
    CommandExecutorFieldSpec("open-task-contract", "risk", "risk", "list"),
    CommandExecutorFieldSpec("open-task-contract", "status_note", "status-note", "scalar"),
    CommandExecutorFieldSpec("update-task-contract-status", "task_contract_id", "task-contract-id", "scalar", required=True),
    CommandExecutorFieldSpec("update-task-contract-status", "status", "status", "scalar", required=True),
    CommandExecutorFieldSpec("update-task-contract-status", "reason", "reason", "scalar", required=True),
    CommandExecutorFieldSpec("update-task-contract-status", "resolution", "resolution", "list"),
    CommandExecutorFieldSpec("update-task-contract-status", "risk", "risk", "list"),
    CommandExecutorFieldSpec("update-task-contract-status", "status_note", "status-note", "list"),
    CommandExecutorFieldSpec("rewrite-open-task-contract", "task_contract_id", "task-contract-id", "scalar"),
    CommandExecutorFieldSpec("rewrite-open-task-contract", "reason", "reason", "scalar", required=True),
    CommandExecutorFieldSpec("refresh-anchor", "workspace_root", "workspace-root", "scalar"),
    CommandExecutorFieldSpec("draft-external-target-shadow-scope", "workspace_root", "workspace-root", "scalar", required=True),
    CommandExecutorFieldSpec("draft-external-target-shadow-scope", "source_repo", "source-repo", "scalar"),
    CommandExecutorFieldSpec("draft-external-target-shadow-scope", "output", "output", "scalar"),
    CommandExecutorFieldSpec("assess-host-adoption", "workspace_root", "workspace-root", "scalar"),
    CommandExecutorFieldSpec("assess-host-adoption", "source_repo", "source-repo", "scalar"),
    CommandExecutorFieldSpec("assess-host-adoption", "mode", "mode", "scalar"),
    CommandExecutorFieldSpec("assess-host-adoption", "output", "output", "scalar"),
    CommandExecutorFieldSpec("set-phase", "objective_id", "objective-id", "scalar"),
    CommandExecutorFieldSpec("set-phase", "phase", "phase", "scalar", required=True),
    CommandExecutorFieldSpec("set-phase", "reason", "reason", "scalar", required=True),
    CommandExecutorFieldSpec("set-phase", "evidence", "evidence", "list"),
    CommandExecutorFieldSpec("set-phase", "scope_review_note", "scope-review-note", "list"),
    CommandExecutorFieldSpec("set-phase", "rewrite_open_round", "rewrite-open-round", "bool"),
    CommandExecutorFieldSpec("set-phase", "auto_open_round", "auto-open-round", "bool"),
    CommandExecutorFieldSpec("set-phase", "round_title", "round-title", "scalar"),
    CommandExecutorFieldSpec("set-phase", "round_summary", "round-summary", "scalar"),
    CommandExecutorFieldSpec("set-phase", "round_scope_item", "round-scope-item", "list"),
    CommandExecutorFieldSpec("set-phase", "round_scope_path", "round-scope-path", "list"),
    CommandExecutorFieldSpec("set-phase", "round_deliverable", "round-deliverable", "scalar"),
    CommandExecutorFieldSpec("set-phase", "round_validation_plan", "round-validation-plan", "scalar"),
    CommandExecutorFieldSpec("set-phase", "round_risk", "round-risk", "list"),
    CommandExecutorFieldSpec("set-phase", "round_blocker", "round-blocker", "list"),
    CommandExecutorFieldSpec("set-phase", "round_status_note", "round-status-note", "scalar"),
    CommandExecutorFieldSpec("set-phase", "replace_round_scope_items", "replace-round-scope-items", "bool"),
    CommandExecutorFieldSpec("set-phase", "replace_round_scope_paths", "replace-round-scope-paths", "bool"),
    CommandExecutorFieldSpec("set-phase", "replace_round_risks", "replace-round-risks", "bool"),
    CommandExecutorFieldSpec("set-phase", "replace_round_blockers", "replace-round-blockers", "bool"),
    CommandExecutorFieldSpec("activate-exception-contract", "title", "title", "scalar", required=True),
    CommandExecutorFieldSpec("activate-exception-contract", "objective_id", "objective-id", "scalar"),
    CommandExecutorFieldSpec("activate-exception-contract", "summary", "summary", "scalar", required=True),
    CommandExecutorFieldSpec("activate-exception-contract", "reason", "reason", "scalar", required=True),
    CommandExecutorFieldSpec("activate-exception-contract", "temporary_behavior", "temporary-behavior", "scalar", required=True),
    CommandExecutorFieldSpec("activate-exception-contract", "risk", "risk", "scalar", required=True),
    CommandExecutorFieldSpec("activate-exception-contract", "exit_condition", "exit-condition", "scalar", required=True),
    CommandExecutorFieldSpec("activate-exception-contract", "owner_scope", "owner-scope", "list", required=True),
    CommandExecutorFieldSpec("activate-exception-contract", "path", "path", "list"),
    CommandExecutorFieldSpec("activate-exception-contract", "evidence", "evidence", "list"),
    CommandExecutorFieldSpec("retire-exception-contract", "exception_contract_id", "exception-contract-id", "scalar", required=True),
    CommandExecutorFieldSpec("retire-exception-contract", "reason", "reason", "scalar", required=True),
    CommandExecutorFieldSpec("retire-exception-contract", "evidence", "evidence", "list"),
    CommandExecutorFieldSpec("invalidate-exception-contract", "exception_contract_id", "exception-contract-id", "scalar", required=True),
    CommandExecutorFieldSpec("invalidate-exception-contract", "reason", "reason", "scalar", required=True),
    CommandExecutorFieldSpec("invalidate-exception-contract", "evidence", "evidence", "list"),
    CommandExecutorFieldSpec("invalidate-exception-contract", "pivot_id", "pivot-id", "scalar"),
)


BUNDLE_EXECUTOR_FIELD_SPECS: tuple[BundleExecutorFieldSpec, ...] = (
    BundleExecutorFieldSpec("round-close-chain", "round_id", "scalar", required=True),
    BundleExecutorFieldSpec("round-close-chain", "reactivation_reason", "scalar"),
    BundleExecutorFieldSpec("round-close-chain", "validation_pending_reason", "scalar"),
    BundleExecutorFieldSpec("round-close-chain", "captured_reason", "scalar"),
    BundleExecutorFieldSpec("round-close-chain", "closed_reason", "scalar"),
    BundleExecutorFieldSpec("round-close-chain", "validated_by", "list"),
    BundleExecutorFieldSpec("round-close-chain", "blocker", "list"),
    BundleExecutorFieldSpec("round-close-chain", "risk", "list"),
    BundleExecutorFieldSpec("round-close-chain", "clear_blockers", "bool"),
    BundleExecutorFieldSpec("round-close-chain-then-hard-pivot", "round_id", "scalar", required=True),
    BundleExecutorFieldSpec("round-close-chain-then-hard-pivot", "reactivation_reason", "scalar"),
    BundleExecutorFieldSpec("round-close-chain-then-hard-pivot", "validation_pending_reason", "scalar"),
    BundleExecutorFieldSpec("round-close-chain-then-hard-pivot", "captured_reason", "scalar"),
    BundleExecutorFieldSpec("round-close-chain-then-hard-pivot", "closed_reason", "scalar"),
    BundleExecutorFieldSpec("round-close-chain-then-hard-pivot", "validated_by", "list"),
    BundleExecutorFieldSpec("round-close-chain-then-hard-pivot", "blocker", "list"),
    BundleExecutorFieldSpec("round-close-chain-then-hard-pivot", "close_chain_risk", "list"),
    BundleExecutorFieldSpec("round-close-chain-then-hard-pivot", "clear_blockers", "bool"),
    BundleExecutorFieldSpec("round-close-chain-then-hard-pivot", "previous_objective_id", "scalar", required=True),
    BundleExecutorFieldSpec("round-close-chain-then-hard-pivot", "title", "scalar", required=True),
    BundleExecutorFieldSpec("round-close-chain-then-hard-pivot", "summary", "scalar"),
    BundleExecutorFieldSpec("round-close-chain-then-hard-pivot", "problem", "scalar", required=True),
    BundleExecutorFieldSpec("round-close-chain-then-hard-pivot", "success_criterion", "list", required=True),
    BundleExecutorFieldSpec("round-close-chain-then-hard-pivot", "non_goal", "list", required=True),
    BundleExecutorFieldSpec("round-close-chain-then-hard-pivot", "why_now", "scalar", required=True),
    BundleExecutorFieldSpec("round-close-chain-then-hard-pivot", "phase", "scalar", required=True),
    BundleExecutorFieldSpec("round-close-chain-then-hard-pivot", "trigger", "scalar", required=True),
    BundleExecutorFieldSpec("round-close-chain-then-hard-pivot", "pivot_title", "scalar"),
    BundleExecutorFieldSpec("round-close-chain-then-hard-pivot", "evidence", "list"),
    BundleExecutorFieldSpec("round-close-chain-then-hard-pivot", "retained_decision", "list"),
    BundleExecutorFieldSpec("round-close-chain-then-hard-pivot", "invalidated_assumption", "list"),
    BundleExecutorFieldSpec("round-close-chain-then-hard-pivot", "next_control_change", "list"),
    BundleExecutorFieldSpec("round-close-chain-then-hard-pivot", "objective_risk", "list"),
    BundleExecutorFieldSpec("round-close-chain-then-hard-pivot", "path", "list"),
    BundleExecutorFieldSpec("round-close-chain-then-hard-pivot", "supersession_notes", "scalar"),
    BundleExecutorFieldSpec("assess-external-target-once", "workspace_root", "scalar", required=True),
    BundleExecutorFieldSpec("assess-external-target-once", "source_repo", "scalar"),
    BundleExecutorFieldSpec("assess-external-target-once", "draft_output", "scalar"),
    BundleExecutorFieldSpec("assess-external-target-once", "report_output", "scalar"),
    BundleExecutorFieldSpec("assess-external-target-once", "round_id", "scalar", required=True),
    BundleExecutorFieldSpec("assess-external-target-once", "task_contract_id", "scalar", required=True),
    BundleExecutorFieldSpec("assess-external-target-once", "expand_round_scope_path", "list", required=True),
    BundleExecutorFieldSpec("assess-external-target-once", "round_scope_item", "list", required=True),
    BundleExecutorFieldSpec("assess-external-target-once", "round_scope_path", "list", required=True),
    BundleExecutorFieldSpec("assess-external-target-once", "round_deliverable", "scalar", required=True),
    BundleExecutorFieldSpec("assess-external-target-once", "round_validation_plan", "scalar", required=True),
    BundleExecutorFieldSpec("assess-external-target-once", "task_summary", "scalar", required=True),
    BundleExecutorFieldSpec("assess-external-target-once", "task_intent", "scalar", required=True),
    BundleExecutorFieldSpec("assess-external-target-once", "task_path", "list", required=True),
    BundleExecutorFieldSpec("assess-external-target-once", "task_allowed_change", "list", required=True),
    BundleExecutorFieldSpec("assess-external-target-once", "task_forbidden_change", "list", required=True),
    BundleExecutorFieldSpec("assess-external-target-once", "task_completion_criterion", "list", required=True),
)


BUNDLE_GOVERNANCE_SPECS: tuple[BundleGovernanceSpec, ...] = (
    BundleGovernanceSpec(
        name="round-close-chain",
        bundle_kind="executor-wrapper",
        purpose="Advance one round through the legal close sequence by composing only existing round status transitions.",
        composed_commands=("update-round-status",),
        state_resolver="round_status_from_round_id",
        required_validations=("scripts/smoke_adjudication_followups.py",),
    ),
    BundleGovernanceSpec(
        name="round-close-chain-then-hard-pivot",
        bundle_kind="executor-wrapper",
        purpose="Close one predecessor round through the governed close chain and then record one hard pivot without inventing private replacement semantics.",
        composed_commands=("round-close-chain", "record-hard-pivot"),
        state_resolver="hard_pivot_bundle_state_from_previous_objective_and_round",
        required_validations=("scripts/smoke_adjudication_followups.py",),
    ),
    BundleGovernanceSpec(
        name="assess-external-target-once",
        bundle_kind="executor-wrapper",
        purpose="Run one bounded external-target shadow workflow by composing draft, controlled round/task rewrites, anchor refresh, and assessment without introducing freeform mutation authority.",
        composed_commands=(
            "draft-external-target-shadow-scope",
            "rewrite-open-round",
            "rewrite-open-task-contract",
            "refresh-anchor",
            "assess-host-adoption",
        ),
        state_resolver="constant_start_state",
        required_validations=("scripts/smoke_assess_host_adoption.py",),
    ),
)


BUNDLE_STATE_RESOLVER_SPECS: tuple[BundleStateResolverSpec, ...] = (
    BundleStateResolverSpec(
        "round_status_from_round_id",
        "Resolve the current bundle route state from the durable status of the target round referenced by `round_id`.",
    ),
    BundleStateResolverSpec(
        "hard_pivot_bundle_state_from_previous_objective_and_round",
        "Resolve hard-pivot bundle state from the previous objective status plus the durable status of the target predecessor round.",
    ),
    BundleStateResolverSpec(
        "constant_start_state",
        "Always start the bundle from one explicit initial route state because the wrapper has already compiled the required payload.",
    ),
)


BUNDLE_ROUTE_STATE_SPECS: tuple[BundleRouteStateSpec, ...] = (
    BundleRouteStateSpec("round-close-chain", "blocked", required_payload_keys=("reactivation_reason", "validated_by", "validation_pending_reason", "captured_reason", "closed_reason")),
    BundleRouteStateSpec("round-close-chain", "active", required_payload_keys=("validated_by", "validation_pending_reason", "captured_reason", "closed_reason")),
    BundleRouteStateSpec("round-close-chain", "validation_pending", required_payload_keys=("validated_by", "captured_reason", "closed_reason")),
    BundleRouteStateSpec("round-close-chain", "captured", required_payload_keys=("closed_reason",)),
    BundleRouteStateSpec("round-close-chain", "closed", terminal=True),
    BundleRouteStateSpec("round-close-chain-then-hard-pivot", "blocked", required_payload_keys=("reactivation_reason", "validated_by", "validation_pending_reason", "captured_reason", "closed_reason")),
    BundleRouteStateSpec("round-close-chain-then-hard-pivot", "active", required_payload_keys=("validated_by", "validation_pending_reason", "captured_reason", "closed_reason")),
    BundleRouteStateSpec("round-close-chain-then-hard-pivot", "validation_pending", required_payload_keys=("validated_by", "captured_reason", "closed_reason")),
    BundleRouteStateSpec("round-close-chain-then-hard-pivot", "captured", required_payload_keys=("closed_reason",)),
    BundleRouteStateSpec("round-close-chain-then-hard-pivot", "closed", required_payload_keys=("previous_objective_id", "title", "problem", "success_criterion", "non_goal", "why_now", "phase", "trigger")),
    BundleRouteStateSpec("round-close-chain-then-hard-pivot", "pivoted", terminal=True),
    BundleRouteStateSpec("assess-external-target-once", "start"),
    BundleRouteStateSpec("assess-external-target-once", "drafted"),
    BundleRouteStateSpec("assess-external-target-once", "round_expanded"),
    BundleRouteStateSpec("assess-external-target-once", "task_rewritten"),
    BundleRouteStateSpec("assess-external-target-once", "round_rewritten"),
    BundleRouteStateSpec("assess-external-target-once", "anchor_refreshed"),
    BundleRouteStateSpec("assess-external-target-once", "assessed", terminal=True),
)


BUNDLE_STEP_TEMPLATE_SPECS: tuple[BundleStepTemplateSpec, ...] = (
    BundleStepTemplateSpec(
        bundle_name="round-close-chain",
        from_state="blocked",
        to_state="active",
        command_name="update-round-status",
        label="blocked -> active",
        static_scalar_fields=(("status", "active"),),
        bindings=(
            BundleStepBindingSpec("round_id", "round_id"),
            BundleStepBindingSpec("reason", "reactivation_reason"),
            BundleStepBindingSpec("clear_blockers", "clear_blockers", "bool"),
        ),
    ),
    BundleStepTemplateSpec(
        bundle_name="round-close-chain",
        from_state="active",
        to_state="validation_pending",
        command_name="update-round-status",
        label="active -> validation_pending",
        static_scalar_fields=(("status", "validation_pending"),),
        bindings=(
            BundleStepBindingSpec("round_id", "round_id"),
            BundleStepBindingSpec("reason", "validation_pending_reason"),
        ),
    ),
    BundleStepTemplateSpec(
        bundle_name="round-close-chain",
        from_state="validation_pending",
        to_state="captured",
        command_name="update-round-status",
        label="validation_pending -> captured",
        static_scalar_fields=(("status", "captured"),),
        bindings=(
            BundleStepBindingSpec("round_id", "round_id"),
            BundleStepBindingSpec("reason", "captured_reason"),
            BundleStepBindingSpec("validated_by", "validated_by", "list"),
            BundleStepBindingSpec("blocker", "blocker", "list"),
            BundleStepBindingSpec("risk", "risk", "list"),
            BundleStepBindingSpec("clear_blockers", "clear_blockers", "bool"),
        ),
    ),
    BundleStepTemplateSpec(
        bundle_name="round-close-chain",
        from_state="captured",
        to_state="closed",
        command_name="update-round-status",
        label="captured -> closed",
        static_scalar_fields=(("status", "closed"),),
        bindings=(
            BundleStepBindingSpec("round_id", "round_id"),
            BundleStepBindingSpec("reason", "closed_reason"),
        ),
    ),
    BundleStepTemplateSpec(
        bundle_name="round-close-chain-then-hard-pivot",
        from_state="blocked",
        to_state="closed",
        command_name="round-close-chain",
        label="blocked -> closed",
        bindings=(
            BundleStepBindingSpec("round_id", "round_id"),
            BundleStepBindingSpec("reactivation_reason", "reactivation_reason"),
            BundleStepBindingSpec("validation_pending_reason", "validation_pending_reason"),
            BundleStepBindingSpec("captured_reason", "captured_reason"),
            BundleStepBindingSpec("closed_reason", "closed_reason"),
            BundleStepBindingSpec("validated_by", "validated_by", "list"),
            BundleStepBindingSpec("blocker", "blocker", "list"),
            BundleStepBindingSpec("risk", "close_chain_risk", "list"),
            BundleStepBindingSpec("clear_blockers", "clear_blockers", "bool"),
        ),
    ),
    BundleStepTemplateSpec(
        bundle_name="round-close-chain-then-hard-pivot",
        from_state="active",
        to_state="closed",
        command_name="round-close-chain",
        label="active -> closed",
        bindings=(
            BundleStepBindingSpec("round_id", "round_id"),
            BundleStepBindingSpec("validation_pending_reason", "validation_pending_reason"),
            BundleStepBindingSpec("captured_reason", "captured_reason"),
            BundleStepBindingSpec("closed_reason", "closed_reason"),
            BundleStepBindingSpec("validated_by", "validated_by", "list"),
            BundleStepBindingSpec("blocker", "blocker", "list"),
            BundleStepBindingSpec("risk", "close_chain_risk", "list"),
            BundleStepBindingSpec("clear_blockers", "clear_blockers", "bool"),
        ),
    ),
    BundleStepTemplateSpec(
        bundle_name="round-close-chain-then-hard-pivot",
        from_state="validation_pending",
        to_state="closed",
        command_name="round-close-chain",
        label="validation_pending -> closed",
        bindings=(
            BundleStepBindingSpec("round_id", "round_id"),
            BundleStepBindingSpec("captured_reason", "captured_reason"),
            BundleStepBindingSpec("closed_reason", "closed_reason"),
            BundleStepBindingSpec("validated_by", "validated_by", "list"),
            BundleStepBindingSpec("blocker", "blocker", "list"),
            BundleStepBindingSpec("risk", "close_chain_risk", "list"),
            BundleStepBindingSpec("clear_blockers", "clear_blockers", "bool"),
        ),
    ),
    BundleStepTemplateSpec(
        bundle_name="round-close-chain-then-hard-pivot",
        from_state="captured",
        to_state="closed",
        command_name="round-close-chain",
        label="captured -> closed",
        bindings=(
            BundleStepBindingSpec("round_id", "round_id"),
            BundleStepBindingSpec("closed_reason", "closed_reason"),
        ),
    ),
    BundleStepTemplateSpec(
        bundle_name="round-close-chain-then-hard-pivot",
        from_state="closed",
        to_state="pivoted",
        command_name="record-hard-pivot",
        label="closed -> pivoted",
        bindings=(
            BundleStepBindingSpec("previous_objective_id", "previous_objective_id"),
            BundleStepBindingSpec("title", "title"),
            BundleStepBindingSpec("summary", "summary"),
            BundleStepBindingSpec("problem", "problem"),
            BundleStepBindingSpec("success_criterion", "success_criterion", "list"),
            BundleStepBindingSpec("non_goal", "non_goal", "list"),
            BundleStepBindingSpec("why_now", "why_now"),
            BundleStepBindingSpec("phase", "phase"),
            BundleStepBindingSpec("trigger", "trigger"),
            BundleStepBindingSpec("pivot_title", "pivot_title"),
            BundleStepBindingSpec("evidence", "evidence", "list"),
            BundleStepBindingSpec("retained_decision", "retained_decision", "list"),
            BundleStepBindingSpec("invalidated_assumption", "invalidated_assumption", "list"),
            BundleStepBindingSpec("next_control_change", "next_control_change", "list"),
            BundleStepBindingSpec("risk", "objective_risk", "list"),
            BundleStepBindingSpec("path", "path", "list"),
            BundleStepBindingSpec("supersession_notes", "supersession_notes"),
        ),
    ),
    BundleStepTemplateSpec(
        bundle_name="assess-external-target-once",
        from_state="start",
        to_state="drafted",
        command_name="draft-external-target-shadow-scope",
        label="draft external target scope",
        bindings=(
            BundleStepBindingSpec("workspace_root", "workspace_root"),
            BundleStepBindingSpec("source_repo", "source_repo"),
            BundleStepBindingSpec("output", "draft_output"),
        ),
    ),
    BundleStepTemplateSpec(
        bundle_name="assess-external-target-once",
        from_state="drafted",
        to_state="round_expanded",
        command_name="rewrite-open-round",
        label="expand round for scope migration",
        static_scalar_fields=(("reason", "Temporarily expand the active round so the task contract can move from its previous scope into the external target dirty paths."),),
        static_bool_fields=(("replace_scope_paths", True),),
        bindings=(
            BundleStepBindingSpec("round_id", "round_id"),
            BundleStepBindingSpec("scope_path", "expand_round_scope_path", "list"),
        ),
    ),
    BundleStepTemplateSpec(
        bundle_name="assess-external-target-once",
        from_state="round_expanded",
        to_state="task_rewritten",
        command_name="rewrite-open-task-contract",
        label="rewrite task to external target scope",
        static_scalar_fields=(("reason", "Align the active task contract to the observed external target dirty paths before running assess-host-adoption."),),
        static_bool_fields=(
            ("replace_paths", True),
            ("replace_allowed_changes", True),
            ("replace_forbidden_changes", True),
            ("replace_completion_criteria", True),
        ),
        bindings=(
            BundleStepBindingSpec("task_contract_id", "task_contract_id"),
            BundleStepBindingSpec("summary", "task_summary"),
            BundleStepBindingSpec("intent", "task_intent"),
            BundleStepBindingSpec("path", "task_path", "list"),
            BundleStepBindingSpec("allowed_change", "task_allowed_change", "list"),
            BundleStepBindingSpec("forbidden_change", "task_forbidden_change", "list"),
            BundleStepBindingSpec("completion_criterion", "task_completion_criterion", "list"),
        ),
    ),
    BundleStepTemplateSpec(
        bundle_name="assess-external-target-once",
        from_state="task_rewritten",
        to_state="round_rewritten",
        command_name="rewrite-open-round",
        label="finalize round to external target scope",
        static_scalar_fields=(
            ("reason", "Align the active round to the observed external target dirty paths before running assess-host-adoption."),
        ),
        static_bool_fields=(
            ("replace_scope_items", True),
            ("replace_scope_paths", True),
        ),
        bindings=(
            BundleStepBindingSpec("round_id", "round_id"),
            BundleStepBindingSpec("scope_item", "round_scope_item", "list"),
            BundleStepBindingSpec("scope_path", "round_scope_path", "list"),
            BundleStepBindingSpec("deliverable", "round_deliverable"),
            BundleStepBindingSpec("validation_plan", "round_validation_plan"),
        ),
    ),
    BundleStepTemplateSpec(
        bundle_name="assess-external-target-once",
        from_state="round_rewritten",
        to_state="anchor_refreshed",
        command_name="refresh-anchor",
        label="refresh anchor to external workspace",
        bindings=(BundleStepBindingSpec("workspace_root", "workspace_root"),),
    ),
    BundleStepTemplateSpec(
        bundle_name="assess-external-target-once",
        from_state="anchor_refreshed",
        to_state="assessed",
        command_name="assess-host-adoption",
        label="assess external target",
        static_scalar_fields=(("mode", "external-target-shadow"),),
        bindings=(
            BundleStepBindingSpec("workspace_root", "workspace_root"),
            BundleStepBindingSpec("source_repo", "source_repo"),
            BundleStepBindingSpec("output", "report_output"),
        ),
    ),
)


ADJUDICATION_TARGET_RESOLUTION_SPECS: tuple[AdjudicationTargetResolutionSpec, ...] = (
    AdjudicationTargetResolutionSpec(
        "explicit_or_adjudication_objective",
        "Resolve the objective target from explicit contract input first, then fall back to the adjudication objective context.",
    ),
    AdjudicationTargetResolutionSpec(
        "explicit_round_id_or_invalidated_open_round_or_open_round_for_objective_context",
        "Resolve one open round from explicit round id, one invalidated open round, or the adjudication objective context.",
    ),
    AdjudicationTargetResolutionSpec(
        "resolve_open_task_contracts_from_explicit_ids_or_invalidated_objects",
        "Resolve open task contracts from explicit ids first, then from adjudication invalidated objects.",
    ),
    AdjudicationTargetResolutionSpec(
        "resolve_open_task_contracts_from_invalidated_objects",
        "Resolve open task contracts only from adjudication invalidated objects.",
    ),
    AdjudicationTargetResolutionSpec(
        "resolve_active_exception_contracts_from_invalidated_objects",
        "Resolve active exception contracts from adjudication invalidated objects.",
    ),
    AdjudicationTargetResolutionSpec(
        "explicit_or_adjudication_objective_and_round_close_target_context",
        "Resolve the previous objective from explicit input or adjudication context and resolve one round-close-capable target from explicit round id, invalidated objects, or that objective context.",
    ),
)


ADJUDICATION_BINDING_RESOLVER_SPECS: tuple[AdjudicationBindingResolverSpec, ...] = (
    AdjudicationBindingResolverSpec("contract_scalar", "Read one scalar value from the plan contract."),
    AdjudicationBindingResolverSpec("contract_list", "Read one list value from the plan contract."),
    AdjudicationBindingResolverSpec("contract_bool", "Read one boolean flag from the plan contract."),
    AdjudicationBindingResolverSpec(
        "contract_or_meta_scalar",
        "Read one scalar value from the plan contract, then fall back to adjudication metadata.",
    ),
    AdjudicationBindingResolverSpec(
        "contract_or_meta_list",
        "Read one list value from the plan contract, then fall back to adjudication metadata.",
    ),
    AdjudicationBindingResolverSpec(
        "exception_contract_target_ids",
        "Resolve active exception-contract ids from explicit ids or adjudication invalidated objects.",
    ),
    AdjudicationBindingResolverSpec(
        "task_contract_target_ids",
        "Resolve open task-contract ids from explicit ids or adjudication invalidated objects.",
    ),
    AdjudicationBindingResolverSpec(
        "round_target_id",
        "Resolve one open round id from explicit input, adjudication invalidated objects, or objective context.",
    ),
    AdjudicationBindingResolverSpec(
        "round_close_target_id",
        "Resolve one round-close-capable round id from explicit input, adjudication invalidated objects, or objective context.",
    ),
    AdjudicationBindingResolverSpec(
        "round_validated_by_list",
        "Resolve round validation evidence from explicit plan input or the current round validation plan.",
    ),
)


ADJUDICATION_PLAN_SIDE_EFFECT_SPECS: tuple[AdjudicationPlanSideEffectSpec, ...] = (
    AdjudicationPlanSideEffectSpec(
        "rewrite_active_objective_via_soft_pivot",
        "Rewrite one active objective line in place through the governed soft-pivot primitive.",
    ),
    AdjudicationPlanSideEffectSpec(
        "optionally_rewrite_open_rounds_for_objective_alignment",
        "Optionally rewrite the still-open round through the same governed objective-alignment path.",
    ),
    AdjudicationPlanSideEffectSpec(
        "rewrite_round_contract",
        "Rewrite one still-open round contract through the bounded round rewrite primitive.",
    ),
    AdjudicationPlanSideEffectSpec(
        "advance_round_to_closed",
        "Advance one round to closed by composing only legal round lifecycle transitions.",
    ),
    AdjudicationPlanSideEffectSpec(
        "rewrite_task_contracts",
        "Rewrite one or more still-open task contracts through the bounded task rewrite primitive.",
    ),
    AdjudicationPlanSideEffectSpec(
        "invalidate_open_task_contracts",
        "Invalidate one or more still-open task contracts from adjudication invalidation context.",
    ),
    AdjudicationPlanSideEffectSpec(
        "abandon_open_task_contracts",
        "Abandon one or more still-open task contracts from adjudication invalidation context.",
    ),
    AdjudicationPlanSideEffectSpec(
        "retire_active_exception_contracts",
        "Retire one or more active exception contracts from adjudication invalidation context.",
    ),
    AdjudicationPlanSideEffectSpec(
        "invalidate_active_exception_contracts",
        "Invalidate one or more active exception contracts from adjudication invalidation context.",
    ),
    AdjudicationPlanSideEffectSpec(
        "enter_execution_phase",
        "Enter execution through the governed phase transition surface.",
    ),
    AdjudicationPlanSideEffectSpec(
        "bootstrap_bounded_round",
        "Bootstrap one bounded execution round through governed round-open semantics.",
    ),
    AdjudicationPlanSideEffectSpec(
        "leave_execution_phase",
        "Leave execution through the governed phase transition surface.",
    ),
    AdjudicationPlanSideEffectSpec(
        "rewrite_open_rounds_for_phase_fallback",
        "Rewrite still-open round contracts through the governed phase fallback surface.",
    ),
    AdjudicationPlanSideEffectSpec(
        "close_round_before_hard_pivot",
        "Close one predecessor round through governed bundle semantics before the hard pivot runs.",
    ),
    AdjudicationPlanSideEffectSpec(
        "record_hard_pivot_after_round_close",
        "Record one hard pivot after the predecessor round has been durably closed through the bounded bundle path.",
    ),
)


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
    GuardSpec("no_open_task_contracts_for_round", "no draft or active task contract remains attached to the round before it leaves open execution"),
    GuardSpec("task_contract_round_is_open", "round `{round_id}` exists and remains open for task attachment", ("round_id",), "target round exists and remains open for task attachment"),
    GuardSpec("task_contract_objective_alignment_preserved", "task-contract objective linkage matches the referenced round"),
    GuardSpec("task_contract_intent_present", "task intent is explicit"),
    GuardSpec("task_contract_paths_present", "task scope paths are explicit"),
    GuardSpec("task_contract_paths_within_round_scope", "task scope paths stay inside the round scope"),
    GuardSpec("task_contract_change_contract_present", "allowed changes, forbidden changes, and completion criteria are all present"),
    GuardSpec("task_contract_exists", "task contract `{task_contract_id}` exists", ("task_contract_id",), "task contract exists"),
    GuardSpec(
        "task_contract_status_transition_legal",
        "task-contract transition `{previous_status} -> {next_status}` is legal",
        ("previous_status", "next_status"),
        "task-contract status transition is legal",
    ),
    GuardSpec("task_contract_resolution_present_when_completed", "completed task-contract transitions include at least one resolution record"),
    GuardSpec("task_contract_remains_open", "task contract `{task_contract_id}` exists and remains open", ("task_contract_id",), "task contract exists and remains open"),
    GuardSpec("task_contract_rewrite_reason_present", "task-contract rewrite reason is explicit"),
    GuardSpec("task_contract_rewritten_contract_stays_complete", "rewritten task contract still has intent, path scope, allowed changes, forbidden changes, and completion criteria"),
    GuardSpec("task_contract_identity_preserved", "task-contract identity is preserved while contract content is rewritten"),
    GuardSpec("task_contract_rewrite_produces_material_change", "task-contract rewrite produces at least one material contract change"),
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
    GuardSpec("no_open_task_contracts_for_objective", "no draft or active task contract remains attached to the objective"),
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
    GuardSpec("no_open_task_contracts_on_previous_objective", "no draft or active task contract remains attached to the previous objective"),
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
        executor_supported=True,
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
            "no_open_task_contracts_for_objective",
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
        executor_supported=True,
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
        side_effect_codes=(
            "rewrite_active_objective_in_place",
            "record_pivot_lineage",
            "refresh_active_objective_projection",
            "refresh_pivot_log_projection",
            "force_explicit_round_review_path",
        ),
        durable_owners=("memory:objective", "memory:pivot"),
        projection_owners=("control:active-objective", "control:pivot-log"),
    ),
    TransitionCommandSpec(
        "record-hard-pivot",
        "objective-line",
        executor_supported=True,
        implementation_status="implemented",
        required_inputs=("project_id", "previous_objective_id", "title", "problem", "success_criteria", "non_goals", "phase", "trigger"),
        guard_codes=(
            "previous_objective_is_active",
            "new_objective_fields_present",
            "previous_objective_matches_control_truth",
            "no_open_rounds_on_previous_objective",
            "no_open_task_contracts_on_previous_objective",
        ),
        write_targets=("durable:objective", "durable:pivot", "control:active-objective", "control:pivot-log", "memory:transition-event"),
        side_effect_codes=(
            "supersede_previous_objective",
            "activate_new_objective_line",
            "record_pivot_lineage",
            "refresh_active_objective_projection",
            "refresh_pivot_log_projection",
            "review_or_resolve_stale_exception_contracts",
        ),
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
        side_effect_codes=(
            "rewrite_objective_phase",
            "refresh_active_objective_projection",
            "optionally_bootstrap_execution_round",
            "optionally_rewrite_open_rounds",
        ),
        durable_owners=("memory:objective",),
        projection_owners=("control:active-objective", "control:active-round"),
    ),
    TransitionCommandSpec(
        "open-round",
        "round",
        executor_supported=True,
        implementation_status="implemented",
        required_inputs=("project_id", "title", "scope_item", "deliverable", "validation_plan"),
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
            "no_open_task_contracts_for_round",
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
        mutable_field_codes=(
            "title",
            "summary",
            "scope_items",
            "deliverable",
            "validation_plan",
            "risks",
            "blockers",
            "status_notes",
            "paths",
        ),
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
        "open-task-contract",
        "task-contract",
        executor_supported=True,
        implementation_status="implemented",
        required_inputs=(
            "project_id",
            "round_id",
            "title",
            "intent",
            "paths",
            "allowed_changes",
            "forbidden_changes",
            "completion_criteria",
        ),
        guard_codes=(
            "task_contract_round_is_open",
            "task_contract_objective_alignment_preserved",
            "task_contract_intent_present",
            "task_contract_paths_present",
            "task_contract_paths_within_round_scope",
            "task_contract_change_contract_present",
        ),
        write_targets=("durable:task-contract", "memory:transition-event"),
        side_effect_codes=("record_task_contract", "preserve_round_task_governance_boundary"),
        durable_owners=("memory:task-contract",),
    ),
    TransitionCommandSpec(
        "update-task-contract-status",
        "task-contract",
        executor_supported=True,
        implementation_status="implemented",
        required_inputs=("project_id", "task_contract_id", "status", "reason"),
        guard_codes=(
            "task_contract_exists",
            "task_contract_status_transition_legal",
            "task_contract_resolution_present_when_completed",
        ),
        write_targets=("durable:task-contract", "memory:transition-event"),
        side_effect_codes=("advance_task_contract_lifecycle_state", "record_task_contract_completion_or_resolution"),
        durable_owners=("memory:task-contract",),
    ),
    TransitionCommandSpec(
        "rewrite-open-task-contract",
        "task-contract",
        executor_supported=True,
        implementation_status="implemented",
        required_inputs=("project_id", "task_contract_id", "reason", "mutable_fields"),
        mutable_field_codes=(
            "title",
            "summary",
            "intent",
            "allowed_changes",
            "forbidden_changes",
            "completion_criteria",
            "risks",
            "status_notes",
            "paths",
        ),
        guard_codes=(
            "task_contract_remains_open",
            "task_contract_rewrite_reason_present",
            "task_contract_rewritten_contract_stays_complete",
            "task_contract_identity_preserved",
            "task_contract_paths_within_round_scope",
            "task_contract_rewrite_produces_material_change",
        ),
        write_targets=("durable:task-contract", "memory:transition-event"),
        side_effect_codes=("rewrite_open_task_contract", "preserve_round_task_governance_boundary"),
        durable_owners=("memory:task-contract",),
    ),
    TransitionCommandSpec(
        "activate-exception-contract",
        "exception-contract",
        executor_supported=True,
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
        executor_supported=True,
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
        "draft-external-target-shadow-scope",
        "anchor-maintenance",
        executor_supported=True,
        implementation_status="implemented",
        required_inputs=("project_id", "workspace_root"),
        guard_codes=("workspace_locator_available", "live_workspace_available", "active_objective_available"),
        write_targets=("artifact:shadow-adoption-report",),
        side_effect_codes=("render_external_target_shadow_scope_draft",),
        artifact_owners=("artifact:shadow-adoption-report",),
        live_inspection_owners=("workspace:git-status",),
        emits_transition_event=False,
    ),
    TransitionCommandSpec(
        "assess-host-adoption",
        "anchor-maintenance",
        executor_supported=True,
        implementation_status="implemented",
        required_inputs=("project_id",),
        guard_codes=("workspace_locator_available", "live_workspace_available", "active_objective_available"),
        write_targets=("artifact:shadow-adoption-report",),
        side_effect_codes=("render_shadow_adoption_report",),
        artifact_owners=("artifact:shadow-adoption-report",),
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
        plan_type="rewrite-active-objective-via-soft-pivot",
        compiled_commands=("record-soft-pivot",),
        requires_adjudication_fields=("trigger", "change_summary", "identity_rationale"),
        target_resolution="explicit_or_adjudication_objective",
        side_effect_codes=("rewrite_active_objective_via_soft_pivot", "optionally_rewrite_open_rounds_for_objective_alignment"),
        payload_templates=(
            AdjudicationPayloadTemplateSpec(
                command_name="record-soft-pivot",
                bindings=(
                    AdjudicationPayloadBindingSpec("objective_id", "contract_or_meta_scalar", ("objective_id",)),
                    AdjudicationPayloadBindingSpec("trigger", "contract_scalar", ("trigger",), required=True),
                    AdjudicationPayloadBindingSpec("change_summary", "contract_scalar", ("change_summary",), required=True),
                    AdjudicationPayloadBindingSpec(
                        "identity_rationale",
                        "contract_scalar",
                        ("identity_rationale",),
                        required=True,
                    ),
                    AdjudicationPayloadBindingSpec("pivot_title", "contract_scalar", ("pivot_title",)),
                    AdjudicationPayloadBindingSpec("title", "contract_scalar", ("title",)),
                    AdjudicationPayloadBindingSpec("summary", "contract_scalar", ("summary",)),
                    AdjudicationPayloadBindingSpec("problem", "contract_scalar", ("problem",)),
                    AdjudicationPayloadBindingSpec("success_criterion", "contract_list", ("success_criterion",)),
                    AdjudicationPayloadBindingSpec("non_goal", "contract_list", ("non_goal",)),
                    AdjudicationPayloadBindingSpec("why_now", "contract_scalar", ("why_now",)),
                    AdjudicationPayloadBindingSpec("phase", "contract_scalar", ("phase",)),
                    AdjudicationPayloadBindingSpec("risk", "contract_list", ("risk",)),
                    AdjudicationPayloadBindingSpec("path", "contract_list", ("path",)),
                    AdjudicationPayloadBindingSpec("supersession_notes", "contract_scalar", ("supersession_notes",)),
                    AdjudicationPayloadBindingSpec("evidence", "contract_list", ("evidence",)),
                    AdjudicationPayloadBindingSpec(
                        "retained_decision",
                        "contract_list",
                        ("retained_decision",),
                    ),
                    AdjudicationPayloadBindingSpec(
                        "invalidated_assumption",
                        "contract_list",
                        ("invalidated_assumption",),
                    ),
                    AdjudicationPayloadBindingSpec(
                        "next_control_change",
                        "contract_list",
                        ("next_control_change",),
                    ),
                    AdjudicationPayloadBindingSpec("rewrite_open_round", "contract_bool", ("rewrite_open_round",)),
                    AdjudicationPayloadBindingSpec("round_title", "contract_scalar", ("round_title",)),
                    AdjudicationPayloadBindingSpec("round_summary", "contract_scalar", ("round_summary",)),
                    AdjudicationPayloadBindingSpec("round_scope_item", "contract_list", ("round_scope_item",)),
                    AdjudicationPayloadBindingSpec("round_scope_path", "contract_list", ("round_scope_path",)),
                    AdjudicationPayloadBindingSpec("round_deliverable", "contract_scalar", ("round_deliverable",)),
                    AdjudicationPayloadBindingSpec(
                        "round_validation_plan",
                        "contract_scalar",
                        ("round_validation_plan",),
                    ),
                    AdjudicationPayloadBindingSpec("round_risk", "contract_list", ("round_risk",)),
                    AdjudicationPayloadBindingSpec("round_blocker", "contract_list", ("round_blocker",)),
                    AdjudicationPayloadBindingSpec("round_status_note", "contract_list", ("round_status_note",)),
                    AdjudicationPayloadBindingSpec(
                        "replace_round_scope_items",
                        "contract_bool",
                        ("replace_round_scope_items",),
                    ),
                    AdjudicationPayloadBindingSpec(
                        "replace_round_scope_paths",
                        "contract_bool",
                        ("replace_round_scope_paths",),
                    ),
                    AdjudicationPayloadBindingSpec(
                        "replace_round_risks",
                        "contract_bool",
                        ("replace_round_risks",),
                    ),
                    AdjudicationPayloadBindingSpec(
                        "replace_round_blockers",
                        "contract_bool",
                        ("replace_round_blockers",),
                    ),
                ),
            ),
        ),
    ),
    AdjudicationPlanSpec(
        plan_type="rewrite-open-round-then-close-chain",
        compiled_commands=("rewrite-open-round", "round-close-chain"),
        requires_adjudication_fields=("rewrite_reason", "validation_pending_reason", "captured_reason", "closed_reason"),
        target_resolution="explicit_round_id_or_invalidated_open_round_or_open_round_for_objective_context",
        side_effect_codes=("rewrite_round_contract", "advance_round_to_closed"),
        payload_templates=(
            AdjudicationPayloadTemplateSpec(
                command_name="rewrite-open-round",
                bindings=(
                    AdjudicationPayloadBindingSpec("round_id", "round_target_id", ("round_id",), required=True),
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
                    AdjudicationPayloadBindingSpec("round_id", "round_target_id", ("round_id",), required=True),
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
        plan_type="rewrite-open-task-contracts",
        compiled_commands=("rewrite-open-task-contract",),
        requires_adjudication_fields=("rewrite_reason",),
        target_resolution="resolve_open_task_contracts_from_explicit_ids_or_invalidated_objects",
        side_effect_codes=("rewrite_task_contracts",),
        payload_templates=(
            AdjudicationPayloadTemplateSpec(
                command_name="rewrite-open-task-contract",
                bindings=(
                    AdjudicationPayloadBindingSpec(
                        "task_contract_id",
                        "task_contract_target_ids",
                        ("task_contract_id", "task_contract_ids"),
                        required=True,
                        fanout=True,
                    ),
                    AdjudicationPayloadBindingSpec("reason", "contract_scalar", ("rewrite_reason",), required=True),
                    AdjudicationPayloadBindingSpec("title", "contract_scalar", ("title",)),
                    AdjudicationPayloadBindingSpec("summary", "contract_scalar", ("summary",)),
                    AdjudicationPayloadBindingSpec("intent", "contract_scalar", ("intent",)),
                    AdjudicationPayloadBindingSpec("allowed_change", "contract_list", ("allowed_change",)),
                    AdjudicationPayloadBindingSpec("forbidden_change", "contract_list", ("forbidden_change",)),
                    AdjudicationPayloadBindingSpec("completion_criterion", "contract_list", ("completion_criterion",)),
                    AdjudicationPayloadBindingSpec("risk", "contract_list", ("risk",)),
                    AdjudicationPayloadBindingSpec("status_note", "contract_list", ("status_note",)),
                    AdjudicationPayloadBindingSpec("path", "contract_list", ("path",)),
                    AdjudicationPayloadBindingSpec("replace_allowed_changes", "contract_bool", ("replace_allowed_changes",)),
                    AdjudicationPayloadBindingSpec("replace_forbidden_changes", "contract_bool", ("replace_forbidden_changes",)),
                    AdjudicationPayloadBindingSpec(
                        "replace_completion_criteria",
                        "contract_bool",
                        ("replace_completion_criteria",),
                    ),
                    AdjudicationPayloadBindingSpec("replace_risks", "contract_bool", ("replace_risks",)),
                    AdjudicationPayloadBindingSpec("replace_paths", "contract_bool", ("replace_paths",)),
                ),
            ),
        ),
    ),
    AdjudicationPlanSpec(
        plan_type="invalidate-invalidated-task-contracts",
        compiled_commands=("update-task-contract-status",),
        requires_adjudication_fields=("Objects Invalidated", "reason"),
        target_resolution="resolve_open_task_contracts_from_invalidated_objects",
        side_effect_codes=("invalidate_open_task_contracts",),
        payload_templates=(
            AdjudicationPayloadTemplateSpec(
                command_name="update-task-contract-status",
                static_scalar_fields=(("status", "invalidated"),),
                bindings=(
                    AdjudicationPayloadBindingSpec(
                        "task_contract_id",
                        "task_contract_target_ids",
                        ("task_contract_id", "task_contract_ids"),
                        required=True,
                        fanout=True,
                    ),
                    AdjudicationPayloadBindingSpec("reason", "contract_scalar", ("reason",), required=True),
                    AdjudicationPayloadBindingSpec("risk", "contract_list", ("risk",)),
                    AdjudicationPayloadBindingSpec("status_note", "contract_list", ("status_note",)),
                ),
            ),
        ),
    ),
    AdjudicationPlanSpec(
        plan_type="abandon-invalidated-task-contracts",
        compiled_commands=("update-task-contract-status",),
        requires_adjudication_fields=("Objects Invalidated", "reason"),
        target_resolution="resolve_open_task_contracts_from_invalidated_objects",
        side_effect_codes=("abandon_open_task_contracts",),
        payload_templates=(
            AdjudicationPayloadTemplateSpec(
                command_name="update-task-contract-status",
                static_scalar_fields=(("status", "abandoned"),),
                bindings=(
                    AdjudicationPayloadBindingSpec(
                        "task_contract_id",
                        "task_contract_target_ids",
                        ("task_contract_id", "task_contract_ids"),
                        required=True,
                        fanout=True,
                    ),
                    AdjudicationPayloadBindingSpec("reason", "contract_scalar", ("reason",), required=True),
                    AdjudicationPayloadBindingSpec("risk", "contract_list", ("risk",)),
                    AdjudicationPayloadBindingSpec("status_note", "contract_list", ("status_note",)),
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
    AdjudicationPlanSpec(
        plan_type="leave-execution-with-round-rewrite",
        compiled_commands=("set-phase",),
        requires_adjudication_fields=("reason", "phase"),
        target_resolution="explicit_or_adjudication_objective",
        side_effect_codes=("leave_execution_phase", "rewrite_open_rounds_for_phase_fallback"),
        payload_templates=(
            AdjudicationPayloadTemplateSpec(
                command_name="set-phase",
                static_bool_fields=(("rewrite_open_round", True),),
                bindings=(
                    AdjudicationPayloadBindingSpec("objective_id", "contract_or_meta_scalar", ("objective_id",)),
                    AdjudicationPayloadBindingSpec("phase", "contract_scalar", ("phase",), required=True),
                    AdjudicationPayloadBindingSpec("reason", "contract_scalar", ("reason",), required=True),
                    AdjudicationPayloadBindingSpec("evidence", "contract_list", ("evidence",)),
                    AdjudicationPayloadBindingSpec(
                        "scope_review_note",
                        "contract_list",
                        ("scope_review_note",),
                    ),
                    AdjudicationPayloadBindingSpec("round_title", "contract_scalar", ("round_title",)),
                    AdjudicationPayloadBindingSpec("round_summary", "contract_scalar", ("round_summary",)),
                    AdjudicationPayloadBindingSpec(
                        "round_scope_item",
                        "contract_list",
                        ("round_scope_item",),
                    ),
                    AdjudicationPayloadBindingSpec(
                        "round_scope_path",
                        "contract_list",
                        ("round_scope_path",),
                    ),
                    AdjudicationPayloadBindingSpec(
                        "round_deliverable",
                        "contract_scalar",
                        ("round_deliverable",),
                    ),
                    AdjudicationPayloadBindingSpec(
                        "round_validation_plan",
                        "contract_scalar",
                        ("round_validation_plan",),
                    ),
                    AdjudicationPayloadBindingSpec("round_risk", "contract_list", ("round_risk",)),
                    AdjudicationPayloadBindingSpec("round_blocker", "contract_list", ("round_blocker",)),
                    AdjudicationPayloadBindingSpec(
                        "round_status_note",
                        "contract_scalar",
                        ("round_status_note",),
                    ),
                    AdjudicationPayloadBindingSpec(
                        "replace_round_scope_items",
                        "contract_bool",
                        ("replace_round_scope_items",),
                    ),
                    AdjudicationPayloadBindingSpec(
                        "replace_round_scope_paths",
                        "contract_bool",
                        ("replace_round_scope_paths",),
                    ),
                    AdjudicationPayloadBindingSpec(
                        "replace_round_risks",
                        "contract_bool",
                        ("replace_round_risks",),
                    ),
                    AdjudicationPayloadBindingSpec(
                        "replace_round_blockers",
                        "contract_bool",
                        ("replace_round_blockers",),
                    ),
                ),
            ),
        ),
    ),
    AdjudicationPlanSpec(
        plan_type="close-round-and-record-hard-pivot",
        compiled_commands=("round-close-chain-then-hard-pivot",),
        requires_adjudication_fields=(
            "title",
            "problem",
            "success_criterion",
            "non_goal",
            "why_now",
            "phase",
            "trigger",
            "validation_pending_reason",
            "captured_reason",
            "closed_reason",
        ),
        target_resolution="explicit_or_adjudication_objective_and_round_close_target_context",
        side_effect_codes=("close_round_before_hard_pivot", "record_hard_pivot_after_round_close"),
        payload_templates=(
            AdjudicationPayloadTemplateSpec(
                command_name="round-close-chain-then-hard-pivot",
                bindings=(
                    AdjudicationPayloadBindingSpec("round_id", "round_close_target_id", ("round_id",), required=True),
                    AdjudicationPayloadBindingSpec(
                        "previous_objective_id",
                        "contract_or_meta_scalar",
                        ("previous_objective_id", "objective_id"),
                        required=True,
                    ),
                    AdjudicationPayloadBindingSpec(
                        "reactivation_reason",
                        "contract_scalar",
                        ("reactivation_reason",),
                    ),
                    AdjudicationPayloadBindingSpec(
                        "validation_pending_reason",
                        "contract_scalar",
                        ("validation_pending_reason",),
                        required=True,
                    ),
                    AdjudicationPayloadBindingSpec(
                        "captured_reason",
                        "contract_scalar",
                        ("captured_reason",),
                        required=True,
                    ),
                    AdjudicationPayloadBindingSpec(
                        "closed_reason",
                        "contract_scalar",
                        ("closed_reason",),
                        required=True,
                    ),
                    AdjudicationPayloadBindingSpec("validated_by", "round_validated_by_list", ("validated_by",)),
                    AdjudicationPayloadBindingSpec("clear_blockers", "contract_bool", ("clear_blockers",)),
                    AdjudicationPayloadBindingSpec("blocker", "contract_list", ("close_chain_blocker",)),
                    AdjudicationPayloadBindingSpec("close_chain_risk", "contract_list", ("close_chain_risk",)),
                    AdjudicationPayloadBindingSpec("title", "contract_scalar", ("title",), required=True),
                    AdjudicationPayloadBindingSpec("summary", "contract_scalar", ("summary",)),
                    AdjudicationPayloadBindingSpec("problem", "contract_scalar", ("problem",), required=True),
                    AdjudicationPayloadBindingSpec("success_criterion", "contract_list", ("success_criterion",), required=True),
                    AdjudicationPayloadBindingSpec("non_goal", "contract_list", ("non_goal",), required=True),
                    AdjudicationPayloadBindingSpec("why_now", "contract_scalar", ("why_now",), required=True),
                    AdjudicationPayloadBindingSpec("phase", "contract_scalar", ("phase",), required=True),
                    AdjudicationPayloadBindingSpec("trigger", "contract_scalar", ("trigger",), required=True),
                    AdjudicationPayloadBindingSpec("pivot_title", "contract_scalar", ("pivot_title",)),
                    AdjudicationPayloadBindingSpec("evidence", "contract_list", ("evidence",)),
                    AdjudicationPayloadBindingSpec("retained_decision", "contract_list", ("retained_decision",)),
                    AdjudicationPayloadBindingSpec("invalidated_assumption", "contract_list", ("invalidated_assumption",)),
                    AdjudicationPayloadBindingSpec("next_control_change", "contract_list", ("next_control_change",)),
                    AdjudicationPayloadBindingSpec("objective_risk", "contract_list", ("risk",)),
                    AdjudicationPayloadBindingSpec("path", "contract_list", ("path",)),
                    AdjudicationPayloadBindingSpec("supersession_notes", "contract_scalar", ("supersession_notes",)),
                ),
            ),
        ),
    ),
)


WRITE_TARGET_SPEC_BY_NAME = {spec.target: spec for spec in WRITE_TARGET_SPECS}
TRANSITION_SIDE_EFFECT_SPEC_BY_CODE = {spec.code: spec for spec in TRANSITION_SIDE_EFFECT_SPECS}
GUARD_SPEC_BY_CODE = {spec.code: spec for spec in GUARD_SPECS}
COMMAND_SPEC_BY_NAME = {spec.name: spec for spec in TRANSITION_COMMAND_SPECS}
PLAN_SPEC_BY_TYPE = {spec.plan_type: spec for spec in ADJUDICATION_PLAN_SPECS}
COMMAND_MUTABLE_FIELDS_BY_COMMAND: dict[str, tuple[CommandMutableFieldSpec, ...]] = {}
for _mutable_field_spec in COMMAND_MUTABLE_FIELD_SPECS:
    COMMAND_MUTABLE_FIELDS_BY_COMMAND.setdefault(_mutable_field_spec.command_name, tuple())
    COMMAND_MUTABLE_FIELDS_BY_COMMAND[_mutable_field_spec.command_name] = (
        *COMMAND_MUTABLE_FIELDS_BY_COMMAND[_mutable_field_spec.command_name],
        _mutable_field_spec,
    )
COMMAND_MUTABLE_FIELD_SPEC_BY_COMMAND_AND_CODE = {
    (spec.command_name, spec.code): spec for spec in COMMAND_MUTABLE_FIELD_SPECS
}
COMMAND_EXECUTOR_FIELDS_BY_COMMAND: dict[str, tuple[CommandExecutorFieldSpec, ...]] = {}
for _executor_field_spec in COMMAND_EXECUTOR_FIELD_SPECS:
    COMMAND_EXECUTOR_FIELDS_BY_COMMAND.setdefault(_executor_field_spec.command_name, tuple())
    COMMAND_EXECUTOR_FIELDS_BY_COMMAND[_executor_field_spec.command_name] = (
        *COMMAND_EXECUTOR_FIELDS_BY_COMMAND[_executor_field_spec.command_name],
        _executor_field_spec,
    )
BUNDLE_EXECUTOR_FIELDS_BY_BUNDLE: dict[str, tuple[BundleExecutorFieldSpec, ...]] = {}
for _bundle_field_spec in BUNDLE_EXECUTOR_FIELD_SPECS:
    BUNDLE_EXECUTOR_FIELDS_BY_BUNDLE.setdefault(_bundle_field_spec.bundle_name, tuple())
    BUNDLE_EXECUTOR_FIELDS_BY_BUNDLE[_bundle_field_spec.bundle_name] = (
        *BUNDLE_EXECUTOR_FIELDS_BY_BUNDLE[_bundle_field_spec.bundle_name],
        _bundle_field_spec,
    )
BUNDLE_GOVERNANCE_SPEC_BY_NAME = {spec.name: spec for spec in BUNDLE_GOVERNANCE_SPECS}
BUNDLE_STATE_RESOLVER_SPEC_BY_NAME = {spec.name: spec for spec in BUNDLE_STATE_RESOLVER_SPECS}
BUNDLE_ROUTE_STATES_BY_BUNDLE: dict[str, tuple[BundleRouteStateSpec, ...]] = {}
for _bundle_route_state_spec in BUNDLE_ROUTE_STATE_SPECS:
    BUNDLE_ROUTE_STATES_BY_BUNDLE.setdefault(_bundle_route_state_spec.bundle_name, tuple())
    BUNDLE_ROUTE_STATES_BY_BUNDLE[_bundle_route_state_spec.bundle_name] = (
        *BUNDLE_ROUTE_STATES_BY_BUNDLE[_bundle_route_state_spec.bundle_name],
        _bundle_route_state_spec,
    )
BUNDLE_ROUTE_STATE_BY_BUNDLE_AND_STATE = {
    (spec.bundle_name, spec.state): spec for spec in BUNDLE_ROUTE_STATE_SPECS
}
BUNDLE_STEP_TEMPLATES_BY_BUNDLE: dict[str, tuple[BundleStepTemplateSpec, ...]] = {}
for _bundle_step_template_spec in BUNDLE_STEP_TEMPLATE_SPECS:
    BUNDLE_STEP_TEMPLATES_BY_BUNDLE.setdefault(_bundle_step_template_spec.bundle_name, tuple())
    BUNDLE_STEP_TEMPLATES_BY_BUNDLE[_bundle_step_template_spec.bundle_name] = (
        *BUNDLE_STEP_TEMPLATES_BY_BUNDLE[_bundle_step_template_spec.bundle_name],
        _bundle_step_template_spec,
    )
BUNDLE_STEP_TEMPLATE_BY_BUNDLE_AND_FROM_STATE = {
    (spec.bundle_name, spec.from_state): spec for spec in BUNDLE_STEP_TEMPLATE_SPECS
}
ADJUDICATION_TARGET_RESOLUTION_SPEC_BY_NAME = {
    spec.name: spec for spec in ADJUDICATION_TARGET_RESOLUTION_SPECS
}
ADJUDICATION_BINDING_RESOLVER_SPEC_BY_NAME = {
    spec.name: spec for spec in ADJUDICATION_BINDING_RESOLVER_SPECS
}
ADJUDICATION_PLAN_SIDE_EFFECT_SPEC_BY_CODE = {
    spec.code: spec for spec in ADJUDICATION_PLAN_SIDE_EFFECT_SPECS
}


def _owner_labels_for_command(spec: TransitionCommandSpec, owner_bucket: str) -> set[str]:
    if owner_bucket == "durable":
        return set(spec.durable_owners)
    if owner_bucket == "projection":
        return set(spec.projection_owners)
    if owner_bucket == "artifact":
        return set(spec.artifact_owners)
    return set()


def validate_transition_command_semantics(spec: TransitionCommandSpec) -> None:
    declared_write_targets = set(spec.write_targets)
    non_event_write_targets = {
        target
        for target in declared_write_targets
        if WRITE_TARGET_SPEC_BY_NAME[target].surface != "event"
    }
    covered_write_targets: set[str] = set()

    covered_owner_labels = {
        "durable": set(),
        "projection": set(),
        "artifact": set(),
        "live inspection": set(),
    }

    for target in declared_write_targets:
        target_spec = WRITE_TARGET_SPEC_BY_NAME[target]
        expected_owner_labels = set(target_spec.owner_labels)
        command_owner_labels = _owner_labels_for_command(spec, target_spec.owner_bucket)
        if not expected_owner_labels.issubset(command_owner_labels):
            missing = ", ".join(sorted(expected_owner_labels - command_owner_labels))
            raise SystemExit(
                f"transition command `{spec.name}` writes `{target}` but does not declare owner labels `{missing}`"
            )

    for code in spec.side_effect_codes:
        side_effect = TRANSITION_SIDE_EFFECT_SPEC_BY_CODE[code]
        if not set(side_effect.write_targets).issubset(declared_write_targets):
            unsupported_targets = ", ".join(sorted(set(side_effect.write_targets) - declared_write_targets))
            raise SystemExit(
                f"transition command `{spec.name}` side effect `{code}` reaches undeclared write targets: {unsupported_targets}"
            )
        covered_write_targets.update(side_effect.write_targets)
        covered_owner_labels["durable"].update(side_effect.durable_owners)
        covered_owner_labels["projection"].update(side_effect.projection_owners)
        covered_owner_labels["artifact"].update(side_effect.artifact_owners)
        covered_owner_labels["live inspection"].update(side_effect.live_inspection_owners)

        if not set(side_effect.durable_owners).issubset(spec.durable_owners):
            raise SystemExit(
                f"transition command `{spec.name}` side effect `{code}` reaches undeclared durable owners"
            )
        if not set(side_effect.projection_owners).issubset(spec.projection_owners):
            raise SystemExit(
                f"transition command `{spec.name}` side effect `{code}` reaches undeclared projection owners"
            )
        if not set(side_effect.artifact_owners).issubset(spec.artifact_owners):
            raise SystemExit(
                f"transition command `{spec.name}` side effect `{code}` reaches undeclared artifact owners"
            )
        if not set(side_effect.live_inspection_owners).issubset(spec.live_inspection_owners):
            raise SystemExit(
                f"transition command `{spec.name}` side effect `{code}` reaches undeclared live inspection owners"
            )

    uncovered_write_targets = sorted(non_event_write_targets - covered_write_targets)
    if uncovered_write_targets:
        raise SystemExit(
            f"transition command `{spec.name}` does not cover non-event write targets through side-effect semantics: {', '.join(uncovered_write_targets)}"
        )

    for owner_bucket, command_owner_labels in [
        ("durable", set(spec.durable_owners)),
        ("projection", set(spec.projection_owners)),
        ("artifact", set(spec.artifact_owners)),
        ("live inspection", set(spec.live_inspection_owners)),
    ]:
        uncovered_labels = sorted(command_owner_labels - covered_owner_labels[owner_bucket])
        if uncovered_labels:
            raise SystemExit(
                f"transition command `{spec.name}` does not cover {owner_bucket} owners through side-effect semantics: {', '.join(uncovered_labels)}"
            )


def validate_transition_specs() -> None:
    valid_implementation_statuses = {"implemented", "partial", "planned"}
    valid_write_target_surfaces = {"durable", "projection", "current", "artifact", "snapshot", "event"}
    valid_owner_buckets = {"durable", "projection", "artifact", "none"}
    valid_mutable_value_kinds = {"scalar", "list"}
    valid_mutable_storage_kinds = {"meta_scalar", "meta_list", "section_text", "section_bullets"}
    valid_mutation_modes = {"replace_if_present", "merge_unique", "append_paragraphs"}
    valid_executor_value_kinds = {"scalar", "list", "bool"}
    owner_label_sets = {
        "durable": SUPPORTED_DURABLE_OWNER_LABELS,
        "projection": SUPPORTED_PROJECTION_OWNER_LABELS,
        "artifact": SUPPORTED_ARTIFACT_OWNER_LABELS,
        "live inspection": SUPPORTED_LIVE_INSPECTION_OWNER_LABELS,
    }
    if len(WRITE_TARGET_SPEC_BY_NAME) != len(WRITE_TARGET_SPECS):
        raise SystemExit("duplicate write targets found in transition registry")
    if len(TRANSITION_SIDE_EFFECT_SPEC_BY_CODE) != len(TRANSITION_SIDE_EFFECT_SPECS):
        raise SystemExit("duplicate transition side-effect codes found in transition registry")
    if len(GUARD_SPEC_BY_CODE) != len(GUARD_SPECS):
        raise SystemExit("duplicate guard codes found in transition registry")
    if len(COMMAND_SPEC_BY_NAME) != len(TRANSITION_COMMAND_SPECS):
        raise SystemExit("duplicate transition command names found in transition registry")
    if len(PLAN_SPEC_BY_TYPE) != len(ADJUDICATION_PLAN_SPECS):
        raise SystemExit("duplicate adjudication plan types found in transition registry")
    if len(ADJUDICATION_TARGET_RESOLUTION_SPEC_BY_NAME) != len(ADJUDICATION_TARGET_RESOLUTION_SPECS):
        raise SystemExit("duplicate adjudication target-resolution names found in transition registry")
    if len(ADJUDICATION_BINDING_RESOLVER_SPEC_BY_NAME) != len(ADJUDICATION_BINDING_RESOLVER_SPECS):
        raise SystemExit("duplicate adjudication binding resolver names found in transition registry")
    if len(ADJUDICATION_PLAN_SIDE_EFFECT_SPEC_BY_CODE) != len(ADJUDICATION_PLAN_SIDE_EFFECT_SPECS):
        raise SystemExit("duplicate adjudication plan side-effect codes found in transition registry")
    if len(COMMAND_MUTABLE_FIELD_SPEC_BY_COMMAND_AND_CODE) != len(COMMAND_MUTABLE_FIELD_SPECS):
        raise SystemExit("duplicate command mutable-field codes found in transition registry")
    if sum(len(specs) for specs in BUNDLE_EXECUTOR_FIELDS_BY_BUNDLE.values()) != len(BUNDLE_EXECUTOR_FIELD_SPECS):
        raise SystemExit("duplicate bundle executor payload-field semantics found in transition registry")
    if len(BUNDLE_GOVERNANCE_SPEC_BY_NAME) != len(BUNDLE_GOVERNANCE_SPECS):
        raise SystemExit("duplicate bundle governance names found in transition registry")
    if len(BUNDLE_STATE_RESOLVER_SPEC_BY_NAME) != len(BUNDLE_STATE_RESOLVER_SPECS):
        raise SystemExit("duplicate bundle state resolver names found in transition registry")
    if len(BUNDLE_ROUTE_STATE_BY_BUNDLE_AND_STATE) != len(BUNDLE_ROUTE_STATE_SPECS):
        raise SystemExit("duplicate bundle route states found in transition registry")
    if len(BUNDLE_STEP_TEMPLATE_BY_BUNDLE_AND_FROM_STATE) != len(BUNDLE_STEP_TEMPLATE_SPECS):
        raise SystemExit("duplicate bundle step templates found in transition registry")

    for target_spec in WRITE_TARGET_SPECS:
        if target_spec.surface not in valid_write_target_surfaces:
            raise SystemExit(
                f"write target `{target_spec.target}` uses unsupported surface `{target_spec.surface}`"
            )
        if target_spec.owner_bucket not in valid_owner_buckets:
            raise SystemExit(
                f"write target `{target_spec.target}` uses unsupported owner bucket `{target_spec.owner_bucket}`"
            )
        if target_spec.owner_bucket == "durable":
            unsupported_labels = sorted(set(target_spec.owner_labels) - SUPPORTED_DURABLE_OWNER_LABELS)
        elif target_spec.owner_bucket == "projection":
            unsupported_labels = sorted(set(target_spec.owner_labels) - SUPPORTED_PROJECTION_OWNER_LABELS)
        elif target_spec.owner_bucket == "artifact":
            unsupported_labels = sorted(set(target_spec.owner_labels) - SUPPORTED_ARTIFACT_OWNER_LABELS)
        else:
            unsupported_labels = sorted(set(target_spec.owner_labels))
        if unsupported_labels:
            raise SystemExit(
                f"write target `{target_spec.target}` declares unsupported owner labels: {', '.join(unsupported_labels)}"
            )

    known_write_targets = set(WRITE_TARGET_SPEC_BY_NAME)
    for side_effect_spec in TRANSITION_SIDE_EFFECT_SPECS:
        unknown_targets = sorted(set(side_effect_spec.write_targets) - known_write_targets)
        if unknown_targets:
            raise SystemExit(
                f"transition side effect `{side_effect_spec.code}` declares unknown write targets: {', '.join(unknown_targets)}"
            )
        for owner_kind, declared_labels, allowed_labels in [
            ("durable", set(side_effect_spec.durable_owners), SUPPORTED_DURABLE_OWNER_LABELS),
            ("projection", set(side_effect_spec.projection_owners), SUPPORTED_PROJECTION_OWNER_LABELS),
            ("artifact", set(side_effect_spec.artifact_owners), SUPPORTED_ARTIFACT_OWNER_LABELS),
            ("live inspection", set(side_effect_spec.live_inspection_owners), SUPPORTED_LIVE_INSPECTION_OWNER_LABELS),
        ]:
            unsupported_labels = sorted(declared_labels - allowed_labels)
            if unsupported_labels:
                raise SystemExit(
                    f"transition side effect `{side_effect_spec.code}` declares unsupported {owner_kind} owner labels: {', '.join(unsupported_labels)}"
                )

    known_commands = set(COMMAND_SPEC_BY_NAME)
    for command_name, specs in COMMAND_MUTABLE_FIELDS_BY_COMMAND.items():
        if command_name not in known_commands:
            raise SystemExit(
                f"command mutable-field semantics reference unknown transition command `{command_name}`"
            )
        payload_keys: set[str] = set()
        cli_flags: set[str] = set()
        replace_flags: set[str] = set()
        for field_spec in specs:
            if field_spec.value_kind not in valid_mutable_value_kinds:
                raise SystemExit(
                    f"command mutable field `{command_name}.{field_spec.code}` uses unsupported value kind `{field_spec.value_kind}`"
                )
            if field_spec.storage_kind not in valid_mutable_storage_kinds:
                raise SystemExit(
                    f"command mutable field `{command_name}.{field_spec.code}` uses unsupported storage kind `{field_spec.storage_kind}`"
                )
            if field_spec.mutation_mode not in valid_mutation_modes:
                raise SystemExit(
                    f"command mutable field `{command_name}.{field_spec.code}` uses unsupported mutation mode `{field_spec.mutation_mode}`"
                )
            if field_spec.payload_key in payload_keys:
                raise SystemExit(
                    f"command `{command_name}` reuses mutable payload key `{field_spec.payload_key}`"
                )
            payload_keys.add(field_spec.payload_key)
            if field_spec.cli_flag in cli_flags:
                raise SystemExit(
                    f"command `{command_name}` reuses mutable cli flag `{field_spec.cli_flag}`"
                )
            cli_flags.add(field_spec.cli_flag)
            if field_spec.replace_flag:
                if field_spec.mutation_mode != "merge_unique":
                    raise SystemExit(
                        f"command mutable field `{command_name}.{field_spec.code}` declares replace flag without merge_unique semantics"
                    )
                if field_spec.replace_flag in replace_flags:
                    raise SystemExit(
                        f"command `{command_name}` reuses mutable replace flag `{field_spec.replace_flag}`"
                    )
                replace_flags.add(field_spec.replace_flag)
            if field_spec.include_reason_note and field_spec.mutation_mode != "append_paragraphs":
                raise SystemExit(
                    f"command mutable field `{command_name}.{field_spec.code}` includes reason notes without append_paragraph semantics"
                )

    for command_name, specs in COMMAND_EXECUTOR_FIELDS_BY_COMMAND.items():
        if command_name not in known_commands:
            raise SystemExit(
                f"command executor-field semantics reference unknown transition command `{command_name}`"
            )
        payload_keys: set[str] = set()
        cli_flags: set[str] = set()
        for field_spec in specs:
            if field_spec.value_kind not in valid_executor_value_kinds:
                raise SystemExit(
                    f"command executor field `{command_name}.{field_spec.payload_key}` uses unsupported value kind `{field_spec.value_kind}`"
                )
            if field_spec.payload_key in payload_keys:
                raise SystemExit(
                    f"command `{command_name}` reuses executor payload key `{field_spec.payload_key}`"
                )
            payload_keys.add(field_spec.payload_key)
            if field_spec.cli_flag in cli_flags:
                raise SystemExit(
                    f"command `{command_name}` reuses executor cli flag `{field_spec.cli_flag}`"
                )
            cli_flags.add(field_spec.cli_flag)

    for bundle_name, specs in BUNDLE_EXECUTOR_FIELDS_BY_BUNDLE.items():
        if bundle_name not in BUNDLE_GOVERNANCE_SPEC_BY_NAME:
            raise SystemExit(
                f"bundle executor payload-field semantics reference unknown governed bundle `{bundle_name}`"
            )
        payload_keys: set[str] = set()
        for field_spec in specs:
            if field_spec.value_kind not in valid_executor_value_kinds:
                raise SystemExit(
                    f"bundle `{bundle_name}` payload field `{field_spec.payload_key}` uses unsupported value kind `{field_spec.value_kind}`"
                )
            if field_spec.payload_key in payload_keys:
                raise SystemExit(
                    f"bundle `{bundle_name}` reuses payload key `{field_spec.payload_key}`"
                )
            payload_keys.add(field_spec.payload_key)

    valid_bundle_binding_value_kinds = {"scalar", "list", "bool"}
    all_step_target_names = known_commands | set(BUNDLE_GOVERNANCE_SPEC_BY_NAME)
    for bundle_name, route_states in BUNDLE_ROUTE_STATES_BY_BUNDLE.items():
        if bundle_name not in BUNDLE_GOVERNANCE_SPEC_BY_NAME:
            raise SystemExit(f"bundle route semantics reference unknown governed bundle `{bundle_name}`")
        known_payload_keys = bundle_allowed_payload_keys(bundle_name)
        states = {spec.state for spec in route_states}
        terminal_states = {spec.state for spec in route_states if spec.terminal}
        if not terminal_states:
            raise SystemExit(f"bundle `{bundle_name}` declares no terminal route state")
        for route_state_spec in route_states:
            unknown_required_payload_keys = sorted(set(route_state_spec.required_payload_keys) - known_payload_keys)
            if unknown_required_payload_keys:
                raise SystemExit(
                    f"bundle `{bundle_name}` route state `{route_state_spec.state}` requires undeclared payload keys: "
                    + ", ".join(unknown_required_payload_keys)
                )

        step_templates = BUNDLE_STEP_TEMPLATES_BY_BUNDLE.get(bundle_name, ())
        if not step_templates:
            raise SystemExit(f"bundle `{bundle_name}` declares no step templates")
        stepped_from_states: set[str] = set()
        for step_template in step_templates:
            if step_template.bundle_name != bundle_name:
                raise SystemExit(
                    f"bundle step template `{step_template.label}` is indexed under the wrong bundle `{bundle_name}`"
                )
            if step_template.from_state not in states:
                raise SystemExit(
                    f"bundle `{bundle_name}` step template `{step_template.label}` starts from unknown state `{step_template.from_state}`"
                )
            if step_template.to_state not in states:
                raise SystemExit(
                    f"bundle `{bundle_name}` step template `{step_template.label}` ends at unknown state `{step_template.to_state}`"
                )
            if step_template.command_name not in all_step_target_names:
                raise SystemExit(
                    f"bundle `{bundle_name}` step template `{step_template.label}` references unknown command `{step_template.command_name}`"
                )
            stepped_from_states.add(step_template.from_state)
            if step_template.command_name in BUNDLE_GOVERNANCE_SPEC_BY_NAME:
                allowed_step_payload_keys = bundle_allowed_payload_keys(step_template.command_name)
            else:
                allowed_step_payload_keys = command_allowed_executor_payload_keys(step_template.command_name)
            template_target_keys = {
                key for key, _value in step_template.static_scalar_fields
            } | {
                key for key, _value in step_template.static_bool_fields
            } | {
                binding.target_key for binding in step_template.bindings
            }
            unknown_template_target_keys = sorted(template_target_keys - allowed_step_payload_keys)
            if unknown_template_target_keys:
                raise SystemExit(
                    f"bundle `{bundle_name}` step template `{step_template.label}` targets undeclared payload keys for `{step_template.command_name}`: "
                    + ", ".join(unknown_template_target_keys)
                )
            for binding in step_template.bindings:
                if binding.value_kind not in valid_bundle_binding_value_kinds:
                    raise SystemExit(
                        f"bundle `{bundle_name}` step template `{step_template.label}` uses unsupported binding value kind `{binding.value_kind}`"
                    )
                if binding.source_key not in known_payload_keys:
                    raise SystemExit(
                        f"bundle `{bundle_name}` step template `{step_template.label}` reads undeclared bundle payload key `{binding.source_key}`"
                    )
        non_terminal_states = states - terminal_states
        uncovered_non_terminal_states = sorted(non_terminal_states - stepped_from_states)
        if uncovered_non_terminal_states:
            raise SystemExit(
                f"bundle `{bundle_name}` has non-terminal route states without step templates: "
                + ", ".join(uncovered_non_terminal_states)
            )

    for bundle_spec in BUNDLE_GOVERNANCE_SPECS:
        if bundle_spec.name in known_commands:
            raise SystemExit(
                f"bundle governance `{bundle_spec.name}` collides with a transition command name"
            )
        if not bundle_spec.state_resolver:
            raise SystemExit(f"bundle governance `{bundle_spec.name}` does not declare a state resolver")
        if bundle_spec.state_resolver not in BUNDLE_STATE_RESOLVER_SPEC_BY_NAME:
            raise SystemExit(
                f"bundle governance `{bundle_spec.name}` declares unknown bundle state resolver `{bundle_spec.state_resolver}`"
            )
        known_governed_commands = known_commands | set(BUNDLE_GOVERNANCE_SPEC_BY_NAME)
        unknown_composed_commands = sorted(set(bundle_spec.composed_commands) - known_governed_commands)
        if unknown_composed_commands:
            raise SystemExit(
                f"bundle governance `{bundle_spec.name}` composes unknown transition commands: {', '.join(unknown_composed_commands)}"
            )
        for command_name in bundle_spec.composed_commands:
            if command_name in BUNDLE_GOVERNANCE_SPEC_BY_NAME:
                continue
            command_spec = COMMAND_SPEC_BY_NAME[command_name]
            if not command_spec.executor_supported:
                raise SystemExit(
                    f"bundle governance `{bundle_spec.name}` composes non-executor-supported command `{command_name}`"
                )

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
        unknown_write_targets = sorted(set(spec.write_targets) - known_write_targets)
        if unknown_write_targets:
            raise SystemExit(
                f"transition command `{spec.name}` declares unknown write targets: {', '.join(unknown_write_targets)}"
            )
        unknown_guard_codes = sorted(set(spec.guard_codes) - set(GUARD_SPEC_BY_CODE))
        if unknown_guard_codes:
            raise SystemExit(
                f"transition command `{spec.name}` declares unknown guard codes: {', '.join(unknown_guard_codes)}"
            )
        unknown_side_effect_codes = sorted(set(spec.side_effect_codes) - set(TRANSITION_SIDE_EFFECT_SPEC_BY_CODE))
        if unknown_side_effect_codes:
            raise SystemExit(
                f"transition command `{spec.name}` declares unknown transition side-effect codes: {', '.join(unknown_side_effect_codes)}"
            )
        if spec.emits_transition_event and "memory:transition-event" not in spec.write_targets and spec.implementation_status == "implemented":
            raise SystemExit(f"transition command `{spec.name}` emits transition events but does not declare `memory:transition-event`")
        if not spec.emits_transition_event and "memory:transition-event" in spec.write_targets:
            raise SystemExit(f"transition command `{spec.name}` declares `memory:transition-event` despite `emits_transition_event=False`")
        declared_mutable_codes = set(spec.mutable_field_codes)
        known_mutable_codes = {
            field_spec.code for field_spec in COMMAND_MUTABLE_FIELDS_BY_COMMAND.get(spec.name, ())
        }
        unknown_mutable_codes = sorted(declared_mutable_codes - known_mutable_codes)
        if unknown_mutable_codes:
            raise SystemExit(
                f"transition command `{spec.name}` declares unknown mutable field codes: {', '.join(unknown_mutable_codes)}"
            )
        if "mutable_fields" in spec.required_inputs and not declared_mutable_codes:
            raise SystemExit(
                f"transition command `{spec.name}` requires `mutable_fields` but declares no mutable field semantics"
            )
        if "mutable_fields" not in spec.required_inputs and declared_mutable_codes:
            raise SystemExit(
                f"transition command `{spec.name}` declares mutable field semantics without requiring `mutable_fields`"
            )
        undocumented_mutable_specs = sorted(known_mutable_codes - declared_mutable_codes)
        if undocumented_mutable_specs:
            raise SystemExit(
                f"transition command `{spec.name}` has registry mutable field semantics not declared on the command spec: {', '.join(undocumented_mutable_specs)}"
            )
        if spec.executor_supported:
            executor_specs = COMMAND_EXECUTOR_FIELDS_BY_COMMAND.get(spec.name, ())
            required_runtime_inputs = {
                field_name for field_name in spec.required_inputs if field_name not in {"project_id", "mutable_fields"}
            }
            covered_runtime_inputs = executor_runtime_inputs_covered(spec.name)
            missing_runtime_inputs = sorted(required_runtime_inputs - covered_runtime_inputs)
            if missing_runtime_inputs:
                raise SystemExit(
                    f"transition command `{spec.name}` is executor-supported but lacks executor payload semantics for: {', '.join(missing_runtime_inputs)}"
                )
        if spec.implementation_status in {"implemented", "partial"}:
            validate_transition_command_semantics(spec)
    allowed_bundle_commands = set(BUNDLE_GOVERNANCE_SPEC_BY_NAME)
    for plan_spec in ADJUDICATION_PLAN_SPECS:
        if plan_spec.implementation_status not in valid_implementation_statuses:
            raise SystemExit(
                f"adjudication plan `{plan_spec.plan_type}` uses unsupported implementation status `{plan_spec.implementation_status}`"
            )
        if plan_spec.implementation_status in {"implemented", "partial"} and not plan_spec.has_semantic_contract():
            raise SystemExit(
                f"adjudication plan `{plan_spec.plan_type}` is {plan_spec.implementation_status} but lacks semantic registry coverage"
            )
        if plan_spec.target_resolution not in ADJUDICATION_TARGET_RESOLUTION_SPEC_BY_NAME:
            raise SystemExit(
                f"adjudication plan `{plan_spec.plan_type}` declares unknown target-resolution contract `{plan_spec.target_resolution}`"
            )
        unknown_plan_side_effect_codes = sorted(
            set(plan_spec.side_effect_codes) - set(ADJUDICATION_PLAN_SIDE_EFFECT_SPEC_BY_CODE)
        )
        if unknown_plan_side_effect_codes:
            raise SystemExit(
                f"adjudication plan `{plan_spec.plan_type}` declares unknown adjudication plan side-effect codes: "
                + ", ".join(unknown_plan_side_effect_codes)
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
            if template.command_name in BUNDLE_GOVERNANCE_SPEC_BY_NAME:
                allowed_payload_targets = bundle_allowed_payload_keys(template.command_name)
            else:
                command_spec = COMMAND_SPEC_BY_NAME.get(template.command_name)
                if command_spec is None or not command_spec.executor_supported:
                    continue
                allowed_payload_targets = command_allowed_executor_payload_keys(template.command_name)
            template_targets = {
                key for key, _value in template.static_scalar_fields
            } | {
                key for key, _value in template.static_bool_fields
            } | {
                binding.target_key for binding in template.bindings
            }
            unknown_resolvers = sorted(
                {
                    binding.resolver
                    for binding in template.bindings
                    if binding.resolver not in ADJUDICATION_BINDING_RESOLVER_SPEC_BY_NAME
                }
            )
            if unknown_resolvers:
                raise SystemExit(
                    f"adjudication plan `{plan_spec.plan_type}` declares unknown binding resolvers for `{template.command_name}`: "
                    + ", ".join(unknown_resolvers)
                )
            unknown_template_targets = sorted(template_targets - allowed_payload_targets)
            if unknown_template_targets:
                raise SystemExit(
                    f"adjudication plan `{plan_spec.plan_type}` targets undeclared payload keys for `{template.command_name}`: {', '.join(unknown_template_targets)}"
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


def write_target_spec(target: str) -> WriteTargetSpec:
    validate_transition_specs()
    spec = WRITE_TARGET_SPEC_BY_NAME.get(target.strip())
    if spec is None:
        raise SystemExit(f"unknown write target `{target}`")
    return spec


def transition_side_effect_spec(code: str) -> TransitionSideEffectSpec:
    validate_transition_specs()
    spec = TRANSITION_SIDE_EFFECT_SPEC_BY_CODE.get(code.strip())
    if spec is None:
        raise SystemExit(f"unknown transition side effect `{code}`")
    return spec


def mutable_field_specs_for_command(command_name: str) -> list[CommandMutableFieldSpec]:
    validate_transition_specs()
    return list(COMMAND_MUTABLE_FIELDS_BY_COMMAND.get(command_name.strip(), ()))


def executor_field_specs_for_command(command_name: str) -> list[CommandExecutorFieldSpec]:
    validate_transition_specs()
    return list(COMMAND_EXECUTOR_FIELDS_BY_COMMAND.get(command_name.strip(), ()))


def bundle_field_specs(bundle_name: str) -> list[BundleExecutorFieldSpec]:
    validate_transition_specs()
    return list(BUNDLE_EXECUTOR_FIELDS_BY_BUNDLE.get(bundle_name.strip(), ()))


def bundle_governance_spec(bundle_name: str) -> BundleGovernanceSpec:
    validate_transition_specs()
    spec = BUNDLE_GOVERNANCE_SPEC_BY_NAME.get(bundle_name.strip())
    if spec is None:
        raise SystemExit(f"unknown governed bundle `{bundle_name}`")
    return spec


def bundle_state_resolver_names() -> list[str]:
    validate_transition_specs()
    return [spec.name for spec in BUNDLE_STATE_RESOLVER_SPECS]


def bundle_state_resolver_spec(name: str) -> BundleStateResolverSpec:
    validate_transition_specs()
    spec = BUNDLE_STATE_RESOLVER_SPEC_BY_NAME.get(name.strip())
    if spec is None:
        raise SystemExit(f"unknown bundle state resolver `{name}`")
    return spec


def bundle_route_state_specs(bundle_name: str) -> list[BundleRouteStateSpec]:
    validate_transition_specs()
    return list(BUNDLE_ROUTE_STATES_BY_BUNDLE.get(bundle_name.strip(), ()))


def bundle_route_state_spec(bundle_name: str, state: str) -> BundleRouteStateSpec:
    validate_transition_specs()
    spec = BUNDLE_ROUTE_STATE_BY_BUNDLE_AND_STATE.get((bundle_name.strip(), state.strip()))
    if spec is None:
        raise SystemExit(f"unknown route state `{state}` for governed bundle `{bundle_name}`")
    return spec


def bundle_step_template_specs(bundle_name: str) -> list[BundleStepTemplateSpec]:
    validate_transition_specs()
    return list(BUNDLE_STEP_TEMPLATES_BY_BUNDLE.get(bundle_name.strip(), ()))


def bundle_step_template_spec(bundle_name: str, from_state: str) -> BundleStepTemplateSpec:
    validate_transition_specs()
    spec = BUNDLE_STEP_TEMPLATE_BY_BUNDLE_AND_FROM_STATE.get((bundle_name.strip(), from_state.strip()))
    if spec is None:
        raise SystemExit(f"unknown route step from `{from_state}` for governed bundle `{bundle_name}`")
    return spec


def command_allowed_mutation_payload_keys(command_name: str) -> set[str]:
    normalized_name = command_name.strip()
    spec = COMMAND_SPEC_BY_NAME.get(normalized_name)
    if spec is None:
        raise SystemExit(f"unknown transition command `{command_name}`")
    allowed = {
        field_name
        for field_name in spec.required_inputs
        if field_name not in {"project_id", "mutable_fields"}
    }
    for field_spec in COMMAND_MUTABLE_FIELDS_BY_COMMAND.get(normalized_name, ()):
        allowed.add(field_spec.payload_key)
        if field_spec.replace_flag:
            allowed.add(field_spec.replace_flag)
    return allowed


def command_allowed_executor_payload_keys(command_name: str) -> set[str]:
    normalized_name = command_name.strip()
    spec = COMMAND_SPEC_BY_NAME.get(normalized_name)
    if spec is None:
        raise SystemExit(f"unknown transition command `{command_name}`")
    allowed = {
        field_spec.payload_key for field_spec in COMMAND_EXECUTOR_FIELDS_BY_COMMAND.get(normalized_name, ())
    }
    if "mutable_fields" in spec.required_inputs:
        allowed.update(command_allowed_mutation_payload_keys(normalized_name))
    return allowed


def executor_runtime_inputs_covered(command_name: str) -> set[str]:
    normalized_name = command_name.strip()
    spec = COMMAND_SPEC_BY_NAME.get(normalized_name)
    if spec is None:
        raise SystemExit(f"unknown transition command `{command_name}`")
    covered = {
        field_spec.payload_key for field_spec in COMMAND_EXECUTOR_FIELDS_BY_COMMAND.get(normalized_name, ())
    }
    plural_runtime_aliases = {
        "success_criterion": "success_criteria",
        "non_goal": "non_goals",
        "allowed_change": "allowed_changes",
        "forbidden_change": "forbidden_changes",
        "completion_criterion": "completion_criteria",
        "path": "paths",
        "owner_scope": "owner_scope",
    }
    for payload_key, runtime_key in plural_runtime_aliases.items():
        if payload_key in covered:
            covered.add(runtime_key)
    return covered


def normalize_runtime_input_keys(command_name: str, provided_inputs: set[str]) -> set[str]:
    normalized_name = command_name.strip()
    spec = COMMAND_SPEC_BY_NAME.get(normalized_name)
    if spec is None:
        raise SystemExit(f"unknown transition command `{command_name}`")
    normalized = set(provided_inputs)
    alias_pairs = (
        ("success_criterion", "success_criteria"),
        ("non_goal", "non_goals"),
        ("allowed_change", "allowed_changes"),
        ("forbidden_change", "forbidden_changes"),
        ("completion_criterion", "completion_criteria"),
        ("path", "paths"),
    )
    for singular_key, plural_key in alias_pairs:
        if singular_key in normalized:
            normalized.add(plural_key)
        if plural_key in normalized:
            normalized.add(singular_key)
    return normalized


def bundle_allowed_payload_keys(bundle_name: str) -> set[str]:
    normalized_name = bundle_name.strip()
    if normalized_name not in BUNDLE_GOVERNANCE_SPEC_BY_NAME:
        raise SystemExit(f"unknown governed bundle `{bundle_name}`")
    return {
        field_spec.payload_key
        for field_spec in BUNDLE_EXECUTOR_FIELDS_BY_BUNDLE.get(normalized_name, ())
    }


def semantic_transition_command_names() -> list[str]:
    validate_transition_specs()
    return [spec.name for spec in TRANSITION_COMMAND_SPECS if spec.has_semantic_contract()]


def executor_supported_command_names() -> list[str]:
    validate_transition_specs()
    return [spec.name for spec in TRANSITION_COMMAND_SPECS if spec.executor_supported]


def bundle_governance_names() -> list[str]:
    validate_transition_specs()
    return [spec.name for spec in BUNDLE_GOVERNANCE_SPECS]


def adjudication_target_resolution_names() -> list[str]:
    validate_transition_specs()
    return [spec.name for spec in ADJUDICATION_TARGET_RESOLUTION_SPECS]


def adjudication_binding_resolver_names() -> list[str]:
    validate_transition_specs()
    return [spec.name for spec in ADJUDICATION_BINDING_RESOLVER_SPECS]


def adjudication_plan_side_effect_codes() -> list[str]:
    validate_transition_specs()
    return [spec.code for spec in ADJUDICATION_PLAN_SIDE_EFFECT_SPECS]


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
        "write_target_semantics": [spec.to_dict() for spec in WRITE_TARGET_SPECS],
        "transition_side_effect_semantics": [spec.to_dict() for spec in TRANSITION_SIDE_EFFECT_SPECS],
        "command_mutable_field_semantics": [spec.to_dict() for spec in COMMAND_MUTABLE_FIELD_SPECS],
        "command_executor_field_semantics": [spec.to_dict() for spec in COMMAND_EXECUTOR_FIELD_SPECS],
        "bundle_executor_field_semantics": [spec.to_dict() for spec in BUNDLE_EXECUTOR_FIELD_SPECS],
        "bundle_governance": [spec.to_dict() for spec in BUNDLE_GOVERNANCE_SPECS],
        "bundle_state_resolver_semantics": [spec.to_dict() for spec in BUNDLE_STATE_RESOLVER_SPECS],
        "bundle_route_state_semantics": [spec.to_dict() for spec in BUNDLE_ROUTE_STATE_SPECS],
        "bundle_step_template_semantics": [spec.to_dict() for spec in BUNDLE_STEP_TEMPLATE_SPECS],
        "adjudication_target_resolution_semantics": [spec.to_dict() for spec in ADJUDICATION_TARGET_RESOLUTION_SPECS],
        "adjudication_binding_resolver_semantics": [spec.to_dict() for spec in ADJUDICATION_BINDING_RESOLVER_SPECS],
        "adjudication_plan_side_effect_semantics": [spec.to_dict() for spec in ADJUDICATION_PLAN_SIDE_EFFECT_SPECS],
        "transition_commands": [spec.to_dict() for spec in TRANSITION_COMMAND_SPECS],
        "adjudication_plan_families": [spec.to_dict() for spec in ADJUDICATION_PLAN_SPECS],
    }
