# Session Memory Implementation Plan

Date: 2026-03-24
Scope: Kernelization phase for the repo governance kernel

## Goal

Implement the smallest honest reusable kernel for repository governance defined
in [`PRODUCT.md`](./PRODUCT.md):

- files remain the source of truth
- SQLite plus FTS5 remain retrieval support layers
- control objects remain file-first
- machine behavior remains registry-first

The product is a repo governance kernel, not a general autonomous rewrite
engine.

Its automation target remains bounded registry-owned execution.
It is not a general autonomous rewrite engine.

## Current State

The repository already has a meaningful bounded kernel slice:

- objective, pivot, round, task-contract, exception-contract, adjudication, and
  transition-event files exist
- projected control files exist
- transition registry exists
- audit and worktree enforcement exist
- bounded adjudication follow-up execution exists
- governed bundle execution exists for the bounded implemented subset

The current gap is not "no semantics". The current gap is that the kernel is
still mixed with self-hosted sample complexity and still only partially unified
end to end.

## Kernelization Priorities

### 1. Stabilize the kernel surface

Keep the reusable kernel centered on:

- objective
- round
- task-contract
- exception-contract
- adjudication
- audit
- enforcement
- bounded transition runtime

Do not broaden the primitive surface unless the behavior cannot honestly remain
composition.

### 2. Strengthen task-contract as an execution gate

Task contracts should become more than durable notes.

Needed outcomes:

- enforcement narrows dirty implementation scope to active task contracts when
  they exist
- promotion and closure commands refuse to strand open task contracts
- context assembly and role contexts continue to surface active task contracts
  as current authority

### 3. Make enforcement the hard promotion gate

Important promotion and closure paths should converge on the same blockers:

- `audit-control-state`
- `enforce-worktree`

The system should not keep separate local notions of "good enough to proceed".

### 4. Continue eliminating private semantics

Keep moving these surfaces into the registry/runtime owner layer:

- command payload semantics
- mutable-field semantics
- bundle route/state semantics
- bundle payload semantics
- target resolution semantics
- compiler binding semantics

No new executor-local or compiler-local private authority should be added.

### 5. Separate kernel from sample

Make the conceptual split increasingly real:

- kernel
  - reusable governance semantics and runtime
- sample
  - `projects/session-memory/...`
  - self-hosted rounds, adjudications, and product history

This can begin as documentation and module-boundary cleanup before it becomes a
physical repo split.

## Out Of Scope

The following should stay out of scope for this phase:

- general autonomous rewrite
- prose-driven durable rewrite inference
- arbitrary multi-object adjudication execution
- ontology expansion for its own sake
- new private bundle families
- product broadening back into a generic memory platform

## Implementation Order

1. keep canonical docs aligned on the kernel framing
2. make task-contract enforcement narrower and more real
3. raise promotion and closure paths onto shared enforcement gates
4. continue registry-first unification of remaining execution semantics
5. separate kernel-owned runtime surfaces from sample-owned repo artifacts
6. validate the kernel on more repos after the owner-layer surface stabilizes

## Validation Standard

Kernelization is only considered real when:

- canonical docs agree on the product boundary
- product-doc audit stays clean
- control audit stays clean on the real project
- enforcement stays clean on the real project after the round closes
- newly added execution semantics are registry-owned, audit-visible, and
  smoke-proven
- sample-specific complexity is distinguishable from reusable kernel semantics
