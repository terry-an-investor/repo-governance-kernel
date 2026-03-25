---
id: taskc-2026-03-24-1037-land-first-task-contract-owner-layer
type: task-contract
title: "Land first task-contract owner layer"
status: completed
project_id: repo-governance-kernel
workspace_id: ws-1490b759
workspace_root: C:/Users/terryzzb/Desktop/session-memory
branch: master
git_sha: a43b816258cb88a3b7e11b2160d0d8612069c814
paths:
  - PRODUCT.md
  - CONTROL_SYSTEM.md
  - ARCHITECTURE.md
  - STATE_MACHINE.md
  - TRANSITION_COMMANDS.md
  - scripts/round_control.py
  - scripts/transition_specs.py
  - scripts/open_task_contract.py
  - scripts/audit_task_contracts.py
  - scripts/audit_control_state.py
  - state/repo-governance-kernel/memory/task-contracts
thread_ids: []
evidence_refs: []
tags:
  - task-contract
  - control-plane
confidence: high
created_at: 2026-03-24T10:37:10+08:00
updated_at: 2026-03-24T10:53:00+08:00
objective_id: obj-2026-03-23-0002
phase: execution
round_id: "round-2026-03-24-0907-lift-rewrite-open-round-field-semantics-into-registry-owned-owner-layer-contracts"
supersedes: []
superseded_by: []
---

## Summary

Make task-level execution boundaries durable beneath the active round by aligning docs, registry semantics, creation flow, and integrity audit.

## Intent

Make task-level execution boundaries durable beneath the active round by aligning docs, registry semantics, creation flow, and integrity audit.

## Allowed Changes

- Define task-contract as a round-governed durable object in canonical docs.
- Add registry-backed task-contract creation semantics and shared helper consumption.
- Create one real sample task-contract for this round.

## Forbidden Changes

- Do not claim general autonomous rewrite from task-contract prose.
- Do not introduce a second private task orchestration stack outside the transition registry and shared helper.
- Do not widen task paths outside the active round scope.

## Completion Criteria

- Canonical docs describe product/control/task-contract layering consistently.
- Repo can create and load durable task-contract objects through repo-owned code.
- Task-contract audit passes on one real sample in session-memory.

## Resolution

- Canonical docs, registry, create path, audit path, and real sample all landed in commit a43b816.

## Active Risks

- Task-contract semantics may drift back into prose if command and audit coverage diverge.

## Status Notes

active -> completed: The first task-contract owner-layer round was implemented, validated, committed, and then closed.

resolution recorded:
- Canonical docs, registry, create path, audit path, and real sample all landed in commit a43b816.


