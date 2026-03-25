---
id: round-2026-03-25-0843-make-task-contract-a-real-hard-execution-gate
type: round-contract
title: "Make task-contract a real hard execution gate"
status: active
project_id: session-memory
workspace_id: ws-1490b759
workspace_root: C:/Users/terryzzb/Desktop/session-memory
branch: master
git_sha: 86e350032843e594e4243c8bd4aa1a4f1e57a4a3
paths:
  - kernel
  - scripts
  - docs
  - README.md
  - pyproject.toml
  - uv.lock
thread_ids: []
evidence_refs: []
tags:
  - round
  - control-plane
confidence: high
created_at: 2026-03-25T08:43:50+08:00
updated_at: 2026-03-25T09:04:45+08:00
objective_id: obj-2026-03-23-0002
phase: execution
supersedes: []
superseded_by: []
---

## Summary

Finish task-contract hard-gate coverage on high-level adjudication and bundle surfaces, then cut the 0.1.0a2 alpha release with aligned package metadata and release evidence.

## Scope

- Prove governed bundle and adjudication follow-up surfaces fail closed when unresolved task contracts still block the round close chain.
- Cut the 0.1.0a2 alpha release by updating package metadata, release-facing docs, and release-grade validation evidence in one controlled round.

## Deliverable

One hard-gate-complete owner layer plus one 0.1.0a2 release cut with aligned versioning, docs, and release evidence.

## Validation Plan

Run focused bundle/adjudication hard-gate proof, smoke_phase1, smoke_kernel_bootstrap, audit-control-state, enforce-worktree, audit_product_docs, uv build, and installed-wheel verification after the release cut lands.

## Active Risks

- High-level workflow surfaces may still bypass the low-level task-contract gate unless one bundle-backed proof demonstrates the blocked path directly.
- The release cut can drift from the real package surface if version, docs, and installed-wheel evidence are not updated in the same round.

## Blockers

_none recorded_

## Status Notes

_none recorded_

Round rewritten because Expand the round to cover the remaining high-level hard-gate proof and the 0.1.0a2 release cut so code, docs, and versioning stay inside the same honest control boundary.

Round rewritten because Include uv.lock in the release-cut boundary so package metadata and the lockfile stay aligned inside the same honest round.
