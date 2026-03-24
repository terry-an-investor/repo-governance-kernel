---
id: round-2026-03-24-1928-land-live-host-shadow-assessment-and-adoption-report-owner-layer
type: round-contract
title: "Land live-host shadow assessment and adoption report owner layer"
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
  - round
  - control-plane
confidence: high
created_at: 2026-03-24T19:28:36+08:00
updated_at: 2026-03-24T19:38:43+08:00
objective_id: obj-2026-03-23-0002
phase: execution
supersedes: []
superseded_by: []
---

## Summary

A kernel command and helper surface that can assess a host adoption state and write a readable shadow-adoption report.

## Scope

- Promote host adoption assessment and report generation into the kernel owner layer.
- Keep live-host rollout in shadow mode by producing honest assessment output before any broader automation claim.

## Deliverable

A kernel command and helper surface that can assess a host adoption state and write a readable shadow-adoption report.

## Validation Plan

Run focused host-adoption smokes plus audit-control-state and enforce-worktree on the repo after the owner-layer command lands.

## Active Risks

- The first command surface could stay too frozen-host-specific and fail to generalize to live-host shadow assessment.

## Blockers

_none recorded_

## Status Notes

_none recorded_

Round rewritten because The stage-1 implementation also touched the host canonical command doc and the new command-level smoke, so the round scope must cover the real changed paths honestly.
