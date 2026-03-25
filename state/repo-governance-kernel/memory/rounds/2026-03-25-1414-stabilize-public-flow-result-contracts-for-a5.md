---
id: round-2026-03-25-1414-stabilize-public-flow-result-contracts-for-a5
type: round-contract
title: "Stabilize public flow result contracts for a5"
status: closed
project_id: repo-governance-kernel
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
  - round
  - control-plane
confidence: high
created_at: 2026-03-25T14:14:53+08:00
updated_at: 2026-03-25T14:35:23+08:00
objective_id: obj-2026-03-23-0002
phase: execution
supersedes: []
superseded_by: []
---

## Summary

One shared public-flow contract for onboarding and one-time external-target assessment, with stable success and blocked payloads proven by smoke.

## Scope

- Add one shared public-flow result contract layer for the highest-frequency package entrypoints.
- Rewrite onboarding and external-target assessment direct and intent wrappers to emit the same success and blocked categories.
- Update smoke coverage and package-facing docs to treat the shared result contract as the a5 product surface.

## Deliverable

One shared public-flow contract for onboarding and one-time external-target assessment, with stable success and blocked payloads proven by smoke.

## Validation Plan

Run smoke_repo_onboarding, smoke_assess_host_adoption, smoke_kernel_bootstrap, and smoke_repo_acceptance after the contract rewrite.
py_compile
scripts/smoke_repo_onboarding.py
scripts/smoke_assess_host_adoption.py
scripts/smoke_kernel_bootstrap.py
commit ed70c6e
audit-control-state
enforce-worktree
commit ed70c6e

## Active Risks

_none recorded_

## Blockers

_none recorded_

## Status Notes

_none recorded_

Round rewritten because The a5 implementation extracted one shared public-flow contract owner layer that must be governed inside the same round scope.

active -> validation_pending: a5 public flow result contracts landed and local smoke validation completed

validated by:
- py_compile
- scripts/smoke_repo_onboarding.py
- scripts/smoke_assess_host_adoption.py
- scripts/smoke_kernel_bootstrap.py

validation_pending -> captured: a5 public flow result contract behavior is now durably recorded and validated

validated by:
- commit ed70c6e
- audit-control-state
- enforce-worktree

captured -> closed: a5 public flow result contract round is complete and no open implementation work remains in this boundary

validated by:
- commit ed70c6e

