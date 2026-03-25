---
id: taskc-2026-03-25-1705-land-b1-minimal-evidence-layer-public-subcontracts
type: task-contract
title: "Land b1 minimal evidence-layer public subcontracts"
status: completed
project_id: repo-governance-kernel
workspace_id: ws-1490b759
workspace_root: C:/Users/terryzzb/Desktop/session-memory
branch: master
git_sha: c18f66b4923034042037b9252c432b9797e59ad4
paths:
  - kernel/public_flow_contracts.py
  - kernel/public_surface.py
  - kernel/repo_onboarding.py
  - kernel/commands/assess_external_target_once.py
  - kernel/commands/onboard_repo_from_intent.py
  - kernel/commands/assess_external_target_from_intent.py
  - docs/canonical/PUBLIC_SURFACE.md
  - docs/canonical/IMPLEMENTATION_PLAN.md
  - kernel/README.md
  - README.md
  - scripts/smoke_repo_onboarding.py
  - scripts/smoke_assess_host_adoption.py
  - scripts/smoke_kernel_bootstrap.py
  - kernel/docs/PUBLIC_SURFACE.md
thread_ids: []
evidence_refs: []
tags:
  - task-contract
  - control-plane
confidence: high
created_at: 2026-03-25T17:05:04+08:00
updated_at: 2026-03-25T17:14:37+08:00
objective_id: obj-2026-03-23-0002
phase: execution
round_id: "round-2026-03-25-1704-harden-public-evidence-layer-response-contracts-for-b1"
supersedes: []
superseded_by: []
---

## Summary

Move the smallest repeated execution/outcome/postconditions kernels into one owner-layer public contract so agent callers can depend on them directly.

## Intent

Move the smallest repeated execution/outcome/postconditions kernels into one owner-layer public contract so agent callers can depend on them directly.

## Allowed Changes

- Add owner-layer stable subcontract declarations only for repeated evidence-layer kernels that are already shared across public flows.
- Update machine-readable public-surface descriptors, package docs, canonical docs, and targeted smoke assertions to the same contract truth.

## Forbidden Changes

- Do not freeze whole evidence payloads when only a smaller repeated kernel is actually reusable.
- Do not broaden package authority beyond onboarding and one-time external-target assessment.

## Completion Criteria

- Public contract descriptors, docs, and smokes all agree on the new minimal stable evidence-layer subcontracts.
- The targeted public-flow validation path passes after the contract upgrade.

## Resolution

- added owner-layer dotted subcontract support plus b1-target candidate subcontract catalogs for the smallest repeated execution/outcome/postconditions kernels
- aligned canonical docs, package docs, READMEs, and public-surface notes to separate the released b0 stable promise from the in-progress b1 candidate catalog
- passed describe-public-surface, smoke_repo_onboarding.py, smoke_assess_host_adoption.py, smoke_kernel_bootstrap.py, audit_product_docs.py, audit-control-state, and enforce-worktree

## Active Risks

_none recorded_

## Status Notes

Task contract rewritten because the package-facing public-surface summary under kernel/docs changed with the same candidate contract truth

Expanded the active b1 task scope to include the package-facing public-surface summary.

active -> completed: the b1 evidence-layer hardening slice now records machine-readable candidate subcontracts, aligns docs, and passes the targeted validation path

resolution recorded:
- added owner-layer dotted subcontract support plus b1-target candidate subcontract catalogs for the smallest repeated execution/outcome/postconditions kernels
- aligned canonical docs, package docs, READMEs, and public-surface notes to separate the released b0 stable promise from the in-progress b1 candidate catalog
- passed describe-public-surface, smoke_repo_onboarding.py, smoke_assess_host_adoption.py, smoke_kernel_bootstrap.py, audit_product_docs.py, audit-control-state, and enforce-worktree

Completed after the package-facing contract catalog, docs, and targeted smokes all agreed on the same b1-target evidence-layer promotion candidates.

