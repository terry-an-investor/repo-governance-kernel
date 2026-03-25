---
id: taskc-2026-03-25-1332-correct-a4-public-surface-versioning-and-cut-tag
type: task-contract
title: "Correct a4 public-surface versioning and cut tag"
status: completed
project_id: repo-governance-kernel
workspace_id: ws-1490b759
workspace_root: C:/Users/terryzzb/Desktop/session-memory
branch: master
git_sha: 092d70cbe011a40d730a23b365d4e357b4decb94
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
updated_at: 2026-03-25T13:37:09+08:00
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

- Updated machine-readable and release-facing public-surface descriptors so the current preview reports 0.1.0a4 while recording 0.1.0a3 as the freeze lineage for the unchanged entrypoint set.
- Pushed commit 092d70c to origin and created the annotated tag v0.1.0a4 on that corrected release commit.

## Active Risks

- If a4 still emits a3 from its public descriptor, users and agents will keep reading the installed package as the wrong release line.

## Status Notes

active -> completed: The a4 release identity and missing tag are now corrected on origin.

resolution recorded:
- Updated machine-readable and release-facing public-surface descriptors so the current preview reports 0.1.0a4 while recording 0.1.0a3 as the freeze lineage for the unchanged entrypoint set.
- Pushed commit 092d70c to origin and created the annotated tag v0.1.0a4 on that corrected release commit.

active -> completed: The a4 public release identity and tag are now corrected.

