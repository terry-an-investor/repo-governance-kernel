---
id: round-2026-03-23-1548-implement-remaining-objective-line-transitions
type: round-contract
title: "Implement remaining objective-line transitions"
status: closed
project_id: session-memory
workspace_id: ws-1490b759
workspace_root: C:/Users/terryzzb/Desktop/session-memory
branch: master
git_sha: d7af73f203cc6011b645485368685954b2876164
paths:
  - scripts/round_control.py
  - scripts/session_memory.py
  - scripts/close_objective.py
  - scripts/open_objective.py
  - scripts/record_hard_pivot.py
  - scripts/record_soft_pivot.py
  - scripts/smoke_objective_line.py
  - scripts/smoke_phase1.py
  - state/session-memory/current/current-task.md
  - CONTROL_SYSTEM.md
  - TRANSITION_COMMANDS.md
  - STATE_MACHINE.md
  - SCHEMA.md
thread_ids: []
evidence_refs: []
tags:
  - round
  - control-plane
confidence: high
created_at: 2026-03-23T15:48:39+08:00
updated_at: 2026-03-23T16:19:36+08:00
objective_id: obj-2026-03-23-0002
phase: execution
supersedes: []
superseded_by: []
---

## Summary

A real remaining objective-line slice with close-objective and record-soft-pivot commands using the shared transition engine and proven on disposable fixtures.

## Scope

- add close-objective so objective lines can end honestly without manual file edits
- add record-soft-pivot so execution-frame changes do not require fake hard pivots or silent rewrites
- validate the new objective-line commands against disposable fixtures and keep projection/event semantics aligned with the shared transition engine

## Deliverable

A real remaining objective-line slice with close-objective and record-soft-pivot commands using the shared transition engine and proven on disposable fixtures.

## Validation Plan

Run objective-line fixture regression for close-objective and soft-pivot, then pass audit-control-state, role-context compilation, and full smoke.
uv run python scripts/smoke_objective_line.py
uv run python scripts/session_memory.py smoke

## Active Risks

- Soft-pivot semantics can blur into hard pivot if objective identity and success criteria boundaries are not enforced tightly.
- Close-objective can create dead-end control state if active projections are not updated consistently.

## Blockers

_none recorded_

## Status Notes

This round starts after shared transition-engine extraction and targets the still-missing canonical objective-line commands.

active -> validation_pending: Remaining objective-line transition slice is implemented and ready for validation closeout.

validation_pending -> captured: Objective-line transition slice validated on disposable fixtures and full phase-1 smoke.

validated by:
- uv run python scripts/smoke_objective_line.py
- uv run python scripts/session_memory.py smoke

captured -> closed: Remaining objective-line transition slice is complete and a successor adjudication round will take over.

