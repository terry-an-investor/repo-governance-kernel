# Active Round

- Round id: `round-2026-03-24-0655-separate-durable-current-task-control-from-live-workspace-projection`
- Objective id: `obj-2026-03-23-0002`
- Status: `active`

## Scope

- Remove live workspace snapshot fields from current-task so it remains a durable control-and-orientation file.
- Add one reusable non-durable live workspace projection command and make handoff capture emit it separately.

## Deliverable

Current-task keeps only durable control plus workspace locator fields, while live repo facts are rendered through a separate reusable projection command and capture artifact.

## Validation Plan

Refresh current-task under the new split semantics, render a live workspace projection artifact, run capture-handoff or equivalent real-path validation, then rerun audit and enforce-worktree.

## Active Risks

_none recorded_

## Blockers

_none recorded_
