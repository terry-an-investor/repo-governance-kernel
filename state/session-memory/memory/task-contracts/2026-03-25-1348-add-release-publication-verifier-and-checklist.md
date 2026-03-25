---
id: taskc-2026-03-25-1348-add-release-publication-verifier-and-checklist
type: task-contract
title: "Add release publication verifier and checklist"
status: completed
project_id: session-memory
workspace_id: ws-1490b759
workspace_root: C:/Users/terryzzb/Desktop/session-memory
branch: master
git_sha: 94badecd4ce4fa3ae52b8fcab8c9e58096927200
paths:
  - scripts
  - docs
  - README.md
  - .github
thread_ids: []
evidence_refs: []
tags:
  - task-contract
  - control-plane
confidence: high
created_at: 2026-03-25T13:48:28+08:00
updated_at: 2026-03-25T13:52:11+08:00
objective_id: obj-2026-03-23-0002
phase: execution
round_id: "round-2026-03-25-1348-add-release-publication-verifier-and-checklist"
supersedes: []
superseded_by: []
---

## Summary

Make release completion auditable by adding one repo-owned verifier for remote branch, tag, release object, and assets, then wire it into canonical release instructions.

## Intent

Stop future release cuts from ending at push or tag by making remote publication verification an explicit repo-owned step.

## Allowed Changes

- Add one repo-owned script that verifies remote branch head, release tag, GitHub Release object, and expected assets for a version.
- Update release-facing docs to include the verifier and a concrete publication checklist.

## Forbidden Changes

- Do not broaden package command semantics or release another version as part of this process fix.
- Do not depend on unstated manual GitHub UI checks as the only release completion proof.

## Completion Criteria

- One repo-owned verifier can confirm that v0.1.0a4 exists on origin as both a tag and a GitHub Release with the expected assets.
- Canonical release docs include an explicit post-push publication checklist and verification step.
- audit-control-state and enforce-worktree remain ok after the process fix.

## Resolution

- Added scripts/verify_release_publication.py plus the session_memory.py alias so one repo-owned command can verify remote branch, tag, GitHub Release object, and expected assets for a version.
- Updated docs/canonical/RELEASE.md to include a concrete publication checklist and verifier usage, including the difference between immediate cut verification and later historical release audit.

## Active Risks

- If release publication remains an implicit memory step, future cuts can still stop at push or tag and be mistaken for complete releases.

## Status Notes

active -> completed: The repo now has a release publication verifier and canonical checklist for remote release completion.

resolution recorded:
- Added scripts/verify_release_publication.py plus the session_memory.py alias so one repo-owned command can verify remote branch, tag, GitHub Release object, and expected assets for a version.
- Updated docs/canonical/RELEASE.md to include a concrete publication checklist and verifier usage, including the difference between immediate cut verification and later historical release audit.

active -> completed: Release publication is now an auditable repo-owned step instead of a memory-only step.
