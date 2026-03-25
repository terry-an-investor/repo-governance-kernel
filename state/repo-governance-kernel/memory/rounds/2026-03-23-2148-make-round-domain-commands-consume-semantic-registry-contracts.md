---
id: round-2026-03-23-2148-make-round-domain-commands-consume-semantic-registry-contracts
type: round-contract
title: "Make round-domain commands consume semantic registry contracts"
status: closed
project_id: repo-governance-kernel
workspace_id: ws-1490b759
workspace_root: C:/Users/terryzzb/Desktop/session-memory
branch: master
git_sha: 32c0f9bd5270932e32f84468a3e2953c9c6ce11f
paths:
  - scripts/
  - state/repo-governance-kernel/
  - TRANSITION_COMMANDS.md
  - CONTROL_SYSTEM.md
  - STATE_MACHINE.md
thread_ids: []
evidence_refs: []
tags:
  - round
  - control-plane
confidence: high
created_at: 2026-03-23T21:48:48+08:00
updated_at: 2026-03-23T22:00:08+08:00
objective_id: obj-2026-03-23-0002
phase: execution
supersedes: []
superseded_by: []
---

## Summary

A shared owner-layer round-domain semantics helper that round commands and audit both consume, reducing per-command semantic drift.

## Scope

- Extract a shared round-domain registry consumer so open-round, refresh-round-scope, rewrite-open-round, and update-round-status stop hand-owning duplicated guard and side-effect semantics.
- Use semantic transition-registry contracts to validate round-command guard coverage, write-target coverage, and transition-event expectations in one owner-layer helper.
- Teach control audit or dedicated validation to detect round-domain drift when command implementations and registry-backed semantics diverge.

## Deliverable

A shared owner-layer round-domain semantics helper that round commands and audit both consume, reducing per-command semantic drift.

## Validation Plan

Run targeted round-domain validation, rerun transition-engine and phase-scope-control smokes, rerun real-project audit and enforce-worktree, then refresh current-task anchor.
uv run python scripts/smoke_transition_engine.py -> fixture_audit ok
uv run python scripts/smoke_phase_scope_controls.py -> fixture_audit ok
uv run python scripts/audit_control_state.py --project-id repo-governance-kernel -> status ok
uv run python scripts/enforce_worktree.py --project-id repo-governance-kernel -> status ok, worktree clean

## Active Risks

- A helper that only mirrors existing command logic without asserting registry-backed coverage would add indirection without reducing drift.
- Over-generalizing beyond round-domain commands in the same slice would blur the owner layer and slow validation.

## Blockers

_none recorded_

## Status Notes

active -> validation_pending: Round-domain registry consumer coverage landed and all planned validations passed for this slice.

validation_pending -> captured: Round-domain contract changes were validated in disposable fixtures and the real project, so this slice can be captured.

validated by:
- uv run python scripts/smoke_transition_engine.py -> fixture_audit ok
- uv run python scripts/smoke_phase_scope_controls.py -> fixture_audit ok
- uv run python scripts/audit_control_state.py --project-id repo-governance-kernel -> status ok
- uv run python scripts/enforce_worktree.py --project-id repo-governance-kernel -> status ok, worktree clean

captured -> closed: Round-domain registry consumer coverage is fully landed, validated, and recorded; no open execution contract remains for this slice.


