# Active Round

- Round id: `round-2026-03-24-0728-unify-remaining-command-domains-under-registry-owned-owner-layer-semantics`
- Objective id: `obj-2026-03-23-0002`
- Status: `active`

## Scope

- Add explicit owner-layer fields to the transition registry so durable owners, projection owners, artifact owners, and live inspection owners stop living as private code semantics.
- Make exception-contract and anchor-maintenance commands consume the same registry-backed contract assertion path already used by round and objective-phase commands.

## Deliverable

All implemented transition command domains consume registry-backed owner-layer contracts, and the registry itself carries explicit owner fields that bound private semantics drift.

## Validation Plan

Run real-project audit and enforce-worktree, exercise anchor-maintenance commands and capture-handoff on the real project, then close the round and return the objective to paused.

## Active Risks

_none recorded_

## Blockers

_none recorded_
