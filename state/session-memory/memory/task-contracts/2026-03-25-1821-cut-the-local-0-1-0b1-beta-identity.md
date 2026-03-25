---
id: taskc-2026-03-25-1821-cut-the-local-0-1-0b1-beta-identity
type: task-contract
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
  - task-contract
  - control-plane
confidence: high
created_at: 2026-03-25T18:21:53+08:00
updated_at: 2026-03-25T18:32:25+08:00
objective_id: obj-2026-03-23-0002
phase: execution
round_id: "round-2026-03-25-1821-cut-the-local-0-1-0b1-beta-identity"
supersedes: []
superseded_by: []
---

## Summary

Align package version truth, stable public contract truth, and release evidence around the local 0.1.0b1 beta cut.

## Intent

Turn the selected b1 contract from source-line next-stable semantics into released stable package identity and de-version the remaining forward-looking candidate layer.

## Allowed Changes

- Promote execution and postconditions into the released stable contract, align version truth to 0.1.0b1, and rename the remaining forward-looking candidate layer so it no longer pretends to target a past release.

## Forbidden Changes

- Do not widen automation authority and do not freeze deeper evidence projections such as compiled_bundle, created_control_state, or assessment outcome beyond the minimum honest stable contract.

## Completion Criteria

- The local source tree builds 0.1.0b1 artifacts, public-surface truth is coherent, and release validations pass with control state returned to clean paused truth after close-out.

## Resolution

_none recorded_

## Active Risks

_none recorded_

## Status Notes

Task contract rewritten because Capture the full b1 identity release slice in the active task contract.
