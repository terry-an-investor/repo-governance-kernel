# Session Memory Control System

Date: 2026-03-23
Scope: Multi-project coding control system

## Goal

Turn coding-agent memory into a control system that keeps real software work
coherent while allowing exploration, interruption, parallel review, and
project-level pivots.

The problem is not only recall. The harder problem is control:

- preserving project direction while implementation is moving
- containing workaround debt before it becomes the real architecture
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

## Control Model

The control model has four layers:

1. constitution
2. objective line
3. round control
4. evidence and memory

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
- temporary workarounds introduced during implementation

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
- replacing one workaround with another

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
- invalidate obsolete round contracts

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
- workaround tracking
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
- `workaround`
  - temporary compromise with exit condition and risk
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
- which workarounds or assumptions are now invalid
- what new risks the pivot introduces

## Lifecycle

The smallest honest lifecycle is:

1. open objective
2. explore or execute under one active round
3. capture decisions, failures, workarounds, and evidence
4. detect drift or objective mismatch
5. record soft or hard pivot when needed
6. refresh round control under the new objective line
7. capture snapshot and handoff

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

## Retrieval Consequence

Context assembly should compile from the active control state, not from raw
recency.

That means:

- active objective before historical objective
- current round before old snapshots
- unresolved workaround before settled decision
- current pivot lineage before orphaned historical notes

Historical memory still matters, but it should be loaded through the active
objective line so obsolete context does not dominate the session.

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
