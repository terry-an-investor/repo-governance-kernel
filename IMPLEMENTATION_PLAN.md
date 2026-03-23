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

## Phase 1 Out Of Scope

- DuckDB
- embeddings
- reranking
- automatic transcript extraction
- graph reasoning
- generalized memory ontology expansion
- automatic pivot detection beyond explicit operator-authored records

## Current Implementation Gaps

### Control files

- add canonical project-agnostic control files under `projects/<project_id>/control/`
- make `assemble` read active objective and workaround state
- keep pivot handling explicit before any automation tries to infer it

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
6. rerun real builds and queries

## Validation Standard

Phase 1 is only considered working when:

- the SQLite file is rebuilt successfully from current Markdown memory
- metadata tables contain expected rows
- FTS5 recall returns real project records
- one fresh-session context packet is generated from indexed project memory
