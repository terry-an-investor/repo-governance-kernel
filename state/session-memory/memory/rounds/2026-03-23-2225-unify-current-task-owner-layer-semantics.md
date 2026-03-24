---
id: round-2026-03-23-2225-unify-current-task-owner-layer-semantics
type: round-contract
title: "Unify current-task owner-layer semantics"
status: closed
project_id: session-memory
workspace_id: ws-1490b759
workspace_root: C:/Users/terryzzb/Desktop/session-memory
branch: master
git_sha: caa256bab606d5f992f5e567ca2b034f4c12c544
paths:
  - scripts/control_enforcement.py
  - scripts/audit_control_state.py
  - scripts/refresh_current_task_anchor.py
  - scripts/round_control.py
  - ARCHITECTURE.md
  - CONTROL_SYSTEM.md
  - SCHEMA.md
  - TRANSITION_COMMANDS.md
  - state/session-memory/current/current-task.md
thread_ids: []
evidence_refs: []
tags:
  - round
  - control-plane
confidence: high
created_at: 2026-03-23T22:25:51+08:00
updated_at: 2026-03-23T22:33:19+08:00
objective_id: obj-2026-03-23-0002
phase: execution
supersedes: []
superseded_by: []
---

## Summary

A consistent owner-layer rule for current-task that no longer lets audit and enforcement disagree about its control status.

## Scope

- Make current-task semantics consistent across audit, enforcement, refresh, and canonical docs.

## Deliverable

A consistent owner-layer rule for current-task that no longer lets audit and enforcement disagree about its control status.

## Validation Plan

Refresh current-task to the new semantics, run audit_control_state and enforce_worktree on the real project, then close the round and return the objective to paused.
uv run python scripts/refresh_current_task_anchor.py --project-id session-memory -> objective/round/phase and workspace bullets refreshed
uv run python scripts/audit_control_state.py --project-id session-memory -> status ok
uv run python scripts/enforce_worktree.py --project-id session-memory -> status ok, worktree clean

## Active Risks

_none recorded_

## Blockers

_none recorded_

## Status Notes

_none recorded_

Round rewritten because Add shared current-task control helpers and update transition-command docs as part of the same owner-layer semantics slice.

active -> validation_pending: Current-task owner-layer semantics are now consistent across refresh, audit, enforcement, and canonical docs.

validation_pending -> captured: Real-project refresh, audit, and enforcement all passed with the new current-task semantics in place.

validated by:
- uv run python scripts/refresh_current_task_anchor.py --project-id session-memory -> objective/round/phase and workspace bullets refreshed
- uv run python scripts/audit_control_state.py --project-id session-memory -> status ok
- uv run python scripts/enforce_worktree.py --project-id session-memory -> status ok, worktree clean

captured -> closed: The current-task owner-layer semantics slice is durably recorded and no further execution remains in this bounded round.

