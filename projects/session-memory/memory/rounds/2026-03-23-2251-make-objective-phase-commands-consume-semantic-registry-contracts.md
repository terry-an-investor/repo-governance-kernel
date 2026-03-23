---
id: round-2026-03-23-2251-make-objective-phase-commands-consume-semantic-registry-contracts
type: round-contract
title: "Make objective-phase commands consume semantic registry contracts"
status: active
project_id: session-memory
workspace_id: ws-1490b759
workspace_root: C:/Users/terryzzb/Desktop/session-memory
branch: master
git_sha: 933fae18411c468f3cc506becf8da057b59edeb2
paths:
  - scripts/round_control.py
  - scripts/open_objective.py
  - scripts/close_objective.py
  - scripts/record_soft_pivot.py
  - scripts/record_hard_pivot.py
  - scripts/set_phase.py
  - scripts/audit_control_state.py
  - CONTROL_SYSTEM.md
  - TRANSITION_COMMANDS.md
thread_ids: []
evidence_refs: []
tags:
  - round
  - control-plane
confidence: high
created_at: 2026-03-23T22:51:58+08:00
updated_at: 2026-03-23T22:51:58+08:00
objective_id: obj-2026-03-23-0002
phase: execution
supersedes: []
superseded_by: []
---

## Summary

Objective/phase commands and audit consume one shared registry-backed owner-layer semantics helper, reducing semantic drift outside the round domain.

## Scope

- Extract shared objective/phase owner-layer semantics and make objective-line plus set-phase commands consume them.

## Deliverable

Objective/phase commands and audit consume one shared registry-backed owner-layer semantics helper, reducing semantic drift outside the round domain.

## Validation Plan

Run real-project audit and enforce-worktree, then close the round and return the objective to paused.

## Active Risks

_none recorded_

## Blockers

_none recorded_

## Status Notes

_none recorded_
