---
id: mem-2026-03-23-0001
type: decision
title: Phase-1 retrieval engine stays on SQLite plus FTS5
status: active
project_id: session-memory
workspace_id: ws-1490b759
workspace_root: C:/Users/terryzzb/Desktop/session-memory
branch: master
git_sha: 0d603f3e2ed77feed60c71812169593f982cbaad
paths:
  - docs/canonical/DESIGN_PRINCIPLES.md
  - docs/canonical/ARCHITECTURE.md
  - docs/canonical/SCHEMA.md
  - docs/canonical/IMPLEMENTATION_PLAN.md
  - scripts/build_index.py
  - scripts/query_index.py
thread_ids: []
evidence_refs:
  - type: doc
    ref: C:/Users/terryzzb/Desktop/session-memory/docs/canonical/DESIGN_PRINCIPLES.md
  - type: doc
    ref: C:/Users/terryzzb/Desktop/session-memory/docs/canonical/ARCHITECTURE.md
  - type: doc
    ref: C:/Users/terryzzb/Desktop/session-memory/docs/canonical/SCHEMA.md
  - type: commit
    ref: 0d603f3e2ed77feed60c71812169593f982cbaad
tags:
  - phase-1
  - sqlite
  - fts5
  - retrieval
confidence: high
created_at: 2026-03-23T07:22:44+08:00
updated_at: 2026-03-23T07:22:44+08:00
supersedes: []
superseded_by: []
---

## Summary

The first implementation should keep local retrieval on SQLite plus FTS5 rather
than introducing DuckDB, embeddings, or rerank infrastructure.

## Context

The project needed a real phase-1 implementation path that stayed aligned with
the frozen design. The main risk was reopening architecture churn before the
smallest useful retrieval loop had been pressure-tested.

## Decision

Phase 1 uses:

- Markdown files as source of truth
- SQLite as the local index store
- FTS5 as the full-text retrieval engine

DuckDB and embedding layers stay out of phase 1.

## Rejected Alternatives

- DuckDB-first indexing for phase 1.
- Designing the retrieval layer around embeddings before file and FTS workflow
  were proven.
- Expanding ontology and graph behavior before a stable local recall loop
  existed.

## Evidence

- The canonical docs explicitly freeze SQLite plus FTS5 as the phase-1 engine.
- The committed baseline already builds, queries, and assembles against that
  stack.

## Consequences

- Implementation work should focus on schema fidelity, FTS recall quality, and
  handoff assembly quality.
- Later phases can add semantic retrieval only after this smaller system is
  proven useful.
