# Active Round

- Round id: `round-2026-03-24-0842-lift-transition-guard-semantics-into-registry-owned-owner-layer-contracts`
- Objective id: `obj-2026-03-23-0002`
- Status: `active`

## Scope

- Lift transition guard semantics into registry-owned owner-layer contracts.
- Remove per-domain private guard-text ownership from shared consumers where the registry can own it.

## Deliverable

Transition guard rendering is declared in the machine-readable registry and consumed through shared owner-layer helpers instead of per-domain private maps.

## Validation Plan

Run py_compile on changed scripts, export the registry, run targeted control audit/enforcement, and close the round back to paused.

## Active Risks

_none recorded_

## Blockers

_none recorded_
