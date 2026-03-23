# Active Round

- Round id: `round-2026-03-23-2225-unify-current-task-owner-layer-semantics`
- Objective id: `obj-2026-03-23-0002`
- Status: `active`

## Scope

- Make current-task semantics consistent across audit, enforcement, refresh, and canonical docs.

## Deliverable

A consistent owner-layer rule for current-task that no longer lets audit and enforcement disagree about its control status.

## Validation Plan

Refresh current-task to the new semantics, run audit_control_state and enforce_worktree on the real project, then close the round and return the objective to paused.

## Active Risks

_none recorded_

## Blockers

_none recorded_
