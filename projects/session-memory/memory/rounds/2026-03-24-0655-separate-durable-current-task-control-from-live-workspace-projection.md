---
id: round-2026-03-24-0655-separate-durable-current-task-control-from-live-workspace-projection
type: round-contract
title: "Separate durable current-task control from live workspace projection"
status: closed
project_id: session-memory
workspace_id: ws-1490b759
workspace_root: C:/Users/terryzzb/Desktop/session-memory
branch: master
git_sha: 1c5011a5fe724a33812472aba5e57b901dc65d27
paths:
  - scripts/assemble_context.py
  - scripts/refresh_current_task_anchor.py
  - scripts/capture_handoff.py
  - scripts/create_snapshot.py
  - scripts/session_memory.py
  - scripts/transition_specs.py
  - CONTROL_SYSTEM.md
  - TRANSITION_COMMANDS.md
  - projects/session-memory/current/current-task.md
  - scripts/render_live_workspace_projection.py
thread_ids: []
evidence_refs: []
tags:
  - round
  - control-plane
confidence: high
created_at: 2026-03-24T06:55:53+08:00
updated_at: 2026-03-24T07:02:36+08:00
objective_id: obj-2026-03-23-0002
phase: execution
supersedes: []
superseded_by: []
---

## Summary

Current-task keeps only durable control plus workspace locator fields, while live repo facts are rendered through a separate reusable projection command and capture artifact.

## Scope

- Remove live workspace snapshot fields from current-task so it remains a durable control-and-orientation file.
- Add one reusable non-durable live workspace projection command and make handoff capture emit it separately.

## Deliverable

Current-task keeps only durable control plus workspace locator fields, while live repo facts are rendered through a separate reusable projection command and capture artifact.

## Validation Plan

Refresh current-task under the new split semantics, render a live workspace projection artifact, run capture-handoff or equivalent real-path validation, then rerun audit and enforce-worktree.
uv run python scripts/refresh_current_task_anchor.py --project-id session-memory
uv run python scripts/render_live_workspace_projection.py --project-id session-memory --output artifacts/session-memory/live-workspace-split-check.md
uv run python scripts/capture_handoff.py --project-id session-memory --slug split-live-workspace-handoff-final2 --artifact-dir artifacts/session-memory/split-live-workspace-handoff-final2
uv run python scripts/audit_control_state.py --project-id session-memory
uv run python scripts/enforce_worktree.py --project-id session-memory

## Active Risks

_none recorded_

## Blockers

_none recorded_

## Status Notes

_none recorded_

Round rewritten because The split now needs one dedicated live-workspace projection command file in addition to the previously scoped current-task and handoff files.

active -> validation_pending: Durable current-task control is now separated from the new non-durable live workspace projection path and the closeout validations are complete.

validation_pending -> captured: Real-project refresh, live-workspace rendering, capture-handoff, audit, and enforce-worktree all passed after separating current-task control from live workspace projection.

validated by:
- uv run python scripts/refresh_current_task_anchor.py --project-id session-memory
- uv run python scripts/render_live_workspace_projection.py --project-id session-memory --output artifacts/session-memory/live-workspace-split-check.md
- uv run python scripts/capture_handoff.py --project-id session-memory --slug split-live-workspace-handoff-final2 --artifact-dir artifacts/session-memory/split-live-workspace-handoff-final2
- uv run python scripts/audit_control_state.py --project-id session-memory
- uv run python scripts/enforce_worktree.py --project-id session-memory

captured -> closed: The current-task/live-workspace split is implemented and validated, so this bounded execution round can close.
