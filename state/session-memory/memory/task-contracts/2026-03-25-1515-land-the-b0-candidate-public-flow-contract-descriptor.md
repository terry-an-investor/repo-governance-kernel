---
id: taskc-2026-03-25-1515-land-the-b0-candidate-public-flow-contract-descriptor
type: task-contract
title: "Land the b0 candidate public flow contract descriptor"
status: active
project_id: session-memory
workspace_id: ws-1490b759
workspace_root: C:/Users/terryzzb/Desktop/session-memory
branch: master
git_sha: dd9b5402cf97ad67dd55f5897652f77bd82396f1
paths:
  - kernel/public_flow_contracts.py
  - kernel/public_alpha_surface.py
  - scripts/smoke_repo_onboarding.py
  - scripts/smoke_assess_host_adoption.py
  - scripts/smoke_kernel_bootstrap.py
  - docs/canonical/PUBLIC_ALPHA_SURFACE.md
  - kernel/docs/PUBLIC_ALPHA_SURFACE.md
thread_ids: []
evidence_refs: []
tags:
  - task-contract
  - control-plane
confidence: high
created_at: 2026-03-25T15:15:28+08:00
updated_at: 2026-03-25T15:15:28+08:00
objective_id: obj-2026-03-23-0002
phase: execution
round_id: "round-2026-03-25-1514-start-b0-public-contract-freeze"
supersedes: []
superseded_by: []
---

## Summary

Move public flow field stability out of prose and scattered smoke assumptions into one repo-owned contract descriptor.

## Intent

Use one owner-layer catalog for stable public flow fields so docs, CLI descriptors, and smoke all freeze the same thing.

## Allowed Changes

- Add one machine-readable b0 candidate contract descriptor for stable public flow fields and blocked detail fields.
- Make describe-public-alpha-surface and smoke consume that shared descriptor.
- Update package-facing docs to explain the new owner-layer contract source.

## Forbidden Changes

- Do not widen the public command set or claim full beta compatibility yet.
- Do not add new workflow capability under the cover of contract freeze work.

## Completion Criteria

- One shared owner-layer descriptor names the stable field contract for the four current public flow entrypoints.
- Machine-readable public surface output and smoke assertions consume the same descriptor.
- Canonical/package-facing docs describe this as the b0 candidate contract and validation passes.

## Resolution

_none recorded_

## Active Risks

_none recorded_

## Status Notes

_none recorded_
