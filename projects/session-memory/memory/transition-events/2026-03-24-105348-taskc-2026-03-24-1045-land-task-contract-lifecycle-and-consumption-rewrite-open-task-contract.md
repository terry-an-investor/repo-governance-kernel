---
id: trans-2026-03-24-105348-rewrite-open-task-contract-rewrote-task-contract-taskc-2026-03-24-1045-land-task-contract-lifecycle-and-consumption
type: transition-event
title: "Rewrote task contract taskc-2026-03-24-1045-land-task-contract-lifecycle-and-consumption"
status: recorded
project_id: session-memory
workspace_id: ws-1490b759
workspace_root: C:/Users/terryzzb/Desktop/session-memory
branch: master
git_sha: a43b816258cb88a3b7e11b2160d0d8612069c814
paths:
  - taskc-2026-03-24-1045-land-task-contract-lifecycle-and-consumption
  - round-2026-03-24-1045-complete-task-contract-lifecycle-and-consumption
  - obj-2026-03-23-0002
thread_ids: []
evidence_refs: []
tags:
  - transition-event
  - rewrite-open-task-contract
confidence: high
created_at: 2026-03-24T10:53:48+08:00
updated_at: 2026-03-24T10:53:48+08:00
supersedes: []
superseded_by: []
---

## Summary

Rewrote task contract taskc-2026-03-24-1045-land-task-contract-lifecycle-and-consumption

## Command

rewrite-open-task-contract

## Previous State

task contract `taskc-2026-03-24-1045-land-task-contract-lifecycle-and-consumption` remained `active` with fields allowed_changes, completion_criteria, paths pending rewrite

## Next State

task contract `taskc-2026-03-24-1045-land-task-contract-lifecycle-and-consumption` still remains `active` after rewriting allowed_changes, completion_criteria, paths

## Guards

- task contract `taskc-2026-03-24-1045-land-task-contract-lifecycle-and-consumption` exists and remains open
- task-contract rewrite reason is explicit
- rewritten task contract still has intent, path scope, allowed changes, forbidden changes, and completion criteria
- task-contract identity is preserved while contract content is rewritten
- task scope paths stay inside the round scope
- task-contract rewrite produces at least one material contract change

## Side Effects

- updated durable task contract `session-memory/memory/task-contracts/2026-03-24-1045-land-task-contract-lifecycle-and-consumption.md`

## Evidence

- Task-contract enforcement now consumes active task-contract coverage, so the task boundary must include control_enforcement.py and the tighter honesty work.
- allowed_changes
- completion_criteria
- paths
