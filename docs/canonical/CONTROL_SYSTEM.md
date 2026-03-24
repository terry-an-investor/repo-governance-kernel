# Session Memory Control System

Date: 2026-03-24
Scope: repo governance kernel

Host-repo note: this document explains the control model as used by the host
repository and its dogfood sample. Reusable kernel implementation authority is
owned by `kernel/`.

That host sample is now a dogfood/example surface rather than the primary
product owner of the kernel.

## Goal

`session-memory` is a repo governance kernel.

See [`PRODUCT.md`](./PRODUCT.md) for the canonical product definition.

This control system exists to keep repository development inside explicit
control objects, legal transitions, audit, and enforcement.

## Core Position

The system should store and govern control state, not only remembered facts.

Its current automation scope is bounded registry-owned execution.
Its current autonomy boundary is not a general autonomous rewrite engine.

See [`STATE_MACHINE.md`](./STATE_MACHINE.md) for the explicit transition model.

## Product Alignment

`PRODUCT.md` is the canonical product truth source.

Machine behavior should not follow prose directly. The intended path is:

- `PRODUCT.md` defines the product boundary and positioning
- canonical docs translate that stance into architecture, control, and state
  language
- `STATE_MACHINE.md` and `TRANSITION_COMMANDS.md` freeze the bounded machine
  surface
- `kernel/transition_specs.py` remains the executable owner-layer authority
- audits fail when these layers drift apart

## Repeated Problem Class

The repeated problem is development-control drift:

- the active objective line becomes ambiguous
- scope grows without an explicit contract
- temporary deviation becomes architecture truth silently
- control projection and durable truth disagree
- work is narrated as complete while the repo is still blocked

The kernel exists to make those states explicit, auditable, and punishable.

## Control Objects

The lowest honest owner layer is a small set of first-class control objects:

- `objective`
- `round`
- `task-contract`
- `exception-contract`
- `adjudication`

Other useful objects such as pivot, decision, validation-report, and transition
event still exist, but they support this core rather than replacing it.

## Operational Layers

The control plane should be understood as five layers:

1. durable truth
2. projected control state
3. audit and enforcement
4. adjudication
5. bounded transition execution

### Durable Truth

Durable truth is the append-mostly memory substrate:

- objectives
- pivots
- rounds
- task contracts
- exception contracts
- adjudications
- transition events

These records preserve provenance and authority.

### Projected Control State

Projected control state is the compact mutable read surface:

- `control/active-objective.md`
- `control/active-round.md`
- `control/pivot-log.md`
- `control/exception-ledger.md`
- `current/current-task.md`

Projection is not allowed to outrank durable truth.

### Audit And Enforcement

Audit asks whether the control state is honest enough to keep using.

Enforcement raises the cost of uncontrolled change before dishonest progress is
ratified.

Primary failure classes include:

- projection drift
- execution without a bounded round
- dirty paths outside governed scope
- guarded exception-zone edits without an active exception contract
- promotion while audit or worktree enforcement is blocked

These are transition blockers, not advisory lint.

### Adjudication

Adjudication resolves durable conflicts before mutation.

It should answer:

- which objective line remains active
- which round should be rewritten, closed, split, or invalidated
- which exception contract is stale
- which follow-up rewrites are explicit enough to compile safely

Adjudication should produce an explicit verdict with provenance, not an
implicit guess hidden inside repair logic.

### Bounded Transition Execution

Execution writes new honest state only where the repo already owns the machine
semantics.

That includes:

- primitive transition commands
- governed bundle wrappers
- bounded intent surfaces that compile only into governed commands or bundles
- bounded adjudication follow-up compilation and execution

This layer must stay registry-first.

## Enforcement Gates

The canonical enforcement owner is repository-local, not harness-specific.

Trigger surfaces may vary:

- transition commands
- repo-local git hooks
- CI workflows
- optional harness-native lifecycle hooks

But they must reuse the same repo-owned enforcement commands instead of
reimplementing policy privately.

Current hard gates should converge on:

- dirty non-control paths must stay inside active round scope
- when active task contracts exist, dirty implementation paths should narrow to
  task scope rather than round scope
- dirty projected control files must still match durable truth
- guarded exception-zone edits require one active exception contract
- blocked audit or enforcement must prevent promotion and closure

The current external-host validation evidence now covers one honest sequence:

- bootstrap a host repo into minimum governance state
- pass host-side `audit-control-state`
- adopt one explicit host-side objective, round, and task contract
- re-run `enforce-worktree` and expect any remaining `blocked` verdict to be
  about real scope law, not missing adoption authority
- for one external target repo, draft dirty-path scope first, then run one
  governed bundle-backed single assessment and expect the final verdict to
  reflect the adopted dirty-path boundary instead of hand-authored ambiguity

## Task-Contract Consequence

Round scope is not the same thing as concrete implementation authority.

The intended layering is:

- objective and phase
  - why execution exists
- round
  - what bounded project slice is open
- task contract
  - what concrete implementation slice is active

Task contracts become honest only when they are consumable:

- surfaced in assembled and role-specific contexts
- considered by enforcement
- considered by promotion and closure commands
- prevented from being stranded across pivots or round closure

## Bundle Governance

Bundles are bounded orchestration wrappers, not a second private runtime.

The current governed bundle wrappers include:

- `round-close-chain`
- `round-close-chain-then-hard-pivot`
- `assess-external-target-once`

A bundle wrapper is acceptable only when:

- registry-owned route and step semantics exist
- executor dispatch goes through the shared governed runtime
- payload field semantics are registry-owned
- it composes existing governed steps only
- it remains bounded, audit-visible, and smoke-proven

The ban is on private bundle semantics, not on bundles themselves.

## Bounded Intent Surfaces

Bounded intent surfaces are allowed only when they fail closed into the same
owner-layer command and bundle contracts.

The current bounded intent surface is:

- `assess-external-target-from-intent`

An intent surface is acceptable only when:

- it compiles only into an existing governed command or bundle
- it does not introduce broader mutation authority than the compiled target
- accepted intent classes stay narrow, explicit, and smoke-proven
- requests implying continuous monitoring or freeform mutation are rejected

## Kernelization Direction

The repo should converge toward two explicitly different things:

- reusable kernel
  - control semantics
  - transition registry
  - audit and enforcement runtime
- dogfood/sample project
  - `state/session-memory/...`
  - self-hosted rounds, adjudications, and sample history

Without that split, self-hosting noise will keep appearing as kernel
requirements.

## Design Consequence

The next architecture move is not broader autonomy.

It is:

- strengthen task-contract as a real execution gate
- make enforcement the hard gate for promotion and closure
- continue eliminating private semantics
- keep all new execution surfaces registry-owned
- separate kernel concerns from sample-specific repo history

