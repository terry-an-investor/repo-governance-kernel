---
id: taskc-2026-03-25-1500-require-local-sync-before-remote-push
type: task-contract
title: "Require local sync before remote push"
status: active
project_id: session-memory
workspace_id: ws-1490b759
workspace_root: C:/Users/terryzzb/Desktop/session-memory
branch: master
git_sha: 156be43430c10b020a8f16eed7ff6d0a39c37525
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
updated_at: 2026-03-25T15:00:33+08:00
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

_none recorded_

## Active Risks

_none recorded_

## Status Notes

_none recorded_
