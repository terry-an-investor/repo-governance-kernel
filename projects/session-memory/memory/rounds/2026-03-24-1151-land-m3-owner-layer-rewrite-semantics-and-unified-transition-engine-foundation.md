---
id: round-2026-03-24-1151-land-m3-owner-layer-rewrite-semantics-and-unified-transition-engine-foundation
type: round-contract
title: "Land M3 owner-layer rewrite semantics and unified transition engine foundation"
status: active
project_id: session-memory
workspace_id: ws-1490b759
workspace_root: C:/Users/terryzzb/Desktop/session-memory
branch: master
git_sha: 4190e0ded88287978773a1b6cfee605b15760691
paths:
  - scripts/
  - projects/session-memory/control/
  - projects/session-memory/current/
  - projects/session-memory/memory/
  - CONTROL_SYSTEM.md
  - IMPLEMENTATION_PLAN.md
  - STATE_MACHINE.md
  - TRANSITION_COMMANDS.md
thread_ids: []
evidence_refs: []
tags:
  - round
  - control-plane
confidence: high
created_at: 2026-03-24T11:51:07+08:00
updated_at: 2026-03-24T11:51:07+08:00
objective_id: obj-2026-03-23-0002
phase: execution
supersedes: []
superseded_by: []
---

## Summary

A new M3 slice that broadens rewrite semantics honestly and lands the first unified transition-engine foundation.

## Scope

- Extend registry-owned adjudication rewrite semantics beyond the current bounded round/task/exception slice without inventing new private executor branches.
- Extract shared execution-building primitives so owner-layer commands stop accumulating one-off if/else dispatch paths.

## Deliverable

A new M3 slice that broadens rewrite semantics honestly and lands the first unified transition-engine foundation.

## Validation Plan

Targeted py_compile, audit-control-state, enforce-worktree, and focused smoke coverage pass on the M3 path.

## Active Risks

- Expanding rewrite semantics too fast could reintroduce private owner-layer behavior under a cleaner name.
- A premature unified engine abstraction could hide domain differences instead of making them explicit.

## Blockers

_none recorded_

## Status Notes

_none recorded_
