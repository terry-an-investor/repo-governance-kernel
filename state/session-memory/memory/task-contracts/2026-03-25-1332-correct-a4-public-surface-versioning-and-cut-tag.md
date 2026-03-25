---
id: taskc-2026-03-25-1332-correct-a4-public-surface-versioning-and-cut-tag
type: task-contract
title: "Correct a4 public-surface versioning and cut tag"
status: active
project_id: session-memory
workspace_id: ws-1490b759
workspace_root: C:/Users/terryzzb/Desktop/session-memory
branch: master
git_sha: 275379b93571a3181418ef2d7a1c4c9fe9c5e5b8
paths:
  - kernel
  - docs
  - README.md
thread_ids: []
evidence_refs: []
tags:
  - task-contract
  - control-plane
confidence: high
created_at: 2026-03-25T13:32:22+08:00
updated_at: 2026-03-25T13:32:23+08:00
objective_id: obj-2026-03-23-0002
phase: execution
round_id: "round-2026-03-25-1332-correct-a4-release-semantics-and-cut-real-tag"
supersedes: []
superseded_by: []
---

## Summary

Fix the externally wrong a4 release story by aligning machine-readable/public docs with the current preview and by creating the missing git tag.

## Intent

Stop the current package and docs from reporting a3 as the live release identity after the a4 cut, then publish the missing a4 tag.

## Allowed Changes

- Update public-surface version descriptors so the current preview reports 0.1.0a4 while still recording that the entrypoint set was first frozen in 0.1.0a3.
- Create and push one a4 git tag after the corrected release story is revalidated.

## Forbidden Changes

- Do not broaden the public alpha command set under the cover of a version-story correction.
- Do not cut an a5 version or change package metadata away from 0.1.0a4 in this round.

## Completion Criteria

- Machine-readable and release-facing surfaces report the current preview as 0.1.0a4 without hiding that the command set was first frozen in 0.1.0a3.
- Origin contains one a4 git tag pointing at the corrected release commit.
- audit-control-state and enforce-worktree remain ok after the correction.

## Resolution

_none recorded_

## Active Risks

- If a4 still emits a3 from its public descriptor, users and agents will keep reading the installed package as the wrong release line.

## Status Notes

_none recorded_
