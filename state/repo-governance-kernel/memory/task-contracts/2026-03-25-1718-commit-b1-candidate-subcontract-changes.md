---
id: taskc-2026-03-25-1718-commit-b1-candidate-subcontract-changes
type: task-contract
title: "Commit b1 candidate subcontract changes"
status: completed
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
  - task-contract
  - control-plane
confidence: high
created_at: 2026-03-25T17:18:27+08:00
updated_at: 2026-03-25T17:21:14+08:00
objective_id: obj-2026-03-23-0002
phase: execution
round_id: "round-2026-03-25-1717-ratify-b1-evidence-layer-candidate-subcontract-changes"
supersedes: []
superseded_by: []
---

## Summary

Land the already validated b1 candidate subcontract code and doc changes into git without altering product scope.

## Intent

Land the already validated b1 candidate subcontract code and doc changes into git without altering product scope.

## Allowed Changes

- Commit the already validated b1 candidate subcontract implementation, doc alignment, and smoke assertions.
- Refresh control anchors and ratification control state needed to land that commit honestly.

## Forbidden Changes

- Do not introduce new product behavior beyond the already validated candidate subcontract slice.
- Do not reopen the released b0 stable promise or widen authority.

## Completion Criteria

- The validated b1 candidate subcontract changes are durably committed into git.

## Resolution

- git commit a47358d lands the owner-layer candidate subcontract catalog, doc alignment, smoke assertions, and the earlier bounded implementation-round history

## Active Risks

_none recorded_

## Status Notes

active -> completed: the validated b1 candidate subcontract changes are now durably committed in git commit a47358d

resolution recorded:
- git commit a47358d lands the owner-layer candidate subcontract catalog, doc alignment, smoke assertions, and the earlier bounded implementation-round history

Completed after the ratification commit landed.

