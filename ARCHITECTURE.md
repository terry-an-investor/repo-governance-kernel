# Session Memory Architecture

Date: 2026-03-22
Scope: Multi-project coding-agent memory and control

## Goal

Turn raw coding-agent activity into reusable memory and control state that
supports:

- new-session recovery
- side-session review
- architecture continuity
- failure recall
- decision traceability
- controlled project pivots
- multi-project switching without context contamination

## Architectural Summary

The system should be read together with [`CONTROL_SYSTEM.md`](./CONTROL_SYSTEM.md).
The transition model is defined in [`STATE_MACHINE.md`](./STATE_MACHINE.md).
The future command surface is defined in [`TRANSITION_COMMANDS.md`](./TRANSITION_COMMANDS.md).

Memory is the storage substrate. Control state is the thing that keeps the
project direction coherent.

The architecture also needs to distinguish three different jobs that are easy
to collapse incorrectly:

- projection
  - rebuild compact control files from already coherent durable truth
- audit
  - detect that the current control state is dishonest or incomplete
- adjudication
  - decide how durable conflicts should be resolved before transition commands
    rewrite state

The system has four layers:

1. raw event store
2. extraction and summarization
3. memory store
4. retrieval and context injection

The control layer also depends on coordinated state domains rather than one
global status bit:

- objective-line state
- project phase state
- round state
- exception-contract state
- memory freshness state

This keeps raw history available while making extracted memory explicit and
cheap to consume.

Current implementation has durable truth and projected control state. It now
also gains a first control-audit path and a first durable adjudication record
path. It now also gains a narrow follow-up executor for safe scaffolding. It
still lacks general adjudication-driven state rewrites.

## Layer 1: Raw Event Store

Purpose:

- preserve original evidence
- support later extraction and audit
- avoid losing information before extraction improves

Inputs may include:

- `.codex/sessions/*.jsonl`
- `.codex/archived_sessions/*.jsonl`
- `.codex/history.jsonl`
- `.codex/state_*.sqlite`
- runtime logs
- project-specific governance artifacts
- user-authored notes
- test artifacts
- screenshots or other evidence files

Properties:

- append-heavy
- noisy
- not suitable for direct injection into a fresh session

## Layer 2: Extraction and Summarization

Purpose:

- transform raw event streams into explicit memory objects
- separate durable facts from temporary chat noise

Extraction outputs should include:

- handoff snapshots
- decision records
- failure records
- constraint records
- objective records
- pivot records
- exception-contract records
- task state
- reusable patterns

Extraction can be:

- manual
- automatic on session-end
- automatic before compaction
- periodic for long sessions

First versions should support manual and pre-compaction extraction.

## Layer 3: Memory Store

Purpose:

- store extracted memory in a stable, inspectable, versionable format

Preferred source-of-truth storage:

- Markdown files under one session-memory workspace

Suggested store split:

- `projects/<project_id>/`
  - project-local control state
  - project-local working memory
  - project-local snapshots
  - project-local durable memory
  - project-local artifacts
- `cross-project/`
  - durable memory that applies across projects
- `index/`
  - SQLite metadata store plus FTS5 retrieval index

The SQLite layer is an accelerator and query engine, not the canonical source.
DuckDB is not part of the first implementation plan.

## Layer 4: Retrieval and Context Injection

Purpose:

- retrieve the most relevant memory for a live session
- inject the right subset into model context

This layer should answer:

- what memory matters for this project
- what memory matters for this concrete workspace
- what memory matters for this branch / git sha
- what memory matters for these files
- what memory matters for the current task topic
- what handoff summary should a fresh session read first
- what objective line is currently active
- whether the project is in exploration or execution
- whether a pivot invalidated older assumptions

Before a handoff packet is trusted as current state, this layer should also
answer:

- which workspace / branch / git sha the packet claims to describe
- whether current-task and latest snapshot agree on that anchor
- whether the live workspace still matches that anchor
- whether the packet should be treated as current truth or orientation-only

Retrieval priority:

1. structured filters
2. FTS5 full-text search
3. semantic search
4. reranking

This keeps the system grounded in explicit work state.

Context assembly should compile through the active objective line, not only
through recency.

The default handoff packet should stay orientation-first.

That means project constitution is usually recall-only for the generic packet,
while reviewer / architect / orchestrator contexts may inline it explicitly.

Context injection should surface freshness explicitly.

An assembled packet should include:

- packet generation time
- packet anchor source
- packet anchor metadata
- latest snapshot anchor metadata
- live workspace check
- freshness verdict
- operator guidance when the packet is stale

The current-task anchor should also have a maintenance path.

At minimum, the system should support refreshing:

- branch
- git sha
- worktree state
- changed path count

without forcing a new snapshot every time the workspace moves.

Because `current/current-task.md` is itself a committed control projection, its
anchor metadata should be treated as the workspace facts observed at the last
refresh, not as a self-updating guarantee that the file already names the exact
commit that contains it.

That file is best understood as a control-plane orientation projection:

- the narrative is hand-maintained and not fully derivable from durable truth
- the workspace anchor remains historical metadata until explicitly refreshed
- the durable-control subset should still stay aligned:
  - `Objective id`
  - `Active round id`
  - `Phase`

That means live workspace inspection remains the canonical freshness check for
the current branch, while current-task anchor fields remain useful orientation
metadata.

That creates a useful distinction:

- `stale`
  - packet anchor no longer matches the live workspace
- `fresh_snapshot_behind`
  - current-task matches the live workspace, but the latest snapshot is now
    historical

Snapshot creation should also have a maintenance path.

At minimum, the system should support creating one new snapshot from:

- live workspace anchor
- current-task sections
- blockers
- optional seed material from the latest snapshot

without requiring a manual rewrite of the full handoff document every time.

A higher-level capture flow can then compose:

- current-task anchor refresh
- snapshot creation
- packet assembly

without replacing the lower-level commands as independent primitives.

## Memory Types

The initial schema should stay coding-oriented.

Suggested types:

- `constitution`
  - durable project operating rules and invariants
- `objective`
  - current or historical project goal line
- `pivot`
  - explicit objective-line change record
- `decision`
  - architecture and implementation choices
- `failure`
  - failed attempts, bad assumptions, invalid approaches
- `constraint`
  - environment, product, repo, or tool limitations
- `exception-contract`
  - temporary deviation with risk, owner scope, and exit condition
- `adjudication`
  - explicit durable verdict about conflicting control truth
- `task`
  - current or pending work state
- `artifact`
  - logs, screenshots, traces, benchmark outputs, test evidence
- `handoff`
  - what a new session should know before continuing
- `pattern`
  - reusable tactics or workflow fragments
- `validation-report`
  - structured evidence about what was actually proven

## Required Metadata

Important memory items should carry:

- `id`
- `type`
- `title`
- `summary`
- `project_id`
- `workspace_id`
- `workspace_root`
- `branch`
- `git_sha`
- `paths[]`
- `thread_ids[]`
- `created_at`
- `updated_at`
- `evidence_refs[]`
- `confidence`
- `supersedes[]`
- `tags[]`

Why these matter:

- `project_id` anchors semantic ownership
- `workspace_id / workspace_root` distinguish concrete local workspaces
- `branch / git_sha` anchor memory to code state
- `paths[]` anchor memory to affected scope
- `thread_ids[]` trace back to raw origin
- `evidence_refs[]` provide justification
- `supersedes[]` support memory evolution without silent contradiction

## File Layout Proposal

Suggested root directory:

```text
session-memory/
├── CONTROL_SYSTEM.md
├── STATE_MACHINE.md
├── TRANSITION_COMMANDS.md
├── DESIGN_PRINCIPLES.md
├── ARCHITECTURE.md
├── SCHEMA.md
├── projects/
│   ├── wind-agent/
│   │   ├── control/
│   │   │   ├── constitution.md
│   │   │   ├── active-objective.md
│   │   │   ├── active-round.md
│   │   │   ├── pivot-log.md
│   │   │   └── exception-ledger.md
│   │   ├── current/
│   │   │   ├── current-task.md
│   │   │   ├── blockers.md
│   │   │   └── idea-inbox.md
│   │   ├── snapshots/
│   │   ├── memory/
│   │   │   ├── objectives/
│   │   │   ├── pivots/
│   │   │   ├── rounds/
│   │   │   ├── transition-events/
│   │   │   ├── adjudications/
│   │   │   ├── decisions/
│   │   │   ├── failures/
│   │   │   ├── constraints/
│   │   │   ├── exception-contracts/
│   │   │   ├── patterns/
│   │   │   ├── handoffs/
│   │   │   └── validation-reports/
│   │   └── artifacts/
│   └── another-project/
├── cross-project/
│   ├── decisions/
│   ├── failures/
│   ├── constraints/
│   └── patterns/
├── index/
└── templates/
```

Notes:

- `projects/<project_id>/current/` is mutable working memory
- `projects/<project_id>/control/` is mutable control state
- `projects/<project_id>/snapshots/` is phase-oriented handoff output
- `projects/<project_id>/memory/` stores project-local durable memory
- `cross-project/` stores memories that generalize across projects
- `index/` is optional query acceleration

The control plane is expected to evolve from:

- direct file edits

to:

- transition commands with guards and side effects over these canonical paths

## Snapshot Model

A snapshot is the closest thing to a memory commit for one project workspace.

Each snapshot should summarize:

- current goal
- completed work
- validated facts
- rejected approaches
- active blockers
- important files
- related workspace / branch / git sha
- next steps
- references to evidence or raw session origins

Fresh sessions should read the latest relevant project snapshot first.

## Relationship to Git

Git is not the memory system, but it is a critical anchor.

Git should provide:

- branch context
- commit anchors
- file scope
- change state references

The memory layer should provide:

- why something matters
- why a decision was made
- what was learned
- what the next session should do

Git explains code evolution.
Memory explains reasoning evolution.

## Context Engine Boundary

The context engine is not the same thing as memory storage.

Memory storage is responsible for:

- persistence
- extraction
- retrieval

Context injection is responsible for:

- session bootstrapping
- handoff loading
- compaction support
- side-session or subagent context seeding

This boundary allows:

- different retrieval policies without changing storage
- different compaction logic without changing memory truth
- different recall backends without changing file layout

## Recommended First Implementation

Phase 1 should avoid overbuilding.

Recommended initial stack:

- Markdown source-of-truth files
- a small SQLite index with FTS5
- manual snapshot creation plus optional pre-compaction flush
- structured metadata attached to memory items

Phase-1 design stance:

- design docs are canonical before implementation expands
- implementation should follow the frozen schema and retrieval order
- SQLite plus FTS5 is the default local retrieval engine
- DuckDB is deferred unless a later phase needs analytical workloads that
  SQLite does not handle well

Do not start with:

- generalized vector-only memory
- large ontology design
- mandatory reranking
- DuckDB-first indexing
- automatic extraction of every transcript fragment

## Architectural Thesis

The most important property of the system is not search quality.

It is this:

A new coding-agent session should be able to recover the real state of the
current project workspace from explicit memory objects, without replaying entire
transcripts and without guessing what still matters.
