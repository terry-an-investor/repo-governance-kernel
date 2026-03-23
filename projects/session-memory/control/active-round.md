# Active Round

- Round id: `round-2026-03-23-1530-extract-shared-transition-engine-primitive`
- Objective id: `obj-2026-03-23-0002`
- Status: `active`

## Scope

- pull duplicated transition-writing logic out of objective, round, and exception commands into one shared owner-layer primitive
- make command families delegate projection and transition-event side effects through the shared primitive instead of hand-rolling them
- reduce the active exception contract by shrinking the duplicated transition surface rather than normalizing it

## Deliverable

A shared transition-engine primitive adopted by the existing objective, round, and exception-contract commands for the overlapping file-write and transition-event responsibilities.

## Validation Plan

Run command-level regression on the migrated command families, then pass audit-control-state, role-context compilation, exception-contract smoke, and full smoke.

## Active Risks

- Refactoring shared transition ownership can regress existing commands if file-shape preservation is not held constant.
- The shared engine can become a vague wrapper if it does not own concrete guards and side effects honestly.

## Blockers

_none recorded_
