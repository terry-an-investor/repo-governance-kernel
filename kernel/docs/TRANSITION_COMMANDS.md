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
- `draft-external-target-shadow-scope`
- `assess-host-adoption`
- `capture-snapshot`
- `audit-control-state`
- `enforce-worktree`
- `adjudicate-control-state`
- `execute-adjudication-followups`
- `reconcile-control-state`

### `refresh-anchor`

Refresh the governed host's current-task anchor against the live workspace.

### `render-live-workspace`

Render a non-durable workspace projection from the current anchor and git state.

### `draft-external-target-shadow-scope`

Draft the smallest honest round/task boundary for one external target repo
before running `assess-host-adoption`.

This command is an owner-layer drafting surface:

- it requires one active objective, one open round, and one active task contract
- it inspects one explicit external workspace root live, without mutating that repo
- it suggests round and task-contract `paths` directly from the currently observed dirty paths
- it writes one readable draft artifact and suggested command sequence, not durable control truth
- its artifact contract is separate from the later shadow assessment report so drafting and assessment stay distinguishable in the owner layer
- it exists to reduce hand-authored ambiguity in `external-target-shadow` setup before the real assessment command runs

### `assess-host-adoption`

Assess one governed host in shadow mode and write a readable adoption report.

This command is an owner-layer observation surface:

- it requires one active objective, one open round, and one active task contract
- it inspects the current live workspace through the governed anchor
- it resolves one explicit assessment mode:
  - `governed-host-shadow`
  - `external-target-shadow`
- it interprets active round and task-contract `paths` against dirty paths relative to the assessed workspace root
- it always writes one assessment artifact rather than durable control truth
- it does not reuse the external-target drafting artifact contract; the draft and final report are separate owner-layer artifacts
- it may write the report into the governed host repo or to an explicit external output path
- it does not authorize arbitrary live-host mutation or general autonomous rewrite

### `capture-snapshot`

Capture one bounded historical snapshot from the current anchored workspace state.

### `enforce-worktree`

Block dishonest promotion when the live worktree no longer matches active
control truth.

This command normally inspects the workspace root from the governed anchor, but
it may also accept one explicit `workspace_root` override when the execution
environment differs from the durable host path, such as CI runners.

## Governed Bundles

Current governed bundle wrappers include:

- `round-close-chain`
- `round-close-chain-then-hard-pivot`
- `assess-external-target-once`

Bundle rules:

- bundle route semantics must be registry-owned
- bundle step templates must be registry-owned
- bundle payload field semantics must be registry-owned
- bundles may compose only existing governed commands or bundles
- bundles may not write durable truth directly outside those governed steps
- bundles must stay bounded, audit-visible, and smoke-proven

## Bounded Intent Surfaces

Current bounded natural-language wrappers include:

- `assess-external-target-from-intent`

Intent-surface rules:

- the intent parser must compile only into an existing governed command or bundle
- the parser may not introduce new mutation authority beyond the compiled surface
- accepted intent classes must stay narrow, explicit, and smoke-proven
- rejected requests must fail closed when they imply broader monitoring or freeform mutation
- `assess-external-target-from-intent` currently compiles only one-time external-target assessment requests into `assess-external-target-once`
