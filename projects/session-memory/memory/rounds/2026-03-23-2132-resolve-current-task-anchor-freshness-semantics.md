---
id: round-2026-03-23-2132-resolve-current-task-anchor-freshness-semantics
type: round-contract
title: "Resolve current-task anchor freshness semantics"
status: active
project_id: session-memory
workspace_id: ws-1490b759
workspace_root: C:/Users/terryzzb/Desktop/session-memory
branch: master
git_sha: 646c4f1114410f17b2a401d09221f1084eea6c59
paths:
  - scripts/
  - projects/session-memory/
  - ARCHITECTURE.md
  - SCHEMA.md
  - CONTROL_SYSTEM.md
thread_ids: []
evidence_refs: []
tags:
  - round
  - control-plane
confidence: high
created_at: 2026-03-23T21:32:55+08:00
updated_at: 2026-03-23T21:32:55+08:00
objective_id: obj-2026-03-23-0002
phase: execution
supersedes: []
superseded_by: []
---

## Summary

A consistent freshness model where current-task anchor metadata is truthful, packet freshness no longer treats self-referential commit lag as a failure, and project control docs explain the rule.

## Scope

- Make current-task anchor semantics honest so committed control projections do not pretend to equal the commit that contains them.
- Adjust freshness assessment to treat live workspace revalidation as canonical when current-task anchor metadata is historical orientation data.
- Update canonical docs and project control state to reflect the corrected owner-layer freshness semantics.

## Deliverable

A consistent freshness model where current-task anchor metadata is truthful, packet freshness no longer treats self-referential commit lag as a failure, and project control docs explain the rule.

## Validation Plan

Validate assembled freshness behavior on the real project, rerun audit-control-state and enforce-worktree, and refresh current-task anchor under the corrected semantics.

## Active Risks

- A weak freshness downgrade could hide genuinely stale current-task narratives if live revalidation is not surfaced prominently.
- Changing anchor semantics without updating docs and packet guidance would create a silent control-language split.

## Blockers

_none recorded_

## Status Notes

_none recorded_
