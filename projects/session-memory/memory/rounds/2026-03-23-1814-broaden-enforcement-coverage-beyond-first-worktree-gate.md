---
id: round-2026-03-23-1814-broaden-enforcement-coverage-beyond-first-worktree-gate
type: round-contract
title: "Compile bounded adjudication phase-side-effect plans"
status: active
project_id: session-memory
workspace_id: ws-1490b759
workspace_root: C:/Users/terryzzb/Desktop/session-memory
branch: master
git_sha: 89b42b6ee1244f2dcade5cdf438ca5ca239b63f1
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
updated_at: 2026-03-23T20:30:10+08:00
objective_id: obj-2026-03-23-0002
phase: execution
supersedes: []
superseded_by: []
---

## Summary

Extend the adjudication plan compiler so execution-phase bootstrap can compile from durable adjudication round bootstrap fields instead of hand-authored set-phase payload JSON.

## Scope

- Add a bounded adjudication plan type that compiles execution-phase bootstrap into an explicit set-phase auto-open-round payload using existing adjudication round bootstrap fields.
- Exercise the new phase-side-effect plan path in disposable adjudication smoke without falling back to hand-authored set-phase executor payloads.
- Validate that adjudication smoke, phase/scope smoke, full phase-1 smoke, audit-control-state, and enforce-worktree all pass after the phase-side-effect plan milestone lands.

## Deliverable

A bounded adjudication plan compiler that can compile execution-phase bootstrap side effects from durable adjudication fields alongside existing round and exception-contract plan bundles.

## Validation Plan

Run adjudication followup smoke with phase-side-effect plan input, rerun phase/scope smoke and full phase-1 smoke, then rerun audit-control-state and enforce-worktree on the real project.

## Active Risks

- Phase-side-effect plans could become a hidden parallel schema if the compiler stops reusing the existing adjudication round bootstrap fields and set-phase contract.
- Phase bootstrap compilation could conflict with later followups if phase entry and open-round side effects are not kept in one bounded deterministic bundle.

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

Round rewritten because The exception-contract plan milestone is complete, and the next bounded durable rewrite family is adjudication-driven phase-side-effect bundling through existing round bootstrap fields.

The active round now targets bounded phase-side-effect plan compilation so adjudication can drive execution bootstrap through repo-owned plan expansion instead of hand-authored payloads.
