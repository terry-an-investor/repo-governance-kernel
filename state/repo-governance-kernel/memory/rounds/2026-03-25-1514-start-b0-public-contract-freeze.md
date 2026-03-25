---
id: round-2026-03-25-1514-start-b0-public-contract-freeze
type: round-contract
title: "Start b0 public contract freeze"
status: closed
project_id: repo-governance-kernel
workspace_id: ws-1490b759
workspace_root: C:/Users/terryzzb/Desktop/session-memory
branch: master
git_sha: 00f1703978ec0b681ea5bdebb1813ee25f5253e4
paths:
  - kernel/public_flow_contracts.py
  - kernel/public_alpha_surface.py
  - scripts/smoke_repo_onboarding.py
  - scripts/smoke_assess_host_adoption.py
  - scripts/smoke_kernel_bootstrap.py
  - docs/canonical/PUBLIC_ALPHA_SURFACE.md
  - kernel/docs/PUBLIC_ALPHA_SURFACE.md
thread_ids: []
evidence_refs: []
tags:
  - round
  - control-plane
confidence: high
created_at: 2026-03-25T15:14:50+08:00
updated_at: 2026-03-25T15:21:02+08:00
objective_id: obj-2026-03-23-0002
phase: execution
supersedes: []
superseded_by: []
---

## Summary

One repo-owned b0 candidate contract descriptor for public flows, wired into docs and smoke.

## Scope

- Define one machine-readable owner-layer contract for the four current public flow entrypoints and their stable success/blocked fields.
- Make describe-public-alpha-surface export that contract and make smoke consume it.
- Update canonical and package-facing docs to mark this as the b0 candidate contract source of truth.

## Deliverable

One repo-owned b0 candidate contract descriptor for public flows, wired into docs and smoke.

## Validation Plan

Run py_compile, onboarding smoke, assessment smoke, bootstrap smoke, audit-product-docs, audit-control-state, and enforce-worktree.
uv run python -m py_compile kernel\\public_flow_contracts.py kernel\\public_alpha_surface.py scripts\\smoke_repo_onboarding.py scripts\\smoke_assess_host_adoption.py scripts\\smoke_kernel_bootstrap.py
uv run python scripts\\smoke_repo_onboarding.py
uv run python scripts\\smoke_assess_host_adoption.py
uv run python scripts\\smoke_kernel_bootstrap.py
uv run python scripts\\audit_product_docs.py
uv run python -m kernel.cli audit-control-state --project-id repo-governance-kernel
uv run python -m kernel.cli enforce-worktree --project-id repo-governance-kernel --workspace-root C:/Users/terryzzb/Desktop/session-memory
py_compile + smoke_repo_onboarding + smoke_assess_host_adoption + smoke_kernel_bootstrap + audit_product_docs + audit-control-state + enforce-worktree

## Active Risks

_none recorded_

## Blockers

_none recorded_

## Status Notes

active -> validation_pending: The b0 candidate contract freeze slice passed py_compile, public flow smokes, product doc audit, audit-control-state, and enforce-worktree.

validated by:
- uv run python -m py_compile kernel\\public_flow_contracts.py kernel\\public_alpha_surface.py scripts\\smoke_repo_onboarding.py scripts\\smoke_assess_host_adoption.py scripts\\smoke_kernel_bootstrap.py
- uv run python scripts\\smoke_repo_onboarding.py
- uv run python scripts\\smoke_assess_host_adoption.py
- uv run python scripts\\smoke_kernel_bootstrap.py
- uv run python scripts\\audit_product_docs.py
- uv run python -m kernel.cli audit-control-state --project-id repo-governance-kernel
- uv run python -m kernel.cli enforce-worktree --project-id repo-governance-kernel --workspace-root C:/Users/terryzzb/Desktop/session-memory

validation_pending -> captured: The validated b0 candidate contract freeze result is now durable and ready to close.

validated by:
- py_compile + smoke_repo_onboarding + smoke_assess_host_adoption + smoke_kernel_bootstrap + audit_product_docs + audit-control-state + enforce-worktree

captured -> closed: The b0 candidate contract freeze slice is complete and its validated result has been captured in durable history.

