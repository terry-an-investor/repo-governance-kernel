# Active Round

- Round id: `round-2026-03-23-1548-implement-remaining-objective-line-transitions`
- Objective id: `obj-2026-03-23-0002`
- Status: `active`

## Scope

- add close-objective so objective lines can end honestly without manual file edits
- add record-soft-pivot so execution-frame changes do not require fake hard pivots or silent rewrites
- validate the new objective-line commands against disposable fixtures and keep projection/event semantics aligned with the shared transition engine

## Deliverable

A real remaining objective-line slice with close-objective and record-soft-pivot commands using the shared transition engine and proven on disposable fixtures.

## Validation Plan

Run objective-line fixture regression for close-objective and soft-pivot, then pass audit-control-state, role-context compilation, and full smoke.

## Active Risks

- Soft-pivot semantics can blur into hard pivot if objective identity and success criteria boundaries are not enforced tightly.
- Close-objective can create dead-end control state if active projections are not updated consistently.

## Blockers

_none recorded_
