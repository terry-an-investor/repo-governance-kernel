# Active Round

- Round id: `round-2026-03-23-1814-broaden-enforcement-coverage-beyond-first-worktree-gate`
- Objective id: `obj-2026-03-23-0002`
- Status: `active`

## Scope

- Add bounded exception-contract executor plan types so adjudication can compile retire and invalidate rewrites from durable truth instead of hand-authored payload JSON.
- Teach execute-adjudication-followups and the adjudication smoke fixture to exercise exception-contract plan compilation through adjudication invalidated object sets.
- Validate that adjudication smoke, full phase-1 smoke, audit-control-state, and enforce-worktree all pass after the exception-contract plan compiler milestone lands.

## Deliverable

A bounded adjudication plan compiler that covers both round rewrite-close chains and exception-contract retire/invalidate rewrites through durable plan contracts.

## Validation Plan

Run adjudication followup smoke with retire and invalidate exception-contract plan contracts, rerun full phase-1 smoke, then rerun audit-control-state and enforce-worktree on the real project.

## Active Risks

- Exception plan compilation could become implicit verdict interpretation if target resolution stops being deterministic and auditable.
- Compiler and executor merge logic could regress into duplicate or conflicting followup execution as more bounded plan types are added.

## Blockers

_none recorded_
