# Active Round

- Round id: `round-2026-03-24-1134-land-m1-m2-automatic-rewrite-contracts`
- Objective id: `obj-2026-03-23-0002`
- Status: `active`

## Scope

- Lift governed bundle payload semantics into the transition registry so bundle execution stops carrying private payload keys.
- Broaden adjudication plan contracts to cover task-contract and round target resolution through the existing owner-layer pattern.

## Deliverable

M1 bundle payload semantics and M2 adjudication plan-family expansion land with smoke coverage and honest docs.

## Validation Plan

Registry audit, worktree enforcement, targeted py_compile, and adjudication followup smoke pass on the changed path.

## Active Risks

- Expanding executor support too broadly could reintroduce private semantics instead of reducing them.

## Blockers

_none recorded_
