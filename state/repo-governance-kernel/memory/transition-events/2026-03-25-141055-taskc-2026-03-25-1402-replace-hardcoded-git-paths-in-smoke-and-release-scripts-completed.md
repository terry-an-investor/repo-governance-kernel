---
id: trans-2026-03-25-141055-update-task-contract-status-updated-task-contract-taskc-2026-03-25-1402-replace-hardcoded-git-paths-in-smoke-and-release-scripts-to-completed
type: transition-event
title: "Updated task contract taskc-2026-03-25-1402-replace-hardcoded-git-paths-in-smoke-and-release-scripts to completed"
status: recorded
project_id: repo-governance-kernel
workspace_id: ws-1490b759
workspace_root: C:/Users/terryzzb/Desktop/session-memory
branch: master
git_sha: 5900e057f83b733d1c02d997617ef95f94646552
paths:
  - taskc-2026-03-25-1402-replace-hardcoded-git-paths-in-smoke-and-release-scripts
  - round-2026-03-25-1402-make-smoke-git-resolution-ci-portable
  - obj-2026-03-23-0002
thread_ids: []
evidence_refs: []
tags:
  - transition-event
  - update-task-contract-status
confidence: high
created_at: 2026-03-25T14:10:55+08:00
updated_at: 2026-03-25T14:10:55+08:00
supersedes: []
superseded_by: []
---

## Summary

Updated task contract taskc-2026-03-25-1402-replace-hardcoded-git-paths-in-smoke-and-release-scripts to completed

## Command

update-task-contract-status

## Previous State

task contract `taskc-2026-03-25-1402-replace-hardcoded-git-paths-in-smoke-and-release-scripts` status `active`

## Next State

task contract `taskc-2026-03-25-1402-replace-hardcoded-git-paths-in-smoke-and-release-scripts` is now `completed`

## Guards

- task contract `taskc-2026-03-25-1402-replace-hardcoded-git-paths-in-smoke-and-release-scripts` exists
- task-contract transition `active -> completed` is legal
- completed task-contract transitions include at least one resolution record

## Side Effects

- updated durable task contract `repo-governance-kernel/memory/task-contracts/2026-03-25-1402-replace-hardcoded-git-paths-in-smoke-and-release-scripts.md`

## Evidence

- The shared git executable resolver landed, the affected scripts were migrated, and the targeted smoke plus CI validations passed.
- Added scripts/git_exec.py, rewrote the affected smoke and release verification scripts to consume it, and validated the path with smoke_config_runtime, smoke_repo_onboarding, smoke_kernel_bootstrap, verify_release_publication --help, smoke_repo_acceptance, and GitHub Actions run 23527409033.

