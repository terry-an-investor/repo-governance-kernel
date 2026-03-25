---
id: trans-2026-03-25-190521-open-task-contract-opened-task-contract-taskc-2026-03-25-1905-land-repo-governance-kernel-rename-and-legacy-surface-cleanup
type: transition-event
title: "Opened task contract taskc-2026-03-25-1905-land-repo-governance-kernel-rename-and-legacy-surface-cleanup"
status: recorded
project_id: repo-governance-kernel
workspace_id: ws-1490b759
workspace_root: C:/Users/terryzzb/Desktop/session-memory
branch: master
git_sha: ccf86ba6952d1ffe3fc12e96136f287de2ca3536
paths:
  - taskc-2026-03-25-1905-land-repo-governance-kernel-rename-and-legacy-surface-cleanup
  - round-2026-03-25-1904-retire-stale-product-identities-and-legacy-scaffolding
  - obj-2026-03-23-0002
thread_ids: []
evidence_refs: []
tags:
  - transition-event
  - open-task-contract
confidence: high
created_at: 2026-03-25T19:05:21+08:00
updated_at: 2026-03-25T19:05:21+08:00
supersedes: []
superseded_by: []
---

## Summary

Opened task contract taskc-2026-03-25-1905-land-repo-governance-kernel-rename-and-legacy-surface-cleanup

## Command

open-task-contract

## Previous State

round `round-2026-03-25-1904-retire-stale-product-identities-and-legacy-scaffolding` had no durable task-contract records

## Next State

task contract `taskc-2026-03-25-1905-land-repo-governance-kernel-rename-and-legacy-surface-cleanup` is now active beneath round `round-2026-03-25-1904-retire-stale-product-identities-and-legacy-scaffolding`

## Guards

- round `round-2026-03-25-1904-retire-stale-product-identities-and-legacy-scaffolding` exists and remains open for task attachment
- task-contract objective linkage matches the referenced round
- task intent is explicit
- task scope paths are explicit
- task scope paths stay inside the round scope
- allowed changes, forbidden changes, and completion criteria are all present

## Side Effects

- wrote durable task contract `repo-governance-kernel/memory/task-contracts/2026-03-25-1905-land-repo-governance-kernel-rename-and-legacy-surface-cleanup.md`

## Evidence

- Retire stale repo-owned names, delete legacy-only surfaces, and keep the control line honest through validation.
- Live repo surfaces no longer present stale retired names or demo-only framing as the product identity, and rename validation passes.
