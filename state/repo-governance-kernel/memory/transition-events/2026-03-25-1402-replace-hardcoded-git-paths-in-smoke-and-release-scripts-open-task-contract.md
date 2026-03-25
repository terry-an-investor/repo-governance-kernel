---
id: trans-2026-03-25-140240-open-task-contract-opened-task-contract-taskc-2026-03-25-1402-replace-hardcoded-git-paths-in-smoke-and-release-scripts
type: transition-event
title: "Opened task contract taskc-2026-03-25-1402-replace-hardcoded-git-paths-in-smoke-and-release-scripts"
status: recorded
project_id: repo-governance-kernel
workspace_id: ws-1490b759
workspace_root: C:/Users/terryzzb/Desktop/session-memory
branch: master
git_sha: a434b6ae3bd90cdc6f4cda3137669d1ed3dd6a69
paths:
  - taskc-2026-03-25-1402-replace-hardcoded-git-paths-in-smoke-and-release-scripts
  - round-2026-03-25-1402-make-smoke-git-resolution-ci-portable
  - obj-2026-03-23-0002
thread_ids: []
evidence_refs: []
tags:
  - transition-event
  - open-task-contract
confidence: high
created_at: 2026-03-25T14:02:40+08:00
updated_at: 2026-03-25T14:02:40+08:00
supersedes: []
superseded_by: []
---

## Summary

Opened task contract taskc-2026-03-25-1402-replace-hardcoded-git-paths-in-smoke-and-release-scripts

## Command

open-task-contract

## Previous State

round `round-2026-03-25-1402-make-smoke-git-resolution-ci-portable` had no durable task-contract records

## Next State

task contract `taskc-2026-03-25-1402-replace-hardcoded-git-paths-in-smoke-and-release-scripts` is now active beneath round `round-2026-03-25-1402-make-smoke-git-resolution-ci-portable`

## Guards

- round `round-2026-03-25-1402-make-smoke-git-resolution-ci-portable` exists and remains open for task attachment
- task-contract objective linkage matches the referenced round
- task intent is explicit
- task scope paths are explicit
- task scope paths stay inside the round scope
- allowed changes, forbidden changes, and completion criteria are all present

## Side Effects

- wrote durable task contract `repo-governance-kernel/memory/task-contracts/2026-03-25-1402-replace-hardcoded-git-paths-in-smoke-and-release-scripts.md`

## Evidence

- Remove Windows-only git executable assumptions from repo-owned smoke and release verification scripts and validate the resulting cross-platform path.
- The changed smoke and release scripts all consume the shared git resolver and the targeted smoke validations pass.

