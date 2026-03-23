---
id: round-2026-03-23-1213-implement-first-transition-slice
type: round-contract
title: "Implement first transition command slice"
status: active
project_id: session-memory
workspace_id: ws-1490b759
workspace_root: C:/Users/terryzzb/Desktop/session-memory
branch: master
git_sha: cb2047abe10b8520e6a0b26d4ddc13250d5344e2
paths:
  - scripts/open_round.py
  - scripts/update_round_status.py
  - scripts/round_control.py
  - scripts/session_memory.py
  - projects/session-memory/control/active-round.md
thread_ids: []
evidence_refs: []
tags:
  - round
  - control-plane
confidence: high
created_at: 2026-03-23T12:13:22+08:00
updated_at: 2026-03-23T12:24:08+08:00
objective_id: obj-2026-03-23-0002
phase: execution
supersedes: []
superseded_by: []
---

## Summary

A working first transition slice that can open a round, move it through legal statuses, and write transition-event records.

## Scope

- implement open-round and update-round-status as real commands
- persist transition events for round commands
- validate the first enforced control-state transitions on session-memory

## Deliverable

A working first transition slice that can open a round, move it through legal statuses, and write transition-event records.

## Validation Plan

Run command-level transitions on the real session-memory round path and pass smoke after the new active round is opened.

## Active Risks

- Guard logic may still be too narrow for future objective and workaround transitions.
- Round file rewriting could regress frontmatter fidelity if metadata preservation is incomplete.

## Blockers

_none recorded_

## Status Notes

active -> blocked: metadata preservation validation via real transition

blocked -> active: round rewrite validation complete; resume implementation
