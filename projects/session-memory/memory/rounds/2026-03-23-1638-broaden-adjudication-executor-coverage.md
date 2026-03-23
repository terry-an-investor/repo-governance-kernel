---
id: round-2026-03-23-1638-broaden-adjudication-executor-coverage
type: round-contract
title: "Broaden adjudication executor coverage"
status: closed
project_id: session-memory
workspace_id: ws-1490b759
workspace_root: C:/Users/terryzzb/Desktop/session-memory
branch: master
git_sha: 543d21175ed79f2f99f9639e6e43ff00b2c3aea1
paths:
  - scripts/build_index.py
  - scripts/execute_adjudication_followups.py
  - scripts/adjudicate_control_state.py
  - scripts/round_control.py
  - scripts/smoke_adjudication_followups.py
  - scripts/smoke_phase1.py
  - projects/session-memory/current/current-task.md
  - TRANSITION_COMMANDS.md
  - STATE_MACHINE.md
  - SCHEMA.md
  - CONTROL_SYSTEM.md
  - projects/session-memory/
thread_ids: []
evidence_refs: []
tags:
  - round
  - control-plane
confidence: high
created_at: 2026-03-23T16:38:13+08:00
updated_at: 2026-03-23T16:49:47+08:00
objective_id: obj-2026-03-23-0002
phase: execution
supersedes: []
superseded_by: []
---

## Summary

A broader adjudication execution slice with clearer structured follow-up contract and at least one additional validated path or explicit boundary.

## Scope

- Extend structured adjudication follow-ups beyond the first supported subset without letting executor logic guess intent.
- Decide whether structured follow-up schema should stay as executor JSON bullets or move into richer adjudication fields.
- Validate at least one additional supported follow-up path or explicit blocked boundary with disposable fixtures and live audit.

## Deliverable

A broader adjudication execution slice with clearer structured follow-up contract and at least one additional validated path or explicit boundary.

## Validation Plan

Add targeted adjudication regression, rerun audit-control-state, then rerun full phase-1 smoke.
uv run python scripts/smoke_adjudication_followups.py
uv run python scripts/session_memory.py smoke

## Active Risks

_none recorded_

## Blockers

_none recorded_

## Status Notes

active -> validation_pending: Structured adjudication contract upgrade and blocked-boundary coverage are ready for validation closeout.

validation_pending -> captured: Frontmatter executor_followups and prose-only blocked-boundary behavior validated on targeted fixture and full smoke.

validated by:
- uv run python scripts/smoke_adjudication_followups.py
- uv run python scripts/session_memory.py smoke

captured -> closed: Structured adjudication contract broadening is complete and a successor round will extend executor bundles.
