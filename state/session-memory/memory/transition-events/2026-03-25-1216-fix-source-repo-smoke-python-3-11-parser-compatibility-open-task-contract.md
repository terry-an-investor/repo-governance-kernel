---
id: trans-2026-03-25-121603-open-task-contract-opened-task-contract-taskc-2026-03-25-1216-fix-source-repo-smoke-python-3-11-parser-compatibility
type: transition-event
title: "Opened task contract taskc-2026-03-25-1216-fix-source-repo-smoke-python-3-11-parser-compatibility"
status: recorded
project_id: session-memory
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
  - open-task-contract
confidence: high
created_at: 2026-03-25T12:16:03+08:00
updated_at: 2026-03-25T12:16:03+08:00
supersedes: []
superseded_by: []
---

## Summary

Opened task contract taskc-2026-03-25-1216-fix-source-repo-smoke-python-3-11-parser-compatibility

## Command

open-task-contract

## Previous State

round `round-2026-03-25-1116-start-explicit-package-config-layering-for-a4` already had 2 durable task-contract record(s)

## Next State

task contract `taskc-2026-03-25-1216-fix-source-repo-smoke-python-3-11-parser-compatibility` is now active beneath round `round-2026-03-25-1116-start-explicit-package-config-layering-for-a4`

## Guards

- round `round-2026-03-25-1116-start-explicit-package-config-layering-for-a4` exists and remains open for task attachment
- task-contract objective linkage matches the referenced round
- task intent is explicit
- task scope paths are explicit
- task scope paths stay inside the round scope
- allowed changes, forbidden changes, and completion criteria are all present

## Side Effects

- wrote durable task contract `session-memory/memory/task-contracts/2026-03-25-1216-fix-source-repo-smoke-python-3-11-parser-compatibility.md`

## Evidence

- Repair the new CI failure by making the repo_onboarding smoke parse cleanly under the GitHub Actions Python 3.11 runtime instead of relying on newer parser behavior.
- scripts/smoke_repo_onboarding.py parses and runs under uv-managed Python 3.11.
- uv run --python 3.11 python scripts/smoke_phase1.py passes on the repaired tree.
- Repo-level control audit and worktree enforcement remain ok after the fix.
