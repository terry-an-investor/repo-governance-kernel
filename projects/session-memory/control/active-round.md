# Active Round

- Round id: `round-2026-03-24-0907-lift-rewrite-open-round-field-semantics-into-registry-owned-owner-layer-contracts`
- Objective id: `obj-2026-03-23-0002`
- Status: `active`

## Scope

- Align canonical docs so product, control, state-machine, and transition surfaces explicitly place task-contract under round governance instead of leaving task-level execution semantics in prose.
- Add a first file-first task-contract object model and creation path that can attach one concrete task contract to an active round without inventing a new DSL.
- Add a minimal audit path for task-contract integrity and pressure-test the model with one real task contract in the session-memory project.

## Deliverable

Session-memory docs describe a three-layer product/control/task contract architecture, the repo can create and read durable task-contract objects, and one real task-contract sample plus audit path proves the layer is no longer only prose.

## Validation Plan

Run targeted py_compile for the new task-contract scripts, create one real task-contract for the active round, run the new task-contract audit, refresh current-task anchor, then run control audit and worktree enforcement before commit.

## Active Risks

_none recorded_

## Blockers

_none recorded_
