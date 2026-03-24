---
id: trans-2026-03-24-211105-open-task-contract-opened-task-contract-taskc-2026-03-24-2111-separate-alpha-single-assessment-artifacts-and-add-package-smoke
type: transition-event
title: "Opened task contract taskc-2026-03-24-2111-separate-alpha-single-assessment-artifacts-and-add-package-smoke"
status: recorded
project_id: session-memory
workspace_id: ws-1490b759
workspace_root: C:/Users/terryzzb/Desktop/session-memory
branch: master
git_sha: 1212345248b7910d6feb2bf2b4de3482b32bd7c6
paths:
  - taskc-2026-03-24-2111-separate-alpha-single-assessment-artifacts-and-add-package-smoke
  - round-2026-03-24-2110-stabilize-package-first-single-assessment-alpha-surface
  - obj-2026-03-23-0002
thread_ids: []
evidence_refs: []
tags:
  - transition-event
  - open-task-contract
confidence: high
created_at: 2026-03-24T21:11:05+08:00
updated_at: 2026-03-24T21:11:05+08:00
supersedes: []
superseded_by: []
---

## Summary

Opened task contract taskc-2026-03-24-2111-separate-alpha-single-assessment-artifacts-and-add-package-smoke

## Command

open-task-contract

## Previous State

round `round-2026-03-24-2110-stabilize-package-first-single-assessment-alpha-surface` had no durable task-contract records

## Next State

task contract `taskc-2026-03-24-2111-separate-alpha-single-assessment-artifacts-and-add-package-smoke` is now active beneath round `round-2026-03-24-2110-stabilize-package-first-single-assessment-alpha-surface`

## Guards

- round `round-2026-03-24-2110-stabilize-package-first-single-assessment-alpha-surface` exists and remains open for task attachment
- task-contract objective linkage matches the referenced round
- task intent is explicit
- task scope paths are explicit
- task scope paths stay inside the round scope
- allowed changes, forbidden changes, and completion criteria are all present

## Side Effects

- wrote durable task contract `session-memory/memory/task-contracts/2026-03-24-2111-separate-alpha-single-assessment-artifacts-and-add-package-smoke.md`

## Evidence

- Make the 0.1.0a2 alpha surface more product-like by splitting external-target drafting from shadow assessment reporting at the owner layer, then adding one install-first smoke that validates kernel bootstrap and audit from an installed wheel.
- Draft and assessment commands no longer share one overloaded artifact owner label.
- One package-first smoke proves installed-wheel bootstrap and host-side audit from a disposable repo.
- Repo audit and enforcement remain clean after the alpha-surface tightening.
