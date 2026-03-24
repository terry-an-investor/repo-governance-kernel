---
id: round-2026-03-24-0907-lift-rewrite-open-round-field-semantics-into-registry-owned-owner-layer-contracts
type: round-contract
title: "Lift rewrite-open-round field semantics into registry-owned owner-layer contracts"
status: active
project_id: session-memory
workspace_id: ws-1490b759
workspace_root: C:/Users/terryzzb/Desktop/session-memory
branch: master
git_sha: 06d9df9240bb711603afec0ab2952081167c0027
paths:
  - scripts/transition_specs.py
  - scripts/rewrite_open_round.py
  - scripts/execute_adjudication_followups.py
  - scripts/smoke_adjudication_followups.py
  - scripts/audit_control_state.py
  - CONTROL_SYSTEM.md
  - TRANSITION_COMMANDS.md
  - projects/session-memory/current/current-task.md
thread_ids: []
evidence_refs: []
tags:
  - round
  - control-plane
confidence: high
created_at: 2026-03-24T09:07:16+08:00
updated_at: 2026-03-24T09:07:16+08:00
objective_id: obj-2026-03-23-0002
phase: execution
supersedes: []
superseded_by: []
---

## Summary

Registry-owned rewrite field semantics govern rewrite-open-round mutation surface and adjudication executor payloads.

## Scope

- Lift rewrite-open-round mutable field declarations into the transition registry instead of leaving field semantics private to rewrite_open_round.py and executor plumbing.
- Make adjudication rewrite payload execution consume the same registry-owned field semantics and reject undeclared private rewrite keys.
- Update canonical docs and current-task so the registry contract truthfully includes rewrite field semantics for the bounded round primitive.

## Deliverable

Registry-owned rewrite field semantics govern rewrite-open-round mutation surface and adjudication executor payloads.

## Validation Plan

Run targeted py_compile, registry export, adjudication follow-up smoke, control audit, and worktree enforcement after the rewrite field semantics land.

## Active Risks

_none recorded_

## Blockers

_none recorded_

## Status Notes

_none recorded_
