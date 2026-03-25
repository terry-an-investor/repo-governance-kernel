---
id: round-2026-03-25-1821-cut-the-local-0-1-0b1-beta-identity
type: round-contract
title: "Cut the local 0.1.0b1 beta identity"
status: active
project_id: session-memory
workspace_id: ws-1490b759
workspace_root: C:/Users/terryzzb/Desktop/session-memory
branch: master
git_sha: b4b3bca630cb1c0a19098b00529ac238e24927de
paths:
  - pyproject.toml
  - uv.lock
  - kernel/public_flow_contracts.py
  - kernel/public_surface.py
  - README.md
  - docs/README.md
  - kernel/README.md
  - docs/canonical/PUBLIC_SURFACE.md
  - docs/canonical/RELEASE.md
  - docs/canonical/IMPLEMENTATION_PLAN.md
  - docs/canonical/TRANSITION_COMMANDS.md
  - kernel/docs/PUBLIC_SURFACE.md
  - kernel/docs/TRANSITION_COMMANDS.md
  - scripts/smoke_kernel_bootstrap.py
  - scripts/smoke_repo_onboarding.py
  - scripts/smoke_assess_host_adoption.py
thread_ids: []
evidence_refs: []
tags:
  - round
  - control-plane
confidence: high
created_at: 2026-03-25T18:21:36+08:00
updated_at: 2026-03-25T18:32:14+08:00
objective_id: obj-2026-03-23-0002
phase: execution
supersedes: []
superseded_by: []
---

## Summary

A coherent local 0.1.0b1 package identity across code, docs, and release evidence.

## Scope

- Promote the selected b1 contract into the released package identity without widening authority.

## Deliverable

A coherent local 0.1.0b1 package identity across code, docs, and release evidence.

## Validation Plan

Run the public-surface describe command, docs audit, bootstrap/onboarding/adoption/task-contract/acceptance smokes, uv build, and control-state enforcement for the local 0.1.0b1 release cut.

## Active Risks

_none recorded_

## Blockers

_none recorded_

## Status Notes

_none recorded_

Round rewritten because Capture the full b1 identity release slice in the active round scope.
