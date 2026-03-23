---
id: round-2026-03-23-1649-expand-adjudication-rewrite-bundles
type: round-contract
title: "Expand adjudication rewrite bundles"
status: active
project_id: session-memory
workspace_id: ws-1490b759
workspace_root: C:/Users/terryzzb/Desktop/session-memory
branch: master
git_sha: 543d21175ed79f2f99f9639e6e43ff00b2c3aea1
paths:
  - scripts/execute_adjudication_followups.py
  - scripts/adjudicate_control_state.py
  - scripts/smoke_adjudication_followups.py
  - projects/session-memory/
thread_ids: []
evidence_refs: []
tags:
  - round
  - control-plane
confidence: high
created_at: 2026-03-23T16:49:58+08:00
updated_at: 2026-03-23T16:49:58+08:00
objective_id: obj-2026-03-23-0002
phase: execution
supersedes: []
superseded_by: []
---

## Summary

A broader adjudication execution layer that can apply one additional multi-step rewrite bundle while preserving honest blocked boundaries.

## Scope

- Add one more safe adjudication execution bundle beyond the current structured subset, such as a multi-step round close chain or a governed objective close bundle.
- Keep machine-executable follow-up contracts explicit and bounded instead of inferring them from verdict prose.
- Validate at least one richer adjudication rewrite bundle on disposable fixtures and the live control state.

## Deliverable

A broader adjudication execution layer that can apply one additional multi-step rewrite bundle while preserving honest blocked boundaries.

## Validation Plan

Add targeted bundle regression, rerun audit-control-state, then rerun full phase-1 smoke.

## Active Risks

_none recorded_

## Blockers

_none recorded_

## Status Notes

_none recorded_
