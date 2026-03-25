---
id: trans-2026-03-25-103136-update-task-contract-status-updated-task-contract-taskc-2026-03-25-1031-tighten-root-readme-install-and-onboarding-contract-to-completed
type: transition-event
title: "Updated task contract taskc-2026-03-25-1031-tighten-root-readme-install-and-onboarding-contract to completed"
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
  - update-task-contract-status
confidence: high
created_at: 2026-03-25T10:31:36+08:00
updated_at: 2026-03-25T10:31:36+08:00
supersedes: []
superseded_by: []
---

## Summary

Updated task contract taskc-2026-03-25-1031-tighten-root-readme-install-and-onboarding-contract to completed

## Command

update-task-contract-status

## Previous State

task contract `taskc-2026-03-25-1031-tighten-root-readme-install-and-onboarding-contract` status `active`

## Next State

task contract `taskc-2026-03-25-1031-tighten-root-readme-install-and-onboarding-contract` is now `completed`

## Guards

- task contract `taskc-2026-03-25-1031-tighten-root-readme-install-and-onboarding-contract` exists
- task-contract transition `active -> completed` is legal
- completed task-contract transitions include at least one resolution record

## Side Effects

- updated durable task contract `repo-governance-kernel/memory/task-contracts/2026-03-25-1031-tighten-root-readme-install-and-onboarding-contract.md`

## Evidence

- Root README now carries the minimal package install and onboarding contract for agent callers.
- Added isolated-environment package install steps to the root README.
- Added bounded onboard-repo and onboard-repo-from-intent initialization examples and preconditions to the root README.
- Added minimal post-onboarding audit and enforce follow-up commands to the root README.

