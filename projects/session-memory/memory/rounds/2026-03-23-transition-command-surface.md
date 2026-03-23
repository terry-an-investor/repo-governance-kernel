---
id: round-2026-03-23-0001
type: round-contract
title: Freeze transition command surface and round architecture
status: active
project_id: session-memory
workspace_id: ws-1490b759
workspace_root: C:/Users/terryzzb/Desktop/session-memory
branch: master
git_sha: 28ce1ee53c5e071c3797ec9c4dd7bb766fb21c93
paths:
  - STATE_MACHINE.md
  - TRANSITION_COMMANDS.md
  - SCHEMA.md
  - ARCHITECTURE.md
  - projects/session-memory/control/active-round.md
thread_ids: []
evidence_refs:
  - type: doc
    ref: C:/Users/terryzzb/Desktop/session-memory/STATE_MACHINE.md
  - type: doc
    ref: C:/Users/terryzzb/Desktop/session-memory/CONTROL_SYSTEM.md
tags:
  - round
  - control-plane
  - transition-command-surface
confidence: high
created_at: 2026-03-23T23:20:00+08:00
updated_at: 2026-03-23T23:20:00+08:00
objective_id: obj-2026-03-23-0002
phase: execution
supersedes: []
superseded_by: []
---

## Summary

Freeze the canonical transition command surface and add the missing round and
transition object paths before implementing enforcement code.

## Scope

- define the future transition commands
- define guards and side effects
- add canonical round paths to the schema
- create one real active-round sample

## Deliverable

Canonical docs and sample files that make future command implementation honest
instead of ad hoc.

## Validation Plan

- docs are mutually consistent
- round paths exist in schema and architecture
- the sample active round reflects the real current design work

## Active Risks

- command surface may still be too broad for the first implementation slice
- no transition engine exists yet to enforce these semantics

## Blockers

- enforcement commands are still unimplemented

## Status Notes

This round is design-first. It should freeze the control-plane command surface
without pretending that transition enforcement already exists.
