---
id: round-2026-03-23-1530-extract-shared-transition-engine-primitive
type: round-contract
title: "Extract shared transition engine primitive"
status: closed
project_id: repo-governance-kernel
workspace_id: ws-1490b759
workspace_root: C:/Users/terryzzb/Desktop/session-memory
branch: master
git_sha: 0300b70fbe9fb8027d7798c16b94373c6272ee86
paths:
  - scripts/round_control.py
  - scripts/open_objective.py
  - scripts/open_round.py
  - scripts/update_round_status.py
  - scripts/activate_exception_contract.py
  - scripts/retire_exception_contract.py
  - scripts/invalidate_exception_contract.py
  - scripts/record_hard_pivot.py
  - scripts/repo_governance_kernel.py
  - scripts/smoke_transition_engine.py
  - state/repo-governance-kernel/current/current-task.md
  - TRANSITION_COMMANDS.md
  - STATE_MACHINE.md
thread_ids: []
evidence_refs: []
tags:
  - round
  - control-plane
confidence: high
created_at: 2026-03-23T15:30:31+08:00
updated_at: 2026-03-23T15:48:22+08:00
objective_id: obj-2026-03-23-0002
phase: execution
supersedes: []
superseded_by: []
---

## Summary

A shared transition-engine primitive adopted by the existing objective, round, and exception-contract commands for the overlapping file-write and transition-event responsibilities.

## Scope

- pull duplicated transition-writing logic out of objective, round, and exception commands into one shared owner-layer primitive
- make command families delegate projection and transition-event side effects through the shared primitive instead of hand-rolling them
- reduce the active exception contract by shrinking the duplicated transition surface rather than normalizing it

## Deliverable

A shared transition-engine primitive adopted by the existing objective, round, and exception-contract commands for the overlapping file-write and transition-event responsibilities.

## Validation Plan

Run command-level regression on the migrated command families, then pass audit-control-state, role-context compilation, exception-contract smoke, and full smoke.
uv run python scripts/smoke_transition_engine.py
uv run python scripts/smoke_exception_contracts.py
uv run python scripts/repo_governance_kernel.py smoke

## Active Risks

- Refactoring shared transition ownership can regress existing commands if file-shape preservation is not held constant.
- The shared engine can become a vague wrapper if it does not own concrete guards and side effects honestly.

## Blockers

_none recorded_

## Status Notes

This round starts from the newly recorded exception contract and aims to shrink that debt instead of just documenting it.

active -> validation_pending: shared transition-engine primitive implemented; promote to validation before capture

validation_pending -> captured: shared transition-engine primitive validated across objective, round, exception, and hard-pivot fixtures

validated by:
- uv run python scripts/smoke_transition_engine.py
- uv run python scripts/smoke_exception_contracts.py
- uv run python scripts/repo_governance_kernel.py smoke

captured -> closed: shared transition-engine milestone completed and next work shifts to remaining objective-line commands


