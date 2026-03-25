---
id: trans-2026-03-25-122909-update-task-contract-status-updated-task-contract-taskc-2026-03-25-1221-rename-stale-phase-1-acceptance-smoke-surface-to-completed
type: transition-event
title: "Updated task contract taskc-2026-03-25-1221-rename-stale-phase-1-acceptance-smoke-surface to completed"
status: recorded
project_id: session-memory
workspace_id: ws-1490b759
workspace_root: C:/Users/terryzzb/Desktop/session-memory
branch: master
git_sha: bb118b9346eae2b83714ffc5dd6d388aaebbd9b9
paths:
  - taskc-2026-03-25-1221-rename-stale-phase-1-acceptance-smoke-surface
  - round-2026-03-25-1116-start-explicit-package-config-layering-for-a4
  - obj-2026-03-23-0002
thread_ids: []
evidence_refs: []
tags:
  - transition-event
  - update-task-contract-status
confidence: high
created_at: 2026-03-25T12:29:09+08:00
updated_at: 2026-03-25T12:29:09+08:00
supersedes: []
superseded_by: []
---

## Summary

Updated task contract taskc-2026-03-25-1221-rename-stale-phase-1-acceptance-smoke-surface to completed

## Command

update-task-contract-status

## Previous State

task contract `taskc-2026-03-25-1221-rename-stale-phase-1-acceptance-smoke-surface` status `active`

## Next State

task contract `taskc-2026-03-25-1221-rename-stale-phase-1-acceptance-smoke-surface` is now `completed`

## Guards

- task contract `taskc-2026-03-25-1221-rename-stale-phase-1-acceptance-smoke-surface` exists
- task-contract transition `active -> completed` is legal
- completed task-contract transitions include at least one resolution record

## Side Effects

- updated durable task contract `session-memory/memory/task-contracts/2026-03-25-1221-rename-stale-phase-1-acceptance-smoke-surface.md`

## Evidence

- Renamed the stale phase-1 smoke surface to repo acceptance smoke, updated live references, and revalidated the renamed acceptance path under Python 3.11.
- Renamed scripts/smoke_phase1.py to scripts/smoke_repo_acceptance.py and updated the repo smoke alias.
- Updated CI, pre-push, README, harness docs, and release docs to call the acceptance surface repo acceptance smoke.
- Validated the renamed script and scripts/session_memory.py smoke under Python 3.11, then reran audit-control-state and enforce-worktree.
