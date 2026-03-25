---
id: round-2026-03-23-2315-make-current-task-workspace-anchor-semantics-explicitly-snapshot-based
type: round-contract
title: "Make current-task workspace anchor semantics explicitly snapshot-based"
status: closed
project_id: repo-governance-kernel
workspace_id: ws-1490b759
workspace_root: C:/Users/terryzzb/Desktop/session-memory
branch: master
git_sha: 8481148a853ec840f7c5241153dfbd8f19545050
paths:
  - scripts/assemble_context.py
  - scripts/refresh_current_task_anchor.py
  - scripts/round_control.py
  - CONTROL_SYSTEM.md
  - TRANSITION_COMMANDS.md
  - state/repo-governance-kernel/current/current-task.md
thread_ids: []
evidence_refs: []
tags:
  - round
  - control-plane
confidence: high
created_at: 2026-03-23T23:15:35+08:00
updated_at: 2026-03-23T23:20:30+08:00
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
uv run python scripts/refresh_current_task_anchor.py --project-id repo-governance-kernel
uv run python scripts/assemble_context.py --project-id repo-governance-kernel --memory-limit 5 --output artifacts/repo-governance-kernel/current-task-snapshot-anchor-context.md
uv run python scripts/audit_control_state.py --project-id repo-governance-kernel
uv run python scripts/enforce_worktree.py --project-id repo-governance-kernel

## Active Risks

_none recorded_

## Blockers

_none recorded_

## Status Notes

active -> validation_pending: Current-task workspace anchor fields now use explicit snapshot wording, parser compatibility is in place, and the real-project validation commands are ready for round closeout.

validation_pending -> captured: Real-project refresh, assemble-context, audit, and enforce-worktree all passed with current-task workspace anchors expressed as last-refresh snapshot metadata.

validated by:
- uv run python scripts/refresh_current_task_anchor.py --project-id repo-governance-kernel
- uv run python scripts/assemble_context.py --project-id repo-governance-kernel --memory-limit 5 --output artifacts/repo-governance-kernel/current-task-snapshot-anchor-context.md
- uv run python scripts/audit_control_state.py --project-id repo-governance-kernel
- uv run python scripts/enforce_worktree.py --project-id repo-governance-kernel

captured -> closed: The snapshot-semantics slice is implemented and validated, so this bounded execution round can close without leaving the objective in execution.


