---
id: round-2026-03-23-1638-broaden-adjudication-executor-coverage
type: round-contract
title: "Broaden adjudication executor coverage"
status: active
project_id: session-memory
workspace_id: ws-1490b759
workspace_root: C:/Users/terryzzb/Desktop/session-memory
branch: master
git_sha: 76bea946dd7920915a34c0def4894f74b383a0cc
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
created_at: 2026-03-23T16:38:13+08:00
updated_at: 2026-03-23T16:38:13+08:00
objective_id: obj-2026-03-23-0002
phase: execution
supersedes: []
superseded_by: []
---

## Summary

A broader adjudication execution slice with clearer structured follow-up contract and at least one additional validated path or explicit boundary.

## Scope

- Extend structured adjudication follow-ups beyond the first supported subset without letting executor logic guess intent.
- Decide whether structured follow-up schema should stay as executor JSON bullets or move into richer adjudication fields.
- Validate at least one additional supported follow-up path or explicit blocked boundary with disposable fixtures and live audit.

## Deliverable

A broader adjudication execution slice with clearer structured follow-up contract and at least one additional validated path or explicit boundary.

## Validation Plan

Add targeted adjudication regression, rerun audit-control-state, then rerun full phase-1 smoke.

## Active Risks

_none recorded_

## Blockers

_none recorded_

## Status Notes

_none recorded_
