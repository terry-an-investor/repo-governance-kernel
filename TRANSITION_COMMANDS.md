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
4. workaround transitions
5. anchor maintenance

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

Primary writes:

- objective file frontmatter/body update
- active objective control file update

Guards:

- the objective must exist
- closing status must be `closed` or `invalidated`

## 2. Pivot Commands

### `record-soft-pivot`

Purpose:

- update the active objective line without replacing objective identity

Required inputs:

- `project_id`
- `objective_id`
- `trigger`
- `change_summary`
- `evidence_refs`

Primary writes:

- `projects/<project_id>/memory/pivots/<timestamp>-<slug>.md`
- `projects/<project_id>/control/pivot-log.md`
- active objective file update

Guards:

- referenced objective must be active
- change must not require a new objective id

Side effects:

- invalidate or review any active round whose scope no longer matches

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
- invalidate or retire stale workarounds when required

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

## 5. Workaround Commands

### `activate-workaround`

Purpose:

- create or promote a workaround to active debt

Required inputs:

- `project_id`
- `title`
- `reason`
- `risk`
- `owner_scope`
- `exit_condition`

Primary writes:

- `projects/<project_id>/memory/workarounds/<timestamp>-<slug>.md`
- `projects/<project_id>/control/workaround-ledger.md`

Guards:

- all required fields must be present

### `retire-workaround`

Purpose:

- mark a workaround as retired

Required inputs:

- `project_id`
- `workaround_id`
- `reason`

Primary writes:

- workaround file update
- workaround ledger update

### `invalidate-workaround`

Purpose:

- mark a workaround invalid because a pivot or other state change made it
  obsolete

Required inputs:

- `project_id`
- `workaround_id`
- `reason`
- optional `pivot_id`

Primary writes:

- workaround file update
- workaround ledger update

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

## Minimal First Implementation Set

The smallest honest set to implement first is:

1. `open-objective`
2. `record-hard-pivot`
3. `open-round`
4. `update-round-status`
5. `activate-workaround`

This set is enough to make the control plane materially real.

## Current Implementation Status

The current implementation now includes two real enforced slices:

- objective-line:
  - `open-objective`
  - `record-hard-pivot`
- round:
  - `open-round`
  - `update-round-status`

These slices already do these things:

- write durable `objective`, `pivot`, and `round-contract` files
- update `control/active-objective.md`, `control/pivot-log.md`, and `control/active-round.md`
- reject illegal round-status transitions
- refuse hard pivots that would silently outrun a durable still-open round tied to the old objective
- refuse opening a second active objective when a durable active objective already exists
- preserve existing round metadata when rewriting status
- record `transition-event` files for both objective-line and round operations

It does not yet implement:

- soft-pivot transition commands
- workaround transition commands
- explicit phase transition commands
- a unified transition engine shared across every command domain

## Explicit Non-Goal

Do not implement all commands at once.

Freeze the command surface first, then implement one small coherent slice with
real file writes and guard checks.
