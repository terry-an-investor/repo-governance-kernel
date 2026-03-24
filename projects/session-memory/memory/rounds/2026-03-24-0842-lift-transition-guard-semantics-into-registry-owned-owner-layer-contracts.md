---
id: round-2026-03-24-0842-lift-transition-guard-semantics-into-registry-owned-owner-layer-contracts
type: round-contract
title: "Lift transition guard semantics into registry-owned owner-layer contracts"
status: active
project_id: session-memory
workspace_id: ws-1490b759
workspace_root: C:/Users/terryzzb/Desktop/session-memory
branch: master
git_sha: d77385036afc78caa4459d488bc9385fdec51cd4
paths:
  - scripts/transition_specs.py
  - scripts/round_control.py
  - scripts/audit_control_state.py
  - scripts/list_transition_registry.py
  - CONTROL_SYSTEM.md
  - TRANSITION_COMMANDS.md
thread_ids: []
evidence_refs: []
tags:
  - round
  - control-plane
confidence: high
created_at: 2026-03-24T08:42:32+08:00
updated_at: 2026-03-24T08:42:32+08:00
objective_id: obj-2026-03-23-0002
phase: execution
supersedes: []
superseded_by: []
---

## Summary

Transition guard rendering is declared in the machine-readable registry and consumed through shared owner-layer helpers instead of per-domain private maps.

## Scope

- Lift transition guard semantics into registry-owned owner-layer contracts.
- Remove per-domain private guard-text ownership from shared consumers where the registry can own it.

## Deliverable

Transition guard rendering is declared in the machine-readable registry and consumed through shared owner-layer helpers instead of per-domain private maps.

## Validation Plan

Run py_compile on changed scripts, export the registry, run targeted control audit/enforcement, and close the round back to paused.

## Active Risks

_none recorded_

## Blockers

_none recorded_

## Status Notes

_none recorded_
