---
id: trans-2026-03-25-122100-open-task-contract-opened-task-contract-taskc-2026-03-25-1221-rename-stale-phase-1-acceptance-smoke-surface
type: transition-event
title: "Opened task contract taskc-2026-03-25-1221-rename-stale-phase-1-acceptance-smoke-surface"
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
  - open-task-contract
confidence: high
created_at: 2026-03-25T12:21:00+08:00
updated_at: 2026-03-25T12:21:00+08:00
supersedes: []
superseded_by: []
---

## Summary

Opened task contract taskc-2026-03-25-1221-rename-stale-phase-1-acceptance-smoke-surface

## Command

open-task-contract

## Previous State

round `round-2026-03-25-1116-start-explicit-package-config-layering-for-a4` already had 3 durable task-contract record(s)

## Next State

task contract `taskc-2026-03-25-1221-rename-stale-phase-1-acceptance-smoke-surface` is now active beneath round `round-2026-03-25-1116-start-explicit-package-config-layering-for-a4`

## Guards

- round `round-2026-03-25-1116-start-explicit-package-config-layering-for-a4` exists and remains open for task attachment
- task-contract objective linkage matches the referenced round
- task intent is explicit
- task scope paths are explicit
- task scope paths stay inside the round scope
- allowed changes, forbidden changes, and completion criteria are all present

## Side Effects

- wrote durable task contract `session-memory/memory/task-contracts/2026-03-25-1221-rename-stale-phase-1-acceptance-smoke-surface.md`

## Evidence

- Replace the stale smoke_phase1 name with a clearer repo-acceptance smoke entrypoint and update repo-owned triggers and docs so the validation surface says what it actually is.
- The top-level repo acceptance smoke has one new canonical path and repo-owned triggers no longer reference smoke_phase1.py.
- The renamed acceptance smoke passes under Python 3.11 and through the normal repo validation path.
- Canonical docs and repo-facing quickstart text stop describing the top-level acceptance smoke as phase-1.
