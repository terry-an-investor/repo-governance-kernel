# Active Round

- Round id: `round-2026-03-23-2315-make-current-task-workspace-anchor-semantics-explicitly-snapshot-based`
- Objective id: `obj-2026-03-23-0002`
- Status: `active`

## Scope

- Rename current-task workspace anchor bullets so they read as last-refresh snapshot metadata rather than live truth.
- Keep assemble-context, refresh-current-task-anchor, and canonical docs aligned on the same snapshot semantics.

## Deliverable

Current-task workspace anchor fields are explicitly snapshot-scoped, parser-compatible, and documented as historical orientation metadata rather than self-updating live state.

## Validation Plan

Refresh current-task under the new wording, run real-project audit and enforce-worktree, and verify assemble-context still reads the renamed anchor fields.

## Active Risks

_none recorded_

## Blockers

_none recorded_
