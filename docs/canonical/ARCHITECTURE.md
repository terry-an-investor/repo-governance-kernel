# Repo Governance Kernel Architecture

Date: 2026-03-24
Scope: repo governance kernel

Host-repo note: this file now describes how the host repository integrates the
reusable kernel with its self-hosted control state. Kernel-specific architecture
notes live under `kernel/docs/`.

## Goal

`repo-governance-kernel` is a repo governance kernel.

See [`PRODUCT.md`](./PRODUCT.md) for the canonical product definition.

The architecture exists to keep repository development flowing through explicit
control objects and bounded execution semantics instead of transcript-local
intent.

## Architectural Summary

The system should be read together with [`CONTROL_SYSTEM.md`](./CONTROL_SYSTEM.md).
The transition model is defined in [`STATE_MACHINE.md`](./STATE_MACHINE.md).
The bounded command surface is defined in [`TRANSITION_COMMANDS.md`](./TRANSITION_COMMANDS.md).

The architectural split should be:

- kernel
  - reusable governance semantics and enforcement runtime
- repo-owned control state
  - this repository's own control objects, docs, and local history

The kernel itself has five layers:

1. durable control truth
2. projected control state
3. audit and enforcement
4. adjudication
5. bounded execution runtime

Memory and retrieval still exist, but they support those layers rather than
defining the product by themselves.

## Layer 1: Durable Control Truth

Purpose:

- preserve the explicit control objects that define repository authority

Core objects:

- objectives
- pivots
- rounds
- task contracts
- exception contracts
- adjudications
- transition events

These are durable Markdown objects under `state/<project_id>/memory/`.

## Layer 2: Projected Control State

Purpose:

- provide a compact current-state surface for humans and agents

Primary projections:

- `control/active-objective.md`
- `control/active-round.md`
- `control/pivot-log.md`
- `control/exception-ledger.md`
- `current/current-task.md`

Projection is not authority. Projection is the fast read surface built from
durable truth plus bounded orientation content.

## Layer 3: Audit And Enforcement

Purpose:

- detect dishonesty
- block illegal promotion before it becomes ratified state

Primary kernel surfaces:

- `kernel/audit_control_state.py`
- `kernel/control_enforcement.py`
- `scripts/enforce_worktree.py`
- repo-local git hooks
- CI invocations of the same repo-owned enforcement commands

This layer is where the kernel becomes operational instead of merely
descriptive.

## Layer 4: Adjudication

Purpose:

- resolve conflicting durable truth into an explicit verdict before mutation

Adjudication should never be treated as free-form repair prose.

It exists to answer questions like:

- which objective line remains authoritative
- which open round should be rewritten, closed, or invalidated
- which exception contract is stale
- which follow-up rewrites are explicit enough to compile safely

## Layer 5: Bounded Execution Runtime

Purpose:

- execute only the subset of transitions the repo already owns semantically

Primary kernel surfaces:

- `kernel/transition_specs.py`
- shared resolver/runtime helpers under `kernel/`
- `kernel/governed_bundle_runtime.py`
- `kernel/executor_runtime.py`
- transition command entrypoints under `kernel/commands/`
- bounded intent-compilation entrypoints under `kernel/commands/`
- repo-local compatibility wrappers under `scripts/`
- bounded adjudication follow-up compiler/executor

This runtime must stay registry-first:

- no private command semantics
- no private bundle semantics
- no compiler-local free-string semantics
- no executor payload admission outside registry-owned contracts

## Memory And Retrieval Support

Memory and retrieval remain useful because the kernel still needs:

- durable storage for control objects
- searchable historical evidence
- context assembly for fresh sessions and role-specific review

But these are supporting layers now:

- memory store keeps provenance inspectable
- SQLite plus FTS5 accelerate retrieval
- context assembly surfaces current control state and supporting evidence

They should not pull the product back into "memory platform" framing.

## Kernel vs Sample Split

The architecture should increasingly separate:

- reusable kernel semantics
  - schema-neutral control concepts
  - state domains
  - transition registry
  - audit and enforcement runtime
- repo-owned control-state semantics
  - `state/repo-governance-kernel/...`
  - self-hosted rounds and adjudications
  - local product history
  - fixture and smoke-specific local data

Without that split, repo-local noise gets mistaken for kernel complexity.

## File Layout

The current repository still contains both kernel and repo-owned control surfaces:

```text
repo-governance-kernel/
├── README.md
├── AGENTS.md
├── docs/
│   ├── canonical/
│   │   ├── PRODUCT.md
│   │   ├── ARCHITECTURE.md
│   │   ├── CONTROL_SYSTEM.md
│   │   ├── STATE_MACHINE.md
│   │   ├── TRANSITION_COMMANDS.md
│   │   └── ...
│   ├── evaluation/
│   ├── history/
│   └── operations/
├── kernel/
│   ├── transition_specs.py
│   ├── round_control.py
│   ├── resolver_runtime.py
│   ├── control_enforcement.py
│   ├── audit_control_state.py
│   └── ...
├── scripts/
│   ├── enforce_worktree.py
│   ├── audit_control_state.py
│   ├── transition_specs.py
│   └── ...
├── state/
│   └── repo-governance-kernel/
└── index/
```

That mixed layout is acceptable in the current phase, but the conceptual
boundary should already be explicit in docs and runtime ownership.

## Architectural Consequence

The right next move is not to grow more autonomous behavior.

The right next move is:

- narrow the kernel surface
- make enforcement harder
- make task contracts executable gates
- keep all new semantics registry-owned
- separate kernel concerns from repo-owned control-state concerns

