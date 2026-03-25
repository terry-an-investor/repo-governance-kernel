---
id: taskc-2026-03-24-1929-implement-owner-layer-host-adoption-assessment-for-shadow-mode
type: task-contract
title: "Implement owner-layer host adoption assessment for shadow mode"
status: completed
project_id: repo-governance-kernel
workspace_id: ws-1490b759
workspace_root: C:/Users/terryzzb/Desktop/session-memory
branch: master
git_sha: 1212345248b7910d6feb2bf2b4de3482b32bd7c6
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
updated_at: 2026-03-24T21:10:01+08:00
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

- Kernel-owned assess-host-adoption, draft-external-target-shadow-scope, assess-external-target-once, and assess-external-target-from-intent now define the bounded single-assessment surface.
- Canonical docs and preview package metadata were aligned and published as 0.1.0a1.
- Focused smoke, audit, enforcement, build, isolated install, and push all completed on the clean repo state.

## Active Risks

_none recorded_

## Status Notes

Task contract rewritten because The implementation task also added one host canonical doc update and one command-level smoke, so the task boundary must include those real paths.

Task contract rewritten because The task now includes canonical doc refresh, alpha preview version metadata alignment, and package rebuild evidence, so the contract must match the real changed paths and completion bar.

active -> completed: The owner-layer host adoption assessment, external-target bundle wrapper, bounded intent entry, and 0.1.0a1 release alignment all landed and validated on the committed clean state.

resolution recorded:
- Kernel-owned assess-host-adoption, draft-external-target-shadow-scope, assess-external-target-once, and assess-external-target-from-intent now define the bounded single-assessment surface.
- Canonical docs and preview package metadata were aligned and published as 0.1.0a1.
- Focused smoke, audit, enforcement, build, isolated install, and push all completed on the clean repo state.

