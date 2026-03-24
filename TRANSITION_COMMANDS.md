# Session Memory Transition Commands

Date: 2026-03-24
Scope: Canonical transition command surface for the repo governance kernel

## Goal

Freeze the bounded command surface that drives the kernel state machine defined
by [`PRODUCT.md`](./PRODUCT.md) and [`STATE_MACHINE.md`](./STATE_MACHINE.md).

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

## Primitive Command Intent

### `open-objective`

Create one new objective and optionally make it active.

### `close-objective`

Move the active objective to `closed` or `invalidated`.

### `record-soft-pivot`

Rewrite the active objective line without changing objective identity.

### `record-hard-pivot`

Replace the active objective line with a new objective.

### `set-phase`

Change project phase explicitly and only through owner-layer semantics.

### `open-round`

Create one bounded execution contract and make it active.

### `rewrite-open-round`

Rewrite one open round contract without changing round identity.

### `refresh-round-scope`

Refresh one open round's path scope from live evidence or explicit path edits.

### `update-round-status`

Move one round across its legal lifecycle.

### `open-task-contract`

Create one durable task contract inside an open round.

### `rewrite-open-task-contract`

Rewrite one open task contract without changing task identity.

### `update-task-contract-status`

Move one task contract across its bounded lifecycle.

### `activate-exception-contract`

Create or promote an exception contract to active temporary debt.

### `retire-exception-contract`

Resolve one active exception contract as retired.

### `invalidate-exception-contract`

Mark one active exception contract invalid because later truth made it obsolete.

### `refresh-anchor`

Refresh the durable orientation bullets in `current/current-task.md`.

### `render-live-workspace`

Render a non-durable view of live git/worktree state.

### `draft-external-target-shadow-scope`

Draft the smallest honest round/task boundary for one external target repo
before running `assess-host-adoption`.

This command is an owner-layer drafting surface:

- it requires one active objective, one open round, and one active task contract
- it inspects one explicit external workspace root live, without mutating that repo
- it suggests round and task-contract `paths` directly from the currently observed dirty paths
- it writes one readable draft artifact and suggested command sequence, not durable control truth
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
- it may write the report into the governed host repo or to an explicit external output path
- it does not authorize arbitrary live-host mutation or general autonomous rewrite

### `capture-snapshot`

Capture one historical snapshot from current control and workspace state.

### `audit-control-state`

Detect dishonest or conflicting control state without mutation.

### `enforce-worktree`

Block dishonest promotion when the live worktree no longer matches active
control truth.

### `adjudicate-control-state`

Record an explicit durable verdict when control truth conflicts.

### `execute-adjudication-followups`

Execute only the explicit bounded follow-up subset the repo can compile safely.

**`reconcile-control-state`**

Rebuild projected control files from already coherent durable truth.

## Shared Guard Expectations

The command surface should keep these expectations uniform:

- no second active objective
- no execution without bounded round authority
- no task-contract scope outside round scope
- no promotion or closure while audit or worktree enforcement is blocked
- no objective close or hard pivot that strands open rounds or active exception
  contracts
- no rewrite that changes object identity silently

Those guards belong in the registry and runtime, not in doc-only prose.

## Governed Bundles

Bundles are allowed only as governed wrappers.

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

The ban is on private bundle semantics, not on all bundle composition.

## Adjudication Execution Boundary

`execute-adjudication-followups` is allowed to run only when follow-up intent is
already structured enough to map onto the bounded command or bundle surface.

Allowed pattern classes today include bounded:

- objective rewrite via soft pivot
- round rewrite and close-chain flows
- task-contract rewrite and status flows
- exception-contract retirement or invalidation flows
- phase entry/bootstrap and bounded phase fallback flows
- predecessor-round close plus hard-pivot replacement flow

It must continue to reject:

- prose-only follow-ups
- ambiguous target resolution
- undeclared payload keys
- ungoverned bundles

## Current Implementation Status

The implemented subset already has real owner-layer runtime coverage across:

- objective-line commands
- phase command
- round commands
- task-contract commands
- exception-contract commands
- bounded governed bundle execution
- bounded adjudication follow-up compilation and execution

It still does not provide:

- general automatic rewrite from adjudication prose
- arbitrary multi-object or multi-round rewrite execution
- a fully unified transition engine across every repository mutation path

Those remain out of scope until they become explicit owner-layer semantics.

## Explicit Non-Goal

Do not expand the command surface casually.

If a new behavior is only a composition of existing governed commands, it
should normally stay a governed bundle or a higher-level compiler plan, not a
new primitive command.
