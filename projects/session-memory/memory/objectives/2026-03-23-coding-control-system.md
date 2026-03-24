---
id: obj-2026-03-23-0002
type: objective
title: "Coding control system built on a memory substrate"
status: active
project_id: session-memory
workspace_id: ws-1490b759
workspace_root: C:/Users/terryzzb/Desktop/session-memory
branch: master
git_sha: d2f0d9ccac241d8be477261932632c6d49d6ea32
paths:
  - CONTROL_SYSTEM.md
  - DESIGN_PRINCIPLES.md
  - ARCHITECTURE.md
  - SCHEMA.md
  - IMPLEMENTATION_PLAN.md
  - projects/session-memory/control/
thread_ids: []
evidence_refs:
  - type: doc
    ref: C:/Users/terryzzb/Desktop/session-memory/CONTROL_SYSTEM.md
  - type: doc
    ref: C:/Users/terryzzb/Desktop/session-memory/SCHEMA.md
  - type: note
    ref: C:/Users/terryzzb/Desktop/session-memory/projects/session-memory/current/current-task.md
tags:
  - objective
  - control-system
  - active
confidence: high
created_at: 2026-03-23T21:10:00+08:00
updated_at: 2026-03-24T11:22:35+08:00
phase: paused
supersedes:
  - obj-2026-03-23-0001
superseded_by: []
---

## Summary

The project should evolve from a memory-focused handoff system into a coding
control system that uses memory as its storage substrate.

## Problem

The real user pain is not only recovering facts. It is preserving direction,
containing temporary hacks, supporting project-aware review, and handling pivot
without losing provenance.

## Success Criteria

- active objective and pivot lineage are first-class
- context assembly prefers active control state over raw recency
- active exception contracts are tracked separately from target design
- reviewer or side-session contexts can be compiled from project control state

## Non-Goals

- generic role prompts without durable project knowledge
- replacing git or project docs
- broad semantic retrieval before file workflow proves itself

## Why Now

The file-first memory path is already proven enough to expose the real next
bottleneck: objective drift, uncontrolled exception-contract debt, and fresh sessions
that still lack an explicit control line.

## Current Phase

paused

## Active Risks

- The system can still regress into a memory-only framing if control objects do
  not become operational inputs.
- Overfitting the schema to one project's governance remains a risk.

## Supersession Notes

This objective replaces the narrower memory-and-handoff framing while retaining
its file-first storage and retrieval foundation.

Phase changed from `execution` to `paused` because Development is intentionally paused after closing the last bounded execution round, so the active objective should not remain marked as execution.

Phase changed from `paused` to `execution` because A short bounded execution slice is needed to codify the Win11-native tooling rule instead of leaving the repository in an ad hoc shell-selection state.

Phase changed from `execution` to `paused` because The short Win11-native tooling round is closed, so the active objective should return to paused instead of remaining in execution.

Phase changed from `paused` to `execution` because A bounded execution slice is needed to unify current-task owner-layer semantics across audit, enforcement, refresh, and docs.

Phase changed from `execution` to `paused` because The current-task owner-layer semantics round is closed, so the active objective should return to paused rather than remain in execution.

Phase changed from `paused` to `execution` because A bounded execution slice is needed to make objective/phase commands consume registry-backed owner-layer semantics without leaving partial helper changes unmanaged.

Phase changed from `execution` to `paused` because The bounded execution round for objective/phase registry consumer coverage is closed, so the objective should return to paused until the next execution slice is opened.

Phase changed from `paused` to `execution` because A bounded execution slice is needed to make current-task workspace anchor semantics explicitly snapshot-based instead of looking like self-updating live truth.

Phase changed from `execution` to `paused` because The bounded current-task snapshot-semantics round is closed, so the active objective should return to paused until the next execution slice is opened.

Phase changed from `paused` to `execution` because A bounded execution slice is needed to separate durable current-task control state from non-durable live workspace projection.

Phase changed from `execution` to `paused` because The bounded round that separated durable current-task control from live workspace projection is closed, so the active objective should return to paused.

Phase changed from `paused` to `execution` because A bounded execution slice is needed to move exception-contract and anchor-maintenance commands under the same registry-backed owner-layer contract and to add explicit owner fields that block private semantics drift.

Phase changed from `execution` to `paused` because Execution slice finished after registry-owner unification closed its bounded round.

Phase changed from `paused` to `execution` because A bounded governance slice is needed to remove caller-side duplication of registry-owned guard, write-target, and owner declarations so command callers stop restating static semantics already owned by the transition registry.

Phase changed from `execution` to `paused` because Caller-thinning governance slice finished after the bounded round closed.

Phase changed from `paused` to `execution` because A bounded execution slice is needed to move adjudication rewrite semantics toward a registry-owned executable contract instead of leaving plan compilation and target resolution scattered across compiler branches.

Phase changed from `execution` to `paused` because Registry-owned adjudication payload-template governance round is closed; objective returns to paused until the next executable-semantics slice opens.

Phase changed from `paused` to `execution` because Open a bounded governance round to lift transition guard rendering into registry-owned owner-layer semantics.

Phase changed from `execution` to `paused` because Registry-owned transition guard semantics governance round is closed; objective returns to paused until the next executable-semantics slice opens.

Phase changed from `paused` to `execution` because Open a bounded governance round to lift transition side-effect and write semantics into registry-owned owner-layer contracts.

Phase changed from `execution` to `paused` because Registry-owned write-target and side-effect semantics governance round is closed; objective returns to paused until the next executable-semantics slice opens.

Phase changed from `paused` to `execution` because Open a bounded governance round to lift rewrite-open-round field semantics into registry-owned owner-layer contracts.

Phase changed from `execution` to `paused` because Task-contract lifecycle and consumption slice is committed and its ratification round is closed, so the active objective should not remain in execution without an open round.

Phase changed from `paused` to `execution` because A bounded execution slice is needed to codify the default external clone root and inspect one reference repository under that same rule.

Phase changed from `execution` to `paused` because The bounded clone-root rule and xurl inspection round is closed, so the active objective should return to paused.

Phase changed from `paused` to `execution` because A bounded docs slice is needed to record the future xurl-based external session adapter as a canonical follow-up instead of leaving it as chat-only context.

Phase changed from `execution` to `paused` because The bounded xurl adapter follow-up round is closed, so the active objective should return to paused.
