---
id: round-2026-03-25-1553-freeze-b0-public-flow-subcontracts
type: round-contract
title: "Freeze b0 public flow subcontracts"
status: active
project_id: session-memory
workspace_id: ws-1490b759
workspace_root: C:/Users/terryzzb/Desktop/session-memory
branch: master
git_sha: 96e1f2dd79c134ccff6516cba4a98c6ba7725adb
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
updated_at: 2026-03-25T15:59:48+08:00
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

## Active Risks

_none recorded_

## Blockers

_none recorded_

## Status Notes

_none recorded_

Round rewritten because This slice also tightened the installed-package bootstrap smoke, so the durable round scope must explicitly cover that validation surface.
