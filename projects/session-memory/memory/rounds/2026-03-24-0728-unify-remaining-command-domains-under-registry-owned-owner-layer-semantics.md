---
id: round-2026-03-24-0728-unify-remaining-command-domains-under-registry-owned-owner-layer-semantics
type: round-contract
title: "Unify remaining command domains under registry-owned owner-layer semantics"
status: closed
project_id: session-memory
workspace_id: ws-1490b759
workspace_root: C:/Users/terryzzb/Desktop/session-memory
branch: master
git_sha: b9d5208d360a69a2b504363441d351ef65529e41
paths:
  - scripts/transition_specs.py
  - scripts/round_control.py
  - scripts/audit_control_state.py
  - scripts/activate_exception_contract.py
  - scripts/retire_exception_contract.py
  - scripts/invalidate_exception_contract.py
  - scripts/refresh_current_task_anchor.py
  - scripts/render_live_workspace_projection.py
  - scripts/create_snapshot.py
  - scripts/list_transition_registry.py
  - scripts/capture_handoff.py
  - scripts/open_objective.py
  - scripts/close_objective.py
  - scripts/record_soft_pivot.py
  - scripts/record_hard_pivot.py
  - scripts/set_phase.py
  - scripts/open_round.py
  - scripts/refresh_round_scope.py
  - scripts/rewrite_open_round.py
  - scripts/update_round_status.py
  - CONTROL_SYSTEM.md
  - TRANSITION_COMMANDS.md
thread_ids: []
evidence_refs: []
tags:
  - round
  - control-plane
confidence: high
created_at: 2026-03-24T07:28:55+08:00
updated_at: 2026-03-24T07:41:30+08:00
objective_id: obj-2026-03-23-0002
phase: execution
supersedes: []
superseded_by: []
---

## Summary

All implemented transition command domains consume registry-backed owner-layer contracts, and the registry itself carries explicit owner fields that bound private semantics drift.

## Scope

- Add explicit owner-layer fields to the transition registry so durable owners, projection owners, artifact owners, and live inspection owners stop living as private code semantics.
- Make exception-contract and anchor-maintenance commands consume the same registry-backed contract assertion path already used by round and objective-phase commands.

## Deliverable

All implemented transition command domains consume registry-backed owner-layer contracts, and the registry itself carries explicit owner fields that bound private semantics drift.

## Validation Plan

Run real-project audit and enforce-worktree, exercise anchor-maintenance commands and capture-handoff on the real project, then close the round and return the objective to paused.
uv run python scripts/audit_control_state.py --project-id session-memory => status ok
uv run python scripts/enforce_worktree.py --project-id session-memory => status ok
uv run python scripts/refresh_current_task_anchor.py --project-id session-memory => refreshed current-task anchor
uv run python scripts/render_live_workspace_projection.py --project-id session-memory --output artifacts/session-memory/registry-owner-layer-live-workspace.md => artifact written
uv run python scripts/create_snapshot.py --project-id session-memory --slug registry-owner-layer-check --output artifacts/session-memory/registry-owner-layer-snapshot.md => artifact written
uv run python scripts/capture_handoff.py --project-id session-memory --slug registry-owner-layer-handoff --artifact-dir artifacts/session-memory/registry-owner-layer-handoff => packet captured

## Active Risks

_none recorded_

## Blockers

_none recorded_

## Status Notes

active -> validation_pending: Registry-owner unification implementation landed and validation evidence is ready for capture.

validation_pending -> captured: Owner-layer registry unification passed real validation and artifacts were captured.

validated by:
- uv run python scripts/audit_control_state.py --project-id session-memory => status ok
- uv run python scripts/enforce_worktree.py --project-id session-memory => status ok
- uv run python scripts/refresh_current_task_anchor.py --project-id session-memory => refreshed current-task anchor
- uv run python scripts/render_live_workspace_projection.py --project-id session-memory --output artifacts/session-memory/registry-owner-layer-live-workspace.md => artifact written
- uv run python scripts/create_snapshot.py --project-id session-memory --slug registry-owner-layer-check --output artifacts/session-memory/registry-owner-layer-snapshot.md => artifact written
- uv run python scripts/capture_handoff.py --project-id session-memory --slug registry-owner-layer-handoff --artifact-dir artifacts/session-memory/registry-owner-layer-handoff => packet captured

captured -> closed: Registry-owner unification round is complete and its validation evidence is durably captured.
