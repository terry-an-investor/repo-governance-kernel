---
id: taskc-2026-03-25-1415-unify-a5-public-flow-success-and-blocked-payloads
type: task-contract
title: "Unify a5 public flow success and blocked payloads"
status: completed
project_id: session-memory
workspace_id: ws-1490b759
workspace_root: C:/Users/terryzzb/Desktop/session-memory
branch: master
git_sha: ed70c6e4ca73a2f6079c1312e3f82ba12b879ffb
paths:
  - kernel/commands/onboard_repo.py
  - kernel/commands/onboard_repo_from_intent.py
  - kernel/commands/assess_external_target_once.py
  - kernel/commands/assess_external_target_from_intent.py
  - kernel/repo_onboarding.py
  - kernel/host_adoption.py
  - scripts/smoke_repo_onboarding.py
  - scripts/smoke_assess_host_adoption.py
  - scripts/smoke_kernel_bootstrap.py
  - docs/canonical/PUBLIC_ALPHA_SURFACE.md
  - docs/canonical/IMPLEMENTATION_PLAN.md
  - docs/canonical/RELEASE.md
  - kernel/docs/PUBLIC_ALPHA_SURFACE.md
  - kernel/public_flow_contracts.py
thread_ids: []
evidence_refs: []
tags:
  - task-contract
  - control-plane
confidence: high
created_at: 2026-03-25T14:15:05+08:00
updated_at: 2026-03-25T14:34:38+08:00
objective_id: obj-2026-03-23-0002
phase: execution
round_id: "round-2026-03-25-1414-stabilize-public-flow-result-contracts-for-a5"
supersedes: []
superseded_by: []
---

## Summary

Land one shared result contract layer for the package-facing onboarding and external-target assessment flows.

## Intent

Replace ad hoc public workflow payloads with one stable direct-and-intent result envelope that surfaces blocked states explicitly for agents.

## Allowed Changes

- Add one shared public-flow result contract helper for success and blocked outcomes.
- Rewrite the four high-frequency public entrypoints to emit the same top-level categories and blocked semantics.
- Update smoke coverage and package-facing docs to depend on the shared contract instead of command-local payload quirks.

## Forbidden Changes

- Do not broaden a5 into new autonomous execution surfaces or monitoring features.
- Do not keep parallel ad hoc result schemas for the same public flow family.

## Completion Criteria

- The public onboarding and one-time external-target assessment flows share one stable result envelope, blocked states are explicit, and the updated smoke suite passes.

## Resolution

- direct and intent public entrypoints now emit a shared structured success or blocked result envelope
- onboarding and external assessment wrappers now reframe lower-layer payloads instead of returning ad hoc shapes

## Active Risks

_none recorded_

## Status Notes

Task contract rewritten because The a5 implementation extracted one shared public-flow contract owner layer that must be covered by the active task contract.

active -> completed: a5 public flow result contract work passed smoke validation and is captured in commit ed70c6e

resolution recorded:
- direct and intent public entrypoints now emit a shared structured success or blocked result envelope
- onboarding and external assessment wrappers now reframe lower-layer payloads instead of returning ad hoc shapes
