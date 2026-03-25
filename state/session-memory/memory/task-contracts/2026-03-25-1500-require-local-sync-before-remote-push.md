---
id: taskc-2026-03-25-1500-require-local-sync-before-remote-push
type: task-contract
title: "Require local sync before remote push"
status: completed
project_id: session-memory
workspace_id: ws-1490b759
workspace_root: C:/Users/terryzzb/Desktop/session-memory
branch: master
git_sha: dac91cb3add4232dd3f5167565a073ad020c5c29
paths:
  - AGENTS.md
  - docs/canonical/RELEASE.md
thread_ids: []
evidence_refs: []
tags:
  - task-contract
  - control-plane
confidence: high
created_at: 2026-03-25T15:00:33+08:00
updated_at: 2026-03-25T15:02:19+08:00
objective_id: obj-2026-03-23-0002
phase: execution
round_id: "round-2026-03-25-1500-require-local-sync-before-remote-push"
supersedes: []
superseded_by: []
---

## Summary

Make push ordering explicit so release and control truth are synced locally before any remote mutation.

## Intent

Encode local close-out before push as a repo-owned rule instead of relying on operator memory.

## Allowed Changes

- Update repo rules and release docs to require task/round close-out, anchor refresh, and clean audit/enforcement before pushing.
- Clarify release cut ordering so tags are created locally against the release commit before branch and tag push.

## Forbidden Changes

- Do not broaden product capability or mutate unrelated workflow rules.

## Completion Criteria

- AGENTS.md and RELEASE.md both require local sync before push.
- audit_product_docs, audit-control-state, and enforce-worktree return ok after the rule change.

## Resolution

- repo rules now require local task/round close-out, anchor refresh, paused phase recovery, and clean audit/enforcement before push
- the canonical release checklist now requires tagging locally, syncing the release round locally, and only then pushing branch and tag

## Active Risks

_none recorded_

## Status Notes

active -> completed: the local push-order rule is now encoded in AGENTS.md and RELEASE.md in commit dac91cb

resolution recorded:
- repo rules now require local task/round close-out, anchor refresh, paused phase recovery, and clean audit/enforcement before push
- the canonical release checklist now requires tagging locally, syncing the release round locally, and only then pushing branch and tag
