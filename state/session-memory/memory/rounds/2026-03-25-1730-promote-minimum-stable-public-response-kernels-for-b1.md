---
id: round-2026-03-25-1730-promote-minimum-stable-public-response-kernels-for-b1
type: round-contract
title: "Promote minimum stable public response kernels for b1"
status: active
project_id: session-memory
workspace_id: ws-1490b759
workspace_root: C:/Users/terryzzb/Desktop/session-memory
branch: master
git_sha: 204802ce4f1822967cb5a957116471141e697a89
paths:
  - kernel/public_flow_contracts.py
  - kernel/public_surface.py
  - scripts/smoke_repo_onboarding.py
  - scripts/smoke_assess_host_adoption.py
  - scripts/smoke_kernel_bootstrap.py
  - docs/canonical/PUBLIC_SURFACE.md
  - docs/canonical/IMPLEMENTATION_PLAN.md
  - kernel/docs/PUBLIC_SURFACE.md
  - docs/canonical/RELEASE.md
  - README.md
  - kernel/README.md
thread_ids: []
evidence_refs: []
tags:
  - round
  - control-plane
confidence: high
created_at: 2026-03-25T17:30:52+08:00
updated_at: 2026-03-25T17:40:53+08:00
objective_id: obj-2026-03-23-0002
phase: execution
supersedes: []
superseded_by: []
---

## Summary

Stable public contract promotion for the minimum repeated b1-ready kernels.

## Scope

- Promote repeated public response kernels that are already stable across direct and intent surfaces.

## Deliverable

Stable public contract promotion for the minimum repeated b1-ready kernels.

## Validation Plan

Run public-surface descriptor and smoke validations for onboarding and assessment flows.

## Active Risks

_none recorded_

## Blockers

_none recorded_

## Status Notes

_none recorded_

Round rewritten because Add canonical release guidance to the same bounded b1 contract-promotion slice so public docs stay mutually consistent.

Round rewritten because Bring the package entry docs into the same bounded b1 contract-promotion slice so the first user-facing docs do not drift from canonical truth.
