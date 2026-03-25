---
id: trans-2026-03-25-112655-open-task-contract-opened-task-contract-taskc-2026-03-25-1126-harden-filename-budgeting-and-local-smoke-gate-for-ci-parity
type: transition-event
title: "Opened task contract taskc-2026-03-25-1126-harden-filename-budgeting-and-local-smoke-gate-for-ci-parity"
status: recorded
project_id: session-memory
workspace_id: ws-1490b759
workspace_root: C:/Users/terryzzb/Desktop/session-memory
branch: master
git_sha: 80b47b322a49439cb9b79eb6884b8b6bdc8a89af
paths:
  - taskc-2026-03-25-1126-harden-filename-budgeting-and-local-smoke-gate-for-ci-parity
  - round-2026-03-25-1116-start-explicit-package-config-layering-for-a4
  - obj-2026-03-23-0002
thread_ids: []
evidence_refs: []
tags:
  - transition-event
  - open-task-contract
confidence: high
created_at: 2026-03-25T11:26:55+08:00
updated_at: 2026-03-25T11:26:55+08:00
supersedes: []
superseded_by: []
---

## Summary

Opened task contract taskc-2026-03-25-1126-harden-filename-budgeting-and-local-smoke-gate-for-ci-parity

## Command

open-task-contract

## Previous State

round `round-2026-03-25-1116-start-explicit-package-config-layering-for-a4` had no durable task-contract records

## Next State

task contract `taskc-2026-03-25-1126-harden-filename-budgeting-and-local-smoke-gate-for-ci-parity` is now active beneath round `round-2026-03-25-1116-start-explicit-package-config-layering-for-a4`

## Guards

- round `round-2026-03-25-1116-start-explicit-package-config-layering-for-a4` exists and remains open for task attachment
- task-contract objective linkage matches the referenced round
- task intent is explicit
- task scope paths are explicit
- task scope paths stay inside the round scope
- allowed changes, forbidden changes, and completion criteria are all present

## Side Effects

- wrote durable task contract `session-memory/memory/task-contracts/2026-03-25-1126-harden-filename-budgeting-and-local-smoke-gate-for-ci-parity.md`

## Evidence

- Fix the recurring submit regression by centralizing durable file-name budgeting for pivot/objective writes and aligning the local pre-push gate with the CI smoke surface that currently catches the escape.
- Shared durable file naming is reused by the pivot or objective write surfaces that currently assemble unbounded file names.
- The local pre-push hook and the documented release-facing validation surface both cover the smoke that caught the a3 escape.
- The changed path is validated by focused smoke plus the repo-level audit and enforcement commands.
