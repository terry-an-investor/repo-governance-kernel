---
id: round-2026-03-24-0830-lift-adjudication-followups-into-registry-owned-rewrite-semantics
type: round-contract
title: "Lift adjudication followups into registry-owned rewrite semantics"
status: active
project_id: session-memory
workspace_id: ws-1490b759
workspace_root: C:/Users/terryzzb/Desktop/session-memory
branch: master
git_sha: a4fe9a80c4afa3b901a927ebc81a1232babbb91a
paths:
  - scripts/transition_specs.py
  - scripts/compile_adjudication_executor_plan.py
  - scripts/execute_adjudication_followups.py
  - scripts/round_control.py
  - scripts/smoke_adjudication_followups.py
  - scripts/audit_control_state.py
  - CONTROL_SYSTEM.md
  - TRANSITION_COMMANDS.md
thread_ids: []
evidence_refs: []
tags:
  - round
  - control-plane
confidence: high
created_at: 2026-03-24T08:30:20+08:00
updated_at: 2026-03-24T08:30:20+08:00
objective_id: obj-2026-03-23-0002
phase: execution
supersedes: []
superseded_by: []
---

## Summary

Adjudication plan compilation is driven by registry-owned rewrite semantics for at least the currently supported bounded plan families, reducing private compiler semantics drift.

## Scope

- Move adjudication plan compilation closer to registry-owned executable rewrite semantics.
- Reduce per-plan private compiler branching in favor of machine-readable rewrite contract fields.

## Deliverable

Adjudication plan compilation is driven by registry-owned rewrite semantics for at least the currently supported bounded plan families, reducing private compiler semantics drift.

## Validation Plan

Compile changed scripts, run adjudication follow-up smoke coverage, run real-project audit and enforce, then close the round and return the objective to paused.

## Active Risks

_none recorded_

## Blockers

_none recorded_

## Status Notes

_none recorded_
