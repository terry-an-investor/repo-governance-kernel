---
id: product-session-memory
product_name: session-memory
product_category: "repo governance control plane"
product_approach: "memory-driven"
positioning_phrase: "memory-driven repo governance control plane"
automation_scope: "bounded automatic execution"
autonomy_boundary: "not a general autonomous rewrite engine"
current_stage: "phase-1 control plane"
target_user_segments:
  - vibe coding builders
  - non-senior engineers
  - AI-native technical leads
canonical_semantics_surfaces:
  - PRODUCT.md frontmatter
  - scripts/transition_specs.py
  - scripts/audit_product_docs.py
  - scripts/audit_control_state.py
---
# Session Memory Product

Date: 2026-03-24
Scope: Canonical product definition for the repository

## Product Definition

`session-memory` is a memory-driven repo governance control plane.

Memory is the substrate, not the end product. The product job is to keep a
software repository honest and navigable while humans and coding agents keep
changing it.

The product does that by making project control explicit:

- what the active objective is
- what phase the project is in
- what bounded round is currently allowed to move code
- what concrete task contracts are allowed to move inside that round
- what temporary exceptions exist
- what adjudications and follow-up actions are trusted

## Target Users

Primary users today:

- vibe coding builders who can get code written quickly but struggle to keep a
  real project coherent over time
- non-senior engineers who need help maintaining scope, state honesty, and
  closure discipline while using LLM-heavy workflows
- AI-native technical leads who need auditable control state instead of
  transcript archaeology

## User Pain

The main pain is not code generation. The main pain is project control drift.

Common failure modes:

- the project loses its real mainline after several high-speed LLM sessions
- scope expands silently because nobody owns a bounded execution contract
- temporary workarounds become architecture truth without an explicit exception
- one chat says "done" while the worktree and control files disagree
- a new session or reviewer cannot tell what the project is actually trying to
  ship

## Product Promise

The product promise is:

- preserve the active mainline across sessions and handoffs
- make code work happen inside explicit bounded rounds
- keep exceptions explicit and recoverable
- block dishonest advancement before it is ratified
- allow bounded automatic follow-up actions where the repo already owns the
  semantics

## Current Capabilities

Today the product already provides:

- durable objective, pivot, round, exception-contract, and adjudication records
- first file-first task-contract records attached to round governance
- bounded task-contract lifecycle commands for status change and in-place rewrite
- projected control files for active objective, active round, pivot log, and
  exception ledger
- control audit and worktree enforcement
- assembled and role-specific contexts that surface active task contracts
- bounded adjudication follow-up execution
- role-context and handoff bundle preparation
- multi-project operation with `session-memory` and `wind-agent`

## Product Boundaries

The current automation scope is bounded automatic execution.

The current autonomy boundary is not a general autonomous rewrite engine.

That means:

- the system can execute only the repo-owned safe subset whose semantics are
  already explicit
- prose does not authorize arbitrary durable rewrites
- rounds define the outer execution envelope, but task contracts define the
  concrete allowed subtask before execution semantics broaden
- new automation surfaces must first become explicit owner-layer contracts
- task contracts do not yet authorize automatic rewrite by themselves; they
  only make task-level intent and boundaries durable enough to audit

## Product To Semantics Path

Product docs should guide machine behavior only through explicit structured
contracts, never through free-form prose interpretation.

The required path is:

1. `PRODUCT.md` owns the canonical product contract
2. `PRODUCT.md` frontmatter carries the machine-readable product stance
3. canonical control docs define the round-governed task-contract layer between
   project control and low-level command semantics
4. machine-semantic docs such as `STATE_MACHINE.md` and
   `TRANSITION_COMMANDS.md` implement only the bounded executable subset
5. owner-layer registries such as `scripts/transition_specs.py` carry the
   executable semantics
6. audits fail when canonical docs, machine-readable product contract, and
   machine-semantic docs drift apart

This keeps "start from the product" real without pretending that natural
language alone is executable authority.

## Current Stage

Current stage: `phase-1 control plane`

This stage is about proving that memory-backed repo governance is useful and
operable before broadening automation.

## Roadmap

Near-term product milestones:

- keep product positioning stable across canonical docs
- make task-contract the honest task-level owner layer under round governance
- make task-contract semantics consumable across context assembly, lifecycle
  commands, and honesty gates
- continue lifting private execution semantics into owner-layer registries
- tighten product-doc-to-machine-semantics audits
- split reusable governance-kernel capabilities from this repo's local sample
  semantics
- validate the product on additional real repositories
