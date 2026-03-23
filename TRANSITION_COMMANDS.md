# Session Memory Transition Commands

Date: 2026-03-23
Scope: Canonical transition command surface for the coding control system

## Goal

Freeze the command surface that should eventually drive the control state
machine.

This document does not implement enforcement. It defines:

- command names
- required inputs
- guards
- side effects
- canonical file ownership

## Design Position

Commands should map to state transitions, not to ad hoc file edits.

That means:

- each command owns one honest transition
- each command has explicit guards
- each command has defined write targets
- side effects are part of the contract, not operator folklore

## Command Domains

The minimal command surface should cover:

1. objective-line transitions
2. phase transitions
3. round transitions
4. exception-contract transitions
5. anchor maintenance
6. control diagnostics and adjudication

## 1. Objective-Line Commands

### `open-objective`

Purpose:

- create one new objective and optionally make it active

Required inputs:

- `project_id`
- `title`
- `problem`
- `success_criteria`
- `non_goals`
- `phase`

Primary writes:

- `projects/<project_id>/memory/objectives/<timestamp>-<slug>.md`
- `projects/<project_id>/control/active-objective.md`

Guards:

- objective must have problem, success criteria, and non-goals
- if marked active, it must have a valid phase
- no other durable active objective may already exist

Side effects:

- update active objective control file
- add objective id to the active control state

### `close-objective`

Purpose:

- move the active objective to `closed` or `invalidated`

Required inputs:

- `project_id`
- `objective_id`
- `closing_status`
- `reason`
- optional `evidence`

Primary writes:

- objective file frontmatter/body update
- `control/active-objective.md`
- `control/pivot-log.md`

Guards:

- referenced objective must match both control and durable active objective truth
- closing status must be `closed` or `invalidated`
- no durable `draft`, `active`, `blocked`, or `validation_pending` round may remain tied to the objective
- no active exception contract may remain tied to the objective

Side effects:

- remove `control/active-objective.md`
- leave the project with zero active objectives when no successor mainline exists
- keep `pivot-log.md` honest about the absence of an active lineage

## 2. Pivot Commands

### `record-soft-pivot`

Purpose:

- update the active objective line without replacing objective identity

Required inputs:

- `project_id`
- `objective_id`
- `trigger`
- `change_summary`
- `identity_rationale`
- optional revised objective fields:
  - `title`
  - `summary`
  - `problem`
  - `success_criteria`
  - `non_goals`
  - `why_now`
  - `phase`
  - `risks`
  - `paths`
- optional `evidence_refs`

Primary writes:

- active objective durable file update
- `projects/<project_id>/memory/pivots/<timestamp>-<slug>.md`
- `projects/<project_id>/control/pivot-log.md`
- `projects/<project_id>/control/active-objective.md`

Guards:

- referenced objective must match both control and durable active objective truth
- at least one material objective field must change
- resulting problem, success criteria, non-goals, and phase must remain present
- if resulting phase is `execution`, one durable open round must stay aligned to the same objective
- if an open round remains while objective-shape fields change, the round review path must be recorded explicitly
- identity rationale must be recorded because the system cannot infer whether a hard pivot was required

Side effects:

- update the durable active objective in place
- refresh `control/active-objective.md`
- record a durable pivot that explains both the change and the preserved objective identity
- force explicit round review notes instead of silently mutating round contracts

### `record-hard-pivot`

Purpose:

- replace the active objective line with a new objective

Required inputs:

- `project_id`
- `previous_objective_id`
- new objective fields:
  - `title`
  - `problem`
  - `success_criteria`
  - `non_goals`
  - `phase`
- `trigger`
- `evidence_refs`

Primary writes:

- new objective file
- previous objective file update
- pivot file
- `control/active-objective.md`
- `control/pivot-log.md`

Guards:

- previous objective must exist and be active
- new objective must satisfy the same minimum fields as `open-objective`
- previous objective must match the control and durable active objective line
- no durable `active`, `blocked`, or `validation_pending` round may remain tied
  to the previous objective

Side effects:

- supersede the previous objective
- re-anchor control state to the new objective
- review active round contracts
- invalidate or retire stale exception contracts when required

## 3. Phase Commands

### `set-phase`

Purpose:

- change project phase explicitly

Required inputs:

- `project_id`
- `phase`
- `reason`

Primary writes:

- `control/active-objective.md`
- optional transition event record

Guards:

- phase must be one of:
  - `exploration`
  - `execution`
  - `paused`
- `exploration -> execution` requires:
  - active objective
  - non-goals
  - one validation path
- `execution -> exploration` requires:
  - explicit mismatch or ambiguity reason

Side effects:

- re-evaluate active round state when phase changes materially

## 4. Round Commands

### `open-round`

Purpose:

- create one bounded execution contract and make it active

Required inputs:

- `project_id`
- `objective_id`
- `title`
- `scope`
- `deliverable`
- `validation_plan`

Primary writes:

- `projects/<project_id>/memory/rounds/<timestamp>-<slug>.md`
- `projects/<project_id>/control/active-round.md`

Guards:

- linked objective must be active
- scope must be explicit
- validation plan must be present

### `update-round-status`

Purpose:

- move the active round across its lifecycle

Required inputs:

- `project_id`
- `round_id`
- `status`
- optional `reason`

Allowed target status values:

- `blocked`
- `validation_pending`
- `captured`
- `closed`
- `abandoned`

Primary writes:

- round contract file update
- `control/active-round.md`

Guards:

- round must exist
- status transition must be legal from the current round status

Side effects:

- `blocked` should require blocker recording
- `closed` should require validation or explicit abandonment history

### `refresh-round`

Purpose:

- adjust round metadata without changing round identity

Required inputs:

- `project_id`
- `round_id`
- one or more mutable fields:
  - `scope`
  - `deliverable`
  - `validation_plan`
  - `risks`

Primary writes:

- round contract file
- `control/active-round.md`

Guards:

- round must be active or blocked
- refresh must not quietly perform a hard pivot

## 5. Exception-Contract Commands

### `activate-exception-contract`

Purpose:

- create or promote an exception contract to active debt

Required inputs:

- `project_id`
- `title`
- `reason`
- `risk`
- `owner_scope`
- `exit_condition`

Primary writes:

- `projects/<project_id>/memory/exception-contracts/<timestamp>-<slug>.md`
- `projects/<project_id>/control/exception-ledger.md`

Guards:

- all required fields must be present

### `retire-exception-contract`

Purpose:

- mark an exception contract as retired

Required inputs:

- `project_id`
- `exception_contract_id`
- `reason`

Primary writes:

- exception-contract file update
- exception ledger update

### `invalidate-exception-contract`

Purpose:

- mark an exception contract invalid because a pivot or other state change made it
  obsolete

Required inputs:

- `project_id`
- `exception_contract_id`
- `reason`
- optional `pivot_id`

Primary writes:

- exception-contract file update
- exception ledger update

## 6. Anchor And Capture Commands

### `refresh-anchor`

Purpose:

- refresh live workspace anchor facts without rewriting narrative state

Primary writes:

- `projects/<project_id>/current/current-task.md`

This command already has partial implementation.

### `capture-snapshot`

Purpose:

- create a historical snapshot from the current control and workspace state

Primary writes:

- `projects/<project_id>/snapshots/<timestamp>-<slug>.md`

This command already has partial implementation.

## 7. Transition Event Recording

The system should eventually record transition events as first-class durable
objects.

Suggested write target:

- `projects/<project_id>/memory/transition-events/<timestamp>-<slug>.md`

Suggested object type:

- `transition-event`

These records should preserve:

- command name
- target object ids
- previous state
- next state
- operator reason
- guard outcome
- side effects performed

## Related Repair Command

`reconcile-control-state` is not a transition command.

It is a repair path that rebuilds projected control files from durable memory:

- `control/active-objective.md`
- `control/pivot-log.md`
- `control/active-round.md`

It should:

- trust durable objective, pivot, and round records over stale projected files
- refuse repair when durable truth is ambiguous
- avoid inventing a new transition event when it is only restoring projection

## Related Diagnostic And Adjudication Commands

### `audit-control-state`

Purpose:

- detect dishonest, incomplete, or conflicting control state without mutating it

It should report at least:

- durable objective or round ambiguity
- projection drift between durable truth and control files
- current-task drift where the main orientation file no longer mentions the
  active durable objective or active durable round
- exception-ledger projection drift against durable exception-contract records
- execution phase without one bounded open round
- blocked rounds without blockers
- missing control surfaces such as constitution or exception ledger
- placeholder control surfaces that still do not restore real project law
- constitution-derived machine-checkable hooks such as live round-scope
  coverage against dirty paths

### `adjudicate-control-state`

Purpose:

- resolve durable-state conflicts into an explicit control verdict before
  transition commands rewrite durable truth

This is the layer that should answer:

- which objective remains the active mainline
- which open rounds should be closed, split, or invalidated
- which exception contracts should be retired or invalidated
- which historical durable records remain legitimate history versus misleading
  stale state

Suggested primary writes:

- `projects/<project_id>/memory/adjudications/<timestamp>-<slug>.md`
- follow-up updates to the affected durable control objects

Current implementation status:

- records a durable adjudication verdict from the current audit result
- can optionally embed structured round bootstrap fields in the adjudication
  record
- can carry explicit machine-executable follow-up entries in adjudication frontmatter
  `executor_followups`
- still does not decide those follow-up rewrites automatically from verdict text alone

This design still matters because refusing ambiguous repair is not the same
thing as resolving ambiguous durable truth.

### `execute-adjudication-followups`

Purpose:

- execute the safe automatic subset of an adjudication's required follow-up
  transitions

Current implementation status:

- can scaffold missing `control/constitution.md`
- can scaffold missing `control/exception-ledger.md`
- can execute explicit structured follow-ups encoded in adjudication frontmatter
  `executor_followups`
- currently supports structured execution for:
  - `close-objective`
  - `update-round-status`
  - `retire-exception-contract`
  - `invalidate-exception-contract`
- can rerun control audit after those follow-ups
- can open a bounded round when structured round bootstrap fields exist in the
  adjudication record or are passed explicitly
- treats an already-open aligned round as `noop` instead of reopening it
- reports prose-only, unsupported, or underspecified follow-ups as blocked instead of
  pretending they were executed

## Minimal First Implementation Set

The smallest honest set to implement first is:

1. `open-objective`
2. `record-hard-pivot`
3. `open-round`
4. `update-round-status`
5. `activate-exception-contract`

This set is enough to make the control plane materially real.

## Current Implementation Status

The current implementation now includes real enforced slices in three command domains:

- objective-line:
  - `open-objective`
  - `close-objective`
  - `record-soft-pivot`
  - `record-hard-pivot`
- round:
  - `open-round`
  - `update-round-status`
- exception-contract:
  - `activate-exception-contract`
  - `retire-exception-contract`
  - `invalidate-exception-contract`

These slices already do these things:

- write durable `objective`, `pivot`, and `round-contract` files
- write durable `exception-contract` files
- update `control/active-objective.md`, `control/pivot-log.md`, `control/active-round.md`, and `control/exception-ledger.md`
- reject illegal round-status transitions
- refuse hard pivots that would silently outrun a durable still-open round tied to the old objective
- refuse opening a second active objective when a durable active objective already exists
- refuse retiring or invalidating exception contracts that are not currently active
- preserve existing round metadata when rewriting status
- record `transition-event` files for both objective-line and round operations
- record `transition-event` files for exception-contract operations

It does not yet implement:

- explicit phase transition commands
- adjudication-driven automatic follow-up rewrites
- automatic round rewrites from soft-pivot or hard-pivot verdicts

## Explicit Non-Goal

Do not implement all commands at once.

Freeze the command surface first, then implement one small coherent slice with
real file writes and guard checks.
