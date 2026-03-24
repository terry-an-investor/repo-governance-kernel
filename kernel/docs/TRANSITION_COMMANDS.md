# Repo Governance Kernel Transition Commands

Date: 2026-03-24
Scope: Canonical transition command surface for the repo governance kernel

## Goal

Freeze the bounded command surface that drives the kernel state machine.

The current automation scope is bounded registry-owned execution.
The current autonomy boundary is not a general autonomous rewrite engine.

This document defines:

- command names
- required inputs
- legal guards
- write ownership
- bounded side effects
- governed bundle rules

The executable authority for the implemented subset remains:

- `kernel/transition_specs.py`

## Design Position

Commands should map to legal state transitions, not ad hoc file edits.

That means:

- each primitive command owns one honest transition
- each primitive command declares its guard and write surface
- executor payload admission is registry-owned
- governed bundles are explicit wrappers, not a second hidden runtime
- command callers should not restate static semantics privately

## Kernel Command Surface

The kernel should stay centered on a small set of first-class commands.

### Objective-Line Commands

- `open-objective`
- `close-objective`
- `record-soft-pivot`
- `record-hard-pivot`

### Phase Command

- `set-phase`

### Round Commands

- `open-round`
- `rewrite-open-round`
- `refresh-round-scope`
- `update-round-status`

### Task-Contract Commands

- `open-task-contract`
- `rewrite-open-task-contract`
- `update-task-contract-status`

### Exception-Contract Commands

- `activate-exception-contract`
- `retire-exception-contract`
- `invalidate-exception-contract`

### Orientation, Audit, And Repair Commands

- `refresh-anchor`
- `render-live-workspace`
- `capture-snapshot`
- `audit-control-state`
- `enforce-worktree`
- `adjudicate-control-state`
- `execute-adjudication-followups`
- `reconcile-control-state`

## Governed Bundles

Current governed bundle wrappers include:

- `round-close-chain`
- `round-close-chain-then-hard-pivot`

Bundle rules:

- bundle route semantics must be registry-owned
- bundle step templates must be registry-owned
- bundle payload field semantics must be registry-owned
- bundles may compose only existing governed commands or bundles
- bundles may not write durable truth directly outside those governed steps
- bundles must stay bounded, audit-visible, and smoke-proven
