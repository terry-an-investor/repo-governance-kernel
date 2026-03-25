---
id: round-2026-03-25-1704-harden-public-evidence-layer-response-contracts-for-b1
type: round-contract
title: "Harden public evidence-layer response contracts for b1"
status: closed
project_id: session-memory
workspace_id: ws-1490b759
workspace_root: C:/Users/terryzzb/Desktop/session-memory
branch: master
git_sha: c18f66b4923034042037b9252c432b9797e59ad4
paths:
  - kernel/public_flow_contracts.py
  - kernel/public_surface.py
  - kernel/repo_onboarding.py
  - kernel/commands/assess_external_target_once.py
  - kernel/commands/onboard_repo_from_intent.py
  - kernel/commands/assess_external_target_from_intent.py
  - docs/canonical/PUBLIC_SURFACE.md
  - docs/canonical/IMPLEMENTATION_PLAN.md
  - kernel/README.md
  - README.md
  - scripts/smoke_repo_onboarding.py
  - scripts/smoke_assess_host_adoption.py
  - scripts/smoke_kernel_bootstrap.py
  - kernel/docs/PUBLIC_SURFACE.md
thread_ids: []
evidence_refs: []
tags:
  - round
  - control-plane
confidence: high
created_at: 2026-03-25T17:04:34+08:00
updated_at: 2026-03-25T17:15:50+08:00
objective_id: obj-2026-03-23-0002
phase: execution
supersedes: []
superseded_by: []
---

## Summary

One owner-layer public contract catalog and aligned docs/smokes that make the minimal stable evidence-layer response fields explicit for b1.

## Scope

- Define owner-layer stable nested subcontracts for the reusable execution/outcome/postconditions kernels that agent callers already consume across the public workflows.
- Keep the beta contract narrow: freeze only the smallest repeated response kernels, not whole evidence objects.

## Deliverable

One owner-layer public contract catalog and aligned docs/smokes that make the minimal stable evidence-layer response fields explicit for b1.

## Validation Plan

Run targeted public-flow smokes, public-surface inspection, docs audit, and repo audit/enforcement after the contract upgrade lands.
describe-public-surface plus targeted public workflow smokes and repo audit/enforcement
contract catalog, docs sync, targeted smokes, and repo audit/enforcement
targeted public workflow validation and repo-owned audit/enforcement all returned ok

## Active Risks

_none recorded_

## Blockers

_none recorded_

## Status Notes

_none recorded_

Round rewritten because the package-facing public-surface summary under kernel/docs is part of the same contract change and must stay inside the active b1 hardening boundary

Expanded b1 hardening scope to include the package-facing public surface summary so enforcement matches the actual doc sync work.

active -> validation_pending: the bounded b1 hardening slice is implemented and has passed its targeted public-surface, smoke, docs, audit, and enforcement validation path

validated by:
- describe-public-surface plus targeted public workflow smokes and repo audit/enforcement

validation_pending -> captured: the b1 evidence-layer hardening slice is durably recorded in the local worktree and validated before commit

validated by:
- contract catalog, docs sync, targeted smokes, and repo audit/enforcement

captured -> closed: the bounded b1 hardening slice is complete, so the round can close before the next beta-hardening slice opens

validated by:
- targeted public workflow validation and repo-owned audit/enforcement all returned ok
