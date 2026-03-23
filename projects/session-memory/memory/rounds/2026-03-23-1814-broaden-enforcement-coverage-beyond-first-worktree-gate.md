---
id: round-2026-03-23-1814-broaden-enforcement-coverage-beyond-first-worktree-gate
type: round-contract
title: "Compile bounded adjudication exception-contract plans"
status: active
project_id: session-memory
workspace_id: ws-1490b759
workspace_root: C:/Users/terryzzb/Desktop/session-memory
branch: master
git_sha: 66977f269575e0111cb73def17e97647cccfa526
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
updated_at: 2026-03-23T20:16:35+08:00
objective_id: obj-2026-03-23-0002
phase: execution
supersedes: []
superseded_by: []
---

## Summary

Extend adjudication executor plan compilation so exception-contract rewrites also come from durable plan contracts instead of hand-authored low-level payloads.

## Scope

- Add bounded exception-contract executor plan types so adjudication can compile retire and invalidate rewrites from durable truth instead of hand-authored payload JSON.
- Teach execute-adjudication-followups and the adjudication smoke fixture to exercise exception-contract plan compilation through adjudication invalidated object sets.
- Validate that adjudication smoke, full phase-1 smoke, audit-control-state, and enforce-worktree all pass after the exception-contract plan compiler milestone lands.

## Deliverable

A bounded adjudication plan compiler that covers both round rewrite-close chains and exception-contract retire/invalidate rewrites through durable plan contracts.

## Validation Plan

Run adjudication followup smoke with retire and invalidate exception-contract plan contracts, rerun full phase-1 smoke, then rerun audit-control-state and enforce-worktree on the real project.

## Active Risks

- Exception plan compilation could become implicit verdict interpretation if target resolution stops being deterministic and auditable.
- Compiler and executor merge logic could regress into duplicate or conflicting followup execution as more bounded plan types are added.

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

Round rewritten because The current milestone has moved from initial adjudication plan compilation to bounded exception-contract plan compilation, so the durable round contract must be rewritten to the current mainline.

The active round now targets bounded exception-contract plan compilation so adjudication can compile more of its durable verdict into repo-owned execution contracts.
