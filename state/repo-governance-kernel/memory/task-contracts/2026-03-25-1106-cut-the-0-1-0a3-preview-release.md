---
id: taskc-2026-03-25-1106-cut-the-0-1-0a3-preview-release
type: task-contract
title: "Cut the 0.1.0a3 preview release"
status: completed
project_id: repo-governance-kernel
workspace_id: ws-1490b759
workspace_root: C:/Users/terryzzb/Desktop/session-memory
branch: master
git_sha: 0fcdc4fc4110039273ff0f761eebe95870db9551
paths:
  - pyproject.toml
  - uv.lock
  - docs
  - README.md
  - kernel/README.md
  - scripts
thread_ids: []
evidence_refs: []
tags:
  - task-contract
  - control-plane
confidence: high
created_at: 2026-03-25T11:06:51+08:00
updated_at: 2026-03-25T11:08:57+08:00
objective_id: obj-2026-03-23-0002
phase: execution
round_id: "round-2026-03-25-0946-make-package-first-repo-onboarding-real"
supersedes: []
superseded_by: []
---

## Summary

Promote the completed a3 feature line into the actual 0.1.0a3 preview by updating package metadata, release-facing docs, and package proof.

## Intent

Finish a3 as a versioned preview release rather than leaving the package metadata and docs at a2 while the a3 surface is already complete.

## Allowed Changes

- Bump the package version from 0.1.0a2 to 0.1.0a3 in release-owned metadata.
- Update release-facing docs and command examples to treat a3 as the current preview release.
- Rebuild and validate the installed-wheel package proof against 0.1.0a3 artifacts.

## Forbidden Changes

- Do not broaden product scope or add new command surfaces during the release cut.
- Do not ship unvalidated package metadata or stale artifact names.

## Completion Criteria

- Package metadata and release-facing docs agree that the current preview release is 0.1.0a3.
- Build and installed-wheel smoke proof pass against 0.1.0a3 artifacts.
- Audit and enforcement remain clean after the release cut.

## Resolution

- Bumped package metadata and release-facing docs from 0.1.0a2 to 0.1.0a3 and advanced the next target line to 0.1.0a4.
- Rebuilt the 0.1.0a3 sdist and wheel artifacts.
- Revalidated the installed-wheel package proof, including the public alpha surface descriptor.

## Active Risks

_none recorded_

## Status Notes

active -> completed: The a3 feature line is now cut as a validated 0.1.0a3 preview release.

resolution recorded:
- Bumped package metadata and release-facing docs from 0.1.0a2 to 0.1.0a3 and advanced the next target line to 0.1.0a4.
- Rebuilt the 0.1.0a3 sdist and wheel artifacts.
- Revalidated the installed-wheel package proof, including the public alpha surface descriptor.

