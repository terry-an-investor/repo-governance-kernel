---
id: trans-2026-03-25-133223-open-task-contract-opened-task-contract-taskc-2026-03-25-1332-correct-a4-public-surface-versioning-and-cut-tag
type: transition-event
title: "Opened task contract taskc-2026-03-25-1332-correct-a4-public-surface-versioning-and-cut-tag"
status: recorded
project_id: repo-governance-kernel
workspace_id: ws-1490b759
workspace_root: C:/Users/terryzzb/Desktop/session-memory
branch: master
git_sha: 275379b93571a3181418ef2d7a1c4c9fe9c5e5b8
paths:
  - taskc-2026-03-25-1332-correct-a4-public-surface-versioning-and-cut-tag
  - round-2026-03-25-1332-correct-a4-release-semantics-and-cut-real-tag
  - obj-2026-03-23-0002
thread_ids: []
evidence_refs: []
tags:
  - transition-event
  - open-task-contract
confidence: high
created_at: 2026-03-25T13:32:23+08:00
updated_at: 2026-03-25T13:32:23+08:00
supersedes: []
superseded_by: []
---

## Summary

Opened task contract taskc-2026-03-25-1332-correct-a4-public-surface-versioning-and-cut-tag

## Command

open-task-contract

## Previous State

round `round-2026-03-25-1332-correct-a4-release-semantics-and-cut-real-tag` had no durable task-contract records

## Next State

task contract `taskc-2026-03-25-1332-correct-a4-public-surface-versioning-and-cut-tag` is now active beneath round `round-2026-03-25-1332-correct-a4-release-semantics-and-cut-real-tag`

## Guards

- round `round-2026-03-25-1332-correct-a4-release-semantics-and-cut-real-tag` exists and remains open for task attachment
- task-contract objective linkage matches the referenced round
- task intent is explicit
- task scope paths are explicit
- task scope paths stay inside the round scope
- allowed changes, forbidden changes, and completion criteria are all present

## Side Effects

- wrote durable task contract `repo-governance-kernel/memory/task-contracts/2026-03-25-1332-correct-a4-public-surface-versioning-and-cut-tag.md`

## Evidence

- Stop the current package and docs from reporting a3 as the live release identity after the a4 cut, then publish the missing a4 tag.
- Machine-readable and release-facing surfaces report the current preview as 0.1.0a4 without hiding that the command set was first frozen in 0.1.0a3.
- Origin contains one a4 git tag pointing at the corrected release commit.
- audit-control-state and enforce-worktree remain ok after the correction.

