---
id: taskc-2026-03-24-1929-implement-owner-layer-host-adoption-assessment-for-shadow-mode
type: task-contract
title: "Implement owner-layer host adoption assessment for shadow mode"
status: active
project_id: session-memory
workspace_id: ws-1490b759
workspace_root: C:/Users/terryzzb/Desktop/session-memory
branch: master
git_sha: bd220d0e673e7162f02cdf3d8c823145bd11d88a
paths:
  - kernel
  - scripts/evaluation_bundle.py
  - scripts/smoke_wind_agent_snapshot_bootstrap.py
  - scripts/smoke_wind_agent_snapshot_adoption.py
  - scripts/smoke_brooks_semantic_research_snapshot_adoption.py
  - README.md
  - RELEASE.md
  - TRANSITION_COMMANDS.md
  - scripts/smoke_assess_host_adoption.py
  - ARCHITECTURE.md
  - CONTROL_SYSTEM.md
  - PRODUCT.md
  - pyproject.toml
  - uv.lock
thread_ids: []
evidence_refs: []
tags:
  - task-contract
  - control-plane
confidence: high
created_at: 2026-03-24T19:29:00+08:00
updated_at: 2026-03-24T21:00:57+08:00
objective_id: obj-2026-03-23-0002
phase: execution
round_id: "round-2026-03-24-1928-land-live-host-shadow-assessment-and-adoption-report-owner-layer"
supersedes: []
superseded_by: []
---

## Summary

Implement owner-layer host adoption assessment, bundle-backed external-target single assessment, bounded intent entry, and preview release alignment for shadow mode.

## Intent

Replace duplicated host-adoption reporting logic with one kernel-owned assessment surface, one governed external-target single-assessment flow, one bounded intent entry, and aligned alpha preview docs/version metadata without claiming direct host mutation.

## Allowed Changes

- Add reusable kernel command and runtime surfaces for host adoption assessment, external-target drafting, bundle-backed single assessment, and bounded intent compilation.
- Update canonical product, control, architecture, and release docs plus package metadata so public claims match the implemented owner-layer surface.
- Rebuild the alpha preview package and verify isolated install help output.

## Forbidden Changes

- Do not claim general live-host automatic rewrite, continuous monitoring, or stable beta compatibility.
- Do not mutate external source repositories during validation.

## Completion Criteria

- Kernel-owned host adoption assessment and external-target single-assessment surfaces run through the shared owner-layer runtime.
- Package-facing docs and alpha version metadata reflect the implemented bundle-backed and intent-driven boundary.
- uv build, isolated install help check, repo audit, and worktree enforcement all pass.

## Resolution

_none recorded_

## Active Risks

_none recorded_

## Status Notes

Task contract rewritten because The implementation task also added one host canonical doc update and one command-level smoke, so the task boundary must include those real paths.

Task contract rewritten because The task now includes canonical doc refresh, alpha preview version metadata alignment, and package rebuild evidence, so the contract must match the real changed paths and completion bar.
