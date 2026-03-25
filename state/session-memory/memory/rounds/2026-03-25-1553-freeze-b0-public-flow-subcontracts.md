---
id: round-2026-03-25-1553-freeze-b0-public-flow-subcontracts
type: round-contract
title: "Freeze b0 public flow subcontracts"
status: closed
project_id: session-memory
workspace_id: ws-1490b759
workspace_root: C:/Users/terryzzb/Desktop/session-memory
branch: master
git_sha: c72085d98b4ea4358d900f60d942455b8e9571b2
paths:
  - kernel/public_flow_contracts.py
  - kernel/public_alpha_surface.py
  - docs/canonical/PUBLIC_ALPHA_SURFACE.md
  - kernel/docs/PUBLIC_ALPHA_SURFACE.md
  - scripts/smoke_repo_onboarding.py
  - scripts/smoke_assess_host_adoption.py
  - scripts/smoke_kernel_bootstrap.py
thread_ids: []
evidence_refs: []
tags:
  - round
  - control-plane
confidence: high
created_at: 2026-03-25T15:53:04+08:00
updated_at: 2026-03-25T16:03:59+08:00
objective_id: obj-2026-03-23-0002
phase: execution
supersedes: []
superseded_by: []
---

## Summary

One machine-readable b0 candidate subcontract catalog for stable nested public flow fields, exported through the public alpha surface and enforced by smoke.

## Scope

- Define one owner-layer catalog for stable public subcontracts beneath the four public flow payloads.
- Freeze only flow_contract and intent_compilation nested fields in this slice; leave execution, outcome, and postconditions outside the stable minimum contract.

## Deliverable

One machine-readable b0 candidate subcontract catalog for stable nested public flow fields, exported through the public alpha surface and enforced by smoke.

## Validation Plan

Run py_compile, the public flow smokes, the kernel bootstrap smoke, product doc audit, audit-control-state, and enforce-worktree.
uv run python -m py_compile kernel\\public_flow_contracts.py kernel\\public_alpha_surface.py scripts\\smoke_repo_onboarding.py scripts\\smoke_assess_host_adoption.py scripts\\smoke_kernel_bootstrap.py
uv run python scripts\\smoke_repo_onboarding.py
uv run python scripts\\smoke_assess_host_adoption.py
uv run python scripts\\smoke_kernel_bootstrap.py
uv run python scripts\\audit_product_docs.py
uv run python -m kernel.cli audit-control-state --project-id session-memory
uv run python -m kernel.cli enforce-worktree --project-id session-memory --workspace-root C:/Users/terryzzb/Desktop/session-memory
py_compile + smoke_repo_onboarding + smoke_assess_host_adoption + smoke_kernel_bootstrap + audit_product_docs + audit-control-state + enforce-worktree

## Active Risks

_none recorded_

## Blockers

_none recorded_

## Status Notes

_none recorded_

Round rewritten because This slice also tightened the installed-package bootstrap smoke, so the durable round scope must explicitly cover that validation surface.

active -> validation_pending: The b0 public subcontract slice passed py_compile, all three public smokes, product doc audit, audit-control-state, and enforce-worktree after scope rewrite.

validated by:
- uv run python -m py_compile kernel\\public_flow_contracts.py kernel\\public_alpha_surface.py scripts\\smoke_repo_onboarding.py scripts\\smoke_assess_host_adoption.py scripts\\smoke_kernel_bootstrap.py
- uv run python scripts\\smoke_repo_onboarding.py
- uv run python scripts\\smoke_assess_host_adoption.py
- uv run python scripts\\smoke_kernel_bootstrap.py
- uv run python scripts\\audit_product_docs.py
- uv run python -m kernel.cli audit-control-state --project-id session-memory
- uv run python -m kernel.cli enforce-worktree --project-id session-memory --workspace-root C:/Users/terryzzb/Desktop/session-memory

validation_pending -> captured: The validated b0 public subcontract result is now durable and can leave open execution.

validated by:
- py_compile + smoke_repo_onboarding + smoke_assess_host_adoption + smoke_kernel_bootstrap + audit_product_docs + audit-control-state + enforce-worktree

captured -> closed: The b0 public subcontract freeze slice is complete and its validated result has been captured in durable history.
