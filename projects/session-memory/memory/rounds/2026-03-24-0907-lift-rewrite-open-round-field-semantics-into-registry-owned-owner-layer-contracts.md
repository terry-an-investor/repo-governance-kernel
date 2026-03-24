---
id: round-2026-03-24-0907-lift-rewrite-open-round-field-semantics-into-registry-owned-owner-layer-contracts
type: round-contract
title: "Generalize bundle governance and institutionalize bundle exceptions"
status: active
project_id: session-memory
workspace_id: ws-1490b759
workspace_root: C:/Users/terryzzb/Desktop/session-memory
branch: master
git_sha: 54b3538e95f0dc2a749ed553cb76760703e50b87
paths:
  - scripts/transition_specs.py
  - scripts/execute_adjudication_followups.py
  - scripts/audit_control_state.py
  - CONTROL_SYSTEM.md
  - TRANSITION_COMMANDS.md
  - projects/session-memory/current/current-task.md
thread_ids: []
evidence_refs: []
tags:
  - round
  - control-plane
confidence: high
created_at: 2026-03-24T09:07:16+08:00
updated_at: 2026-03-24T09:41:34+08:00
objective_id: obj-2026-03-23-0002
phase: execution
supersedes: []
superseded_by: []
---

## Summary

Stop broadening bundle-local semantics ad hoc and establish repo-owned rules for when a bundle wrapper may exist and how it must be constrained.

## Scope

- Generalize the bundle problem beyond round-close-chain and define the repo law for bundle wrappers versus primitive transition commands.
- Move bundle wrapper admission out of local literals into one explicit owner-layer governance surface that executor and plan validation both consume.
- Update canonical docs and current-task so bundle governance is treated as a system rule, not an implementation afterthought.

## Deliverable

Bundle wrappers are governed by explicit repo-owned rules and one narrow machine-readable governance surface instead of private ad hoc exceptions.

## Validation Plan

Run py_compile, transition registry export, adjudication follow-up smoke, control audit, and worktree enforcement after bundle governance law lands.

## Active Risks

_none recorded_

## Blockers

_none recorded_

## Status Notes

_none recorded_

Round rewritten because Scope shifted from continuing bundle-semantic registration to bundle governance institutionalization.
