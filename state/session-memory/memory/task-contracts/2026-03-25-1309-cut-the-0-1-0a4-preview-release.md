---
id: taskc-2026-03-25-1309-cut-the-0-1-0a4-preview-release
type: task-contract
title: "Cut the 0.1.0a4 preview release"
status: active
project_id: session-memory
workspace_id: ws-1490b759
workspace_root: C:/Users/terryzzb/Desktop/session-memory
branch: master
git_sha: f8bcaaa227040371b83759566be5fab542de7927
paths:
  - pyproject.toml
  - uv.lock
  - README.md
  - kernel
  - docs
thread_ids: []
evidence_refs: []
tags:
  - task-contract
  - control-plane
confidence: high
created_at: 2026-03-25T13:09:39+08:00
updated_at: 2026-03-25T13:09:39+08:00
objective_id: obj-2026-03-23-0002
phase: execution
round_id: "round-2026-03-25-1116-start-explicit-package-config-layering-for-a4"
supersedes: []
superseded_by: []
---

## Summary

Promote the landed a4 config-layering slice into the actual 0.1.0a4 preview by updating package metadata, release-facing docs, and package proof.

## Intent

Finish a4 as a versioned preview release instead of leaving the package metadata and release docs at a3 after the config-layering and installability work has already landed.

## Allowed Changes

- Bump the package version from 0.1.0a3 to 0.1.0a4 in release-owned metadata and aligned package-facing docs.
- Refresh release evidence so the current preview release, next target line, build artifact names, and installed-wheel proof all describe the actual a4 cut.

## Forbidden Changes

- Do not broaden the frozen public alpha command set under the cover of an a4 version cut.
- Do not claim provider-level or model-level config support that the shared runtime does not yet implement.

## Completion Criteria

- Package metadata and release-facing docs agree that the current preview release is 0.1.0a4 and the next planned cut is 0.1.0a5.
- Build and installed-wheel proof pass against 0.1.0a4 artifacts.
- audit-control-state and enforce-worktree remain ok after the release cut.

## Resolution

_none recorded_

## Active Risks

- If current release docs keep saying a3, installed users will not know whether the config-layering runtime is actually part of the published preview.

## Status Notes

_none recorded_
