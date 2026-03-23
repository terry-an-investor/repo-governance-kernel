# Session Memory Schema

Date: 2026-03-22
Scope: Multi-project coding-agent memory and control

## Purpose

This document defines the canonical file schema for multi-project coding-agent
memory and control.

The design goal is to keep memory:

- human-readable
- git-friendly
- easy to index
- easy for a fresh coding-agent session to consume
- safe across multiple projects and multiple local workspaces

## Design Summary

The source of truth is Markdown files with structured YAML frontmatter.

Memory is split into:

- mutable control-state files
- mutable working-state files
- immutable or append-mostly durable memory items
- phase-oriented handoff snapshots

Memory is also split by scope:

- project-local memory
- cross-project memory

## Top-Level Layout

```text
session-memory/
├── projects/
│   ├── <project_id>/
│   │   ├── control/
│   │   │   ├── constitution.md
│   │   │   ├── active-objective.md
│   │   │   ├── pivot-log.md
│   │   │   └── workaround-ledger.md
│   │   ├── current/
│   │   │   ├── current-task.md
│   │   │   ├── blockers.md
│   │   │   └── idea-inbox.md
│   │   ├── snapshots/
│   │   ├── memory/
│   │   │   ├── objectives/
│   │   │   ├── pivots/
│   │   │   ├── decisions/
│   │   │   ├── failures/
│   │   │   ├── constraints/
│   │   │   ├── workarounds/
│   │   │   ├── patterns/
│   │   │   ├── handoffs/
│   │   │   └── validation-reports/
│   │   └── artifacts/
├── cross-project/
│   ├── decisions/
│   ├── failures/
│   ├── constraints/
│   └── patterns/
├── index/
└── templates/
```

## Canonical Memory Object Types

Initial memory object types:

- `constitution`
- `objective`
- `pivot`
- `decision`
- `failure`
- `constraint`
- `workaround`
- `pattern`
- `handoff`
- `task`
- `artifact`
- `validation-report`
- `hypothesis`

## Identity Model

The minimum identity split is:

- `project_id`
  - semantic project identity such as `wind-agent`
- `workspace_id`
  - concrete local workspace or worktree identity
- `workspace_root`
  - human-readable absolute workspace path

This split exists because one project can have:

- multiple local clones
- multiple worktrees
- multiple branches active at once
- different machines or roots

## Shared Frontmatter

All durable memory objects should use this shared frontmatter shape when
possible.

```yaml
id: mem-2026-03-22-0001
type: decision
title: Prepared query context must be a first-class consumer contract
status: active
project_id: wind-agent
workspace_id: ws-8c2176c3
workspace_root: C:/Users/terryzzb/Desktop/wind-agent
branch: master
git_sha: 765c444c9dcd04ba09c58cd7e637ccd7a4669cca
paths:
  - src/wind/query/surface.js
  - src/wind/state_machine/adapters.js
thread_ids: []
evidence_refs:
  - type: session
    ref: .codex/sessions/2026/03/22/rollout-...
  - type: artifact
    ref: outputs/query-surface-prepared-context-live-.../summary.json
tags:
  - transient-surface
  - contract
confidence: high
created_at: 2026-03-22T20:00:00+08:00
updated_at: 2026-03-22T20:00:00+08:00
supersedes: []
superseded_by: []
```

Control-bearing objects may also add these optional linkage fields when they
matter:

- `objective_id`
  - the objective line this item belongs to
- `pivot_id`
  - the pivot event that introduced or invalidated this item
- `phase`
  - suggested values:
    - `exploration`
    - `execution`

## Shared Field Definitions

- `id`
  - stable memory item identifier
- `type`
  - one of the canonical memory object types
- `title`
  - short human-readable label
- `status`
  - suggested values:
    - `active`
    - `historical`
    - `superseded`
    - `invalidated`
- `project_id`
  - semantic project identifier
- `workspace_id`
  - stable identifier for one concrete local workspace
- `workspace_root`
  - human-readable absolute workspace root
- `branch`
  - git branch at the time of extraction
- `git_sha`
  - commit anchor for the remembered state
- `paths`
  - affected files, directories, or module scopes
- `thread_ids`
  - source coding-agent sessions
- `evidence_refs`
  - logs, docs, screenshots, traces, transcripts, tests, commits, project-local
    governance artifacts
- `tags`
  - lightweight thematic labels
- `confidence`
  - suggested values:
    - `low`
    - `medium`
    - `high`
- `created_at`
  - first extraction time
- `updated_at`
  - last significant edit
- `supersedes`
  - memory ids replaced by this item
- `superseded_by`
  - memory ids that replaced this item
- `objective_id`
  - optional linkage to the active or historical objective line
- `pivot_id`
  - optional linkage to the pivot record that changed context
- `phase`
  - optional project phase at extraction time, usually `exploration` or
    `execution`

## Durable Memory File Shapes

### Objective

Use for the current or historical project objective line.

Suggested sections:

- summary
- problem
- success criteria
- non-goals
- current phase
- active risks
- supersession notes

### Pivot

Use for explicit changes to the project's objective line.

Suggested sections:

- summary
- pivot type
- trigger
- previous objective
- new objective
- evidence
- decisions retained
- assumptions invalidated
- next control changes

### Workaround

Use for temporary compromises that are intentionally not the target design.

Suggested sections:

- summary
- reason
- temporary behavior
- risk
- exit condition
- owner scope
- evidence

### Validation Report

Use for structured evidence about what was actually checked.

Suggested sections:

- claim
- command or procedure
- result
- coverage
- gaps
- artifacts

### Hypothesis

Use for exploration-stage framings that are not yet promoted to objective.

### Decision

Use for architecture or implementation choices.

```markdown
---
id: mem-2026-03-22-0001
type: decision
title: Prepared query context must be a first-class consumer contract
status: active
project_id: wind-agent
workspace_id: ws-8c2176c3
workspace_root: C:/Users/terryzzb/Desktop/wind-agent
branch: master
git_sha: 765c444c9dcd04ba09c58cd7e637ccd7a4669cca
paths:
  - src/wind/query/
  - src/wind/state_machine/
thread_ids: []
evidence_refs: []
tags: [transient-surface, contract]
confidence: high
created_at: 2026-03-22T20:00:00+08:00
updated_at: 2026-03-22T20:00:00+08:00
supersedes: []
superseded_by: []
---

## Summary

One-paragraph summary of the decision.

## Context

What problem forced the decision.

## Decision

What was chosen.

## Rejected Alternatives

What was considered and rejected.

## Evidence

Concrete evidence or validation that supports the decision.

## Consequences

What changes because this decision exists.
```

### Failure

Use for failed approaches, wrong assumptions, or misleading evidence.

```markdown
---
id: mem-2026-03-22-0002
type: failure
title: Active round contract drifted behind the real worktree
status: active
project_id: wind-agent
workspace_id: ws-8c2176c3
workspace_root: C:/Users/terryzzb/Desktop/wind-agent
branch: master
git_sha: 765c444c9dcd04ba09c58cd7e637ccd7a4669cca
paths:
  - .round/active.json
  - src/native/
thread_ids: []
evidence_refs: []
tags: [governance, scope-drift]
confidence: high
created_at: 2026-03-22T20:00:00+08:00
updated_at: 2026-03-22T20:00:00+08:00
supersedes: []
superseded_by: []
---

## Summary

Short statement of what failed.

## Trigger

What action or situation exposed the failure.

## Bad Assumption

What was believed that turned out to be wrong.

## Evidence

What proved the assumption false.

## Follow-up

What should be done next time instead.
```

### Constraint

Use for environment, product, repo, runtime, or tool limits.

### Pattern

Use for reusable tactics or process fragments.

Patterns may live in either:

- `projects/<project_id>/memory/patterns/`
- `cross-project/patterns/`

depending on whether the lesson is project-local or reusable across projects.

### Handoff

Use for session-to-session transfer state.

Handoff is special: it can be snapshot-like, but it should still be treated as
an object with provenance.

## Control-State Files

Control-state files are mutable and optimize for current project governance.

### `projects/<project_id>/control/constitution.md`

Purpose:

- capture durable rules, invariants, and quality bars for one project

Suggested shape:

```markdown
# Constitution

## Product Boundaries

## Architecture Invariants

## Quality Bar

## Validation Rules

## Forbidden Shortcuts
```

### `projects/<project_id>/control/active-objective.md`

Purpose:

- state the currently active objective line and whether the project is in
  exploration or execution

Suggested shape:

```markdown
# Active Objective

- Objective id:
- Phase: exploration | execution
- Status: active

## Problem

## Success Criteria

## Non-Goals

## Why Now

## Current Risks
```

### `projects/<project_id>/control/pivot-log.md`

Purpose:

- provide a compact chronological view of objective-line changes

Suggested shape:

```markdown
# Pivot Log

## Active Lineage

## Recent Pivots

## Historical Objectives
```

### `projects/<project_id>/control/workaround-ledger.md`

Purpose:

- track temporary compromises separately from real architecture

Suggested shape:

```markdown
# Workaround Ledger

## Active

## Retired

## Invalidated By Pivot
```

## Working-State Files

Working-state files are mutable and optimized for live use, not immutable
history.

### `projects/<project_id>/current/current-task.md`

Purpose:

- the single most important current-state file for one project

Suggested shape:

```markdown
# Current Task

## Goal

## Current State

## Validated Facts

## Important Files

## Active Risks

## Next Steps
```

Recommended `Current State` anchor bullets:

- `Objective id`
- `Phase`
- `Workspace id`
- `Workspace root`
- `Branch`
- `HEAD anchor`

Optional but useful:

- one explicit worktree hint such as `clean` or `dirty`
- `Changed path count`
- `Last anchor refresh`

Recommended maintenance path:

- refresh these anchor bullets from the live workspace without rewriting the
  whole task narrative

### `projects/<project_id>/current/blockers.md`

Purpose:

- explicit blockers, uncertainties, and dependencies for one project

Suggested shape:

```markdown
# Blockers

## Active

## Waiting

## Cleared
```

### `projects/<project_id>/current/idea-inbox.md`

Purpose:

- offload ideas without interrupting the mainline

Suggested shape:

```markdown
# Idea Inbox

## New

## Triaged

## Discarded
```

## Snapshot Schema

Snapshots are commit-like summaries for phase transitions and handoff.

Suggested filename:

```text
projects/<project_id>/snapshots/YYYY-MM-DD-HHMM-<topic>.md
```

Suggested frontmatter:

```yaml
id: snap-2026-03-22-2030-mainline
type: handoff
title: Mainline handoff after owner-layer review
project_id: wind-agent
workspace_id: ws-8c2176c3
workspace_root: C:/Users/terryzzb/Desktop/wind-agent
branch: master
git_sha: 765c444c9dcd04ba09c58cd7e637ccd7a4669cca
paths:
  - src/
  - native/
thread_ids: []
created_at: 2026-03-22T20:30:00+08:00
updated_at: 2026-03-22T20:30:00+08:00
tags: [handoff, owner-layer]
```

Suggested body:

- goal
- completed work
- validated facts
- rejected approaches
- blockers
- important files
- next steps

Recommended maintenance path:

- create a new snapshot from live workspace anchor plus current-task sections
- allow latest snapshot sections such as `Completed Work` and
  `Rejected Approaches` to seed the new snapshot when they remain relevant
- do not mutate the previous snapshot in place

## Assembled Packet Freshness Block

The assembled fresh-session packet should synthesize a `Packet Freshness` block
from:

- `current/current-task.md`
- the latest snapshot frontmatter
- the live workspace when it is reachable

Suggested fields:

- `generated_at`
- `freshness_verdict`
- `packet_anchor_source`
- packet anchor:
  - `workspace_id`
  - `workspace_root`
  - `branch`
  - `git_sha`
  - optional worktree hint
- latest snapshot anchor:
  - `source`
  - `updated_at`
  - `branch`
  - `git_sha`
- live workspace check:
  - branch
  - git sha
  - clean or dirty state
- anchor warnings
- operator guidance

The verdict should tell a fresh session whether the packet still matches the
live workspace or should only be treated as orientation context.

Suggested initial verdicts:

- `fresh`
- `live_match_dirty`
- `fresh_snapshot_behind`
- `fresh_snapshot_behind_dirty`
- `stale`
- `workspace_unavailable`

## Snapshot Writer Workflow

The minimal snapshot writer should:

1. read `current/current-task.md`
2. read `current/blockers.md` when present
3. inspect the live workspace for branch and git sha
4. optionally read the latest snapshot as seed material
5. write one new snapshot file

This keeps the maintenance flow additive and git-friendly.

## Capture Workflow

The minimal high-level capture workflow should:

1. refresh `current/current-task.md` anchor bullets from the live workspace
2. write one new snapshot
3. assemble one fresh-session packet against the updated current-task state

This workflow is a convenience layer over the lower-level primitives, not a
replacement for them.

## File Naming

Durable item naming should be explicit and grep-friendly.

Suggested patterns:

```text
projects/<project_id>/memory/<type>s/YYYY-MM-DD-<slug>.md
cross-project/<type>s/YYYY-MM-DD-<slug>.md
```

Examples:

- `projects/wind-agent/memory/decisions/2026-03-22-prepared-query-context-first-class-contract.md`
- `projects/wind-agent/memory/failures/2026-03-22-round-contract-worktree-drift.md`
- `cross-project/patterns/2026-03-22-handoff-before-context-compaction.md`

## SQLite Index Shape

The initial SQLite index should be small, metadata-focused, and paired with an
FTS5 table for body and summary recall.

DuckDB is not part of the phase-1 schema.

Suggested tables:

- `memory_items`
- `memory_paths`
- `memory_evidence_refs`
- `memory_links`
- `memory_fts`

### `memory_items`

Suggested columns:

- `id`
- `type`
- `title`
- `status`
- `scope_kind`
- `project_id`
- `workspace_id`
- `workspace_root`
- `branch`
- `git_sha`
- `summary_text`
- `body_text`
- `source_file`
- `confidence`
- `created_at`
- `updated_at`

### `memory_paths`

Suggested columns:

- `memory_id`
- `path`

### `memory_evidence_refs`

Suggested columns:

- `memory_id`
- `evidence_type`
- `ref`

### `memory_links`

Suggested columns:

- `src_memory_id`
- `link_type`
- `dst_memory_id`

### `memory_fts`

Suggested columns:

- `id`
- `title`
- `summary_text`
- `body_text`

Suggested model:

- FTS5 virtual table
- `id` kept aligned with `memory_items.id`
- used only after structured filtering has already narrowed the candidate set

## Indexing Order

Recommended retrieval order:

1. filter by `project_id`
2. narrow by `workspace_id` when needed
3. narrow by `branch` and `git_sha` when appropriate
4. narrow by `paths`
5. query FTS5 text
6. only then apply semantic retrieval if needed

## First Implementation Boundaries

The first implementation should not attempt:

- automatic extraction of every raw transcript fragment
- full graph reasoning
- mandatory embeddings
- generalized non-coding memory categories

The first implementation should provide:

- file schema
- per-project working-state files
- snapshot files
- durable memory item files
- SQLite metadata index
- FTS5 full-text table
