---
id: round-2026-03-23-1516-implement-exception-contract-transition-slice
type: round-contract
title: "Implement exception-contract transition slice"
status: closed
project_id: repo-governance-kernel
workspace_id: ws-1490b759
workspace_root: C:/Users/terryzzb/Desktop/session-memory
branch: master
git_sha: 41f9d2e9e3d3caaaae16446b43d74b2ace393ccf
paths:
  - SCHEMA.md
  - STATE_MACHINE.md
  - TRANSITION_COMMANDS.md
  - scripts/assemble_context.py
  - scripts/activate_exception_contract.py
  - scripts/invalidate_exception_contract.py
  - scripts/reconcile_control_state.py
  - scripts/retire_exception_contract.py
  - scripts/round_control.py
  - scripts/repo_governance_kernel.py
  - scripts/smoke_exception_contracts.py
  - scripts/update_round_status.py
  - scripts/compile_role_context.py
  - scripts/audit_control_state.py
  - scripts/execute_adjudication_followups.py
  - state/repo-governance-kernel/control/exception-ledger.md
  - state/repo-governance-kernel/current/current-task.md
  - state/repo-governance-kernel/memory/exception-contracts/
  - state/wind-agent/control/exception-ledger.md
  - scripts/open_round.py
thread_ids: []
evidence_refs: []
tags:
  - round
  - control-plane
confidence: high
created_at: 2026-03-23T15:16:23+08:00
updated_at: 2026-03-23T15:30:14+08:00
objective_id: obj-2026-03-23-0002
phase: execution
supersedes: []
superseded_by: []
---

## Summary

A working exception-contract transition slice that can create, retire, and invalidate durable exception contracts, keep the exception ledger projected, and prove the slice on a real project sample.

## Scope

- implement durable exception-contract commands with honest guards and transition events
- project active, retired, and invalidated exception contracts into control/exception-ledger.md
- validate the slice on one real sample exception contract instead of placeholder-only governance

## Deliverable

A working exception-contract transition slice that can create, retire, and invalidate durable exception contracts, keep the exception ledger projected, and prove the slice on a real project sample.

## Validation Plan

Run real exception-contract transitions on session-memory and one live sample, then pass control audit, role-context compilation, index rebuild, and smoke.
uv run python scripts/repo_governance_kernel.py smoke
uv run python scripts/smoke_exception_contracts.py
uv run python scripts/repo_governance_kernel.py compile-role-context --project-id repo-governance-kernel --role reviewer

## Active Risks

- Ledger projection may drift if command paths and reconcile paths do not share the same owner-layer primitives.
- A fake sample exception contract would weaken the whole control-system claim, so the sample must be tied to a real live deviation.

## Blockers

_none recorded_

## Status Notes

This round replaces the earlier first-transition slice and broadens enforcement from round-only control into exception-contract control.

active -> validation_pending: exception-contract slice implemented; promote to validation before capture

validation_pending -> captured: exception-contract transition slice validated on session-memory

validated by:
- uv run python scripts/repo_governance_kernel.py smoke
- uv run python scripts/smoke_exception_contracts.py
- uv run python scripts/repo_governance_kernel.py compile-role-context --project-id repo-governance-kernel --role reviewer

captured -> closed: exception-contract milestone completed and next work shifts to shared transition-engine extraction


