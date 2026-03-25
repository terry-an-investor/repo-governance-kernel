---
id: trans-2026-03-25-173120-open-task-contract-opened-task-contract-taskc-2026-03-25-1731-promote-minimum-stable-b1-public-subcontracts
type: transition-event
title: "Opened task contract taskc-2026-03-25-1731-promote-minimum-stable-b1-public-subcontracts"
status: recorded
project_id: session-memory
workspace_id: ws-1490b759
workspace_root: C:/Users/terryzzb/Desktop/session-memory
branch: master
git_sha: 204802ce4f1822967cb5a957116471141e697a89
paths:
  - taskc-2026-03-25-1731-promote-minimum-stable-b1-public-subcontracts
  - round-2026-03-25-1730-promote-minimum-stable-public-response-kernels-for-b1
  - obj-2026-03-23-0002
thread_ids: []
evidence_refs: []
tags:
  - transition-event
  - open-task-contract
confidence: high
created_at: 2026-03-25T17:31:20+08:00
updated_at: 2026-03-25T17:31:20+08:00
supersedes: []
superseded_by: []
---

## Summary

Opened task contract taskc-2026-03-25-1731-promote-minimum-stable-b1-public-subcontracts

## Command

open-task-contract

## Previous State

round `round-2026-03-25-1730-promote-minimum-stable-public-response-kernels-for-b1` had no durable task-contract records

## Next State

task contract `taskc-2026-03-25-1731-promote-minimum-stable-b1-public-subcontracts` is now active beneath round `round-2026-03-25-1730-promote-minimum-stable-public-response-kernels-for-b1`

## Guards

- round `round-2026-03-25-1730-promote-minimum-stable-public-response-kernels-for-b1` exists and remains open for task attachment
- task-contract objective linkage matches the referenced round
- task intent is explicit
- task scope paths are explicit
- task scope paths stay inside the round scope
- allowed changes, forbidden changes, and completion criteria are all present

## Side Effects

- wrote durable task contract `session-memory/memory/task-contracts/2026-03-25-1731-promote-minimum-stable-b1-public-subcontracts.md`

## Evidence

- Move only the repeatedly observed execution and postcondition kernels into the stable public contract across onboarding and one-time external assessment flows.
- describe-public-surface and the targeted public smokes prove the promoted stable contract and docs match the owner-layer truth.
