---
id: taskc-2026-03-25-0843-land-task-contract-hard-execution-gate
type: task-contract
title: "Land task-contract hard execution gate"
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
  - task-contract
  - control-plane
confidence: high
created_at: 2026-03-25T08:43:50+08:00
updated_at: 2026-03-25T08:43:50+08:00
objective_id: obj-2026-03-23-0002
phase: execution
round_id: "round-2026-03-25-0843-make-task-contract-a-real-hard-execution-gate"
supersedes: []
superseded_by: []
---

## Summary

Make unresolved active task contracts block dishonest promotion and objective-line transitions through one shared owner-layer gate.

## Intent

Replace duplicated per-command open-task checks with one reusable blocker primitive, wire promotion and closure commands through it, and prove the blocked and allowed paths with a focused smoke.

## Allowed Changes

- Add one reusable owner-layer task-contract blocking helper and make promotion or closure commands consume it instead of open-coding the same checks.
- Tighten transition commands and docs so unresolved active task contracts become an explicit hard gate for dishonest promotion, closure, and objective-line replacement.
- Add one focused validation path that proves the gate blocks before task resolution and permits the honest transition after resolution.

## Forbidden Changes

- Do not broaden into continuous monitoring, background orchestration, or free-form autonomous rewrite.
- Do not introduce a second private policy implementation outside the shared owner-layer gate.

## Completion Criteria

- A shared owner-layer task-contract blocker primitive exists and the affected transition commands consume it.
- At least one focused smoke proves a dishonest promotion or closure attempt is blocked until the attached task contract is resolved.
- audit-control-state, enforce-worktree, and smoke_phase1 remain clean after the gate lands.

## Resolution

_none recorded_

## Active Risks

- If the gate only checks round closure but not objective-line replacement, the system will still allow stranded execution authority through another transition surface.

## Status Notes

_none recorded_
