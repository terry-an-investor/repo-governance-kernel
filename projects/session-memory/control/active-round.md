# Active Round

- Round id: `round-2026-03-24-0907-lift-rewrite-open-round-field-semantics-into-registry-owned-owner-layer-contracts`
- Objective id: `obj-2026-03-23-0002`
- Status: `active`

## Scope

- Generalize the bundle problem beyond round-close-chain and define the repo law for bundle wrappers versus primitive transition commands.
- Move bundle wrapper admission out of local literals into one explicit owner-layer governance surface that executor and plan validation both consume.
- Update canonical docs and current-task so bundle governance is treated as a system rule, not an implementation afterthought.

## Deliverable

Bundle wrappers are governed by explicit repo-owned rules and one narrow machine-readable governance surface instead of private ad hoc exceptions.

## Validation Plan

Run py_compile, transition registry export, adjudication follow-up smoke, control audit, and worktree enforcement after bundle governance law lands.

## Active Risks

_none recorded_

## Blockers

_none recorded_
