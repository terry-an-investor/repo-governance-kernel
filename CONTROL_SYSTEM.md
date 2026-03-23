# Session Memory Control System

Date: 2026-03-23
Scope: Multi-project coding control system

## Goal

Turn coding-agent memory into a control system that keeps real software work
coherent while allowing exploration, interruption, parallel review, and
project-level pivots.

The problem is not only recall. The harder problem is control:

- preserving project direction while implementation is moving
- containing temporary deviation debt before it becomes the real architecture
- allowing new ideas without derailing the active mainline
- making architecture review and side-session work actually project-aware
- supporting legitimate project pivots without losing provenance

## Core Position

The system should store control state, not only remembered facts.

See [`STATE_MACHINE.md`](./STATE_MACHINE.md) for the explicit transition model.

A fresh agent or side-session reviewer does not merely need "context". It needs
to know:

- what outcome the project is currently trying to produce
- what was intentionally deferred
- what temporary compromises exist
- what evidence is trusted
- whether the project is still on the same objective line
- whether a pivot has already happened

The system still needs one layer that remains only partially implemented in code today:

- adjudication
  - when durable control objects conflict, decide which line remains active,
    which objects are stale or invalid, and what must be rewritten

Rejecting ambiguity is only a guard. It is not the control system's final job.

Another way to say this:

- spec defines what must already be explicit before implementation is trusted
- harness defines what must already be observed before progress is accepted

If those two layers are weak, an agent will often "help" by filling gaps with:

- fabricated intermediate facts
- hand-waved mocks
- silent requirement edits
- accidental scope shifts

So the control system should not only preserve memory. It should front-load the
precision that gives human review leverage.

That also means committed control projections must stay honest about what they
can know. A file such as `current/current-task.md` may record the workspace
locator needed to re-open the project, but the live workspace inspection
remains the canonical freshness owner layer for the current branch and worktree
state.

`current/current-task.md` should be treated as a control-plane orientation
projection:

- it is not just an arbitrary scratch note
- it is not a fully derivable projection like `control/active-round.md`
- its `Objective id`, `Active round id`, and `Phase` bullets should stay
  aligned with durable control truth
- it should keep only stable workspace locator fields such as `Workspace id`
  and `Workspace root`
- live repo facts such as branch, HEAD, and dirty state should be rendered
  through a separate non-durable live workspace projection instead of being
  committed into `current/current-task.md`

## Operational Layers

The control plane should be understood as five operational layers:

1. durable truth
2. projected control state
3. control audit
4. adjudication
5. transition execution

### Durable Truth

Durable truth is the append-mostly memory substrate:

- objectives
- pivots
- round contracts
- exception contracts
- transition events

These records preserve provenance, but they can still conflict.

### Projected Control State

Projected control state is the compact mutable surface:

- `control/active-objective.md`
- `control/active-round.md`
- `control/pivot-log.md`
- `control/exception-ledger.md`

These files are optimized for fast consumption by humans and agents. They are
not the final authority when durable truth disagrees with them.

### Control Audit

Control audit asks whether the current state is honest enough to keep using.

It should detect failures such as:

- projection drift
- execution without a bounded round
- multiple durable active lines
- blocked rounds without declared blockers
- missing constitution or exception tracking

Audit surfaces problems. It does not decide the winner.

### Adjudication

Adjudication is the missing resolution layer between detection and mutation.

It should answer questions like:

- which durable objective is still the real mainline
- whether an open round should be closed, split, or invalidated
- whether an exception contract is still a temporary deviation or has leaked
  into architecture truth
- whether old durable records are legitimate history or now misleading debris

Adjudication should produce an explicit verdict with provenance, not an
implicit guess hidden inside one repair script.

### Transition Execution

Transition execution is the command layer that writes the new honest state:

- open or close objectives
- record pivots
- open or update rounds
- activate, retire, or invalidate exception contracts
- rebuild projections after the durable state is coherent

### Enforcement Gates

Enforcement gates are the lightweight automatic penalties that raise the cost of
uncontrolled code changes before dishonest state is ratified.

This design should not depend on a specific agent harness exposing native tool
lifecycle hooks.

Harness-specific native hooks are useful when they exist, but they are not the
owner layer in this system.

The owner layer here is repository-local and harness-agnostic:

- transition gates inside control commands
- repo-local git hooks that call the same enforcement primitive
- CI workflows that call the same enforcement primitive again

For implemented command domains, those transition gates should converge toward
shared registry-backed owner-layer consumers instead of letting each command
silently own its own private guard and write semantics.

That means the system can borrow the hooks idea without coupling project
control to one vendor's runtime semantics.

They should run before important promotions such as:

- round capture
- round closure
- commit or push

The trigger surfaces may differ, but they must reuse the same repo-owned
commands. A GitHub Actions workflow that reimplements the policy in YAML logic
instead of calling `scripts/enforce_worktree.py` and
`scripts/audit_control_state.py` would be architecture drift.

The first enforcement slice should block at least these failures:

- dirty non-control paths outside the active round scope
- direct manual edits to projected control files that drift from durable truth
- promotion or closure while control audit is already blocked

The next honest slice should also allow projects to declare guarded exception
zones in the constitution:

- when dirty paths enter those guarded zones, one active exception contract
  must explicitly cover them
- this keeps temporary deviation explicit instead of letting workaround debt
  silently merge into architecture truth

These gates are not advisory lint. They are transition blockers.

## Control Model

The control model has four layers:

1. constitution
2. objective line
3. round control
4. evidence and memory

Phase and round-scope changes are now first-class owner-layer transitions, not
manual edits:

- `set-phase` changes durable objective phase and active-objective projection together
- objective-line plus phase commands consume one shared registry-backed owner-layer contract for declared inputs, guard coverage, write-target coverage, and transition-event expectations
- entering `execution` must already have one bounded round or bootstrap one in
  the same command
- `refresh-round-scope` rewrites durable round `paths` from live dirty-path
  evidence instead of relying on manual frontmatter edits
- `rewrite-open-round` rewrites one open round contract durably while preserving
  round identity, so pivots and adjudication can mutate round truth through a
  bounded owner-layer primitive instead of ad hoc file edits
- `audit_control_state` now warns when either the objective/phase-domain helper
  or the round-domain helper drifts from the semantic transition registry

## Precision Surfaces

The control system should make a small number of precision surfaces explicit
before implementation broadens.

These are the surfaces that reduce agent improvisation and increase human
review leverage:

- objective precision
  - goal, success criteria, non-goals, current phase
- state precision
  - objective, round, exception-contract, and freshness states
- transition precision
  - guards, legal status moves, and bounded side effects
- evidence precision
  - what counts as a real observed effect versus a weak proxy
- harness precision
  - which audits, smokes, and enforcement gates block dishonest advancement

This is why this project keeps moving work out of prompts and into:

- control objects
- transition commands
- bounded executor plan contracts
- owner-layer enforcement commands

That shift is not ceremony. It is where review becomes tractable.

## Review Leverage

Human review should not depend on reading an entire session transcript or
mentally simulating every agent improvisation.

The system should instead present reviewers with structured surfaces:

- durable truth objects
- projected control state
- explicit adjudication verdicts
- bounded executable plans
- harness outputs tied to observed state change

This allows reviewers to ask higher-value questions:

- is the chosen mainline actually justified
- is the state transition legal
- is a workaround explicitly temporary
- did the repo observe the claimed effect
- did the implementation bypass the declared control surface

When those surfaces are missing, review collapses into archaeology after the
code is already written.

### 1. Constitution

The constitution is the long-lived project operating contract.

It captures durable rules such as:

- product boundaries
- quality bar
- architecture invariants
- validation expectations
- naming or layering rules
- anti-patterns that must not quietly re-enter

The constitution changes rarely.

### 2. Objective Line

The objective line explains why the project currently exists.

It must make explicit:

- the current objective
- the user or operator problem being solved
- success conditions
- explicit non-goals
- the current project phase
- the supersession history when the goal changes

This layer is where pivot happens.

### 3. Round Control

Round control governs the current unit of execution.

It should contain:

- the active round contract
- allowed scope
- concrete deliverable
- validation expectation for this round
- active risks
- current blockers
- deferred ideas that must not hijack the round
- active exception contracts introduced during implementation

This is the layer that keeps agile work from turning into uncontrolled drift.

### 4. Evidence And Memory

Evidence and memory explain what is actually known.

This includes:

- decisions
- failures
- constraints
- patterns
- snapshots
- validation reports
- artifacts

These objects justify or challenge the control state.

## Why Pivot Must Be First-Class

Projects often begin with incomplete problem definition.

A healthy system must allow:

- starting with a weak or exploratory objective
- discovering that the framing was wrong
- changing direction without pretending the old direction never existed

Without a first-class pivot concept, teams silently overwrite goals. That
creates false continuity and makes later sessions over-trust obsolete context.

## Pivot Definition

A pivot is an explicit change to the project's objective line.

It is not merely:

- editing `current-task.md`
- changing implementation steps
- replacing one exception contract with another

A pivot exists when one or more of these change materially:

- the core problem being solved
- the intended user or operator outcome
- the success criteria
- the dominant product shape
- the system boundary

## Pivot Types

### Soft Pivot

Use when the core objective remains intact, but the execution frame changes.

Typical examples:

- reprioritizing milestones
- changing architecture approach
- shrinking current scope
- moving from implementation-first to stabilization-first

A soft pivot should usually:

- preserve the same objective id
- create a pivot record
- update the active objective fields
- record why the same objective id still holds
- force an explicit round review path when the objective shape changed under an open round
- use `rewrite-open-round` when the project intends to keep the same round id
  but must durably rewrite the round contract to match the new objective shape

### Hard Pivot

Use when the project's reason for existence has changed enough that the
objective line should branch.

Typical examples:

- the project changes from memory system to coding control system
- the target user or workflow changes
- the product surface is no longer the same product

A hard pivot should usually:

- close or supersede the previous objective
- create a new objective id
- create a pivot record that links old and new objectives
- recompile current control context from the new objective line

### Objective Close

Use when the project intentionally ends the current objective line without
opening a successor yet.

An objective close should usually:

- update the durable objective status to `closed` or `invalidated`
- remove `control/active-objective.md`
- leave zero active objectives until a new mainline is opened
- refuse to proceed while open rounds or active exception contracts still depend on the closing objective

## Exploration vs Execution

The system must distinguish exploration state from execution state.

### Exploration State

Exploration is where the project is still discovering what it should become.

Allowed properties:

- incomplete hypotheses
- parallel ideas
- throwaway probes
- competing framings
- inconclusive evidence

Required controls:

- hypotheses must be explicit
- experiments must carry evidence refs
- exploratory output must not silently become durable project law

### Execution State

Execution is where the project is committed enough that implementation should
be constrained.

Required controls:

- one active round contract
- explicit non-goals
- exception-contract tracking
- validation expectations
- snapshot or handoff capture at phase boundaries

The project may move back from execution to exploration, but this should be an
explicit state change, not a quiet drift.

## First-Class Control Objects

The system should add these project-agnostic control objects:

- `constitution`
  - long-lived project rules and invariants
- `objective`
  - current project goal line with success criteria and non-goals
- `pivot`
  - objective-line change record with provenance
- `round-contract`
  - bounded execution contract for the active round
- `exception-contract`
  - temporary deviation with exit condition, owner scope, and risk
- `adjudication`
  - explicit verdict when durable control truth conflicts
- `idea`
  - deferred or triaged idea that should not disrupt the mainline
- `validation-report`
  - structured evidence about what was actually tested or observed
- `hypothesis`
  - exploration-stage framing or proposed direction

These objects are not role-specific. Reviewer, architect, and orchestrator
contexts should be compiled from them.

## State-Machine Status

The current design should be understood as:

- state-machine oriented

It should not yet be described as:

- state-machine enforced

That means the docs already define state domains, transition intent, and drift
semantics, but the implementation still lacks a unified transition engine.

## Minimal Pivot Record

A pivot record should answer:

- what changed
- why the previous framing became insufficient
- what evidence triggered the change
- which objective was replaced or updated
- which decisions still stand
- which exception contracts or assumptions are now invalid
- what new risks the pivot introduces

## Lifecycle

The smallest honest lifecycle is:

1. open objective
2. explore or execute under one active round
3. capture decisions, failures, exception contracts, and evidence
4. detect drift or objective mismatch
5. record soft or hard pivot when needed
6. refresh round control under the new objective line
7. capture snapshot and handoff

For conflicting durable truth, the lifecycle needs one extra control step:

8. record an adjudication verdict
9. execute only the explicit, structured subset of follow-up rewrites that the
   system can map onto existing transition commands without guessing intent

The current implementation now includes one real durable rewrite primitive in
that subset:

- `rewrite-open-round`
  - a bounded owner-layer round-contract rewrite that preserves round identity
  - reusable by soft pivots, phase fallback, and adjudication follow-ups

That means adjudication should separate:

- human-readable follow-up intent
- machine-compilable bounded plan contracts
- machine-executable follow-up contracts

The machine-executable subset must stay explicit and bounded.
When the verdict already knows a safe rewrite pattern, the repo may carry it as
one bounded plan contract and compile it into low-level executor payloads
through repo-owned code instead of forcing operators to hand-author every JSON
payload. Those plan contracts should stay anchored to the same machine-readable
transition registry that names command guards, write targets, and side-effect
classes for the underlying owner-layer commands.
Those bounded plan contracts may consume adjudication durable context such as
the invalidated object set when target resolution remains deterministic and
auditable.
They may also reuse the adjudication's existing round bootstrap fields when the
repo is compiling a bounded phase-side-effect bundle such as entering
`execution` and auto-opening one round.
Prose alone is not authority to rewrite durable truth.

## Drift Detection

The system should detect at least three different failure modes:

- round drift
  - implementation moved beyond the active round contract
- objective drift
  - current work no longer serves the active objective
- stale memory drift
  - assembled packet no longer matches the live workspace anchor

These are different failures and should not be collapsed into one generic
"staleness" label.

## Automatic Penalties

The system should not rely on etiquette to prevent sloppy implementation.

Instead, it should make disorder expensive through automatic consequences:

- illegal worktree state blocks `captured` and `closed`
- out-of-scope dirty paths block round promotion until scope is narrowed,
  refreshed, or split
- projected control file drift blocks promotion until the projection is repaired
  or the durable source of truth is updated through commands
- a blocked audit prevents the system from pretending progress is honest

This is the core "punishment" model:

- not social disapproval
- not a long review comment
- but refusal to advance the control state for free

## Retrieval Consequence

Context assembly should compile from the active control state, not from raw
recency.

That means:

- active objective before historical objective
- current round before old snapshots
- unresolved exception contract before settled decision
- current pivot lineage before orphaned historical notes

Historical memory still matters, but it should be loaded through the active
objective line so obsolete context does not dominate the session.

## Role Context Consequence

Role contexts should not compile only trusted durable memory.

They should also surface the current control failures that make the project
unsafe to reason about naively.

At minimum, role contexts should expose:

- current audit status
- active control violations
- the evidence paths or ids attached to those violations

Without that layer, a fresh reviewer, architect, or orchestrator can inherit a
clean-looking memory packet while the actual project control plane is already
dishonest.

## Constitution Routing

The constitution should not be injected into every default handoff packet.

Why:

- default handoff should stay compact and orientation-first
- long-lived rules can drown out live execution state if always inlined
- many sessions need current direction more urgently than project law

So the routing rule should be:

- default handoff packet:
  - active objective
  - pivot lineage
  - current execution state
  - freshness
- role-specific compiled context for reviewer, architect, orchestrator:
  - constitution
  - active objective
  - pivot lineage
  - role-relevant execution state and memory

## Design Consequence

This project should be framed as a coding control system built on top of a
memory substrate.

Memory remains necessary, but memory alone is not enough. The system becomes
useful when it can:

- preserve direction
- absorb interruptions
- support review and architecture work with project-specific knowledge
- allow controlled pivots without losing provenance
