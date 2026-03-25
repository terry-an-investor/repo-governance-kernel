---
id: trans-2026-03-25-190930-rewrite-open-task-contract-rewrote-task-contract-taskc-2026-03-25-1905-land-repo-governance-kernel-rename-and-legacy-surface-cleanup
type: transition-event
title: "Rewrote task contract taskc-2026-03-25-1905-land-repo-governance-kernel-rename-and-legacy-surface-cleanup"
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
  - rewrite-open-task-contract
confidence: high
created_at: 2026-03-25T19:09:30+08:00
updated_at: 2026-03-25T19:09:30+08:00
supersedes: []
superseded_by: []
---

## Summary

Rewrote task contract taskc-2026-03-25-1905-land-repo-governance-kernel-rename-and-legacy-surface-cleanup

## Command

rewrite-open-task-contract

## Previous State

task contract `taskc-2026-03-25-1905-land-repo-governance-kernel-rename-and-legacy-surface-cleanup` remained `active` with fields allowed_changes, completion_criteria pending rewrite

## Next State

task contract `taskc-2026-03-25-1905-land-repo-governance-kernel-rename-and-legacy-surface-cleanup` still remains `active` after rewriting allowed_changes, completion_criteria

## Guards

- task contract `taskc-2026-03-25-1905-land-repo-governance-kernel-rename-and-legacy-surface-cleanup` exists and remains open
- task-contract rewrite reason is explicit
- rewritten task contract still has intent, path scope, allowed changes, forbidden changes, and completion criteria
- task-contract identity is preserved while contract content is rewritten
- task scope paths stay inside the round scope
- task-contract rewrite produces at least one material contract change

## Side Effects

- updated durable task contract `repo-governance-kernel/memory/task-contracts/2026-03-25-1905-land-repo-governance-kernel-rename-and-legacy-surface-cleanup.md`

## Evidence

- The active task contract should describe legacy-name cleanup generically instead of repeating retired product names.
- allowed_changes
- completion_criteria
