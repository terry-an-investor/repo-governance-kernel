# Session Memory Design Principles

Date: 2026-03-22
Scope: Memory-driven repo governance control plane

## Goal

Build a memory-driven repo governance control plane that helps a fresh
coding-agent session quickly recover the real engineering state of the current
project and workspace without replaying entire chat transcripts.

See [`PRODUCT.md`](./PRODUCT.md) for the canonical product definition.

The system is not a generic personal memory product. It is a repo governance
control plane for implementation, debugging, architecture review, handoff,
project pivots, and multi-project continuity.

## Core Position

Coding-agent memory should be designed as engineering state, not as chat
history.

The most valuable thing to preserve is not every token that appeared in a
session, but the durable work state extracted from that session:

- what was decided
- what was disproven
- what is currently blocked
- what files and modules are involved
- what evidence supports a conclusion
- what the next session needs to know to continue

## Principles

### 0. Control state matters as much as recall

Useful coding memory is not only a search layer. It must preserve enough
control state to answer:

- what objective is currently active
- whether the project is in exploration or execution
- what concrete task contract is currently authorizing one implementation slice
- which exception contracts are temporary debt
- whether the project has pivoted

Without this layer, retrieval can recover facts while still accelerating drift.

That control state should evolve through explicit state transitions, not through
silent document overwrite.

It should also separate:

- audit
  - detect dishonest or conflicting state
- adjudication
  - decide which durable records remain authoritative
- projection
  - rebuild the compact control files after the durable state is coherent

Without this split, repair logic will silently become an accidental judge.

That same precision should also exist inside execution:

- round contracts bound the project slice
- task contracts bound the concrete task inside that slice

Without the lower layer, a round is often still too coarse and the repo slides
back into transcript-local "just do this part" semantics.

### 1. Files are the source of truth

The canonical memory should live in visible files.

Databases, indexes, embeddings, and caches are accelerators, not the
authoritative memory source.

Why:

- humans can inspect and edit memory directly
- git can version memory naturally
- other tools can consume memory without hidden APIs
- recovery still works if the index layer breaks

### 2. Memory is not transcript

Raw sessions are useful as evidence and fallback, but they are not the memory
model.

We separate:

- raw event history
- extracted work memory

Work memory must be stable, queryable, and explicitly shaped for reuse.

### 3. Working memory and durable memory must stay separate

Not all memory has the same time horizon.

We need at least:

- working memory
  - current task state
  - short-term blockers
  - active ideas
  - temporary plans
- durable memory
  - decisions
  - constraints
  - failure cases
  - reusable patterns
  - long-lived handoff facts

This separation reduces contamination from temporary noise.

The same split should exist for control state:

- durable control
  - constitution
  - objective lineage
  - pivot history
- mutable control
  - active round contract
  - exception ledger
  - idea inbox
  - current blockers

### 4. Multi-project identity must be first-class

The system must not assume one long-lived project.

Each important memory item should carry enough metadata to answer:

- which project is this about
- which concrete local workspace produced it
- which branch / git sha did this apply to
- which files or modules were involved
- which session or thread produced it
- what evidence justified it

The minimum stable identity split is:

- `project_id`
  - semantic project identity
- `workspace_id`
  - concrete checkout / worktree identity
- `workspace_root`
  - human-readable local root path

Without this split, same-project parallel workspaces will bleed into each
other, and cross-project retrieval will become unreliable.

### 5. Project-specific workflows are evidence, not the memory ontology

A repo may have local concepts such as:

- round contracts
- review gates
- bundle runs
- CI artifacts
- custom validation reports

These should appear as `evidence_refs`, `artifact` records, or project-local
notes.

Project-local governance objects are still allowed when they are explicitly
declared and file-first. A task-contract layer in this repo is one such local
governance object: it is reusable inside the repo control plane, but it does
not become a mandatory global schema field for every memory item everywhere.

They must not become mandatory fields of the global schema.

The global schema should express coding-agent memory, not one repository's
governance process.

### 6. Structure first, semantics second

Do not start with embeddings.

Start by defining memory item types and metadata, then build:

1. structured storage
2. structured filtering
3. full-text retrieval
4. semantic retrieval only when needed
5. reranking only when retrieval volume justifies it

Without a memory schema, RAG is only a better search box.

For the first implementation, the preferred storage/retrieval stack is:

- SQLite
- FTS5 for full-text retrieval

Do not introduce DuckDB in phase 1 unless a concrete requirement appears that
SQLite plus FTS5 cannot honestly satisfy.

### 7. Recall and context assembly are different layers

The memory layer answers:

- what do we know
- where is it stored
- how can we retrieve it

The context engine answers:

- what should the model see right now
- what should be compacted
- what should be injected into a new session
- what should be passed to a side session or subagent

These concerns must stay separate.

### 8. The system must optimize for handoff

The primary user problem is not only retrieval. It is session continuity.

The system must help with:

- opening a new coding session without losing the current mainline
- running side-session reviews without derailing the main task
- returning from interruptions with low recovery cost
- switching between projects without memory contamination

Search matters, but handoff is the first-class workflow.

Handoff must also preserve control continuity:

- the active objective
- whether the project is exploring or executing
- recent pivots
- active exception contracts
- the current round boundary

### 9. Start narrow and real

The first system should solve a real coding-memory problem, not attempt to be a
full Memory OS.

Focus first on:

- current state
- current objective
- pivot lineage
- decisions
- failures
- constraints
- handoff
- file / git / workspace provenance

Only expand into broader categories if the narrow system proves useful.

Design should stabilize before implementation broadens.

That means:

- canonical docs first
- schema and directory semantics second
- implementation after those decisions are explicit

### 10. Precision must be front-loaded

Coding agents do not fail only by being weak.

They also fail by helpfully inventing missing reality:

- made-up data
- hand-waved mocks
- hidden requirement changes
- silent scope expansion
- fake completion based on indirect signals

So "be precise" is not enough. The key question is which precision must be
front-loaded before implementation starts so human review has leverage.

The most important precision surfaces are:

- objective precision
  - what outcome is actually being pursued
  - what does not count as success
- state precision
  - which states exist
  - which combinations are legal
- transition precision
  - which inputs authorize which state changes
- evidence precision
  - what counts as observed success
  - what does not count as proof
- harness precision
  - which checks block dishonest advancement automatically
- review precision
  - which structured objects humans should inspect instead of re-deriving intent
    from a pile of code diffs

Without this front-loaded precision, review degrades into post-hoc archaeology.

### 11. Human review needs structured leverage

Human review is strongest when it inspects a decision structure, not only a
natural-language explanation and not only a final code diff.

High-leverage review surfaces include:

- control objects with explicit status and provenance
- transition commands with declared guards and side effects
- bounded adjudication plans
- harness outputs tied to observed state change

The goal is to let reviewers ask:

- is the state model complete
- is this branch legal
- is this transition missing a guard
- is this evidence sufficient
- did the harness observe the claimed effect

instead of forcing them to reverse-engineer hidden assumptions from agent-written code.

### 12. Harness is part of the product, not only validation

Spec without harness becomes advisory prose.

Harness without spec becomes unprincipled scripting.

This project should treat spec and harness as co-owned product surfaces:

- spec defines what the agent is not allowed to invent
- harness defines what the system refuses to accept without evidence

That is why real progress here is not only more memory or better retrieval.
It is better control over what agents may claim, what reviewers inspect, and
what the repo accepts as honest state.

## What the system is

The system is:

- multi-project
- coding-first
- workspace-aware
- git-aware
- file-first
- handoff-oriented
- retrieval-enhanced

## What the system is not

The system is not:

- a raw transcript archive UI
- a general-purpose personal memory product
- a single-project governance clone
- a vector database with notes attached
- a substitute for clear project documentation

## Design Consequence

The preferred design direction is:

- source of truth in Markdown files
- per-project working memory and snapshots
- per-project and cross-project durable memory
- SQLite plus FTS5 as the phase-1 retrieval engine
- optional semantic retrieval as an enhancement layer
- a separate context engine / handoff layer that decides what to inject into a
  live session
