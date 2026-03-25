---
id: trans-2026-03-25-160046-rewrite-open-task-contract-rewrote-task-contract-taskc-2026-03-25-1553-land-b0-public-flow-subcontract-catalog
type: transition-event
title: "Rewrote task contract taskc-2026-03-25-1553-land-b0-public-flow-subcontract-catalog"
status: recorded
project_id: repo-governance-kernel
workspace_id: ws-1490b759
workspace_root: C:/Users/terryzzb/Desktop/session-memory
branch: master
git_sha: 96e1f2dd79c134ccff6516cba4a98c6ba7725adb
paths:
  - taskc-2026-03-25-1553-land-b0-public-flow-subcontract-catalog
  - round-2026-03-25-1553-freeze-b0-public-flow-subcontracts
  - obj-2026-03-23-0002
thread_ids: []
evidence_refs: []
tags:
  - transition-event
  - rewrite-open-task-contract
confidence: high
created_at: 2026-03-25T16:00:46+08:00
updated_at: 2026-03-25T16:00:46+08:00
supersedes: []
superseded_by: []
---

## Summary

Rewrote task contract taskc-2026-03-25-1553-land-b0-public-flow-subcontract-catalog

## Command

rewrite-open-task-contract

## Previous State

task contract `taskc-2026-03-25-1553-land-b0-public-flow-subcontract-catalog` remained `active` with fields paths pending rewrite

## Next State

task contract `taskc-2026-03-25-1553-land-b0-public-flow-subcontract-catalog` still remains `active` after rewriting paths

## Guards

- task contract `taskc-2026-03-25-1553-land-b0-public-flow-subcontract-catalog` exists and remains open
- task-contract rewrite reason is explicit
- rewritten task contract still has intent, path scope, allowed changes, forbidden changes, and completion criteria
- task-contract identity is preserved while contract content is rewritten
- task scope paths stay inside the round scope
- task-contract rewrite produces at least one material contract change

## Side Effects

- updated durable task contract `repo-governance-kernel/memory/task-contracts/2026-03-25-1553-land-b0-public-flow-subcontract-catalog.md`

## Evidence

- The task also updated the installed-package bootstrap smoke to assert the exported subcontract catalog, so the task path boundary must cover that file.
- paths

