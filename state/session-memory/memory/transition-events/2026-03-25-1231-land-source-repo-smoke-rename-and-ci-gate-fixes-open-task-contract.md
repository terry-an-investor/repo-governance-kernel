---
id: trans-2026-03-25-123157-open-task-contract-opened-task-contract-taskc-2026-03-25-1231-land-source-repo-smoke-rename-and-ci-gate-fixes
type: transition-event
title: "Opened task contract taskc-2026-03-25-1231-land-source-repo-smoke-rename-and-ci-gate-fixes"
status: recorded
project_id: session-memory
workspace_id: ws-1490b759
workspace_root: C:/Users/terryzzb/Desktop/session-memory
branch: master
git_sha: bb118b9346eae2b83714ffc5dd6d388aaebbd9b9
paths:
  - taskc-2026-03-25-1231-land-source-repo-smoke-rename-and-ci-gate-fixes
  - round-2026-03-25-1116-start-explicit-package-config-layering-for-a4
  - obj-2026-03-23-0002
thread_ids: []
evidence_refs: []
tags:
  - transition-event
  - open-task-contract
confidence: high
created_at: 2026-03-25T12:31:57+08:00
updated_at: 2026-03-25T12:31:57+08:00
supersedes: []
superseded_by: []
---

## Summary

Opened task contract taskc-2026-03-25-1231-land-source-repo-smoke-rename-and-ci-gate-fixes

## Command

open-task-contract

## Previous State

round `round-2026-03-25-1116-start-explicit-package-config-layering-for-a4` already had 4 durable task-contract record(s)

## Next State

task contract `taskc-2026-03-25-1231-land-source-repo-smoke-rename-and-ci-gate-fixes` is now active beneath round `round-2026-03-25-1116-start-explicit-package-config-layering-for-a4`

## Guards

- round `round-2026-03-25-1116-start-explicit-package-config-layering-for-a4` exists and remains open for task attachment
- task-contract objective linkage matches the referenced round
- task intent is explicit
- task scope paths are explicit
- task scope paths stay inside the round scope
- allowed changes, forbidden changes, and completion criteria are all present

## Side Effects

- wrote durable task contract `session-memory/memory/task-contracts/2026-03-25-1231-land-source-repo-smoke-rename-and-ci-gate-fixes.md`

## Evidence

- Carry the renamed repo acceptance smoke surface and Python 3.11 source-repo smoke fix through commit without leaving CI or local hook paths outside active task coverage.
- The renamed repo acceptance smoke passes under Python 3.11 through both direct script and scripts/session_memory.py smoke entrypoints.
- audit-control-state and enforce-worktree return ok on the source repository with the landing task active.
- The resulting change set can be committed without task-coverage enforcement blocking .githooks or .github paths.
