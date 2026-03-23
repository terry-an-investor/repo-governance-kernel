---
id: round-2026-03-23-1814-broaden-enforcement-coverage-beyond-first-worktree-gate
type: round-contract
title: "Integrate durable open-round rewrites into pivots and adjudication"
status: active
project_id: session-memory
workspace_id: ws-1490b759
workspace_root: C:/Users/terryzzb/Desktop/session-memory
branch: master
git_sha: fdf1e471848c4861dc071dc5627340b551b1bb89
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
updated_at: 2026-03-23T19:44:40+08:00
objective_id: obj-2026-03-23-0002
phase: execution
supersedes: []
superseded_by: []
---

## Summary

Land the durable open-round rewrite primitive and integrate it into soft pivot, phase, and adjudication follow-up execution.

## Scope

- Land rewrite-open-round as the owner-layer primitive for rewriting one open round contract without changing round identity.
- Integrate that primitive into record-soft-pivot, set-phase, and adjudication follow-up execution instead of leaving round review as prose only.
- Validate the rewrite path on disposable fixtures and update canonical control docs plus current project state to match the new capability.

## Deliverable

A durable round rewrite milestone with one reusable rewrite primitive, real integrations for soft pivot and adjudication follow-ups, and canonical docs plus sample state updated to match observed behavior.

## Validation Plan

Run targeted smokes for objective-line and adjudication rewrite flows, then rerun phase-1 smoke, worktree enforcement, and control audit on the real project.

## Active Risks

- The rewrite primitive could stay too narrow and only patch symptoms instead of becoming the reusable owner-layer mutation path.
- Project samples and canonical docs could drift from the new rewrite behavior if the round narrative is not durably updated in the same milestone.

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
