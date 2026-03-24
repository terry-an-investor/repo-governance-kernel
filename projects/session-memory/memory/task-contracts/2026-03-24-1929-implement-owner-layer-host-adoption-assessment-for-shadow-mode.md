---
id: taskc-2026-03-24-1929-implement-owner-layer-host-adoption-assessment-for-shadow-mode
type: task-contract
title: "Implement owner-layer host adoption assessment for shadow mode"
status: active
project_id: session-memory
workspace_id: ws-1490b759
workspace_root: C:/Users/terryzzb/Desktop/session-memory
branch: master
git_sha: 0493b1658e01acd42738d3d22ca9bf5ce93fc6f3
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
thread_ids: []
evidence_refs: []
tags:
  - task-contract
  - control-plane
confidence: high
created_at: 2026-03-24T19:29:00+08:00
updated_at: 2026-03-24T19:39:19+08:00
objective_id: obj-2026-03-23-0002
phase: execution
round_id: "round-2026-03-24-1928-land-live-host-shadow-assessment-and-adoption-report-owner-layer"
supersedes: []
superseded_by: []
---

## Summary

Replace duplicated snapshot smoke reporting logic with one kernel-owned host adoption assessment surface that supports live-host shadow assessment without claiming direct host mutation.

## Intent

Replace duplicated snapshot smoke reporting logic with one kernel-owned host adoption assessment surface that supports live-host shadow assessment without claiming direct host mutation.

## Allowed Changes

- Add a reusable kernel helper and CLI command for host adoption assessment and report generation.
- Repoint existing frozen-host smokes at the owner-layer assessment surface instead of duplicating reporting logic.
- Update package-facing and release docs to describe the new shadow assessment surface and its support boundary.

## Forbidden Changes

- Do not claim general live-host automatic rewrite or stable beta compatibility.
- Do not mutate external source repositories during validation.

## Completion Criteria

- A kernel-owned host adoption assessment command writes a readable report for a governed host repo.
- Existing frozen-host adoption evidence runs through the shared owner-layer surface instead of local report-copy logic.
- Repo audit and worktree enforcement remain honest after the change.

## Resolution

_none recorded_

## Active Risks

_none recorded_

## Status Notes

Task contract rewritten because The implementation task also added one host canonical doc update and one command-level smoke, so the task boundary must include those real paths.
