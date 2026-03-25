---
id: taskc-2026-03-25-1731-promote-minimum-stable-b1-public-subcontracts
type: task-contract
title: "Promote minimum stable b1 public subcontracts"
status: completed
project_id: repo-governance-kernel
workspace_id: ws-1490b759
workspace_root: C:/Users/terryzzb/Desktop/session-memory
branch: master
git_sha: e128136188eb75da4d18423c060e06247443667a
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
  - task-contract
  - control-plane
confidence: high
created_at: 2026-03-25T17:31:20+08:00
updated_at: 2026-03-25T17:44:32+08:00
objective_id: obj-2026-03-23-0002
phase: execution
round_id: "round-2026-03-25-1730-promote-minimum-stable-public-response-kernels-for-b1"
supersedes: []
superseded_by: []
---

## Summary

Promote the minimum repeated response kernels from b1-target into the stable public beta contract without widening authority.

## Intent

Move only the repeatedly observed execution and postcondition kernels into the stable public contract across onboarding and one-time external assessment flows.

## Allowed Changes

- Update stable subcontract catalogs, surface descriptors, smokes, and docs so execution and postconditions are stable across direct and intent entrypoints.
- Keep docs/canonical/RELEASE.md aligned with the current next-stable versus remaining candidate public contract split.
- Update README.md and kernel/README.md to reflect the released b0 stable contract, the source-line b1 next-stable layer, and the remaining b1-target candidates.

## Forbidden Changes

- Do not widen automation authority or freeze deeper evidence projections such as compiled_bundle, created_control_state, or assessment draft payloads.

## Completion Criteria

- describe-public-surface and the targeted public smokes prove the promoted stable contract and docs match the owner-layer truth.

## Resolution

- Promoted execution and postconditions into the source-line b1 next-stable subcontract layer without changing the released b0 contract.
- Kept deeper evidence projections explicit as remaining b1-target candidates and aligned canonical/package docs plus smokes to the new three-layer contract split.

## Active Risks

_none recorded_

## Status Notes

Task contract rewritten because Add canonical release guidance to the same bounded b1 contract-promotion slice so the task scope still covers every canonical public contract doc touched in this round.

Task contract rewritten because Bring the package entry docs into the same bounded b1 contract-promotion slice so the first user-facing docs do not drift from canonical truth.

active -> completed: The bounded b1 public contract promotion slice is implemented and validated.

resolution recorded:
- Promoted execution and postconditions into the source-line b1 next-stable subcontract layer without changing the released b0 contract.
- Kept deeper evidence projections explicit as remaining b1-target candidates and aligned canonical/package docs plus smokes to the new three-layer contract split.

