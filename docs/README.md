# Docs Map

This directory is the documentation tree for the repository.

If you only want the main docs, start with `docs/canonical/`. Those files define
the product, control model, state model, command surface, schema, principles,
implementation direction, and release status.

## Canonical Docs

- `docs/canonical/PRODUCT.md`: what the product is and what it is not
- `docs/canonical/ARCHITECTURE.md`: how the repo is split between kernel and repo-owned control state
- `docs/canonical/CONTROL_SYSTEM.md`: durable truth, projections, audit, and enforcement
- `docs/canonical/STATE_MACHINE.md`: legal state domains and transition rules
- `docs/canonical/TRANSITION_COMMANDS.md`: command, bundle, and intent surface
- `docs/canonical/SCHEMA.md`: object schema and layout contract
- `docs/canonical/DESIGN_PRINCIPLES.md`: repo design constraints
- `docs/canonical/IMPLEMENTATION_PLAN.md`: current implementation direction beyond the `0.1.0b1` beta hardening cut
- `docs/canonical/PUBLIC_SURFACE.md`: current `0.1.0b1` public package contract
- `docs/canonical/RELEASE.md`: release target and validation evidence

## Auxiliary Docs

- `docs/history/`: historical notes and one-off background material
- `docs/operations/`: harness and operational docs that support the repo but are not package-facing contracts

## Agent Wrappers

- `skills/`: repo-owned agent wrappers that package bounded command surfaces for
  agent callers without expanding product authority
