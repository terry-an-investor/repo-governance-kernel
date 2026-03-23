---
id: round-2026-03-23-1814-broaden-enforcement-coverage-beyond-first-worktree-gate
type: round-contract
title: "Compile bounded adjudication executor plans"
status: active
project_id: session-memory
workspace_id: ws-1490b759
workspace_root: C:/Users/terryzzb/Desktop/session-memory
branch: master
git_sha: 41106ce5da36e0681495490949f3b18e6616dbb0
paths:
  - AGENTS.md
  - .githooks/
  - .github/
  - scripts/
  - CONTROL_SYSTEM.md
  - SCHEMA.md
  - STATE_MACHINE.md
  - TRANSITION_COMMANDS.md
  - projects/session-memory/control/
  - projects/session-memory/current/
thread_ids: []
evidence_refs: []
tags:
  - round
  - control-plane
confidence: high
created_at: 2026-03-23T18:14:34+08:00
updated_at: 2026-03-23T20:02:11+08:00
objective_id: obj-2026-03-23-0002
phase: execution
supersedes: []
superseded_by: []
---

## Summary

Add a bounded adjudication plan compiler so durable adjudication records can compile supported rewrite intent into explicit executor followups.

## Scope

- Add executor_plan_contracts to adjudication durable records so higher-level bounded rewrite intent lives in durable truth instead of prompt text.
- Implement compile-adjudication-executor-plan and teach execute-adjudication-followups to compile supported plan contracts before running explicit followups.
- Validate that adjudication smoke and full phase-1 smoke pass when the fixture uses plan contracts instead of hand-authored low-level rewrite payloads.

## Deliverable

A bounded adjudication plan compiler that expands supported durable plan contracts into explicit executor followups and is validated on targeted adjudication smoke plus full phase-1 smoke.

## Validation Plan

Run adjudication followup smoke on plan-contract input, rerun full phase-1 smoke, then rerun audit-control-state and enforce-worktree on the real project.

## Active Risks

- The compiler could quietly overwrite explicit executor payloads instead of merging and deduplicating them.
- Plan-contract support could grow into another hidden orchestration layer unless supported shapes stay explicit and bounded.

## Blockers

_none recorded_

## Status Notes

Opened after closing the first automatic worktree enforcement slice.

Constitution-declared guarded exception paths are now enforced as a second blocked-state class.

The same owner-layer commands are now wired into GitHub Actions so local hook
gates and remote CI gates execute the same enforcement surface.

Explicit `set-phase` and `refresh-round-scope` commands now exist.

`open-round` now rejects non-`execution` objectives so execution contracts
cannot be opened from exploration by accident.

validated by:
- uv run python scripts/smoke_guarded_exception_enforcement.py
- uv run python scripts/smoke_phase_scope_controls.py
- uv run python scripts/audit_control_state.py --project-id session-memory
- uv run python scripts/enforce_worktree.py --project-id session-memory

Round rewritten because This round is now serving the durable open-round rewrite milestone, so the active round contract must be rewritten to match the current mainline work.

This round was durably rewritten from the earlier enforcement-expansion milestone into the open-round rewrite integration milestone.

Round rewritten because The previous rewrite used shell-sensitive quoting, so the durable round scope bullets must be rewritten into clean plain text.

Round rewritten because The active milestone is now adjudication plan compilation, so the open round contract must be rewritten to the current durable objective slice.

The active round was rewritten again to move from raw open-round rewrite integration into bounded adjudication plan compilation.
