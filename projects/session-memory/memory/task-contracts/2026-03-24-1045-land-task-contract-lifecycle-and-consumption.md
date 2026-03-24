---
id: taskc-2026-03-24-1045-land-task-contract-lifecycle-and-consumption
type: task-contract
title: "Land task-contract lifecycle and consumption"
status: completed
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
  - projects/session-memory/current/current-task.md
  - projects/session-memory/memory/task-contracts
  - scripts/control_enforcement.py
thread_ids: []
evidence_refs: []
tags:
  - task-contract
  - control-plane
confidence: high
created_at: 2026-03-24T10:45:43+08:00
updated_at: 2026-03-24T10:56:40+08:00
objective_id: obj-2026-03-23-0002
phase: execution
round_id: "round-2026-03-24-1045-complete-task-contract-lifecycle-and-consumption"
supersedes: []
superseded_by: []
---

## Summary

Turn task-contract from a static durable object into a bounded execution surface that can flow through lifecycle transitions and be consumed by context and honesty checks.

## Intent

Turn task-contract from a static durable object into a bounded execution surface that can flow through lifecycle transitions and be consumed by context and honesty checks.

## Allowed Changes

- Add task-contract lifecycle commands and registry semantics.
- Make context assembly and role-context compilation surface active task contracts.
- Block round or objective transitions that would strand active task contracts.
- Update canonical docs and CLI entrypoints in the same round.
- Narrow live dirty-path authority from round scope to active task-contract scope when active task contracts exist.

## Forbidden Changes

- Do not infer autonomous rewrites from task-contract prose alone.
- Do not add a second private lifecycle or consumption path outside shared helpers and registry.
- Do not widen task paths outside the active round scope.

## Completion Criteria

- Task-contracts can be rewritten and advanced through a bounded lifecycle on the real repo.
- Assembled and role-specific contexts surface active task contracts.
- Control honesty rejects dangling active task contracts across round or objective closure.
- Worktree enforcement passes with active task-contract coverage semantics on the real project.

## Resolution

- Task-contracts now support bounded rewrite and status transitions, appear in assembled and reviewer contexts, and participate in worktree enforcement plus round/objective honesty checks.

## Active Risks

- Task-level enforcement can become too strict if active-task selection and path coverage semantics are underspecified.

## Status Notes

Task contract rewritten because Task-contract enforcement now consumes active task-contract coverage, so the task boundary must include control_enforcement.py and the tighter honesty work.

active -> completed: Task-contract lifecycle, context consumption, honesty gates, and CLI entrypoints landed and passed repo-owned validation.

resolution recorded:
- Task-contracts now support bounded rewrite and status transitions, appear in assembled and reviewer contexts, and participate in worktree enforcement plus round/objective honesty checks.
