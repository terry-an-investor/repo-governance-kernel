# Session Memory Implementation Plan

Date: 2026-03-22
Scope: Phase 1 only

## Goal

Implement the smallest honest retrieval loop that matches the frozen design:

- Markdown files remain the source of truth
- SQLite is the local index store
- FTS5 is the phase-1 full-text engine
- retrieval stays structure-first, then FTS5

## Phase 1 In Scope

- index Markdown memory files under `projects/` and `cross-project/`
- populate SQLite metadata tables
- populate one FTS5 table for recall
- support structured filters:
  - `project_id`
  - `workspace_id`
  - `type`
  - `path`
- support FTS5 text recall after structured narrowing
- assemble one fresh-session context packet from canonical files plus durable memory

## Phase 1 Out Of Scope

- DuckDB
- embeddings
- reranking
- automatic transcript extraction
- graph reasoning
- generalized memory ontology expansion

## Current Implementation Gaps

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

1. align index schema with `SCHEMA.md`
2. add FTS5 population in the builder
3. switch query path from `LIKE` to FTS5
4. rerun real builds and queries
5. only then refine context assembly output

## Validation Standard

Phase 1 is only considered working when:

- the SQLite file is rebuilt successfully from current Markdown memory
- metadata tables contain expected rows
- FTS5 recall returns real project records
- one fresh-session context packet is generated from indexed project memory
