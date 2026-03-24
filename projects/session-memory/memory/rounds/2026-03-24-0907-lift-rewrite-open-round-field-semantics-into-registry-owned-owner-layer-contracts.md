---
id: round-2026-03-24-0907-lift-rewrite-open-round-field-semantics-into-registry-owned-owner-layer-contracts
type: round-contract
title: "Introduce first task-contract owner layer"
status: closed
project_id: session-memory
workspace_id: ws-1490b759
workspace_root: C:/Users/terryzzb/Desktop/session-memory
branch: master
git_sha: a43b816258cb88a3b7e11b2160d0d8612069c814
paths:
  - scripts/transition_specs.py
  - scripts/execute_adjudication_followups.py
  - scripts/audit_control_state.py
  - CONTROL_SYSTEM.md
  - TRANSITION_COMMANDS.md
  - projects/session-memory/current/current-task.md
  - .githooks/pre-push
  - .github/workflows/control-enforcement.yml
  - ARCHITECTURE.md
  - DESIGN_PRINCIPLES.md
  - IMPLEMENTATION_PLAN.md
  - STATE_MACHINE.md
  - PRODUCT.md
  - scripts/audit_product_docs.py
  - scripts/product_semantics.py
  - scripts/round_control.py
  - scripts/audit_task_contracts.py
  - scripts/open_task_contract.py
  - projects/session-memory/memory/task-contracts
thread_ids: []
evidence_refs: []
tags:
  - round
  - control-plane
confidence: high
created_at: 2026-03-24T09:07:16+08:00
updated_at: 2026-03-24T10:44:55+08:00
objective_id: obj-2026-03-23-0002
phase: execution
supersedes: []
superseded_by: []
---

## Summary

Define task-contract as the missing layer between round contracts and concrete implementation tasks, align canonical docs to that architecture, and land the first minimal file-first task-contract object plus audit path on this repository.

## Scope

- Align canonical docs so product, control, state-machine, and transition surfaces explicitly place task-contract under round governance instead of leaving task-level execution semantics in prose.
- Add a first file-first task-contract object model and creation path that can attach one concrete task contract to an active round without inventing a new DSL.
- Add a minimal audit path for task-contract integrity and pressure-test the model with one real task contract in the session-memory project.

## Deliverable

Session-memory docs describe a three-layer product/control/task contract architecture, the repo can create and read durable task-contract objects, and one real task-contract sample plus audit path proves the layer is no longer only prose.

## Validation Plan

Run targeted py_compile for the new task-contract scripts, create one real task-contract for the active round, run the new task-contract audit, refresh current-task anchor, then run control audit and worktree enforcement before commit.
uv run python -m py_compile scripts/round_control.py scripts/transition_specs.py scripts/open_task_contract.py scripts/audit_task_contracts.py scripts/audit_control_state.py
uv run python scripts/audit_product_docs.py
uv run python scripts/audit_task_contracts.py --project-id session-memory
uv run python scripts/audit_control_state.py --project-id session-memory
uv run python scripts/enforce_worktree.py --project-id session-memory
owner-layer validation recorded in round contract and latest commit a43b816

## Active Risks

_none recorded_

## Blockers

_none recorded_

## Status Notes

_none recorded_

Round rewritten because Scope shifted from continuing bundle-semantic registration to bundle governance institutionalization.

Round rewritten because Scope shifted from bundle-governance law to product-definition alignment and doc-driven semantics governance.

Round rewritten because Product-definition alignment round expanded to additional canonical docs, product semantics audit scripts, and enforcement entrypoints that must be explicitly in round scope.

Round rewritten because Scope shifted from product-doc alignment to introducing the first task-contract owner layer and pressure-testing it on the current repository.

Scope refreshed because task-contract owner-layer implementation adds new task-contract scripts and durable task-contract sample path

Live dirty paths included:
- ARCHITECTURE.md
- CONTROL_SYSTEM.md
- DESIGN_PRINCIPLES.md
- IMPLEMENTATION_PLAN.md
- PRODUCT.md
- STATE_MACHINE.md
- TRANSITION_COMMANDS.md
- scripts/audit_control_state.py
- scripts/round_control.py
- scripts/transition_specs.py
- scripts/audit_task_contracts.py
- scripts/open_task_contract.py

active -> validation_pending: First task-contract owner-layer docs, registry, creation path, audit path, and real sample were implemented and validated.

validated by:
- uv run python -m py_compile scripts/round_control.py scripts/transition_specs.py scripts/open_task_contract.py scripts/audit_task_contracts.py scripts/audit_control_state.py
- uv run python scripts/audit_product_docs.py
- uv run python scripts/audit_task_contracts.py --project-id session-memory
- uv run python scripts/audit_control_state.py --project-id session-memory
- uv run python scripts/enforce_worktree.py --project-id session-memory

validation_pending -> captured: Validated first task-contract owner layer on the real project and repo-owned audits all passed.

validated by:
- owner-layer validation recorded in round contract and latest commit a43b816

captured -> closed: First task-contract owner-layer round is complete; successor round will land lifecycle and consumption surfaces.
