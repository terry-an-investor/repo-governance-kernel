---
id: trans-2026-03-25-103119-open-task-contract-opened-task-contract-taskc-2026-03-25-1031-tighten-root-readme-install-and-onboarding-contract
type: transition-event
title: "Opened task contract taskc-2026-03-25-1031-tighten-root-readme-install-and-onboarding-contract"
status: recorded
project_id: repo-governance-kernel
workspace_id: ws-1490b759
workspace_root: C:/Users/terryzzb/Desktop/session-memory
branch: master
git_sha: ecd54dbc378ce752bc782b16b6d9a071710437db
paths:
  - taskc-2026-03-25-1031-tighten-root-readme-install-and-onboarding-contract
  - round-2026-03-25-0946-make-package-first-repo-onboarding-real
  - obj-2026-03-23-0002
thread_ids: []
evidence_refs: []
tags:
  - transition-event
  - open-task-contract
confidence: high
created_at: 2026-03-25T10:31:19+08:00
updated_at: 2026-03-25T10:31:19+08:00
supersedes: []
superseded_by: []
---

## Summary

Opened task contract taskc-2026-03-25-1031-tighten-root-readme-install-and-onboarding-contract

## Command

open-task-contract

## Previous State

round `round-2026-03-25-0946-make-package-first-repo-onboarding-real` already had 2 durable task-contract record(s)

## Next State

task contract `taskc-2026-03-25-1031-tighten-root-readme-install-and-onboarding-contract` is now active beneath round `round-2026-03-25-0946-make-package-first-repo-onboarding-real`

## Guards

- round `round-2026-03-25-0946-make-package-first-repo-onboarding-real` exists and remains open for task attachment
- task-contract objective linkage matches the referenced round
- task intent is explicit
- task scope paths are explicit
- task scope paths stay inside the round scope
- allowed changes, forbidden changes, and completion criteria are all present

## Side Effects

- wrote durable task contract `repo-governance-kernel/memory/task-contracts/2026-03-25-1031-tighten-root-readme-install-and-onboarding-contract.md`

## Evidence

- Refine the root README so one entry document gives agents the exact install, onboard, and immediate follow-up commands for package-first repo initialization.
- An agent can read the root README alone and recover the minimal install and initialization path.
- Root README remains consistent with package-facing command semantics and product docs.

