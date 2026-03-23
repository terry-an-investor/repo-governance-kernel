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
4. exception-contract state
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

An explicit close or invalidation can honestly leave the project with:

- zero active objectives
- no `control/active-objective.md`
- a `pivot-log.md` that shows no active lineage until a new objective is opened

### Guards

An objective should not become `active` unless it has:

- a clear problem statement
- success criteria
- explicit non-goals
- an initial phase assignment

### Side Effects

When an objective becomes `superseded`:

- active round contracts tied to it should be reviewed
- stale exception contracts should be checked for invalidation
- compiled contexts should re-anchor to the new objective

When an objective becomes `closed` or `invalidated` without a successor:

- no fake active-objective projection should remain
- open rounds and active exception contracts tied to that objective must be resolved first

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
- exception-contract debt should not silently carry forward as architecture truth

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

## 4. Exception-Contract State

This domain answers:

- whether a temporary deviation is still active
- whether it has been retired
- whether a pivot invalidated it

### Exception-Contract States

- `proposed`
- `active`
- `retired`
- `invalidated`

### Exception-Contract Transitions

- `proposed -> active`
- `active -> retired`
- `active -> invalidated`

### Guards

An exception contract should not become `active` unless it has:

- reason
- risk
- intended owner scope
- exit condition

### Side Effects

Active exception contracts should influence:

- reviewer contexts
- orchestrator contexts
- architecture discussions

Retired or invalidated exception contracts should not remain in default active context
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
- `activate_exception_contract`
- `retire_exception_contract`
- `invalidate_exception_contract`
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

## Audit vs Adjudication vs Repair

These three responsibilities must stay separate:

- `audit-control-state`
  - detect dishonest or conflicting state
- `adjudicate-control-state`
  - decide which durable objects remain authoritative and which must be
    closed, superseded, split, or invalidated
- `reconcile-control-state`
  - rebuild projected control files only after durable truth is already
    coherent enough to project

Refusing ambiguity belongs to repair. It is not a substitute for adjudication.

## State-Machine Enforcement Gap

Current implementation already does these things:

- stores explicit objective and pivot files
- stores explicit exception-contract files
- stores exception ledger state
- compiles contexts from active control files
- computes freshness verdicts for assembled packets
- enforces a first objective-line slice through:
  - `open-objective`
  - `close-objective`
  - `record-soft-pivot`
  - `record-hard-pivot`
  - only one durable active objective is allowed
  - zero durable active objectives is legal after an explicit objective close
  - hard pivots reject durable still-open rounds tied to the previous objective
  - objective close rejects durable open rounds and active exception contracts tied to the objective
  - soft pivots preserve the same durable objective id while refreshing durable and projected active-objective state together
  - soft pivots can rewrite one open round durably through `rewrite-open-round`
    when objective-shape changes must stay aligned without changing round identity
- enforces one first round slice through:
  - `open-round`
  - `update-round-status`
  - `rewrite-open-round`
  - legal round transitions are rejected
  - round-contract metadata is preserved during status rewrites
  - one open round contract can be durably rewritten while preserving round id
- can repair projected control files from durable state through:
  - `reconcile-control-state`
  - only when durable objective and round truth is unambiguous
- can audit current control honesty through:
  - `audit-control-state`
  - projection drift
  - exception-ledger projection drift against durable exception-contract truth
  - execution without a bounded round
  - missing control surfaces such as constitution or exception ledger
  - placeholder constitution files that still lack real invariants
- now has one first automatic enforcement gate through:
  - `enforce-worktree`
  - dirty non-control paths outside the active round scope become an explicit blocked state
  - dirty projected control files that drift from durable truth become an explicit blocked state
  - constitution-declared guarded exception paths now require one active exception contract to cover them before promotion stays honest
  - blocked control audit prevents round promotion from pretending the worktree is honest
  - repo-local git hooks reuse the same enforcement owner layer before commit or push
  - this enforcement is harness-agnostic rather than dependent on native Claude-style `PreToolUse` or `PostToolUse` hooks
- enforces one first exception-contract slice through:
  - `activate-exception-contract`
  - `retire-exception-contract`
  - `invalidate-exception-contract`
  - projects `control/exception-ledger.md` from durable exception-contract records
  - rejects retire/invalidate transitions when the contract is not currently active
- can record adjudication verdicts through:
  - `adjudicate-control-state`
  - stores explicit adjudication records from the current audit/conflict set
  - can store bounded higher-level machine-readable plan contracts in adjudication
    frontmatter before they are compiled into explicit executor followups
- can execute the safe automatic subset of adjudication follow-ups through:
  - `execute-adjudication-followups`
  - scaffolds missing control surfaces
  - compiles bounded `executor_plan_contracts` into explicit command payloads
    before executing them
  - can resolve bounded exception-contract plan targets from adjudication
    durable `Objects Invalidated` when the selected object set maps
    deterministically to active exception contracts
  - executes explicit structured follow-up contracts from adjudication frontmatter `executor_followups`
    for a bounded subset of existing transition commands
  - can run one bounded multi-step `round-close-chain` bundle that closes a round through legal intermediate states
  - can rewrite one open round, retire or invalidate one exception contract,
    refresh one round scope, change phase explicitly, and then open one
    successor round when the adjudication record is structured enough
  - blocks prose-only follow-up requests instead of guessing durable rewrites from verdict text
  - leaves underspecified round follow-ups blocked until explicit inputs exist
- now enforces explicit phase changes through:
  - `set-phase`
  - entering `execution` requires one bounded round or command-owned bootstrap
  - leaving `execution` with open rounds requires explicit scope review notes or
    explicit round rewrites
- now enforces explicit scope repair through:
  - `refresh-round-scope`
  - rewrites durable round `paths` and active-round projection from live dirty-path evidence
- now rejects `open-round` when the active objective is not already in `execution`
- records transition-event files for round operations

Current implementation does not yet do these things:

- reject illegal transitions outside the implemented round slice
- apply adjudication verdicts as a fully general automatic rewrite engine
- infer executable follow-up rewrites directly from verdict prose without explicit structured contracts
- auto-close or re-scope active rounds when an allowed hard pivot demands it
- auto-invalidate or automatically replace stale round contracts after hard pivots
  or broader verdict bundles without an explicit rewrite contract
- enforce the same worktree gate before every repository mutation path such as commit or push
- cover objective, pivot, round, and exception-contract domains with the same unified enforcement depth
- provide a richer harness integration layer for runtimes that do expose native hooks, without making correctness depend on them

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
