---
id: trans-2026-03-25-151529-open-task-contract-opened-task-contract-taskc-2026-03-25-1515-land-the-b0-candidate-public-flow-contract-descriptor
type: transition-event
title: "Opened task contract taskc-2026-03-25-1515-land-the-b0-candidate-public-flow-contract-descriptor"
status: recorded
project_id: repo-governance-kernel
workspace_id: ws-1490b759
workspace_root: C:/Users/terryzzb/Desktop/session-memory
branch: master
git_sha: dd9b5402cf97ad67dd55f5897652f77bd82396f1
paths:
  - taskc-2026-03-25-1515-land-the-b0-candidate-public-flow-contract-descriptor
  - round-2026-03-25-1514-start-b0-public-contract-freeze
  - obj-2026-03-23-0002
thread_ids: []
evidence_refs: []
tags:
  - transition-event
  - open-task-contract
confidence: high
created_at: 2026-03-25T15:15:29+08:00
updated_at: 2026-03-25T15:15:29+08:00
supersedes: []
superseded_by: []
---

## Summary

Opened task contract taskc-2026-03-25-1515-land-the-b0-candidate-public-flow-contract-descriptor

## Command

open-task-contract

## Previous State

round `round-2026-03-25-1514-start-b0-public-contract-freeze` had no durable task-contract records

## Next State

task contract `taskc-2026-03-25-1515-land-the-b0-candidate-public-flow-contract-descriptor` is now active beneath round `round-2026-03-25-1514-start-b0-public-contract-freeze`

## Guards

- round `round-2026-03-25-1514-start-b0-public-contract-freeze` exists and remains open for task attachment
- task-contract objective linkage matches the referenced round
- task intent is explicit
- task scope paths are explicit
- task scope paths stay inside the round scope
- allowed changes, forbidden changes, and completion criteria are all present

## Side Effects

- wrote durable task contract `repo-governance-kernel/memory/task-contracts/2026-03-25-1515-land-the-b0-candidate-public-flow-contract-descriptor.md`

## Evidence

- Use one owner-layer catalog for stable public flow fields so docs, CLI descriptors, and smoke all freeze the same thing.
- One shared owner-layer descriptor names the stable field contract for the four current public flow entrypoints.
- Machine-readable public surface output and smoke assertions consume the same descriptor.
- Canonical/package-facing docs describe this as the b0 candidate contract and validation passes.

