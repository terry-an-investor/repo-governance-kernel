---
id: trans-2026-03-25-113345-update-task-contract-status-updated-task-contract-taskc-2026-03-25-1126-harden-filename-budgeting-and-local-smoke-gate-for-ci-parity-to-completed
type: transition-event
title: "Updated task contract taskc-2026-03-25-1126-harden-filename-budgeting-and-local-smoke-gate-for-ci-parity to completed"
status: recorded
project_id: repo-governance-kernel
workspace_id: ws-1490b759
workspace_root: C:/Users/terryzzb/Desktop/session-memory
branch: master
git_sha: 80b47b322a49439cb9b79eb6884b8b6bdc8a89af
paths:
  - taskc-2026-03-25-1126-harden-filename-budgeting-and-local-smoke-gate-for-ci-parity
  - round-2026-03-25-1116-start-explicit-package-config-layering-for-a4
  - obj-2026-03-23-0002
thread_ids: []
evidence_refs: []
tags:
  - transition-event
  - update-task-contract-status
confidence: high
created_at: 2026-03-25T11:33:45+08:00
updated_at: 2026-03-25T11:33:45+08:00
supersedes: []
superseded_by: []
---

## Summary

Updated task contract taskc-2026-03-25-1126-harden-filename-budgeting-and-local-smoke-gate-for-ci-parity to completed

## Command

update-task-contract-status

## Previous State

task contract `taskc-2026-03-25-1126-harden-filename-budgeting-and-local-smoke-gate-for-ci-parity` status `active`

## Next State

task contract `taskc-2026-03-25-1126-harden-filename-budgeting-and-local-smoke-gate-for-ci-parity` is now `completed`

## Guards

- task contract `taskc-2026-03-25-1126-harden-filename-budgeting-and-local-smoke-gate-for-ci-parity` exists
- task-contract transition `active -> completed` is legal
- completed task-contract transitions include at least one resolution record

## Side Effects

- updated durable task contract `repo-governance-kernel/memory/task-contracts/2026-03-25-1126-harden-filename-budgeting-and-local-smoke-gate-for-ci-parity.md`

## Evidence

- Shared durable filename budgeting now covers the direct memory-object write surfaces that were escaping into long-path failures, and the source-repo pre-push gate now runs the same phase-1 smoke surface that caught the a3 escape.
- Added one shared durable_markdown_path helper in kernel/round_control.py and routed objective, round, task-contract, exception-contract, adjudication, and pivot writes through it across kernel commands and repo-local script entrypoints.
- Raised the source-repo .githooks/pre-push gate to run scripts/smoke_phase1.py so the same smoke surface runs locally before push instead of only on GitHub Actions.
- Validated the changed path with uv run python scripts/smoke_transition_engine.py, uv run python scripts/smoke_phase1.py, uv run python scripts/audit_product_docs.py, uv run python -m kernel.cli audit-control-state --project-id repo-governance-kernel, and uv run python -m kernel.cli enforce-worktree --project-id repo-governance-kernel --workspace-root C:/Users/terryzzb/Desktop/session-memory

