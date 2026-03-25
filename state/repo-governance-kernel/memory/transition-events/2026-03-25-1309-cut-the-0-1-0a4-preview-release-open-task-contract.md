---
id: trans-2026-03-25-130939-open-task-contract-opened-task-contract-taskc-2026-03-25-1309-cut-the-0-1-0a4-preview-release
type: transition-event
title: "Opened task contract taskc-2026-03-25-1309-cut-the-0-1-0a4-preview-release"
status: recorded
project_id: repo-governance-kernel
workspace_id: ws-1490b759
workspace_root: C:/Users/terryzzb/Desktop/session-memory
branch: master
git_sha: f8bcaaa227040371b83759566be5fab542de7927
paths:
  - taskc-2026-03-25-1309-cut-the-0-1-0a4-preview-release
  - round-2026-03-25-1116-start-explicit-package-config-layering-for-a4
  - obj-2026-03-23-0002
thread_ids: []
evidence_refs: []
tags:
  - transition-event
  - open-task-contract
confidence: high
created_at: 2026-03-25T13:09:39+08:00
updated_at: 2026-03-25T13:09:39+08:00
supersedes: []
superseded_by: []
---

## Summary

Opened task contract taskc-2026-03-25-1309-cut-the-0-1-0a4-preview-release

## Command

open-task-contract

## Previous State

round `round-2026-03-25-1116-start-explicit-package-config-layering-for-a4` already had 5 durable task-contract record(s)

## Next State

task contract `taskc-2026-03-25-1309-cut-the-0-1-0a4-preview-release` is now active beneath round `round-2026-03-25-1116-start-explicit-package-config-layering-for-a4`

## Guards

- round `round-2026-03-25-1116-start-explicit-package-config-layering-for-a4` exists and remains open for task attachment
- task-contract objective linkage matches the referenced round
- task intent is explicit
- task scope paths are explicit
- task scope paths stay inside the round scope
- allowed changes, forbidden changes, and completion criteria are all present

## Side Effects

- wrote durable task contract `repo-governance-kernel/memory/task-contracts/2026-03-25-1309-cut-the-0-1-0a4-preview-release.md`

## Evidence

- Finish a4 as a versioned preview release instead of leaving the package metadata and release docs at a3 after the config-layering and installability work has already landed.
- Package metadata and release-facing docs agree that the current preview release is 0.1.0a4 and the next planned cut is 0.1.0a5.
- Build and installed-wheel proof pass against 0.1.0a4 artifacts.
- audit-control-state and enforce-worktree remain ok after the release cut.

