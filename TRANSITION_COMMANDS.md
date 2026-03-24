# Session Memory Transition Commands

Date: 2026-03-23
Scope: Canonical transition command surface for the coding control system

## Goal

Freeze the command surface that should eventually drive the control state
machine for the memory-driven repo governance control plane defined in
[`PRODUCT.md`](./PRODUCT.md).

The current automation scope is bounded automatic execution.
The current autonomy boundary is not a general autonomous rewrite engine.

This document does not implement enforcement. It defines:

- command names
- required inputs
- guards
- side effects
- canonical file ownership

The command surface is now also mirrored by one machine-readable owner-layer
registry:

- `scripts/transition_specs.py`

The registry still does not encode every full rewrite semantics, but it now owns:

- canonical command names
- command domains
- implementation status
- required inputs
- guard codes
- guard rendering semantics
- write-target semantics
- write targets
- side-effect codes
- transition-command side-effect semantics
- command mutable-field semantics for bounded rewrite primitives
- command executor payload-field semantics for supported automatic commands
- durable owners
- projection owners
- artifact owners
- live inspection owners
- whether a command emits a transition event
- which commands are currently executor-supported
- bounded adjudication plan family names
- adjudication plan target-resolution contracts
- adjudication payload templates and binding resolvers for supported bounded plan families

The current milestone also adds one first enforcement owner layer:

- worktree enforcement before round promotion or closure

The current governed bundle wrappers include:

- `round-close-chain`

## Design Position

Commands should map to state transitions, not to ad hoc file edits.

That means:

- each command owns one honest transition
- each command has explicit guards
- each command has defined write targets
- side effects are part of the contract, not operator folklore
- owner-layer responsibility is registry-owned, not left to per-script private semantics
- bounded rewrite-field semantics must also be registry-owned instead of living
  in private executor or script branches
- supported automatic executor commands should admit only registry-declared
  payload keys and CLI bindings
- bundle wrappers are explicit exceptions:
  - they must be governed explicitly
  - executor bundle dispatch must go through one governed handler registry instead of private branches
  - they must compose existing primitive commands only
  - they must not write durable truth directly
  - they must not invent private semantics outside repo-owned governance

Current implementation status:

- all implemented transition command domains now consume shared registry-backed owner-layer contract assertions
- partial commands must also declare owner-layer fields before they are treated as semantically covered
- command callers should only provide runtime-specific inputs and context; they should not restate registry-owned static guard, write-target, or owner declarations

## Command Domains

The minimal command surface should cover:

1. objective-line transitions
2. phase transitions
3. round transitions
4. task-contract transitions
5. exception-contract transitions
6. anchor maintenance
7. control diagnostics and adjudication

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
- force an explicit round review path instead of silently mutating round contracts
- when the operator chooses the rewrite path, delegate bounded round-contract mutation
  to `rewrite-open-round` instead of relying on manual edits

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

- durable active objective file
- `control/active-objective.md`
- optional transition event record
- optional bounded round contract and `control/active-round.md` when entering
  `execution` through bootstrap
- optional rewritten open round contracts and `control/active-round.md` when
  phase fallback or pause must keep an existing round honest

Guards:

- phase must be one of:
  - `exploration`
  - `execution`
  - `paused`
- `exploration -> execution` requires:
  - active objective
  - non-goals
  - one validation path
  - one bounded open round, either already present or bootstrapped by the command
- `execution -> exploration` requires:
  - explicit mismatch or ambiguity reason
  - explicit round review note or explicit round rewrite when open rounds still
    exist
- `execution -> paused` requires:
  - explicit suspension reason
  - explicit round review note or explicit round rewrite when open rounds still
    exist
- `paused -> execution` requires:
  - one bounded open round, either already present or bootstrapped by the command

Side effects:

- rewrite durable objective phase and active-objective projection together
- emit one transition event
- optionally bootstrap one bounded round when entering `execution`
- optionally rewrite existing open rounds through `rewrite-open-round` when the
  phase change must keep those contracts aligned

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
- linked objective must be in `execution`
- scope must be explicit
- validation plan must be present

### `refresh-round-scope`

Purpose:

- refresh one open round's durable scope paths from live dirty worktree evidence
  or explicit path additions/removals

Required inputs:

- `project_id`
- `reason`
- optional `round_id`

Primary writes:

- durable round contract
- `control/active-round.md`
- transition event record

Guards:

- target round must exist and remain open
- refresh reason must be explicit
- resulting scope path set must be non-empty
- change must be backed by live dirty non-control paths or explicit path edits

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
- `captured` and `closed` must pass automatic worktree enforcement
  - dirty non-control paths must stay inside active round scope
  - dirty projected control files must still match durable truth
  - control audit must not already be blocked

Side effects:

- `blocked` should require blocker recording
- `closed` should require validation or explicit abandonment history
- `captured` or `closed` should fail fast instead of silently promoting a dirty
  dishonest worktree

### `rewrite-open-round`

Purpose:

- rewrite one open round contract without changing round identity

Required inputs:

- `project_id`
- `round_id`
- `reason`
- one or more mutable fields:
  - `title`
  - `summary`
  - `scope`
  - `scope_paths`
  - `deliverable`
  - `validation_plan`
  - `risks`
  - `blockers`
  - `status_notes`

Primary writes:

- round contract file
- `control/active-round.md`
- transition event record

Guards:

- round must remain in one open status
- rewrite reason must be explicit
- rewritten round must still have scope, deliverable, validation plan, and
  scope paths
- rewrite must not quietly perform a hard pivot or change round identity

## 5. Task-Contract Commands

### `open-task-contract`

Purpose:

- create one durable task contract inside an open round without widening round
  authority

Required inputs:

- `project_id`
- `round_id`
- `title`
- `intent`
- `paths`
- `allowed_changes`
- `forbidden_changes`
- `completion_criteria`

Primary writes:

- `projects/<project_id>/memory/task-contracts/<timestamp>-<slug>.md`
- transition event record

Guards:

- target round must exist and remain open
- task-contract objective linkage must align with the referenced round
- task intent must be explicit
- task paths must be explicit
- task paths must stay inside round scope
- allowed changes, forbidden changes, and completion criteria must all be
  present

Side effects:

- record one durable task-level contract beneath round governance
- preserve the round boundary instead of treating task prose as license to
  widen scope

Current implementation status:

- first creation path is implemented
- task contracts are durable Markdown objects and auditable owner-layer inputs
- task contracts can now move through a bounded lifecycle and rewrite in place
- task contracts do not yet compile into general automatic rewrite semantics by
  themselves

### `update-task-contract-status`

Purpose:

- move one task contract through its bounded lifecycle

Required inputs:

- `project_id`
- `task_contract_id`
- `status`
- `reason`

Allowed target status values:

- `active`
- `completed`
- `abandoned`
- `invalidated`

Primary writes:

- task-contract file update
- transition event record

Guards:

- task contract must exist
- task-contract status transition must be legal
- completed task contracts must record at least one resolution entry

### `rewrite-open-task-contract`

Purpose:

- rewrite one open task contract without changing its identity

Required inputs:

- `project_id`
- `task_contract_id`
- `reason`
- one or more mutable fields:
  - `title`
  - `summary`
  - `intent`
  - `paths`
  - `allowed_changes`
  - `forbidden_changes`
  - `completion_criteria`
  - `risks`
  - `status_notes`

Primary writes:

- task-contract file update
- transition event record

Guards:

- task contract must remain in one open status
- rewrite reason must be explicit
- rewritten task contract must still have intent, path scope, allowed changes,
  forbidden changes, and completion criteria
- rewritten task-contract paths must stay inside round scope
- rewrite must preserve task-contract identity

## 6. Exception-Contract Commands

### `activate-exception-contract`

Purpose:

- create or promote an exception contract to active debt

Required inputs:

- `project_id`
- `title`
- `summary`
- `reason`
- `temporary_behavior`
- `risk`
- `owner_scope`
- `exit_condition`

Primary writes:

- `projects/<project_id>/memory/exception-contracts/<timestamp>-<slug>.md`
- `projects/<project_id>/control/exception-ledger.md`

Guards:

- one active objective must exist for the contract to attach honestly
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

Guards:

- referenced exception contract must exist
- referenced exception contract must still be active
- when `pivot_id` is supplied, that pivot must exist

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

## 7. Anchor And Capture Commands

### `refresh-anchor`

Purpose:

- refresh current-task control bullets and stable workspace locator fields
  without rewriting the broader task narrative

Primary writes:

- `projects/<project_id>/current/current-task.md`

It should refresh at least:

- `Objective id`
- `Active round id`
- `Phase`
- `Workspace root`

It should remove any previously committed live-workspace snapshot bullets so
`current/current-task.md` stays a durable control-and-orientation file instead
of pretending to be a live repo projection.

This command already has partial implementation.

Its owner-layer contract is registry-backed:

- durable owner: `current:current-task`
- live inspection owner: `workspace:git-status`

### `render-live-workspace`

Purpose:

- inspect the live repo state and render a separate non-durable workspace
  projection

Primary writes:

- stdout by default
- optional artifact output such as `artifacts/<project_id>/.../live-workspace.md`

It should render at least:

- `Workspace root`
- `Branch`
- `HEAD`
- `Worktree state`
- `Changed path count`
- current `git status --short --branch`

This command keeps live repo truth out of committed `current/current-task.md`
while still giving handoff and debugging flows one reusable workspace
projection primitive.

Its owner-layer contract is registry-backed:

- artifact owner: `artifact:live-workspace-projection`
- live inspection owner: `workspace:git-status`

### `capture-snapshot`

Purpose:

- create a historical snapshot from the current control and workspace state

Primary writes:

- `projects/<project_id>/snapshots/<timestamp>-<slug>.md`

This command already has partial implementation.

Its owner-layer contract is registry-backed:

- artifact owner: `snapshot:historical`
- live inspection owner: `workspace:git-status`

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
- current-task drift where the main orientation file no longer aligns its
  `Objective id`, `Active round id`, or `Phase` bullets with durable control
  truth
- exception-ledger projection drift against durable exception-contract records
- execution phase without one bounded open round
- blocked rounds without blockers
- missing control surfaces such as constitution or exception ledger
- placeholder control surfaces that still do not restore real project law
- constitution-derived machine-checkable hooks such as live round-scope
  coverage against dirty paths

### `enforce-worktree`

Purpose:

- block dishonest promotion when the live worktree no longer matches the active
  round contract or projected control truth

Primary checks:

- dirty non-control paths are covered by active round `paths`
- dirty projected control files still equal the projection implied by durable truth
- dirty `current/current-task.md` still keeps its `Objective id`, `Active round id`,
  and `Phase` bullets aligned with durable control truth
- dirty constitution-guarded exception paths are covered by one active exception contract
- control audit is not already blocked

Primary users:

- `update-round-status` before `captured`
- `update-round-status` before `closed`
- git hooks and CI before commit or push

Current trigger surfaces in this repo:

- `.githooks/pre-commit`
- `.githooks/pre-push`
- `.github/workflows/control-enforcement.yml`

Owner-layer note:

- the canonical enforcement owner is the repository command itself, not a
  harness-native tool hook API
- runtimes with native lifecycle hooks may call this command earlier, but
  correctness must still hold when only repo-local hooks or direct CLI
  invocation exist

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
- can optionally carry higher-level bounded executor plan contracts in
  adjudication frontmatter `executor_plan_contracts`
- can carry explicit machine-executable follow-up entries in adjudication frontmatter
  `executor_followups`
- can already drive durable rewrites through that structured subset when the
  verdict carries an explicit executable contract
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
- can compile bounded higher-level adjudication plan contracts from frontmatter
  `executor_plan_contracts` into explicit executor followups before execution
  through registry-owned payload templates instead of one private compiler branch per
  plan family
  - current supported plan-contract families include:
    - `rewrite-active-objective-via-soft-pivot`
    - `rewrite-open-round-then-close-chain`
    - `rewrite-open-task-contracts`
    - `invalidate-invalidated-task-contracts`
    - `abandon-invalidated-task-contracts`
    - `retire-invalidated-exception-contracts`
    - `invalidate-invalidated-exception-contracts`
    - `enter-execution-with-round-bootstrap`
- can execute explicit structured follow-ups encoded in adjudication frontmatter
  `executor_followups`
- currently supports structured execution for:
  - `close-objective`
  - `record-soft-pivot`
  - `rewrite-open-round`
  - `rewrite-open-task-contract`
  - `round-close-chain`
  - `refresh-round-scope`
  - `set-phase`
  - `update-task-contract-status`
  - `update-round-status`
  - `retire-exception-contract`
  - `invalidate-exception-contract`
- `rewrite-open-round` is the first owner-layer primitive for durable round
  contract mutation without changing round identity
- `round-close-chain` is the first bounded multi-step bundle:
  - reuses legal `update-round-status` transitions only
  - supports `active -> validation_pending -> captured -> closed`
  - supports resuming from `validation_pending` or `captured`
  - refuses unsupported starting statuses instead of improvising
  - remains a governed bundle wrapper, not a primitive transition command
- bounded exception-contract plan bundles can target active exception contracts
  through adjudication `Objects Invalidated` when the mapping stays
  deterministic and auditable
- bounded task-contract plan bundles can target open task contracts through
  adjudication `Objects Invalidated` when the mapping stays deterministic and
  auditable
- bounded task-contract rewrite plans can fan out across explicit
  `task_contract_ids` through the same registry-owned payload-template surface
  used by round rewrite plans
- bounded objective rewrite plans can compile one `record-soft-pivot` command
  from adjudication durable truth and preserve objective identity while
  optionally rewriting the still-open round in the same owner-layer command
- `rewrite-open-round-then-close-chain` can now resolve its round target from
  explicit `round_id`, one invalidated still-open round, or one open round in
  the adjudication objective context instead of requiring a hand-authored round
  id every time
- executor command-building for mutable rewrite commands now flows through one
  shared registry-backed builder path instead of separate per-command rewrite
  branches
- bounded phase-side-effect plans can compile `set-phase --auto-open-round`
  from the adjudication's existing round bootstrap fields instead of requiring
  one hand-authored low-level phase payload
- can rerun control audit after those follow-ups
- can open a bounded round when structured round bootstrap fields exist in the
  adjudication record or are passed explicitly
- treats an already-open aligned round as `noop` instead of reopening it
- reports prose-only, unsupported, or underspecified follow-ups as blocked instead of
  pretending they were executed
- transition-registry note:
  - the current owner-layer registry covers command names, domains,
    implementation status, required inputs, guard codes, guard rendering
    semantics, write-target semantics, write targets, side-effect codes,
    transition-command side-effect semantics, command mutable-field semantics,
    command executor payload-field semantics, bundle executor payload-field
    semantics, executor support,
    adjudication plan families, and bounded adjudication payload-template semantics
  - `audit-control-state` now warns if `TRANSITION_COMMANDS.md` documents command
    or plan names that the registry does not yet cover semantically

## Minimal First Implementation Set

The smallest honest set to implement first is:

1. `open-objective`
2. `record-hard-pivot`
3. `open-round`
4. `update-round-status`
5. `activate-exception-contract`

This set is enough to make the control plane materially real.

## Current Implementation Status

The current implementation now includes real enforced slices in five command domains:

- objective-line:
  - `open-objective`
  - `close-objective`
  - `record-soft-pivot`
  - `record-hard-pivot`
- phase:
  - `set-phase`
- round:
  - `open-round`
  - `refresh-round-scope`
  - `rewrite-open-round`
  - `update-round-status`
- task-contract:
  - `open-task-contract`
  - `update-task-contract-status`
  - `rewrite-open-task-contract`
- exception-contract:
  - `activate-exception-contract`
  - `retire-exception-contract`
  - `invalidate-exception-contract`

These slices already do these things:

- write durable `objective`, `pivot`, and `round-contract` files
- write durable `task-contract` files
- write durable `exception-contract` files
- update `control/active-objective.md`, `control/pivot-log.md`, `control/active-round.md`, and `control/exception-ledger.md`
- make the objective-line plus phase command slice consume one shared
  registry-backed owner-layer contract for declared inputs, guard coverage,
  guard rendering semantics, write-target semantics, transition-command side-effect semantics, write-target coverage, and transition-event expectations
- make the round command slice consume one shared registry-backed owner-layer contract for guard coverage, guard rendering semantics, write-target semantics, transition-command side-effect semantics, write-target coverage, and transition-event expectations
- make the task-contract command slice consume one shared registry-backed owner-layer contract for guard coverage, guard rendering semantics, write-target semantics, transition-command side-effect semantics, write-target coverage, and transition-event expectations
- discover implemented command membership from registry domains instead of
  maintaining private per-domain command sets in the shared helper
- remove private write-target allowlists from shared domain helpers by making
  command side-effect coverage validate against registry-owned write-target and
  owner semantics
- make `rewrite-open-round` plus adjudication rewrite execution consume one
  registry-owned mutable-field contract for allowed field names, merge/replace
  semantics, and payload-key admission
- make supported adjudication executor commands consume one registry-owned
  payload-field contract instead of keeping private payload-to-CLI branches per
  command
- reject illegal round-status transitions
- refuse hard pivots that would silently outrun a durable still-open round tied to the old objective
- refuse opening a second active objective when a durable active objective already exists
- refuse retiring or invalidating exception contracts that are not currently active
- preserve existing round metadata when rewriting status
- rewrite one open round contract durably through `rewrite-open-round`
- record `transition-event` files for both objective-line and round operations
- record `transition-event` files for task-contract operations
- make assembled context and role contexts surface active task contracts for the
  active round
- reject round capture, closure, abandonment, objective close, and hard pivot
  when draft or active task contracts would be stranded
- record `transition-event` files for exception-contract operations
- let `audit-control-state` warn when the objective/phase-domain helper or the
  round-domain helper can no longer satisfy their declared registry semantics
- let `audit-control-state` warn when the task-contract-domain helper can no
  longer satisfy its declared registry semantics

It does not yet implement:

- adjudication-driven automatic follow-up rewrites beyond the explicit bounded
  command subset already encoded in `executor_followups`
- hard-pivot-driven automatic round rewrites or broader multi-round replacement
  bundles

## Explicit Non-Goal

Do not implement all commands at once.

Freeze the command surface first, then implement one small coherent slice with
real file writes and guard checks.
