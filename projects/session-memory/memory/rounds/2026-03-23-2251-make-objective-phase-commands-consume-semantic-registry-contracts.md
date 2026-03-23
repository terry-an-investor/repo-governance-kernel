---
id: round-2026-03-23-2251-make-objective-phase-commands-consume-semantic-registry-contracts
type: round-contract
title: "Make objective-phase commands consume semantic registry contracts"
status: closed
project_id: session-memory
workspace_id: ws-1490b759
workspace_root: C:/Users/terryzzb/Desktop/session-memory
branch: master
git_sha: 129c942e3422dab82a9e72547e59c58ea527bae0
paths:
  - scripts/round_control.py
  - scripts/open_objective.py
  - scripts/close_objective.py
  - scripts/record_soft_pivot.py
  - scripts/record_hard_pivot.py
  - scripts/set_phase.py
  - scripts/audit_control_state.py
  - CONTROL_SYSTEM.md
  - TRANSITION_COMMANDS.md
thread_ids: []
evidence_refs: []
tags:
  - round
  - control-plane
confidence: high
created_at: 2026-03-23T22:51:58+08:00
updated_at: 2026-03-23T22:58:18+08:00
objective_id: obj-2026-03-23-0002
phase: execution
supersedes: []
superseded_by: []
---

## Summary

Objective/phase commands and audit consume one shared registry-backed owner-layer semantics helper, reducing semantic drift outside the round domain.

## Scope

- Extract shared objective/phase owner-layer semantics and make objective-line plus set-phase commands consume them.

## Deliverable

Objective/phase commands and audit consume one shared registry-backed owner-layer semantics helper, reducing semantic drift outside the round domain.

## Validation Plan

Run real-project audit and enforce-worktree, then close the round and return the objective to paused.
uv run python scripts/audit_control_state.py --project-id session-memory
uv run python scripts/enforce_worktree.py --project-id session-memory
uv run python scripts/smoke_objective_line.py
uv run python scripts/smoke_phase_scope_controls.py

## Active Risks

_none recorded_

## Blockers

_none recorded_

## Status Notes

active -> validation_pending: Objective/phase registry consumer helper, docs, and audit coverage are implemented and ready for closeout validation.

validation_pending -> captured: Real-project audit and enforcement passed, and disposable objective-line plus phase-scope smokes exercised the migrated objective/phase command surface.

validated by:
- uv run python scripts/audit_control_state.py --project-id session-memory
- uv run python scripts/enforce_worktree.py --project-id session-memory
- uv run python scripts/smoke_objective_line.py
- uv run python scripts/smoke_phase_scope_controls.py

captured -> closed: The objective/phase registry consumer coverage slice is implemented, validated, and no further execution remains in this bounded round.
