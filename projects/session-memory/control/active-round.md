# Active Round

- Round id: `round-2026-03-23-1213-implement-first-transition-slice`
- Objective id: `obj-2026-03-23-0002`
- Status: `active`

## Scope

- implement open-round and update-round-status as real commands
- persist transition events for round commands
- validate the first enforced control-state transitions on session-memory

## Deliverable

A working first transition slice that can open a round, move it through legal statuses, and write transition-event records.

## Validation Plan

Run command-level transitions on the real session-memory round path and pass smoke after the new active round is opened.

## Active Risks

- Guard logic may still be too narrow for future objective and exception-contract transitions.
- Round file rewriting could regress frontmatter fidelity if metadata preservation is incomplete.

## Blockers

_none recorded_
