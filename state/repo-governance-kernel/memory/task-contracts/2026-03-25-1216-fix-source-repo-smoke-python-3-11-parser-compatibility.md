---
id: taskc-2026-03-25-1216-fix-source-repo-smoke-python-3-11-parser-compatibility
type: task-contract
title: "Fix source-repo smoke Python 3.11 parser compatibility"
status: completed
project_id: repo-governance-kernel
workspace_id: ws-1490b759
workspace_root: C:/Users/terryzzb/Desktop/session-memory
branch: master
git_sha: bb118b9346eae2b83714ffc5dd6d388aaebbd9b9
paths:
  - scripts
thread_ids: []
evidence_refs: []
tags:
  - task-contract
  - control-plane
confidence: high
created_at: 2026-03-25T12:16:02+08:00
updated_at: 2026-03-25T12:20:10+08:00
objective_id: obj-2026-03-23-0002
phase: execution
round_id: "round-2026-03-25-1116-start-explicit-package-config-layering-for-a4"
supersedes: []
superseded_by: []
---

## Summary

Repair the new CI failure by making the repo_onboarding smoke parse cleanly under the GitHub Actions Python 3.11 runtime instead of relying on newer parser behavior.

## Intent

Repair the new CI failure by making the repo_onboarding smoke parse cleanly under the GitHub Actions Python 3.11 runtime instead of relying on newer parser behavior.

## Allowed Changes

- Refactor the failing smoke expression so it produces the same expected string without using Python syntax that breaks on 3.11.
- Add the smallest validation needed to prove the smoke and phase-1 suite pass under Python 3.11.

## Forbidden Changes

- Do not weaken or skip the repo_onboarding smoke just to make CI green.
- Do not change the GitHub workflow Python version to hide a source compatibility bug.

## Completion Criteria

- scripts/smoke_repo_onboarding.py parses and runs under uv-managed Python 3.11.
- uv run --python 3.11 python scripts/smoke_phase1.py passes on the repaired tree.
- Repo-level control audit and worktree enforcement remain ok after the fix.

## Resolution

- Refactored scripts/smoke_repo_onboarding.py to compute the normalized workspace-root string outside the f-string expression so the file parses on Python 3.11.
- Validated the fix with uv run --python 3.11 python scripts/smoke_repo_onboarding.py, uv run --python 3.11 python scripts/smoke_phase1.py, uv run python -m kernel.cli audit-control-state --project-id repo-governance-kernel, and uv run python -m kernel.cli enforce-worktree --project-id repo-governance-kernel --workspace-root C:/Users/terryzzb/Desktop/session-memory

## Active Risks

- If source-repo smoke syntax drifts above the CI interpreter floor, every push will keep failing before product behavior is even exercised.

## Status Notes

active -> completed: The repo_onboarding smoke now parses under Python 3.11 and the full source-repo acceptance smoke passes under the same interpreter version used by GitHub Actions.

resolution recorded:
- Refactored scripts/smoke_repo_onboarding.py to compute the normalized workspace-root string outside the f-string expression so the file parses on Python 3.11.
- Validated the fix with uv run --python 3.11 python scripts/smoke_repo_onboarding.py, uv run --python 3.11 python scripts/smoke_phase1.py, uv run python -m kernel.cli audit-control-state --project-id repo-governance-kernel, and uv run python -m kernel.cli enforce-worktree --project-id repo-governance-kernel --workspace-root C:/Users/terryzzb/Desktop/session-memory

