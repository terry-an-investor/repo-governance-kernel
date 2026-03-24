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
    direct_write_forbidden: bool = True
    private_semantics_forbidden: bool = True
    required_validations: tuple[str, ...] = ()

    def to_dict(self) -> dict[str, object]:
        return {
            "name": self.name,
            "bundle_kind": self.bundle_kind,
            "purpose": self.purpose,
            "composed_commands": list(self.composed_commands),
            "direct_write_forbidden": self.direct_write_forbidden,
            "private_semantics_forbidden": self.private_semantics_forbidden,
            "required_validations": list(self.required_validations),
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
    CommandExecutorFieldSpec("close-objective", "objective_id", "objective-id", "scalar"),
    CommandExecutorFieldSpec("close-objective", "closing_status", "closing-status", "scalar", required=True),
    CommandExecutorFieldSpec("close-objective", "reason", "reason", "scalar", required=True),
    CommandExecutorFieldSpec("close-objective", "evidence", "evidence", "list"),
    CommandExecutorFieldSpec("close-objective", "supersession_note", "supersession-note", "scalar"),
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
    CommandExecutorFieldSpec("update-task-contract-status", "task_contract_id", "task-contract-id", "scalar", required=True),
    CommandExecutorFieldSpec("update-task-contract-status", "status", "status", "scalar", required=True),
    CommandExecutorFieldSpec("update-task-contract-status", "reason", "reason", "scalar", required=True),
    CommandExecutorFieldSpec("update-task-contract-status", "resolution", "resolution", "list"),
    CommandExecutorFieldSpec("update-task-contract-status", "risk", "risk", "list"),
    CommandExecutorFieldSpec("update-task-contract-status", "status_note", "status-note", "list"),
    CommandExecutorFieldSpec("rewrite-open-task-contract", "task_contract_id", "task-contract-id", "scalar"),
    CommandExecutorFieldSpec("rewrite-open-task-contract", "reason", "reason", "scalar", required=True),
    CommandExecutorFieldSpec("set-phase", "objective_id", "objective-id", "scalar"),
    CommandExecutorFieldSpec("set-phase", "phase", "phase", "scalar", required=True),
    CommandExecutorFieldSpec("set-phase", "reason", "reason", "scalar", required=True),
    CommandExecutorFieldSpec("set-phase", "evidence", "evidence", "list"),
    CommandExecutorFieldSpec("set-phase", "scope_review_note", "scope-review-note", "list"),
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
    BundleExecutorFieldSpec("round-close-chain", "validation_pending_reason", "scalar"),
    BundleExecutorFieldSpec("round-close-chain", "captured_reason", "scalar"),
    BundleExecutorFieldSpec("round-close-chain", "closed_reason", "scalar"),
    BundleExecutorFieldSpec("round-close-chain", "validated_by", "list"),
    BundleExecutorFieldSpec("round-close-chain", "blocker", "list"),
    BundleExecutorFieldSpec("round-close-chain", "risk", "list"),
    BundleExecutorFieldSpec("round-close-chain", "clear_blockers", "bool"),
)


BUNDLE_GOVERNANCE_SPECS: tuple[BundleGovernanceSpec, ...] = (
    BundleGovernanceSpec(
        name="round-close-chain",
        bundle_kind="executor-wrapper",
        purpose="Advance one round through the legal close sequence by composing only existing round status transitions.",
        composed_commands=("update-round-status",),
        required_validations=("scripts/smoke_adjudication_followups.py",),
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
    if len(COMMAND_MUTABLE_FIELD_SPEC_BY_COMMAND_AND_CODE) != len(COMMAND_MUTABLE_FIELD_SPECS):
        raise SystemExit("duplicate command mutable-field codes found in transition registry")
    if sum(len(specs) for specs in BUNDLE_EXECUTOR_FIELDS_BY_BUNDLE.values()) != len(BUNDLE_EXECUTOR_FIELD_SPECS):
        raise SystemExit("duplicate bundle executor payload-field semantics found in transition registry")
    if len(BUNDLE_GOVERNANCE_SPEC_BY_NAME) != len(BUNDLE_GOVERNANCE_SPECS):
        raise SystemExit("duplicate bundle governance names found in transition registry")

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

    for bundle_spec in BUNDLE_GOVERNANCE_SPECS:
        if bundle_spec.name in known_commands:
            raise SystemExit(
                f"bundle governance `{bundle_spec.name}` collides with a transition command name"
            )
        unknown_composed_commands = sorted(set(bundle_spec.composed_commands) - known_commands)
        if unknown_composed_commands:
            raise SystemExit(
                f"bundle governance `{bundle_spec.name}` composes unknown transition commands: {', '.join(unknown_composed_commands)}"
            )
        for command_name in bundle_spec.composed_commands:
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
            covered_runtime_inputs = {field_spec.payload_key for field_spec in executor_specs}
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
        "transition_commands": [spec.to_dict() for spec in TRANSITION_COMMAND_SPECS],
        "adjudication_plan_families": [spec.to_dict() for spec in ADJUDICATION_PLAN_SPECS],
    }
