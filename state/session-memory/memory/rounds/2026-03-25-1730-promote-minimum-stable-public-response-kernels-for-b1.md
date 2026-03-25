---
id: round-2026-03-25-1730-promote-minimum-stable-public-response-kernels-for-b1
type: round-contract
title: "Promote minimum stable public response kernels for b1"
status: closed
project_id: session-memory
workspace_id: ws-1490b759
workspace_root: C:/Users/terryzzb/Desktop/session-memory
branch: master
git_sha: e128136188eb75da4d18423c060e06247443667a
paths:
  - kernel/public_flow_contracts.py
  - kernel/public_surface.py
  - scripts/smoke_repo_onboarding.py
  - scripts/smoke_assess_host_adoption.py
  - scripts/smoke_kernel_bootstrap.py
  - docs/canonical/PUBLIC_SURFACE.md
  - docs/canonical/IMPLEMENTATION_PLAN.md
  - kernel/docs/PUBLIC_SURFACE.md
  - docs/canonical/RELEASE.md
  - README.md
  - kernel/README.md
thread_ids: []
evidence_refs: []
tags:
  - round
  - control-plane
confidence: high
created_at: 2026-03-25T17:30:52+08:00
updated_at: 2026-03-25T17:45:29+08:00
objective_id: obj-2026-03-23-0002
phase: execution
supersedes: []
superseded_by: []
---

## Summary

Stable public contract promotion for the minimum repeated b1-ready kernels.

## Scope

- Promote repeated public response kernels that are already stable across direct and intent surfaces.

## Deliverable

Stable public contract promotion for the minimum repeated b1-ready kernels.

## Validation Plan

Run public-surface descriptor and smoke validations for onboarding and assessment flows.
uv run python -m py_compile kernel/public_flow_contracts.py kernel/public_surface.py scripts/smoke_repo_onboarding.py scripts/smoke_assess_host_adoption.py scripts/smoke_kernel_bootstrap.py scripts/audit_product_docs.py
uv run python -m kernel.cli describe-public-surface
uv run python scripts/smoke_repo_onboarding.py
uv run python scripts/smoke_assess_host_adoption.py
uv run python scripts/smoke_kernel_bootstrap.py
uv run python scripts/audit_product_docs.py
uv run python -m kernel.cli audit-control-state --project-id session-memory
uv run python -m kernel.cli enforce-worktree --project-id session-memory --workspace-root C:/Users/terryzzb/Desktop/session-memory
Targeted smokes plus control audits passed before close-out.

## Active Risks

_none recorded_

## Blockers

_none recorded_

## Status Notes

_none recorded_

Round rewritten because Add canonical release guidance to the same bounded b1 contract-promotion slice so public docs stay mutually consistent.

Round rewritten because Bring the package entry docs into the same bounded b1 contract-promotion slice so the first user-facing docs do not drift from canonical truth.

active -> validation_pending: Implementation and targeted validation are complete for the bounded b1 contract promotion slice.

validated by:
- uv run python -m py_compile kernel/public_flow_contracts.py kernel/public_surface.py scripts/smoke_repo_onboarding.py scripts/smoke_assess_host_adoption.py scripts/smoke_kernel_bootstrap.py scripts/audit_product_docs.py
- uv run python -m kernel.cli describe-public-surface
- uv run python scripts/smoke_repo_onboarding.py
- uv run python scripts/smoke_assess_host_adoption.py
- uv run python scripts/smoke_kernel_bootstrap.py
- uv run python scripts/audit_product_docs.py
- uv run python -m kernel.cli audit-control-state --project-id session-memory
- uv run python -m kernel.cli enforce-worktree --project-id session-memory --workspace-root C:/Users/terryzzb/Desktop/session-memory

validation_pending -> captured: Validation evidence is recorded for the bounded b1 contract promotion slice.

validated by:
- Targeted smokes plus control audits passed before close-out.

captured -> closed: The bounded b1 contract promotion slice is complete and its evidence is captured.
