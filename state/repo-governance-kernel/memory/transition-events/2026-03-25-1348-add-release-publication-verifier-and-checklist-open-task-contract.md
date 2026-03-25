---
id: trans-2026-03-25-134829-open-task-contract-opened-task-contract-taskc-2026-03-25-1348-add-release-publication-verifier-and-checklist
type: transition-event
title: "Opened task contract taskc-2026-03-25-1348-add-release-publication-verifier-and-checklist"
status: recorded
project_id: repo-governance-kernel
workspace_id: ws-1490b759
workspace_root: C:/Users/terryzzb/Desktop/session-memory
branch: master
git_sha: d91bfb377b5f7e4102ad75ae002c63e8839a6a91
paths:
  - taskc-2026-03-25-1348-add-release-publication-verifier-and-checklist
  - round-2026-03-25-1348-add-release-publication-verifier-and-checklist
  - obj-2026-03-23-0002
thread_ids: []
evidence_refs: []
tags:
  - transition-event
  - open-task-contract
confidence: high
created_at: 2026-03-25T13:48:29+08:00
updated_at: 2026-03-25T13:48:29+08:00
supersedes: []
superseded_by: []
---

## Summary

Opened task contract taskc-2026-03-25-1348-add-release-publication-verifier-and-checklist

## Command

open-task-contract

## Previous State

round `round-2026-03-25-1348-add-release-publication-verifier-and-checklist` had no durable task-contract records

## Next State

task contract `taskc-2026-03-25-1348-add-release-publication-verifier-and-checklist` is now active beneath round `round-2026-03-25-1348-add-release-publication-verifier-and-checklist`

## Guards

- round `round-2026-03-25-1348-add-release-publication-verifier-and-checklist` exists and remains open for task attachment
- task-contract objective linkage matches the referenced round
- task intent is explicit
- task scope paths are explicit
- task scope paths stay inside the round scope
- allowed changes, forbidden changes, and completion criteria are all present

## Side Effects

- wrote durable task contract `repo-governance-kernel/memory/task-contracts/2026-03-25-1348-add-release-publication-verifier-and-checklist.md`

## Evidence

- Stop future release cuts from ending at push or tag by making remote publication verification an explicit repo-owned step.
- One repo-owned verifier can confirm that v0.1.0a4 exists on origin as both a tag and a GitHub Release with the expected assets.
- Canonical release docs include an explicit post-push publication checklist and verification step.
- audit-control-state and enforce-worktree remain ok after the process fix.

