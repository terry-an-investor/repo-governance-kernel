---
id: trans-2026-03-25-170505-open-task-contract-opened-task-contract-taskc-2026-03-25-1705-land-b1-minimal-evidence-layer-public-subcontracts
type: transition-event
title: "Opened task contract taskc-2026-03-25-1705-land-b1-minimal-evidence-layer-public-subcontracts"
status: recorded
project_id: repo-governance-kernel
workspace_id: ws-1490b759
workspace_root: C:/Users/terryzzb/Desktop/session-memory
branch: master
git_sha: c18f66b4923034042037b9252c432b9797e59ad4
paths:
  - taskc-2026-03-25-1705-land-b1-minimal-evidence-layer-public-subcontracts
  - round-2026-03-25-1704-harden-public-evidence-layer-response-contracts-for-b1
  - obj-2026-03-23-0002
thread_ids: []
evidence_refs: []
tags:
  - transition-event
  - open-task-contract
confidence: high
created_at: 2026-03-25T17:05:05+08:00
updated_at: 2026-03-25T17:05:05+08:00
supersedes: []
superseded_by: []
---

## Summary

Opened task contract taskc-2026-03-25-1705-land-b1-minimal-evidence-layer-public-subcontracts

## Command

open-task-contract

## Previous State

round `round-2026-03-25-1704-harden-public-evidence-layer-response-contracts-for-b1` had no durable task-contract records

## Next State

task contract `taskc-2026-03-25-1705-land-b1-minimal-evidence-layer-public-subcontracts` is now active beneath round `round-2026-03-25-1704-harden-public-evidence-layer-response-contracts-for-b1`

## Guards

- round `round-2026-03-25-1704-harden-public-evidence-layer-response-contracts-for-b1` exists and remains open for task attachment
- task-contract objective linkage matches the referenced round
- task intent is explicit
- task scope paths are explicit
- task scope paths stay inside the round scope
- allowed changes, forbidden changes, and completion criteria are all present

## Side Effects

- wrote durable task contract `repo-governance-kernel/memory/task-contracts/2026-03-25-1705-land-b1-minimal-evidence-layer-public-subcontracts.md`

## Evidence

- Move the smallest repeated execution/outcome/postconditions kernels into one owner-layer public contract so agent callers can depend on them directly.
- Public contract descriptors, docs, and smokes all agree on the new minimal stable evidence-layer subcontracts.
- The targeted public-flow validation path passes after the contract upgrade.

