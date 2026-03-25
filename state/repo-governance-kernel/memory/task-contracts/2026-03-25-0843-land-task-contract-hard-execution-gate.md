---
id: taskc-2026-03-25-0843-land-task-contract-hard-execution-gate
type: task-contract
title: "Land task-contract hard execution gate"
status: completed
project_id: repo-governance-kernel
workspace_id: ws-1490b759
workspace_root: C:/Users/terryzzb/Desktop/session-memory
branch: master
git_sha: afad3f1b796dd2cb73421997d577eacb1635334e
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
  - task-contract
  - control-plane
confidence: high
created_at: 2026-03-25T08:43:50+08:00
updated_at: 2026-03-25T09:45:58+08:00
objective_id: obj-2026-03-23-0002
phase: execution
round_id: "round-2026-03-25-0843-make-task-contract-a-real-hard-execution-gate"
supersedes: []
superseded_by: []
---

## Summary

Complete task-contract hard-gate coverage for bundle-backed adjudication followups, then cut the 0.1.0a2 alpha release with aligned metadata and release evidence.

## Intent

Prove that governed round-close bundles executed through adjudication followups still fail closed on unresolved task contracts, then update versioning and release-facing docs to ship that hardened alpha surface as 0.1.0a2.

## Allowed Changes

- Add one focused validation path that exercises execute-adjudication-followups plus round-close-chain against an unresolved task contract and proves the high-level surface is blocked until task resolution.
- Update package metadata and release-facing docs to 0.1.0a2 only after the hard-gate proof and release-grade validations pass.
- Run build and installed-wheel verification so the release claim is backed by observed package behavior, not only source-tree smoke.

## Forbidden Changes

- Do not bypass task-contract gating with private bundle logic, adjudication special cases, or direct durable rewrites.
- Do not claim 0.1.0a2 release readiness without aligned version metadata, docs, and installed-wheel evidence.

## Completion Criteria

- A focused proof shows execute-adjudication-followups plus round-close-chain is blocked until the attached task contract is resolved.
- Version metadata and release-facing docs all point to 0.1.0a2 and describe the hardened alpha surface consistently.
- smoke_phase1, smoke_kernel_bootstrap, audit-control-state, enforce-worktree, audit_product_docs, uv build, and installed-wheel verification all pass on the release candidate.

## Resolution

- Direct promotion and governed close bundles now share the same unresolved task-contract gate.
- Package metadata, release docs, installed-wheel proof, and entry docs were aligned and published as 0.1.0a2.

## Active Risks

- If the high-level proof only covers direct command entry, governed bundles could still hide a task-contract bypass.
- If the release cut updates version strings without re-proving installed-wheel behavior, the a2 tag would overclaim the package surface.

## Status Notes

Task contract rewritten because Expand the task contract to finish high-level hard-gate proof coverage and the 0.1.0a2 release cut inside the same bounded execution contract.

Task contract rewritten because Include uv.lock in the release-cut execution boundary so version metadata and the lockfile do not drift.

active -> completed: The direct and high-level task-contract hard gate landed, and the 0.1.0a2 release cut plus package/install evidence are complete.

resolution recorded:
- Direct promotion and governed close bundles now share the same unresolved task-contract gate.
- Package metadata, release docs, installed-wheel proof, and entry docs were aligned and published as 0.1.0a2.

