---
id: trans-2026-03-23-154332-retire-exception-contract-retired-exception-contract-exc-2026-03-23-1524-transition-logic-remains-split-across-per-command-scripts
type: transition-event
title: "Retired exception contract exc-2026-03-23-1524-transition-logic-remains-split-across-per-command-scripts"
status: recorded
project_id: repo-governance-kernel
workspace_id: ws-1490b759
workspace_root: C:/Users/terryzzb/Desktop/session-memory
branch: master
git_sha: 0300b70fbe9fb8027d7798c16b94373c6272ee86
paths:
  - exc-2026-03-23-1524-transition-logic-remains-split-across-per-command-scripts
  - obj-2026-03-23-0002
thread_ids: []
evidence_refs: []
tags:
  - transition-event
  - retire-exception-contract
confidence: high
created_at: 2026-03-23T15:43:32+08:00
updated_at: 2026-03-23T15:43:32+08:00
supersedes: []
superseded_by: []
---

## Summary

Retired exception contract exc-2026-03-23-1524-transition-logic-remains-split-across-per-command-scripts

## Command

retire-exception-contract

## Previous State

exception contract `exc-2026-03-23-1524-transition-logic-remains-split-across-per-command-scripts` status `active`

## Next State

exception contract `exc-2026-03-23-1524-transition-logic-remains-split-across-per-command-scripts` is now `retired`

## Guards

- exception contract `exc-2026-03-23-1524-transition-logic-remains-split-across-per-command-scripts` exists
- only active exception contracts can be retired

## Side Effects

- updated durable exception contract `repo-governance-kernel/memory/exception-contracts/2026-03-23-1524-transition-logic-remains-split-across-per-command-scripts.md`
- updated exception-ledger projection `repo-governance-kernel/control/exception-ledger.md`

## Evidence

- objective, round, and exception commands now delegate shared write/projection/event work through apply-transition-transaction
- uv run python scripts/smoke_exception_contracts.py
- uv run python scripts/repo_governance_kernel.py smoke

