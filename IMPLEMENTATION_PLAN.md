# Session Memory Implementation Plan

Date: 2026-03-22
Scope: Phase 1 only

## Goal

Implement the smallest honest retrieval and control loop that matches the
frozen design:

- Markdown files remain the source of truth
- SQLite is the local index store
- FTS5 is the phase-1 full-text engine
- retrieval stays structure-first, then FTS5
- control state stays file-first before automation expands

This phase is now partially state-machine enforced.

Today that enforcement is intentionally narrow:

- the objective-line domain can open a first active objective
- the objective-line domain can record a guarded hard pivot
- the round domain has real transition commands
- illegal round-status transitions are rejected
- transition events are recorded as durable files

It is not yet a unified transition engine across every domain.

## Phase 1 In Scope

- establish canonical control objects in files:
  - constitution
  - active objective
  - pivot log
  - workaround ledger
- index Markdown memory files under `projects/` and `cross-project/`
- populate SQLite metadata tables
- populate one FTS5 table for recall
- support structured filters:
  - `project_id`
  - `workspace_id`
  - `type`
  - `path`
- support FTS5 text recall after structured narrowing
- assemble one fresh-session context packet from canonical files plus durable
  memory
- ensure assembled context compiles through active objective and freshness
  signals rather than raw recency alone
- add role-context compilation so reviewer / architect / orchestrator can read
  project control state instead of relying on prompt text alone
- add frozen role-eval bundle preparation so role-context quality can be judged
  with a fixed rubric instead of prose preference

## Phase 1 Out Of Scope

- DuckDB
- embeddings
- reranking
- automatic transcript extraction
- graph reasoning
- generalized memory ontology expansion
- automatic pivot detection beyond explicit operator-authored records
- unified transition engine with enforced guards and side effects

## Current Implementation Gaps

### Control files

- add canonical project-agnostic control files under `projects/<project_id>/control/`
- make `assemble` read active objective and workaround state
- keep pivot handling explicit before any automation tries to infer it
- keep constitution out of the default handoff packet unless later evidence
  proves that always inlining it helps more than it bloats
- compile constitution into role-specific contexts instead
- define the future transition command surface before implementing enforcement
- first objective/pivot transition slice is now real:
  - `open-objective`
  - `record-hard-pivot`
  - hard pivots now refuse to outrun an active round still tied to the old objective
- first round transition slice is now real:
  - `open-round`
  - `update-round-status`
  - rewrite path now preserves round metadata instead of degrading frontmatter
- next enforcement slice should target workaround commands or a shared transition engine

### `scripts/build_index.py`

- keep:
  - project/cross-project scanning
  - frontmatter extraction
  - metadata table population
- must change:
  - add `memory_links`
  - add `memory_fts` as FTS5
  - ensure the schema matches `SCHEMA.md`

### `scripts/query_index.py`

- keep:
  - CLI shape for `project_id`, `workspace_id`, `type`, `path`
- must change:
  - replace `LIKE` text recall with FTS5-backed recall
  - preserve structure-first filtering

### `scripts/assemble_context.py`

- keep:
  - current-task / blockers / latest snapshot assembly
- may refine later:
  - tighter compaction
  - less duplicated structure

## Implementation Order

1. add canonical control files and objective-line semantics
2. align index schema with `SCHEMA.md`
3. add FTS5 population in the builder
4. switch query path from `LIKE` to FTS5
5. teach context assembly to compile through active objective state
6. add role-context compilers over the same control substrate
7. freeze the explicit state-machine design and transition semantics
8. rerun real builds and queries

## Validation Standard

Phase 1 is only considered working when:

- the SQLite file is rebuilt successfully from current Markdown memory
- metadata tables contain expected rows
- FTS5 recall returns real project records
- one fresh-session context packet is generated from indexed project memory
