---
id: trans-2026-03-25-110651-open-task-contract-opened-task-contract-taskc-2026-03-25-1106-cut-the-0-1-0a3-preview-release
type: transition-event
title: "Opened task contract taskc-2026-03-25-1106-cut-the-0-1-0a3-preview-release"
status: recorded
project_id: repo-governance-kernel
workspace_id: ws-1490b759
workspace_root: C:/Users/terryzzb/Desktop/session-memory
branch: master
git_sha: 0fcdc4fc4110039273ff0f761eebe95870db9551
paths:
  - taskc-2026-03-25-1106-cut-the-0-1-0a3-preview-release
  - round-2026-03-25-0946-make-package-first-repo-onboarding-real
  - obj-2026-03-23-0002
thread_ids: []
evidence_refs: []
tags:
  - transition-event
  - open-task-contract
confidence: high
created_at: 2026-03-25T11:06:51+08:00
updated_at: 2026-03-25T11:06:51+08:00
supersedes: []
superseded_by: []
---

## Summary

Opened task contract taskc-2026-03-25-1106-cut-the-0-1-0a3-preview-release

## Command

open-task-contract

## Previous State

round `round-2026-03-25-0946-make-package-first-repo-onboarding-real` already had 5 durable task-contract record(s)

## Next State

task contract `taskc-2026-03-25-1106-cut-the-0-1-0a3-preview-release` is now active beneath round `round-2026-03-25-0946-make-package-first-repo-onboarding-real`

## Guards

- round `round-2026-03-25-0946-make-package-first-repo-onboarding-real` exists and remains open for task attachment
- task-contract objective linkage matches the referenced round
- task intent is explicit
- task scope paths are explicit
- task scope paths stay inside the round scope
- allowed changes, forbidden changes, and completion criteria are all present

## Side Effects

- wrote durable task contract `repo-governance-kernel/memory/task-contracts/2026-03-25-1106-cut-the-0-1-0a3-preview-release.md`

## Evidence

- Finish a3 as a versioned preview release rather than leaving the package metadata and docs at a2 while the a3 surface is already complete.
- Package metadata and release-facing docs agree that the current preview release is 0.1.0a3.
- Build and installed-wheel smoke proof pass against 0.1.0a3 artifacts.
- Audit and enforcement remain clean after the release cut.

