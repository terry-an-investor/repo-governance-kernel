---
id: trans-2026-03-25-155330-open-task-contract-opened-task-contract-taskc-2026-03-25-1553-land-b0-public-flow-subcontract-catalog
type: transition-event
title: "Opened task contract taskc-2026-03-25-1553-land-b0-public-flow-subcontract-catalog"
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
  - open-task-contract
confidence: high
created_at: 2026-03-25T15:53:30+08:00
updated_at: 2026-03-25T15:53:30+08:00
supersedes: []
superseded_by: []
---

## Summary

Opened task contract taskc-2026-03-25-1553-land-b0-public-flow-subcontract-catalog

## Command

open-task-contract

## Previous State

round `round-2026-03-25-1553-freeze-b0-public-flow-subcontracts` had no durable task-contract records

## Next State

task contract `taskc-2026-03-25-1553-land-b0-public-flow-subcontract-catalog` is now active beneath round `round-2026-03-25-1553-freeze-b0-public-flow-subcontracts`

## Guards

- round `round-2026-03-25-1553-freeze-b0-public-flow-subcontracts` exists and remains open for task attachment
- task-contract objective linkage matches the referenced round
- task intent is explicit
- task scope paths are explicit
- task scope paths stay inside the round scope
- allowed changes, forbidden changes, and completion criteria are all present

## Side Effects

- wrote durable task contract `repo-governance-kernel/memory/task-contracts/2026-03-25-1553-land-b0-public-flow-subcontract-catalog.md`

## Evidence

- Move public nested contract truth into one owner-layer descriptor so callers can rely on subobject fields without reading implementation code.
- describe-public-alpha-surface exports one machine-readable subcontract catalog for flow_contract and intent_compilation.
- Public flow smokes assert the stable nested fields from the owner-layer contract instead of ad hoc field checks.

