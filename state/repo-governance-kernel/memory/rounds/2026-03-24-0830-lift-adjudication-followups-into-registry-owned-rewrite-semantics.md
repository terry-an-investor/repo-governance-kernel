---
id: round-2026-03-24-0830-lift-adjudication-followups-into-registry-owned-rewrite-semantics
type: round-contract
title: "Lift adjudication followups into registry-owned rewrite semantics"
status: closed
project_id: repo-governance-kernel
workspace_id: ws-1490b759
workspace_root: C:/Users/terryzzb/Desktop/session-memory
branch: master
git_sha: a057eb22768df04e3b2936054f61a2f65d7239ac
paths:
  - scripts/transition_specs.py
  - scripts/compile_adjudication_executor_plan.py
  - scripts/execute_adjudication_followups.py
  - scripts/round_control.py
  - scripts/smoke_adjudication_followups.py
  - scripts/audit_control_state.py
  - CONTROL_SYSTEM.md
  - TRANSITION_COMMANDS.md
thread_ids: []
evidence_refs: []
tags:
  - round
  - control-plane
confidence: high
created_at: 2026-03-24T08:30:20+08:00
updated_at: 2026-03-24T08:37:17+08:00
objective_id: obj-2026-03-23-0002
phase: execution
supersedes: []
superseded_by: []
---

## Summary

Adjudication plan compilation is driven by registry-owned rewrite semantics for at least the currently supported bounded plan families, reducing private compiler semantics drift.

## Scope

- Move adjudication plan compilation closer to registry-owned executable rewrite semantics.
- Reduce per-plan private compiler branching in favor of machine-readable rewrite contract fields.

## Deliverable

Adjudication plan compilation is driven by registry-owned rewrite semantics for at least the currently supported bounded plan families, reducing private compiler semantics drift.

## Validation Plan

Compile changed scripts, run adjudication follow-up smoke coverage, run real-project audit and enforce, then close the round and return the objective to paused.
uv run python -m py_compile scripts/transition_specs.py scripts/compile_adjudication_executor_plan.py scripts/execute_adjudication_followups.py
uv run python scripts/list_transition_registry.py
uv run python scripts/smoke_adjudication_followups.py
uv run python scripts/audit_control_state.py --project-id repo-governance-kernel
uv run python scripts/enforce_worktree.py --project-id repo-governance-kernel

## Active Risks

_none recorded_

## Blockers

_none recorded_

## Status Notes

active -> validation_pending: Registry-owned adjudication payload templates compiled and passed targeted smoke plus real-project audit/enforcement.

validation_pending -> captured: Registry-owned adjudication payload templates are validated and ready to close.

validated by:
- uv run python -m py_compile scripts/transition_specs.py scripts/compile_adjudication_executor_plan.py scripts/execute_adjudication_followups.py
- uv run python scripts/list_transition_registry.py
- uv run python scripts/smoke_adjudication_followups.py
- uv run python scripts/audit_control_state.py --project-id repo-governance-kernel
- uv run python scripts/enforce_worktree.py --project-id repo-governance-kernel

captured -> closed: Registry-owned adjudication payload-template governance round closed after validated smoke and control-plane checks.

