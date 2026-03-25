---
id: round-2026-03-25-1514-start-b0-public-contract-freeze
type: round-contract
title: "Start b0 public contract freeze"
status: active
project_id: session-memory
workspace_id: ws-1490b759
workspace_root: C:/Users/terryzzb/Desktop/session-memory
branch: master
git_sha: dd9b5402cf97ad67dd55f5897652f77bd82396f1
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
updated_at: 2026-03-25T15:14:50+08:00
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

## Active Risks

_none recorded_

## Blockers

_none recorded_

## Status Notes

_none recorded_
