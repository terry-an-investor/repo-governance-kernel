---
id: round-2026-03-25-0843-make-task-contract-a-real-hard-execution-gate
type: round-contract
title: "Make task-contract a real hard execution gate"
status: active
project_id: session-memory
workspace_id: ws-1490b759
workspace_root: C:/Users/terryzzb/Desktop/session-memory
branch: master
git_sha: f09a1bc6652290b312ea43a06e38410030bb9e1b
paths:
  - kernel
  - scripts
  - docs
  - README.md
thread_ids: []
evidence_refs: []
tags:
  - round
  - control-plane
confidence: high
created_at: 2026-03-25T08:43:50+08:00
updated_at: 2026-03-25T08:43:50+08:00
objective_id: obj-2026-03-23-0002
phase: execution
supersedes: []
superseded_by: []
---

## Summary

One reusable task-contract hard-gate primitive, promotion and closure commands that consume it consistently, and one proof path showing dishonest transitions block until the task contract is resolved.

## Scope

- Extract one owner-layer task-contract blocker primitive so round promotion, closure, and objective-line replacement stop hand-rolling the same open-contract checks.
- Converge promotion and closure commands on the same hard gate: worktree enforcement plus unresolved task-contract blocking semantics.
- Add one small validation path that proves the new hard gate blocks dishonest promotion and allows the honest path after task resolution.

## Deliverable

One reusable task-contract hard-gate primitive, promotion and closure commands that consume it consistently, and one proof path showing dishonest transitions block until the task contract is resolved.

## Validation Plan

Run audit-control-state, enforce-worktree, smoke_phase1, and one focused hard-gate smoke after the new task-contract gate lands.

## Active Risks

- Promotion and closure semantics may still drift if the new gate only lands in one command family instead of the shared owner layer.

## Blockers

_none recorded_

## Status Notes

_none recorded_
