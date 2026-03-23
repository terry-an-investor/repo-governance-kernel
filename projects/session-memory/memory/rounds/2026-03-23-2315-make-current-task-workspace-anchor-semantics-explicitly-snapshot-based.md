---
id: round-2026-03-23-2315-make-current-task-workspace-anchor-semantics-explicitly-snapshot-based
type: round-contract
title: "Make current-task workspace anchor semantics explicitly snapshot-based"
status: active
project_id: session-memory
workspace_id: ws-1490b759
workspace_root: C:/Users/terryzzb/Desktop/session-memory
branch: master
git_sha: 3df662f331779f6c363aca5fa96ce5cb94257b66
paths:
  - scripts/assemble_context.py
  - scripts/refresh_current_task_anchor.py
  - scripts/round_control.py
  - CONTROL_SYSTEM.md
  - TRANSITION_COMMANDS.md
  - projects/session-memory/current/current-task.md
thread_ids: []
evidence_refs: []
tags:
  - round
  - control-plane
confidence: high
created_at: 2026-03-23T23:15:35+08:00
updated_at: 2026-03-23T23:15:35+08:00
objective_id: obj-2026-03-23-0002
phase: execution
supersedes: []
superseded_by: []
---

## Summary

Current-task workspace anchor fields are explicitly snapshot-scoped, parser-compatible, and documented as historical orientation metadata rather than self-updating live state.

## Scope

- Rename current-task workspace anchor bullets so they read as last-refresh snapshot metadata rather than live truth.
- Keep assemble-context, refresh-current-task-anchor, and canonical docs aligned on the same snapshot semantics.

## Deliverable

Current-task workspace anchor fields are explicitly snapshot-scoped, parser-compatible, and documented as historical orientation metadata rather than self-updating live state.

## Validation Plan

Refresh current-task under the new wording, run real-project audit and enforce-worktree, and verify assemble-context still reads the renamed anchor fields.

## Active Risks

_none recorded_

## Blockers

_none recorded_

## Status Notes

_none recorded_
