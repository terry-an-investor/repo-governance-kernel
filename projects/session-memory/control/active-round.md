# Active Round

- Round id: `round-2026-03-24-0907-lift-rewrite-open-round-field-semantics-into-registry-owned-owner-layer-contracts`
- Objective id: `obj-2026-03-23-0002`
- Status: `active`

## Scope

- Lift rewrite-open-round mutable field declarations into the transition registry instead of leaving field semantics private to rewrite_open_round.py and executor plumbing.
- Make adjudication rewrite payload execution consume the same registry-owned field semantics and reject undeclared private rewrite keys.
- Update canonical docs and current-task so the registry contract truthfully includes rewrite field semantics for the bounded round primitive.

## Deliverable

Registry-owned rewrite field semantics govern rewrite-open-round mutation surface and adjudication executor payloads.

## Validation Plan

Run targeted py_compile, registry export, adjudication follow-up smoke, control audit, and worktree enforcement after the rewrite field semantics land.

## Active Risks

_none recorded_

## Blockers

_none recorded_
