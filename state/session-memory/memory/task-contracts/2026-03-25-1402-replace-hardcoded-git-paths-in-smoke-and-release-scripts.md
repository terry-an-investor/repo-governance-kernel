---
id: taskc-2026-03-25-1402-replace-hardcoded-git-paths-in-smoke-and-release-scripts
type: task-contract
title: "Replace hardcoded git paths in smoke and release scripts"
status: completed
project_id: session-memory
workspace_id: ws-1490b759
workspace_root: C:/Users/terryzzb/Desktop/session-memory
branch: master
git_sha: 5900e057f83b733d1c02d997617ef95f94646552
paths:
  - scripts/git_exec.py
  - scripts/smoke_assess_host_adoption.py
  - scripts/smoke_config_runtime.py
  - scripts/smoke_fixture_lib.py
  - scripts/smoke_kernel_bootstrap.py
  - scripts/smoke_repo_onboarding.py
  - scripts/smoke_wind_agent_snapshot_bootstrap.py
  - scripts/verify_release_publication.py
thread_ids: []
evidence_refs: []
tags:
  - task-contract
  - control-plane
confidence: high
created_at: 2026-03-25T14:02:40+08:00
updated_at: 2026-03-25T14:10:55+08:00
objective_id: obj-2026-03-23-0002
phase: execution
round_id: "round-2026-03-25-1402-make-smoke-git-resolution-ci-portable"
supersedes: []
superseded_by: []
---

## Summary

Land one shared git executable resolver and migrate the affected smoke and release verification scripts to it so CI and Windows local runs share the same owner layer.

## Intent

Remove Windows-only git executable assumptions from repo-owned smoke and release verification scripts and validate the resulting cross-platform path.

## Allowed Changes

- Add a shared repo-owned git executable resolver for scripts.
- Rewrite the affected smoke and release scripts to call the shared resolver.
- Run direct smoke validation and the repo acceptance smoke for the changed paths.

## Forbidden Changes

- Do not broaden this round into unrelated product or workflow changes.
- Do not introduce separate per-script fallback logic outside the shared resolver.

## Completion Criteria

- The changed smoke and release scripts all consume the shared git resolver and the targeted smoke validations pass.

## Resolution

- Added scripts/git_exec.py, rewrote the affected smoke and release verification scripts to consume it, and validated the path with smoke_config_runtime, smoke_repo_onboarding, smoke_kernel_bootstrap, verify_release_publication --help, smoke_repo_acceptance, and GitHub Actions run 23527409033.

## Active Risks

_none recorded_

## Status Notes

active -> completed: The shared git executable resolver landed, the affected scripts were migrated, and the targeted smoke plus CI validations passed.

resolution recorded:
- Added scripts/git_exec.py, rewrote the affected smoke and release verification scripts to consume it, and validated the path with smoke_config_runtime, smoke_repo_onboarding, smoke_kernel_bootstrap, verify_release_publication --help, smoke_repo_acceptance, and GitHub Actions run 23527409033.
