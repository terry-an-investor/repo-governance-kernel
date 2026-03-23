#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass


@dataclass(frozen=True)
class TransitionCommandSpec:
    name: str
    domain: str
    executor_supported: bool = False

    def to_dict(self) -> dict[str, object]:
        return asdict(self)


@dataclass(frozen=True)
class AdjudicationPlanSpec:
    plan_type: str
    compiled_commands: tuple[str, ...]

    def to_dict(self) -> dict[str, object]:
        return {
            "plan_type": self.plan_type,
            "compiled_commands": list(self.compiled_commands),
        }


TRANSITION_COMMAND_SPECS: tuple[TransitionCommandSpec, ...] = (
    TransitionCommandSpec("open-objective", "objective-line"),
    TransitionCommandSpec("close-objective", "objective-line", executor_supported=True),
    TransitionCommandSpec("record-soft-pivot", "objective-line"),
    TransitionCommandSpec("record-hard-pivot", "objective-line"),
    TransitionCommandSpec("set-phase", "phase", executor_supported=True),
    TransitionCommandSpec("open-round", "round"),
    TransitionCommandSpec("refresh-round-scope", "round", executor_supported=True),
    TransitionCommandSpec("update-round-status", "round", executor_supported=True),
    TransitionCommandSpec("rewrite-open-round", "round", executor_supported=True),
    TransitionCommandSpec("activate-exception-contract", "exception-contract"),
    TransitionCommandSpec("retire-exception-contract", "exception-contract", executor_supported=True),
    TransitionCommandSpec("invalidate-exception-contract", "exception-contract", executor_supported=True),
    TransitionCommandSpec("refresh-anchor", "anchor-maintenance"),
    TransitionCommandSpec("capture-snapshot", "anchor-maintenance"),
)


ADJUDICATION_PLAN_SPECS: tuple[AdjudicationPlanSpec, ...] = (
    AdjudicationPlanSpec(
        plan_type="rewrite-open-round-then-close-chain",
        compiled_commands=("rewrite-open-round", "round-close-chain"),
    ),
    AdjudicationPlanSpec(
        plan_type="retire-invalidated-exception-contracts",
        compiled_commands=("retire-exception-contract",),
    ),
    AdjudicationPlanSpec(
        plan_type="invalidate-invalidated-exception-contracts",
        compiled_commands=("invalidate-exception-contract",),
    ),
    AdjudicationPlanSpec(
        plan_type="enter-execution-with-round-bootstrap",
        compiled_commands=("set-phase",),
    ),
)


COMMAND_SPEC_BY_NAME = {spec.name: spec for spec in TRANSITION_COMMAND_SPECS}
PLAN_SPEC_BY_TYPE = {spec.plan_type: spec for spec in ADJUDICATION_PLAN_SPECS}


def validate_transition_specs() -> None:
    if len(COMMAND_SPEC_BY_NAME) != len(TRANSITION_COMMAND_SPECS):
        raise SystemExit("duplicate transition command names found in transition registry")
    if len(PLAN_SPEC_BY_TYPE) != len(ADJUDICATION_PLAN_SPECS):
        raise SystemExit("duplicate adjudication plan types found in transition registry")

    known_commands = set(COMMAND_SPEC_BY_NAME)
    allowed_bundle_commands = {"round-close-chain"}
    for plan_spec in ADJUDICATION_PLAN_SPECS:
        for command_name in plan_spec.compiled_commands:
            if command_name not in known_commands and command_name not in allowed_bundle_commands:
                raise SystemExit(
                    f"adjudication plan `{plan_spec.plan_type}` references unknown compiled command `{command_name}`"
                )


def transition_command_names() -> list[str]:
    validate_transition_specs()
    return [spec.name for spec in TRANSITION_COMMAND_SPECS]


def executor_supported_command_names() -> list[str]:
    validate_transition_specs()
    return [spec.name for spec in TRANSITION_COMMAND_SPECS if spec.executor_supported]


def adjudication_plan_types() -> list[str]:
    validate_transition_specs()
    return [spec.plan_type for spec in ADJUDICATION_PLAN_SPECS]


def export_transition_registry() -> dict[str, object]:
    validate_transition_specs()
    return {
        "transition_commands": [spec.to_dict() for spec in TRANSITION_COMMAND_SPECS],
        "adjudication_plan_families": [spec.to_dict() for spec in ADJUDICATION_PLAN_SPECS],
    }
