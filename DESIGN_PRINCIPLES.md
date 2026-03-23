# Session Memory Design Principles

Date: 2026-03-22
Scope: Multi-project coding-agent memory and control

## Goal

Build a memory and control system that helps a fresh coding-agent session
quickly recover the real engineering state of the current project and workspace
without replaying entire chat transcripts.

The system is not a generic personal memory product. It is a coding-work memory
and control layer for implementation, debugging, architecture review, handoff,
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
- which workarounds are temporary debt
- whether the project has pivoted

Without this layer, retrieval can recover facts while still accelerating drift.

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
  - workaround ledger
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
- active workarounds
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
