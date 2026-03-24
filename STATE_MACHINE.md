# Session Memory State Machine

Date: 2026-03-24
Scope: Control-state transitions for the repo governance kernel

## Goal

Make the kernel's state model explicit enough that the
[`PRODUCT.md`](./PRODUCT.md) contract can be enforced without inventing
semantics ad hoc.

Today the system is:

- state-machine oriented
- bounded registry-owned execution

Today it is only partially:

- state-machine enforced
- not a general autonomous rewrite engine

## Core Position

The kernel should not be modeled as one giant state.

It should be modeled as several coordinated state domains:

1. objective-line state
2. project phase state
3. round state
4. task-contract state
5. exception-contract state
6. memory freshness state

This keeps ownership local and illegal combinations easier to detect.

## 1. Objective-Line State

This domain answers:

- which objective is active
- whether an objective is historical, superseded, closed, or invalidated

### Objective Status

- `proposed`
- `active`
- `superseded`
- `closed`
- `invalidated`

### Objective Guards

An objective should not become `active` unless it has:

- a clear problem statement
- success criteria
- explicit non-goals
- an initial phase assignment

### Objective Consequences

When an objective becomes `superseded`, `closed`, or `invalidated`:

- open rounds tied to it must be resolved explicitly
- active exception contracts tied to it must be resolved explicitly
- no fake active-objective projection should remain

## 2. Project Phase State

This domain answers whether the project is mainly discovering or mainly
executing.

### Phase States

- `exploration`
- `execution`
- `paused`

### Phase Guards

`exploration -> execution` should usually require:

- one active objective
- explicit non-goals
- a validation path
- one bounded open round or an explicit round bootstrap

`execution -> exploration` or `execution -> paused` should usually require:

- an explicit reason
- explicit round review or bounded round rewrite when open rounds still exist

### Phase Consequences

Phase change should not silently launder stale round truth. Open rounds must be
reviewed or rewritten through explicit owner-layer commands.

## 3. Round State

This domain answers what bounded execution slice is active and whether it is
still honest.

### Round States

- `draft`
- `active`
- `blocked`
- `validation_pending`
- `captured`
- `closed`
- `abandoned`

### Round Guards

A round should not become `active` unless it has:

- objective linkage
- explicit scope
- concrete deliverable
- intended validation path

A round should not become `captured` or `closed` unless:

- worktree enforcement passes
- audit is not blocked
- validation or abandonment history makes the transition honest

### Round Consequences

When a round becomes `blocked`, blockers must be explicit.

When a round becomes `closed` or `abandoned`, unfinished work must not remain
disguised as active progress.

## 4. Task-Contract State

This domain answers what concrete task is currently authorized inside one open
round.

### Task-Contract States

- `draft`
- `active`
- `completed`
- `abandoned`
- `invalidated`

### Task-Contract Guards

A task contract should not become `active` unless it has:

- round linkage
- objective linkage aligned with the round
- explicit path scope inside round scope
- explicit allowed changes
- explicit forbidden changes
- explicit completion criteria

### Task-Contract Consequences

When task contracts are active:

- they should narrow implementation authority beneath the round scope
- they should appear in assembled and role-specific context
- promotion or closure should not strand them silently

Task contracts remain a control layer, not free authorization for arbitrary
automatic rewrite.

## 5. Exception-Contract State

This domain answers whether temporary deviation is still active.

### Exception-Contract States

- `proposed`
- `active`
- `retired`
- `invalidated`

### Exception-Contract Guards

An exception contract should not become `active` unless it has:

- reason
- risk
- owner scope
- exit condition

### Exception-Contract Consequences

Active exception contracts should affect review and enforcement.

Retired or invalidated exception contracts should remain historical evidence,
not active authorization.

## 6. Memory Freshness State

This domain answers whether assembled orientation state still matches the live
workspace.

### Freshness States

- `fresh`
- `live_match_dirty`
- `fresh_snapshot_behind`
- `fresh_snapshot_behind_dirty`
- `stale`
- `workspace_unavailable`

This is not a substitute for objective or round state. It is only the workspace
freshness layer.

## Transition Events

The main event types that should drive state change are:

- `open_objective`
- `close_objective`
- `record_soft_pivot`
- `record_hard_pivot`
- `set_phase`
- `open_round`
- `rewrite_open_round`
- `update_round_status`
- `open_task_contract`
- `rewrite_open_task_contract`
- `update_task_contract_status`
- `activate_exception_contract`
- `retire_exception_contract`
- `invalidate_exception_contract`
- `refresh_anchor`

The concrete bounded command contract is defined in
[`TRANSITION_COMMANDS.md`](./TRANSITION_COMMANDS.md).

## Drift As Illegal Or Unhealthy State

The system should treat drift as evidence that the current state is dishonest.

Important drift types:

- `objective_drift`
- `round_drift`
- `task_scope_drift`
- `projection_drift`
- `freshness_drift`

Drift is not only an observation. It should influence allowed transitions.

## Audit vs Adjudication vs Repair

These responsibilities must stay separate:

- `audit-control-state`
  - detect dishonest or conflicting state
- `adjudicate-control-state`
  - decide which durable objects remain authoritative
- `reconcile-control-state`
  - rebuild projections only after durable truth is coherent enough to project

Refusing ambiguity in repair is not the same as resolving ambiguity in durable
truth.

## Current Enforcement Status

The implemented bounded subset already does these things:

- stores explicit objective, pivot, round, task-contract, exception-contract,
  and adjudication files
- projects active-objective, active-round, pivot-log, and exception-ledger
- records transition events for implemented transition domains
- audits projection drift and several control honesty failures
- enforces one first worktree gate for promotion and closure
- executes a bounded adjudication follow-up subset through registry-owned
  command and bundle semantics

The implementation still does not do these things:

- provide a fully unified transition engine across every domain
- infer durable rewrites from verdict prose alone
- execute broader multi-object or multi-round rewrites automatically without
  explicit bounded semantics
- make every mutation path hit the same full enforcement depth

This gap should stay explicit.

## Design Consequence

The next move is not "more states for their own sake".

It is:

- keep the state domains small and honest
- make transition guards consumable by enforcement
- let task contracts become real execution gates
- continue pushing execution semantics into the registry instead of into local
  branches
