---
id: trans-2026-03-25-122010-update-task-contract-status-updated-task-contract-taskc-2026-03-25-1216-fix-source-repo-smoke-python-3-11-parser-compatibility-to-completed
type: transition-event
title: "Updated task contract taskc-2026-03-25-1216-fix-source-repo-smoke-python-3-11-parser-compatibility to completed"
status: recorded
project_id: repo-governance-kernel
workspace_id: ws-1490b759
workspace_root: C:/Users/terryzzb/Desktop/session-memory
branch: master
git_sha: bb118b9346eae2b83714ffc5dd6d388aaebbd9b9
paths:
  - taskc-2026-03-25-1216-fix-source-repo-smoke-python-3-11-parser-compatibility
  - round-2026-03-25-1116-start-explicit-package-config-layering-for-a4
  - obj-2026-03-23-0002
thread_ids: []
evidence_refs: []
tags:
  - transition-event
  - update-task-contract-status
confidence: high
created_at: 2026-03-25T12:20:10+08:00
updated_at: 2026-03-25T12:20:10+08:00
supersedes: []
superseded_by: []
---

## Summary

Updated task contract taskc-2026-03-25-1216-fix-source-repo-smoke-python-3-11-parser-compatibility to completed

## Command

update-task-contract-status

## Previous State

task contract `taskc-2026-03-25-1216-fix-source-repo-smoke-python-3-11-parser-compatibility` status `active`

## Next State

task contract `taskc-2026-03-25-1216-fix-source-repo-smoke-python-3-11-parser-compatibility` is now `completed`

## Guards

- task contract `taskc-2026-03-25-1216-fix-source-repo-smoke-python-3-11-parser-compatibility` exists
- task-contract transition `active -> completed` is legal
- completed task-contract transitions include at least one resolution record

## Side Effects

- updated durable task contract `repo-governance-kernel/memory/task-contracts/2026-03-25-1216-fix-source-repo-smoke-python-3-11-parser-compatibility.md`

## Evidence

- The repo_onboarding smoke now parses under Python 3.11 and the full source-repo acceptance smoke passes under the same interpreter version used by GitHub Actions.
- Refactored scripts/smoke_repo_onboarding.py to compute the normalized workspace-root string outside the f-string expression so the file parses on Python 3.11.
- Validated the fix with uv run --python 3.11 python scripts/smoke_repo_onboarding.py, uv run --python 3.11 python scripts/smoke_phase1.py, uv run python -m kernel.cli audit-control-state --project-id repo-governance-kernel, and uv run python -m kernel.cli enforce-worktree --project-id repo-governance-kernel --workspace-root C:/Users/terryzzb/Desktop/session-memory

