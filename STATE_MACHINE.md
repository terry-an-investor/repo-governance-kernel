# Session Memory State Machine

Date: 2026-03-23
Scope: Control-state transitions for the coding control system

## Goal

Make the control system's state model explicit enough that later enforcement
logic can be implemented without inventing semantics ad hoc.

This document exists because the current system already has state-shaped
concepts, but they are only partially enforced in code.

Today the system is:

- state-machine oriented

Today it is only partially:

- state-machine enforced

## Core Position

The control system should not be modeled as one giant state.

It should be modeled as several coordinated state domains:

1. objective-line state
2. project phase state
3. round state
4. workaround state
5. memory freshness state

This keeps transitions local and makes invalid combinations easier to detect.

## 1. Objective-Line State

This domain answers:

- which objective is active
- whether an objective is historical, superseded, or closed
- whether a pivot changed the active line

### Objective Status

Suggested states:

- `proposed`
- `active`
- `superseded`
- `closed`
- `invalidated`

### Objective Transitions

- `proposed -> active`
  - when the project is willing to execute against this objective
- `active -> superseded`
  - when a hard pivot replaces it
- `active -> closed`
  - when the objective is genuinely completed or intentionally ended
- `active -> invalidated`
  - when the framing is proven wrong without a direct successor

### Guards

An objective should not become `active` unless it has:

- a clear problem statement
- success criteria
- explicit non-goals
- an initial phase assignment

### Side Effects

When an objective becomes `superseded`:

- active round contracts tied to it should be reviewed
- stale workarounds should be checked for invalidation
- compiled contexts should re-anchor to the new objective

## 2. Project Phase State

This domain answers:

- whether the project is mainly discovering direction
- or mainly executing a committed direction

### Phase States

- `exploration`
- `execution`
- `paused`

`paused` is not product completion. It means active execution is intentionally
halted while preserving the control state.

### Phase Transitions

- `exploration -> execution`
  - when the objective is concrete enough to constrain implementation
- `execution -> exploration`
  - when the current framing is no longer good enough and discovery resumes
- `execution -> paused`
  - when the project is intentionally suspended
- `paused -> exploration`
- `paused -> execution`

### Guards

`exploration -> execution` should usually require:

- one active objective
- explicit non-goals
- one initial validation plan
- at least one bounded round definition or equivalent contract

`execution -> exploration` should usually require:

- an explicit reason
- a recorded mismatch, pivot trigger, or unresolved objective ambiguity

### Side Effects

When moving from `execution -> exploration`:

- open round contracts should be re-evaluated
- workaround debt should not silently carry forward as architecture truth

## 3. Round State

This domain answers:

- what the current bounded execution slice is
- whether the slice is still honest

### Round States

- `draft`
- `active`
- `blocked`
- `validation_pending`
- `captured`
- `closed`
- `abandoned`

### Round Transitions

- `draft -> active`
- `active -> blocked`
- `active -> validation_pending`
- `validation_pending -> captured`
- `captured -> closed`
- `active -> abandoned`
- `blocked -> abandoned`
- `blocked -> active`

### Guards

A round should not become `active` unless it has:

- objective linkage
- allowed scope
- concrete deliverable
- intended validation path

A round should not become `closed` unless one of these is true:

- validation result is recorded
- explicit abandonment reason exists
- a successor round or pivot explicitly absorbs the unfinished work

### Side Effects

When a round is marked `blocked`:

- blockers should be explicit
- next-step generation should not pretend execution is still straightforward

When a round is marked `abandoned`:

- the reason should be preserved
- unfinished work should not remain disguised as active progress

## 4. Workaround State

This domain answers:

- whether a compromise is still active
- whether it has been retired
- whether a pivot invalidated it

### Workaround States

- `proposed`
- `active`
- `retired`
- `invalidated`

### Workaround Transitions

- `proposed -> active`
- `active -> retired`
- `active -> invalidated`

### Guards

A workaround should not become `active` unless it has:

- reason
- risk
- intended owner scope
- exit condition

### Side Effects

Active workarounds should influence:

- reviewer contexts
- orchestrator contexts
- architecture discussions

Retired or invalidated workarounds should not remain in default active context
unless they are still needed as historical warning.

## 5. Memory Freshness State

This domain already has partial implementation.

### Freshness States

- `fresh`
- `live_match_dirty`
- `fresh_snapshot_behind`
- `fresh_snapshot_behind_dirty`
- `stale`
- `workspace_unavailable`

This domain is not the same as round or objective state.

It only answers whether the assembled packet still matches the live workspace
anchor and how much it can be trusted as current truth.

## Transition Events

The main event types that should drive state transitions are:

- `open_objective`
- `promote_hypothesis`
- `record_soft_pivot`
- `record_hard_pivot`
- `open_round`
- `mark_blocked`
- `mark_validation_pending`
- `capture_snapshot`
- `close_round`
- `abandon_round`
- `activate_workaround`
- `retire_workaround`
- `invalidate_workaround`
- `refresh_anchor`

These events should become the future command surface.

The concrete command contract is defined in [`TRANSITION_COMMANDS.md`](./TRANSITION_COMMANDS.md).

## Drift As Illegal Or Unhealthy State

The system should treat drift as evidence that the current state is dishonest.

Important drift types:

- `round_drift`
  - live work exceeds declared round boundary
- `objective_drift`
  - active work no longer serves the active objective
- `governance_drift`
  - round progress, validation, or control artifacts lag behind real state
- `freshness_drift`
  - packet anchor no longer matches the live workspace

Drift is not only an observation. It should influence allowed transitions.

## State-Machine Enforcement Gap

Current implementation already does these things:

- stores explicit objective and pivot files
- stores workaround ledger state
- compiles contexts from active control files
- computes freshness verdicts for assembled packets
- enforces a first objective-line slice through:
  - `open-objective`
  - `record-hard-pivot`
  - only one durable active objective is allowed
  - hard pivots reject durable still-open rounds tied to the previous objective
- enforces one first round slice through:
  - `open-round`
  - `update-round-status`
  - legal round transitions are rejected
  - round-contract metadata is preserved during status rewrites
- records transition-event files for round operations

Current implementation does not yet do these things:

- reject illegal transitions outside the implemented round slice
- auto-close or re-scope active rounds when an allowed hard pivot demands it
- auto-invalidate stale round contracts after hard pivots
- enforce guards before phase changes
- update status fields through a single transition engine
- cover objective, pivot, round, and workaround domains with the same enforcement depth

This gap should remain explicit until enforcement exists.

## Design Consequence

The next architecture move should not be "add more memory types first".

It should be:

- define transition commands
- define guards
- define side effects
- make illegal or dishonest control states visible

Only then does the system become a real coding control plane rather than a
well-structured memory workspace.
