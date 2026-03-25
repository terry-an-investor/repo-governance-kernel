---
id: taskc-2026-03-25-1622-land-the-0-1-0b0-beta-release-identity
type: task-contract
title: "Land the 0.1.0b0 beta release identity"
status: completed
project_id: session-memory
workspace_id: ws-1490b759
workspace_root: C:/Users/terryzzb/Desktop/session-memory
branch: master
git_sha: 5dd4f9ce31622b737f88f06b244500f790a1c726
paths:
  - pyproject.toml
  - README.md
  - kernel
  - docs
  - scripts/smoke_kernel_bootstrap.py
  - scripts/verify_release_publication.py
  - uv.lock
  - skills/use-repo-governance-kernel/SKILL.md
thread_ids: []
evidence_refs: []
tags:
  - task-contract
  - control-plane
confidence: high
created_at: 2026-03-25T16:22:21+08:00
updated_at: 2026-03-25T16:38:02+08:00
objective_id: obj-2026-03-23-0002
phase: execution
round_id: "round-2026-03-25-1621-cut-the-0-1-0b0-beta-release"
supersedes: []
superseded_by: []
---

## Summary

Promote the package from 0.1.0a5 preview identity to 0.1.0b0 beta identity across version truth, public surface naming, docs, smoke, and release records.

## Intent

Make the published package identity, public surface descriptor, validation evidence, and release artifacts say the same thing before remote publication.

## Allowed Changes

- Rename stale alpha-specific public surface names to formal public surface names where they define package-facing release truth.
- Update version truth, package docs, canonical docs, and smoke expectations to the 0.1.0b0 beta line.
- Build release artifacts, tag the release commit, publish the GitHub Release, and verify publication truth.

## Forbidden Changes

- Do not widen product authority beyond the bounded beta contract already frozen in the owner layer.
- Do not leave conflicting alpha and beta release identities in code, docs, or release records.

## Completion Criteria

- The repository produces 0.1.0b0 wheel and sdist artifacts and the package-facing surface reports beta release identity consistently.
- The annotated v0.1.0b0 tag, GitHub Release, release assets, and publication verification all point at the intended beta release commit.

## Resolution

- package metadata, public-surface naming, docs, smoke expectations, packaged skill guidance, and uv lock version truth now align on 0.1.0b0
- beta validation passed across docs audit, onboarding, assessment, hard-gate, bundle-gate, acceptance, describe-public-surface, enforce-worktree, and uv build
- annotated tag v0.1.0b0 now points at release commit 5dd4f9c

## Active Risks

_none recorded_

## Status Notes

Task contract rewritten because beta release identity includes version-locked uv metadata and the packaged repo skill command reference

Expanded beta release task scope to cover uv lock version truth and the packaged skill command reference after the public-surface rename.

active -> completed: the 0.1.0b0 beta release identity, validation matrix, artifacts, and release tag are now all landed locally

resolution recorded:
- package metadata, public-surface naming, docs, smoke expectations, packaged skill guidance, and uv lock version truth now align on 0.1.0b0
- beta validation passed across docs audit, onboarding, assessment, hard-gate, bundle-gate, acceptance, describe-public-surface, enforce-worktree, and uv build
- annotated tag v0.1.0b0 now points at release commit 5dd4f9c

Completed after landing the beta release commit and tagging the exact release commit before close-out.
