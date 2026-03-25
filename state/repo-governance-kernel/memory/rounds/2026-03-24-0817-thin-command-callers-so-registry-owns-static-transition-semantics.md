---
id: round-2026-03-24-0817-thin-command-callers-so-registry-owns-static-transition-semantics
type: round-contract
title: "Thin command callers so registry owns static transition semantics"
status: closed
project_id: repo-governance-kernel
workspace_id: ws-1490b759
workspace_root: C:/Users/terryzzb/Desktop/session-memory
branch: master
git_sha: 4eb8003b8b435aef9b873069d10e42e5bc885cc6
paths:
  - scripts/round_control.py
  - scripts/open_objective.py
  - scripts/close_objective.py
  - scripts/record_soft_pivot.py
  - scripts/record_hard_pivot.py
  - scripts/set_phase.py
  - scripts/open_round.py
  - scripts/refresh_round_scope.py
  - scripts/rewrite_open_round.py
  - scripts/update_round_status.py
  - scripts/activate_exception_contract.py
  - scripts/retire_exception_contract.py
  - scripts/invalidate_exception_contract.py
  - scripts/refresh_current_task_anchor.py
  - scripts/render_live_workspace_projection.py
  - scripts/create_snapshot.py
  - CONTROL_SYSTEM.md
  - TRANSITION_COMMANDS.md
thread_ids: []
evidence_refs: []
tags:
  - round
  - control-plane
confidence: high
created_at: 2026-03-24T08:17:25+08:00
updated_at: 2026-03-24T08:24:13+08:00
objective_id: obj-2026-03-23-0002
phase: execution
supersedes: []
superseded_by: []
---

## Summary

Command callers no longer restate registry-owned static transition semantics; shared owner-layer helpers derive those declarations from the machine-readable registry.

## Scope

- Remove duplicated registry-owned guard/write/owner declarations from command caller sites.
- Keep shared owner-layer assertions authoritative while making callers express only runtime-specific inputs and context.

## Deliverable

Command callers no longer restate registry-owned static transition semantics; shared owner-layer helpers derive those declarations from the machine-readable registry.

## Validation Plan

Compile changed scripts, run targeted smoke coverage for objective/phase/round/exception domains, run real-project audit and enforce, then close the round and return the objective to paused.
uv run python -m py_compile scripts/round_control.py scripts/open_objective.py scripts/close_objective.py scripts/record_soft_pivot.py scripts/record_hard_pivot.py scripts/set_phase.py scripts/open_round.py scripts/refresh_round_scope.py scripts/rewrite_open_round.py scripts/update_round_status.py scripts/activate_exception_contract.py scripts/retire_exception_contract.py scripts/invalidate_exception_contract.py scripts/refresh_current_task_anchor.py scripts/render_live_workspace_projection.py scripts/create_snapshot.py => success
uv run python scripts/smoke_objective_line.py => fixture_audit ok
uv run python scripts/smoke_phase_scope_controls.py => blocked_status blocked, allowed_status ok
uv run python scripts/smoke_exception_contracts.py => retired and invalidated fixture contracts exercised
uv run python scripts/smoke_transition_engine.py => objective-line, round, and pivot flow exercised
uv run python scripts/audit_control_state.py --project-id repo-governance-kernel => status ok
uv run python scripts/enforce_worktree.py --project-id repo-governance-kernel => status ok
uv run python scripts/refresh_current_task_anchor.py --project-id repo-governance-kernel => refreshed current-task anchor

## Active Risks

_none recorded_

## Blockers

_none recorded_

## Status Notes

_none recorded_

Scope refreshed because This governance slice also changes the canonical transition-command documentation because caller-side registry restatement behavior is part of the contract surface.

active -> validation_pending: Caller-thinning refactor landed and cross-domain validation evidence is ready for capture.

validation_pending -> captured: Caller-thinning refactor passed compile, smoke, audit, and enforcement validation.

validated by:
- uv run python -m py_compile scripts/round_control.py scripts/open_objective.py scripts/close_objective.py scripts/record_soft_pivot.py scripts/record_hard_pivot.py scripts/set_phase.py scripts/open_round.py scripts/refresh_round_scope.py scripts/rewrite_open_round.py scripts/update_round_status.py scripts/activate_exception_contract.py scripts/retire_exception_contract.py scripts/invalidate_exception_contract.py scripts/refresh_current_task_anchor.py scripts/render_live_workspace_projection.py scripts/create_snapshot.py => success
- uv run python scripts/smoke_objective_line.py => fixture_audit ok
- uv run python scripts/smoke_phase_scope_controls.py => blocked_status blocked, allowed_status ok
- uv run python scripts/smoke_exception_contracts.py => retired and invalidated fixture contracts exercised
- uv run python scripts/smoke_transition_engine.py => objective-line, round, and pivot flow exercised
- uv run python scripts/audit_control_state.py --project-id repo-governance-kernel => status ok
- uv run python scripts/enforce_worktree.py --project-id repo-governance-kernel => status ok
- uv run python scripts/refresh_current_task_anchor.py --project-id repo-governance-kernel => refreshed current-task anchor

captured -> closed: Caller-thinning governance slice is complete and its validation evidence is durably captured.

