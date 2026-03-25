---
id: taskc-2026-03-25-1553-land-b0-public-flow-subcontract-catalog
type: task-contract
title: "Land b0 public flow subcontract catalog"
status: active
project_id: session-memory
workspace_id: ws-1490b759
workspace_root: C:/Users/terryzzb/Desktop/session-memory
branch: master
git_sha: 96e1f2dd79c134ccff6516cba4a98c6ba7725adb
paths:
  - kernel/public_flow_contracts.py
  - kernel/public_alpha_surface.py
  - docs/canonical/PUBLIC_ALPHA_SURFACE.md
  - kernel/docs/PUBLIC_ALPHA_SURFACE.md
  - scripts/smoke_repo_onboarding.py
  - scripts/smoke_assess_host_adoption.py
  - scripts/smoke_kernel_bootstrap.py
thread_ids: []
evidence_refs: []
tags:
  - task-contract
  - control-plane
confidence: high
created_at: 2026-03-25T15:53:30+08:00
updated_at: 2026-03-25T16:00:46+08:00
objective_id: obj-2026-03-23-0002
phase: execution
round_id: "round-2026-03-25-1553-freeze-b0-public-flow-subcontracts"
supersedes: []
superseded_by: []
---

## Summary

Codify stable nested field contracts for flow_contract and intent_compilation across the four public flow entrypoints.

## Intent

Move public nested contract truth into one owner-layer descriptor so callers can rely on subobject fields without reading implementation code.

## Allowed Changes

- Add one owner-layer subcontract catalog for stable nested public flow fields.
- Export the new subcontract catalog through the public alpha descriptor and document its current b0-candidate scope.
- Tighten smoke assertions around stable nested public fields without widening the public command surface.

## Forbidden Changes

- Do not widen the public command set or add new workflow capabilities.
- Do not freeze execution, outcome, or postconditions nested shapes in this slice.

## Completion Criteria

- describe-public-alpha-surface exports one machine-readable subcontract catalog for flow_contract and intent_compilation.
- Public flow smokes assert the stable nested fields from the owner-layer contract instead of ad hoc field checks.

## Resolution

_none recorded_

## Active Risks

_none recorded_

## Status Notes

Task contract rewritten because The task also updated the installed-package bootstrap smoke to assert the exported subcontract catalog, so the task path boundary must cover that file.
