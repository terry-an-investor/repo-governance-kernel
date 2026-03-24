---
id: round-2026-03-24-1045-complete-task-contract-lifecycle-and-consumption
type: round-contract
title: "Complete task-contract lifecycle and consumption"
status: closed
project_id: session-memory
workspace_id: ws-1490b759
workspace_root: C:/Users/terryzzb/Desktop/session-memory
branch: master
git_sha: a43b816258cb88a3b7e11b2160d0d8612069c814
paths:
  - scripts/round_control.py
  - scripts/transition_specs.py
  - scripts/open_task_contract.py
  - scripts/audit_task_contracts.py
  - scripts/audit_control_state.py
  - scripts/update_round_status.py
  - scripts/close_objective.py
  - scripts/record_hard_pivot.py
  - scripts/rewrite_open_round.py
  - scripts/assemble_context.py
  - scripts/compile_role_context.py
  - scripts/session_memory.py
  - scripts/update_task_contract_status.py
  - scripts/rewrite_open_task_contract.py
  - PRODUCT.md
  - CONTROL_SYSTEM.md
  - ARCHITECTURE.md
  - STATE_MACHINE.md
  - TRANSITION_COMMANDS.md
  - IMPLEMENTATION_PLAN.md
  - DESIGN_PRINCIPLES.md
  - state/session-memory/current/current-task.md
  - state/session-memory/memory/task-contracts
  - scripts/control_enforcement.py
thread_ids: []
evidence_refs: []
tags:
  - round
  - control-plane
confidence: high
created_at: 2026-03-24T10:45:11+08:00
updated_at: 2026-03-24T10:58:24+08:00
objective_id: obj-2026-03-23-0002
phase: execution
supersedes: []
superseded_by: []
---

## Summary

Task-contracts can be opened, rewritten, and advanced through a bounded lifecycle; active task contracts are visible in assembled and role-specific contexts; and round/objective transitions refuse to leave dangling active task contracts behind.

## Scope

- Add real task-contract lifecycle commands so task contracts can transition and be rewritten under repo-owned semantics.
- Make assemble-context and role-context surfaces consume active task contracts instead of ignoring them.
- Tighten round and objective honesty rules so active task contracts cannot be stranded across closure or pivot.

## Deliverable

Task-contracts can be opened, rewritten, and advanced through a bounded lifecycle; active task contracts are visible in assembled and role-specific contexts; and round/objective transitions refuse to leave dangling active task contracts behind.

## Validation Plan

Run targeted py_compile, pressure-test the new task-contract lifecycle on a real task contract in session-memory, run task-contract audit, assemble-context and role-context output checks, refresh current-task anchor, then rerun control audit and worktree enforcement.
uv run python -m py_compile scripts/round_control.py scripts/transition_specs.py scripts/open_task_contract.py scripts/update_task_contract_status.py scripts/rewrite_open_task_contract.py scripts/audit_task_contracts.py scripts/audit_control_state.py scripts/control_enforcement.py scripts/assemble_context.py scripts/compile_role_context.py scripts/update_round_status.py scripts/close_objective.py scripts/record_hard_pivot.py scripts/rewrite_open_round.py scripts/session_memory.py
uv run python scripts/audit_product_docs.py
uv run python scripts/audit_task_contracts.py --project-id session-memory
uv run python scripts/audit_control_state.py --project-id session-memory
uv run python scripts/enforce_worktree.py --project-id session-memory
uv run python scripts/session_memory.py audit-task-contracts --project-id session-memory
uv run python scripts/assemble_context.py --project-id session-memory
uv run python scripts/compile_role_context.py --project-id session-memory --role reviewer
owner-layer validation recorded in round contract before capture

## Active Risks

_none recorded_

## Blockers

_none recorded_

## Status Notes

_none recorded_

Scope refreshed because Task-contract enforcement now consumes active task-contract coverage, so control_enforcement.py entered the bounded implementation surface.

Live dirty paths included:
- ARCHITECTURE.md
- CONTROL_SYSTEM.md
- DESIGN_PRINCIPLES.md
- IMPLEMENTATION_PLAN.md
- PRODUCT.md
- STATE_MACHINE.md
- TRANSITION_COMMANDS.md
- scripts/assemble_context.py
- scripts/audit_control_state.py
- scripts/audit_task_contracts.py
- scripts/close_objective.py
- scripts/compile_role_context.py
- scripts/control_enforcement.py
- scripts/open_task_contract.py
- scripts/record_hard_pivot.py
- scripts/rewrite_open_round.py
- scripts/round_control.py
- scripts/session_memory.py
- scripts/transition_specs.py
- scripts/update_round_status.py
- scripts/rewrite_open_task_contract.py
- scripts/update_task_contract_status.py

active -> validation_pending: Task-contract lifecycle and consumption landed with repo-owned validation passing on the real project.

validated by:
- uv run python -m py_compile scripts/round_control.py scripts/transition_specs.py scripts/open_task_contract.py scripts/update_task_contract_status.py scripts/rewrite_open_task_contract.py scripts/audit_task_contracts.py scripts/audit_control_state.py scripts/control_enforcement.py scripts/assemble_context.py scripts/compile_role_context.py scripts/update_round_status.py scripts/close_objective.py scripts/record_hard_pivot.py scripts/rewrite_open_round.py scripts/session_memory.py
- uv run python scripts/audit_product_docs.py
- uv run python scripts/audit_task_contracts.py --project-id session-memory
- uv run python scripts/audit_control_state.py --project-id session-memory
- uv run python scripts/enforce_worktree.py --project-id session-memory
- uv run python scripts/session_memory.py audit-task-contracts --project-id session-memory
- uv run python scripts/assemble_context.py --project-id session-memory
- uv run python scripts/compile_role_context.py --project-id session-memory --role reviewer

validation_pending -> captured: Validated task-contract lifecycle and consumption on the real project with clean control audit and worktree enforcement.

validated by:
- owner-layer validation recorded in round contract before capture

captured -> closed: Task-contract lifecycle and consumption round is complete and committed state will follow.

