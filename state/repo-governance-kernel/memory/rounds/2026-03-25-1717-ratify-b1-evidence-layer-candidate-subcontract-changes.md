---
id: round-2026-03-25-1717-ratify-b1-evidence-layer-candidate-subcontract-changes
type: round-contract
title: "Ratify b1 evidence-layer candidate subcontract changes"
status: closed
project_id: repo-governance-kernel
workspace_id: ws-1490b759
workspace_root: C:/Users/terryzzb/Desktop/session-memory
branch: master
git_sha: a47358d96bde31269421b6cc5815b713daba7e8f
paths:
  - kernel/public_flow_contracts.py
  - kernel/public_surface.py
  - docs/canonical/PUBLIC_SURFACE.md
  - docs/canonical/IMPLEMENTATION_PLAN.md
  - kernel/docs/PUBLIC_SURFACE.md
  - kernel/README.md
  - README.md
  - scripts/smoke_repo_onboarding.py
  - scripts/smoke_assess_host_adoption.py
  - scripts/smoke_kernel_bootstrap.py
thread_ids: []
evidence_refs: []
tags:
  - round
  - control-plane
confidence: high
created_at: 2026-03-25T17:17:37+08:00
updated_at: 2026-03-25T17:22:39+08:00
objective_id: obj-2026-03-23-0002
phase: execution
supersedes: []
superseded_by: []
---

## Summary

One git commit that lands the validated b1 candidate subcontract changes.

## Scope

- Land the already validated b1 candidate subcontract implementation and doc alignment into git.
- Do not widen the implementation scope beyond the validated files already changed.

## Deliverable

One git commit that lands the validated b1 candidate subcontract changes.

## Validation Plan

Require repo audit and enforcement to return ok before and after the ratification commit.
git commit a47358d plus prior targeted validation
git commit a47358d
git commit a47358d

## Active Risks

_none recorded_

## Blockers

_none recorded_

## Status Notes

active -> validation_pending: the ratification commit is landed, so the short ratification round can enter validation-pending close-out

validated by:
- git commit a47358d plus prior targeted validation

validation_pending -> captured: the ratification round is now durably recorded in git commit a47358d

validated by:
- git commit a47358d

captured -> closed: the ratification round is complete now that commit a47358d durably carries the validated b1 candidate subcontract changes

validated by:
- git commit a47358d

