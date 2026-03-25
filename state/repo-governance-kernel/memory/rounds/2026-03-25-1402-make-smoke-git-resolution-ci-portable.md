---
id: round-2026-03-25-1402-make-smoke-git-resolution-ci-portable
type: round-contract
title: "Make smoke git resolution CI-portable"
status: closed
project_id: repo-governance-kernel
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
  - round
  - control-plane
confidence: high
created_at: 2026-03-25T14:02:22+08:00
updated_at: 2026-03-25T14:11:42+08:00
objective_id: obj-2026-03-23-0002
phase: execution
supersedes: []
superseded_by: []
---

## Summary

A repo-owned cross-platform git resolution layer with passing smoke validation for the affected script surfaces.

## Scope

- Add one shared git executable resolver for repo-owned smoke and release verification scripts.
- Rewrite each affected smoke or release verifier entrypoint to consume the shared resolver instead of a hardcoded Windows path.
- Validate the changed paths with direct smoke runs and the repo acceptance smoke.

## Deliverable

A repo-owned cross-platform git resolution layer with passing smoke validation for the affected script surfaces.

## Validation Plan

Run smoke_config_runtime, smoke_repo_onboarding, smoke_kernel_bootstrap, verify_release_publication --help, and smoke_repo_acceptance after the resolver rewrite.
uv run python scripts/smoke_config_runtime.py; uv run python scripts/smoke_repo_onboarding.py; uv run python scripts/smoke_kernel_bootstrap.py; uv run python scripts/verify_release_publication.py --help; uv run python scripts/smoke_repo_acceptance.py; GitHub Actions run 23527409033
uv run python scripts/smoke_config_runtime.py; uv run python scripts/smoke_repo_onboarding.py; uv run python scripts/smoke_kernel_bootstrap.py; uv run python scripts/verify_release_publication.py --help; uv run python scripts/smoke_repo_acceptance.py; GitHub Actions run 23527409033
GitHub Actions run 23527409033

## Active Risks

_none recorded_

## Blockers

_none recorded_

## Status Notes

active -> validation_pending: The bounded CI portability implementation is complete and ready for explicit validation capture.

validated by:
- uv run python scripts/smoke_config_runtime.py; uv run python scripts/smoke_repo_onboarding.py; uv run python scripts/smoke_kernel_bootstrap.py; uv run python scripts/verify_release_publication.py --help; uv run python scripts/smoke_repo_acceptance.py; GitHub Actions run 23527409033

validation_pending -> captured: The implementation and validation evidence for the CI portability fix are now recorded.

validated by:
- uv run python scripts/smoke_config_runtime.py; uv run python scripts/smoke_repo_onboarding.py; uv run python scripts/smoke_kernel_bootstrap.py; uv run python scripts/verify_release_publication.py --help; uv run python scripts/smoke_repo_acceptance.py; GitHub Actions run 23527409033

captured -> closed: The CI portability round is complete and its validated result is now captured in durable history.

validated by:
- GitHub Actions run 23527409033

