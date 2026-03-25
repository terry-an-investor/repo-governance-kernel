---
id: trans-2026-03-25-144217-open-task-contract-opened-task-contract-taskc-2026-03-25-1442-cut-the-0-1-0a5-preview-release
type: transition-event
title: "Opened task contract taskc-2026-03-25-1442-cut-the-0-1-0a5-preview-release"
status: recorded
project_id: session-memory
workspace_id: ws-1490b759
workspace_root: C:/Users/terryzzb/Desktop/session-memory
branch: master
git_sha: 7ff723b146ea86ea7c9751c8e99257a920ae272a
paths:
  - taskc-2026-03-25-1442-cut-the-0-1-0a5-preview-release
  - round-2026-03-25-1441-cut-the-0-1-0a5-preview-release
  - obj-2026-03-23-0002
thread_ids: []
evidence_refs: []
tags:
  - transition-event
  - open-task-contract
confidence: high
created_at: 2026-03-25T14:42:17+08:00
updated_at: 2026-03-25T14:42:17+08:00
supersedes: []
superseded_by: []
---

## Summary

Opened task contract taskc-2026-03-25-1442-cut-the-0-1-0a5-preview-release

## Command

open-task-contract

## Previous State

round `round-2026-03-25-1441-cut-the-0-1-0a5-preview-release` had no durable task-contract records

## Next State

task contract `taskc-2026-03-25-1442-cut-the-0-1-0a5-preview-release` is now active beneath round `round-2026-03-25-1441-cut-the-0-1-0a5-preview-release`

## Guards

- round `round-2026-03-25-1441-cut-the-0-1-0a5-preview-release` exists and remains open for task attachment
- task-contract objective linkage matches the referenced round
- task intent is explicit
- task scope paths are explicit
- task scope paths stay inside the round scope
- allowed changes, forbidden changes, and completion criteria are all present

## Side Effects

- wrote durable task contract `session-memory/memory/task-contracts/2026-03-25-1442-cut-the-0-1-0a5-preview-release.md`

## Evidence

- Align package metadata, machine-readable public-surface descriptors, and release-facing docs on 0.1.0a5, then validate the packaged path before push.
- Package metadata, machine-readable public-surface descriptors, and release-facing docs all report 0.1.0a5 as the current preview release.
- Installed-wheel proof and release-facing doc audit pass against the a5 cut.
- audit-control-state and enforce-worktree both return ok before the release commit is pushed.
