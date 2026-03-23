# Active Round

- Round id: `round-2026-03-23-1814-broaden-enforcement-coverage-beyond-first-worktree-gate`
- Objective id: `obj-2026-03-23-0002`
- Status: `active`

## Scope

- Extend the transition registry spec to encode first semantic fields for implemented command and plan families.
- Wire registry export and validation to reject placeholder semantic coverage for commands that the repo treats as implemented.
- Teach control audit to warn when documented commands are missing semantic coverage in the machine-readable registry.

## Deliverable

A richer transition registry that can describe implemented command semantics beyond names and executor support, plus audit checks that keep that registry honest.

## Validation Plan

Validate registry export shape, rerun targeted audit checks, rerun transition/adjudication smoke, and rerun real-project audit plus worktree enforcement.

## Active Risks

- A shallow semantic schema could still duplicate prose without becoming authoritative enough to drive later consumers.
- Overreaching into fully generic command execution in the same round would blur the owner-layer boundary and regress reviewability.

## Blockers

_none recorded_
