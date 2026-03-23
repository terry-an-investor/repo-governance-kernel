---
id: round-2026-03-23-1619-implement-adjudication-follow-up-rewrite-slice
type: round-contract
title: "Implement adjudication follow-up rewrite slice"
status: active
project_id: session-memory
workspace_id: ws-1490b759
workspace_root: C:/Users/terryzzb/Desktop/session-memory
branch: master
git_sha: d7af73f203cc6011b645485368685954b2876164
paths:
  - scripts/execute_adjudication_followups.py
  - scripts/adjudicate_control_state.py
  - scripts/round_control.py
  - projects/session-memory/
thread_ids: []
evidence_refs: []
tags:
  - round
  - control-plane
confidence: high
created_at: 2026-03-23T16:19:46+08:00
updated_at: 2026-03-23T16:19:46+08:00
objective_id: obj-2026-03-23-0002
phase: execution
supersedes: []
superseded_by: []
---

## Summary

A real adjudication follow-up slice that can execute at least one non-trivial durable control rewrite from a durable adjudication record.

## Scope

- Turn execute-adjudication-followups from scaffold-only behavior into real durable control rewrites for supported verdict shapes.
- Keep adjudication, repair, and transition execution separate while proving at least one honest follow-up path beyond scaffolding.
- Validate the new adjudication path on disposable fixtures and current project control state without introducing fake automation.

## Deliverable

A real adjudication follow-up slice that can execute at least one non-trivial durable control rewrite from a durable adjudication record.

## Validation Plan

Add disposable adjudication fixtures, run targeted adjudication smoke, then rerun audit-control-state and full phase-1 smoke.

## Active Risks

_none recorded_

## Blockers

_none recorded_

## Status Notes

_none recorded_
