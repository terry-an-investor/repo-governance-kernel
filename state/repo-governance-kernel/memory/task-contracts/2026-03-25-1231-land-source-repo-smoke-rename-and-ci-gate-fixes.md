---
id: taskc-2026-03-25-1231-land-source-repo-smoke-rename-and-ci-gate-fixes
type: task-contract
title: "Land source-repo smoke rename and CI gate fixes"
status: completed
project_id: repo-governance-kernel
workspace_id: ws-1490b759
workspace_root: C:/Users/terryzzb/Desktop/session-memory
branch: master
git_sha: 59745309e19dbca9365bc8c99e520c3a8ca467c9
paths:
  - .githooks
  - .github
  - README.md
  - docs
  - scripts
thread_ids: []
evidence_refs: []
tags:
  - task-contract
  - control-plane
confidence: high
created_at: 2026-03-25T12:31:57+08:00
updated_at: 2026-03-25T12:54:54+08:00
objective_id: obj-2026-03-23-0002
phase: execution
round_id: "round-2026-03-25-1116-start-explicit-package-config-layering-for-a4"
supersedes: []
superseded_by: []
---

## Summary

Keep the source repo honest while landing the Python 3.11 smoke fix and the repo acceptance smoke rename.

## Intent

Carry the renamed repo acceptance smoke surface and Python 3.11 source-repo smoke fix through commit without leaving CI or local hook paths outside active task coverage.

## Allowed Changes

- Rename the top-level source-repo smoke surface and update CI, hook, CLI, and live documentation references to the new acceptance name.
- Keep the source-repo smoke path Python 3.11 compatible so the same acceptance surface runs locally and on GitHub Actions.

## Forbidden Changes

- Do not broaden package-facing mutation authority or change package command semantics beyond the source-repo smoke and documentation surfaces needed for this landing.
- Do not rewrite historical snapshot or memory records only to erase old phase-1 wording.

## Completion Criteria

- The renamed repo acceptance smoke passes under Python 3.11 through both direct script and scripts/repo_governance_kernel.py smoke entrypoints.
- audit-control-state and enforce-worktree return ok on the source repository with the landing task active.
- The resulting change set can be committed without task-coverage enforcement blocking .githooks or .github paths.

## Resolution

- Renamed scripts/smoke_phase1.py to scripts/smoke_repo_acceptance.py and updated live references in CI, hooks, CLI, and docs.
- Fixed the Python 3.11 parser-incompatible f-string in scripts/smoke_repo_onboarding.py and revalidated the renamed acceptance surface.

## Active Risks

- The source repo can still claim a renamed acceptance surface dishonestly if CI, hooks, CLI aliases, and docs drift apart.

## Status Notes

active -> completed: The renamed repo acceptance smoke surface, CI gate updates, and Python 3.11 source-repo smoke fix are now committed.

resolution recorded:
- Renamed scripts/smoke_phase1.py to scripts/smoke_repo_acceptance.py and updated live references in CI, hooks, CLI, and docs.
- Fixed the Python 3.11 parser-incompatible f-string in scripts/smoke_repo_onboarding.py and revalidated the renamed acceptance surface.

