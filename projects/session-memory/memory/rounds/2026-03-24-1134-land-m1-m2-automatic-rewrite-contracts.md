---
id: round-2026-03-24-1134-land-m1-m2-automatic-rewrite-contracts
type: round-contract
title: "Land M1/M2 automatic rewrite contracts"
status: active
project_id: session-memory
workspace_id: ws-1490b759
workspace_root: C:/Users/terryzzb/Desktop/session-memory
branch: master
git_sha: 1713efaef14237b3d55919655eb89de1b4bec896
paths:
  - scripts/transition_specs.py
  - scripts/compile_adjudication_executor_plan.py
  - scripts/execute_adjudication_followups.py
  - scripts/smoke_adjudication_followups.py
  - TRANSITION_COMMANDS.md
  - CONTROL_SYSTEM.md
  - STATE_MACHINE.md
  - IMPLEMENTATION_PLAN.md
thread_ids: []
evidence_refs: []
tags:
  - round
  - control-plane
confidence: high
created_at: 2026-03-24T11:34:35+08:00
updated_at: 2026-03-24T11:34:35+08:00
objective_id: obj-2026-03-23-0002
phase: execution
supersedes: []
superseded_by: []
---

## Summary

M1 bundle payload semantics and M2 adjudication plan-family expansion land with smoke coverage and honest docs.

## Scope

- Lift governed bundle payload semantics into the transition registry so bundle execution stops carrying private payload keys.
- Broaden adjudication plan contracts to cover task-contract and round target resolution through the existing owner-layer pattern.

## Deliverable

M1 bundle payload semantics and M2 adjudication plan-family expansion land with smoke coverage and honest docs.

## Validation Plan

Registry audit, worktree enforcement, targeted py_compile, and adjudication followup smoke pass on the changed path.

## Active Risks

- Expanding executor support too broadly could reintroduce private semantics instead of reducing them.

## Blockers

_none recorded_

## Status Notes

_none recorded_
