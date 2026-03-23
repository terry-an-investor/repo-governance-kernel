---
id: piv-2026-03-23-0001
type: pivot
title: Clarify the project from memory system to coding control system
status: active
project_id: session-memory
workspace_id: ws-1490b759
workspace_root: C:/Users/terryzzb/Desktop/session-memory
branch: master
git_sha: 0d603f3e2ed77feed60c71812169593f982cbaad
paths:
  - CONTROL_SYSTEM.md
  - DESIGN_PRINCIPLES.md
  - ARCHITECTURE.md
  - SCHEMA.md
  - IMPLEMENTATION_PLAN.md
  - projects/session-memory/control/
thread_ids: []
evidence_refs:
  - type: doc
    ref: C:/Users/terryzzb/Desktop/session-memory/CONTROL_SYSTEM.md
  - type: note
    ref: C:/Users/terryzzb/Desktop/session-memory/projects/session-memory/current/current-task.md
tags:
  - pivot
  - hard
  - control-system
confidence: high
created_at: 2026-03-23T21:10:00+08:00
updated_at: 2026-03-23T21:10:00+08:00
supersedes: []
superseded_by: []
objective_id: obj-2026-03-23-0002
phase: execution
---

## Summary

The project objective was clarified from "multi-project coding-agent memory and
handoff" to "coding control system built on a memory substrate".

## Pivot Type

Hard pivot.

## Trigger

The project accumulated enough concrete discussion to reveal that the deepest
user pain is code control: staying aligned with end goals, containing monkey
patches, and enabling project-aware review and orchestration.

## Previous Objective

`obj-2026-03-23-0001` focused on memory continuity and handoff quality.

## New Objective

`obj-2026-03-23-0002` treats memory as substrate and adds objective, pivot,
exception-contract, and control-state compilation as first-class concerns.

## Evidence

- The canonical design docs now define control-state semantics.
- The implementation plan now requires active-objective-aware assembly.
- The project's own current task reflects the new objective line.

## Decisions Retained

- files remain canonical
- SQLite plus FTS5 remains the phase-1 retrieval engine
- project-agnostic schema remains mandatory

## Assumptions Invalidated

- Better recall alone is enough to control an evolving codebase.
- Reviewer or architect prompts can be useful without durable project state.

## Next Control Changes

- materialize real control-state files
- teach `assemble` to read active objective and exception-contract state
- evaluate whether control-state injection improves orientation quality
