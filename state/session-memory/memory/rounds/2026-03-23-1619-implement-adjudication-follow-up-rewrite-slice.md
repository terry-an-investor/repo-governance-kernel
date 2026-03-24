---
id: round-2026-03-23-1619-implement-adjudication-follow-up-rewrite-slice
type: round-contract
title: "Implement adjudication follow-up rewrite slice"
status: closed
project_id: session-memory
workspace_id: ws-1490b759
workspace_root: C:/Users/terryzzb/Desktop/session-memory
branch: master
git_sha: 76bea946dd7920915a34c0def4894f74b383a0cc
paths:
  - scripts/execute_adjudication_followups.py
  - scripts/adjudicate_control_state.py
  - scripts/round_control.py
  - scripts/smoke_adjudication_followups.py
  - scripts/smoke_phase1.py
  - state/session-memory/current/current-task.md
  - TRANSITION_COMMANDS.md
  - STATE_MACHINE.md
  - CONTROL_SYSTEM.md
  - state/session-memory/
thread_ids: []
evidence_refs: []
tags:
  - round
  - control-plane
confidence: high
created_at: 2026-03-23T16:19:46+08:00
updated_at: 2026-03-23T16:38:04+08:00
objective_id: obj-2026-03-23-0002
phase: execution
supersedes: []
superseded_by: []
---

## Summary

A real adjudication follow-up slice that can execute at least one non-trivial durable control rewrite from a durable adjudication record.

## Scope

- Turn execute-adjudication-followups from scaffold-only behavior into real durable control rewrites for supported verdict shapes.
- Keep adjudication, repair, and transition execution separate while proving at least one honest follow-up path beyond scaffolding.
- Validate the new adjudication path on disposable fixtures and current project control state without introducing fake automation.

## Deliverable

A real adjudication follow-up slice that can execute at least one non-trivial durable control rewrite from a durable adjudication record.

## Validation Plan

Add disposable adjudication fixtures, run targeted adjudication smoke, then rerun audit-control-state and full phase-1 smoke.
uv run python scripts/smoke_adjudication_followups.py
uv run python scripts/session_memory.py smoke

## Active Risks

_none recorded_

## Blockers

_none recorded_

## Status Notes

active -> validation_pending: First adjudication follow-up rewrite slice is implemented and ready for validation closeout.

validation_pending -> captured: Structured adjudication follow-up executor validated on disposable fixture and full phase-1 smoke.

validated by:
- uv run python scripts/smoke_adjudication_followups.py
- uv run python scripts/session_memory.py smoke

captured -> closed: First adjudication follow-up rewrite slice is complete and a successor round will expand executor coverage.

