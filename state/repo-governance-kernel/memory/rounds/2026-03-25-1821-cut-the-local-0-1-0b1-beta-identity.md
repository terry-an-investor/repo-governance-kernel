---
id: round-2026-03-25-1821-cut-the-local-0-1-0b1-beta-identity
type: round-contract
title: "Cut the local 0.1.0b1 beta identity"
status: closed
project_id: repo-governance-kernel
workspace_id: ws-1490b759
workspace_root: C:/Users/terryzzb/Desktop/session-memory
branch: master
git_sha: 2b5145d2a5d306b61493b7706e76b2175d143c99
paths:
  - pyproject.toml
  - uv.lock
  - kernel/public_flow_contracts.py
  - kernel/public_surface.py
  - README.md
  - docs/README.md
  - kernel/README.md
  - docs/canonical/PUBLIC_SURFACE.md
  - docs/canonical/RELEASE.md
  - docs/canonical/IMPLEMENTATION_PLAN.md
  - docs/canonical/TRANSITION_COMMANDS.md
  - kernel/docs/PUBLIC_SURFACE.md
  - kernel/docs/TRANSITION_COMMANDS.md
  - scripts/smoke_kernel_bootstrap.py
  - scripts/smoke_repo_onboarding.py
  - scripts/smoke_assess_host_adoption.py
thread_ids: []
evidence_refs: []
tags:
  - round
  - control-plane
confidence: high
created_at: 2026-03-25T18:21:36+08:00
updated_at: 2026-03-25T18:38:11+08:00
objective_id: obj-2026-03-23-0002
phase: execution
supersedes: []
superseded_by: []
---

## Summary

A coherent local 0.1.0b1 package identity across code, docs, and release evidence.

## Scope

- Promote the selected b1 contract into the released package identity without widening authority.

## Deliverable

A coherent local 0.1.0b1 package identity across code, docs, and release evidence.

## Validation Plan

Run the public-surface describe command, docs audit, bootstrap/onboarding/adoption/task-contract/acceptance smokes, uv build, and control-state enforcement for the local 0.1.0b1 release cut.
uv run python -m kernel.cli describe-public-surface
uv run python scripts/audit_product_docs.py
uv run python scripts/smoke_repo_onboarding.py
uv run python scripts/smoke_assess_host_adoption.py
uv run python scripts/smoke_kernel_bootstrap.py
uv run python scripts/smoke_task_contract_hard_gate.py
uv run python scripts/smoke_task_contract_bundle_gate.py
uv run python scripts/smoke_repo_acceptance.py
uv run python -m kernel.cli audit-control-state --project-id repo-governance-kernel
uv run python -m kernel.cli enforce-worktree --project-id repo-governance-kernel --workspace-root C:/Users/terryzzb/Desktop/session-memory
uv build

## Active Risks

_none recorded_

## Blockers

_none recorded_

## Status Notes

_none recorded_

Round rewritten because Capture the full b1 identity release slice in the active round scope.

active -> validation_pending: Implementation is complete and the local 0.1.0b1 release matrix has passed.

validation_pending -> captured: Capture the validated 0.1.0b1 local beta release identity before close-out.

validated by:
- uv run python -m kernel.cli describe-public-surface
- uv run python scripts/audit_product_docs.py
- uv run python scripts/smoke_repo_onboarding.py
- uv run python scripts/smoke_assess_host_adoption.py
- uv run python scripts/smoke_kernel_bootstrap.py
- uv run python scripts/smoke_task_contract_hard_gate.py
- uv run python scripts/smoke_task_contract_bundle_gate.py
- uv run python scripts/smoke_repo_acceptance.py
- uv run python -m kernel.cli audit-control-state --project-id repo-governance-kernel
- uv run python -m kernel.cli enforce-worktree --project-id repo-governance-kernel --workspace-root C:/Users/terryzzb/Desktop/session-memory
- uv build

captured -> closed: The validated 0.1.0b1 local beta release identity is now durably captured and can leave execution.

