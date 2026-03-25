---
id: obj-2026-03-23-0002
type: objective
title: "Coding control system built on a memory substrate"
status: active
project_id: session-memory
workspace_id: ws-1490b759
workspace_root: C:/Users/terryzzb/Desktop/session-memory
branch: master
git_sha: 2b5145d2a5d306b61493b7706e76b2175d143c99
paths:
  - docs/canonical/CONTROL_SYSTEM.md
  - docs/canonical/DESIGN_PRINCIPLES.md
  - docs/canonical/ARCHITECTURE.md
  - docs/canonical/SCHEMA.md
  - docs/canonical/IMPLEMENTATION_PLAN.md
  - state/session-memory/control/
thread_ids: []
evidence_refs:
  - type: doc
    ref: C:/Users/terryzzb/Desktop/session-memory/docs/canonical/CONTROL_SYSTEM.md
  - type: doc
    ref: C:/Users/terryzzb/Desktop/session-memory/docs/canonical/SCHEMA.md
  - type: note
    ref: C:/Users/terryzzb/Desktop/session-memory/state/session-memory/current/current-task.md
tags:
  - objective
  - control-system
  - active
confidence: high
created_at: 2026-03-23T21:10:00+08:00
updated_at: 2026-03-25T18:38:23+08:00
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

Phase changed from `paused` to `execution` because A bounded execution slice is needed to land M1 bundle-payload registration and M2 broader adjudication plan contracts for automatic rewrite.

Phase changed from `execution` to `paused` because Preview release preparation round is closed, so the objective returns to paused until the next explicit kernel release or adoption milestone.

Phase changed from `paused` to `execution` because Preview release artifacts are ready, but the working tree still carries unreleased package and doc changes that need one explicit ratification round before landing into git.

Phase changed from `execution` to `paused` because Preview release ratification round is closed, so the objective returns to paused until the next explicit kernel milestone.

Phase changed from `paused` to `execution` because Stage 1 now needs a real owner-layer live-host shadow assessment surface and adoption report, not more snapshot-only smoke logic.

Scope review: Resume controlled implementation to land a kernel-owned host adoption assessment primitive.

Phase changed from `execution` to `paused` because The a4 release slice is complete and the project should leave execution until the next bounded round is opened.

Phase changed from `paused` to `execution` because The current a4 release story is externally wrong and needs one bounded correction round for public-surface versioning and release tagging.

Phase changed from `execution` to `paused` because The a4 release-correction round is closed and the project should leave execution until the next bounded round opens.

Phase changed from `paused` to `execution` because Release publication still lacks a repo-owned completion verifier, so the process can repeat the same push-versus-release mistake.

Phase changed from `execution` to `paused` because The release publication process-fix round is closed and the project should leave execution until the next bounded round opens.

Phase changed from `paused` to `execution` because CI failed because smoke and release scripts hardcoded a Windows git executable path; this round makes git resolution repo-owned and cross-platform.

Phase changed from `execution` to `paused` because no durable open round remains after closing the a5 public flow contract round

Phase changed from `paused` to `execution` because cut the a5 preview release line after landing the shared public flow result contract work

Phase changed from `execution` to `paused` because no durable open round remains after the a5 preview release round closed

Phase changed from `paused` to `execution` because land a repo rule that requires local control-state sync before any remote push

Phase changed from `execution` to `paused` because no durable open round remains after closing the push-order rule round

Phase changed from `paused` to `execution` because start the b0 public contract freeze by moving stable public flow fields into one repo-owned owner layer

Phase changed from `execution` to `paused` because The b0 candidate public flow contract freeze slice is closed; the objective returns to paused until the next beta hardening round starts.

Phase changed from `paused` to `execution` because A bounded beta-hardening slice is needed to freeze stable public subcontracts for flow_contract and intent_compilation instead of leaving nested public semantics implicit in payload examples.

Phase changed from `execution` to `paused` because The b0 public subcontract freeze slice is closed; the objective returns to paused until the next beta-hardening round starts.

Phase changed from `paused` to `execution` because A bounded release slice is needed to promote the package from 0.1.0a5 preview identity to 0.1.0b0 beta identity, including public surface naming, docs, validation, and publication truth.

Phase changed from `execution` to `paused` because the 0.1.0b0 beta release round is now closed locally after release commit 5dd4f9c and tag v0.1.0b0

Phase changed from `paused` to `execution` because A bounded beta-hardening slice is needed to promote the smallest reusable evidence-layer response fields into owner-layer public contracts so agents stop inferring them from smoke code.

Phase changed from `execution` to `paused` because the bounded b1 evidence-layer hardening round is closed, so the objective should return to paused until the next explicit beta-hardening slice opens

Phase changed from `paused` to `execution` because The b1 candidate subcontract work is validated but still uncommitted, so one short ratification round is needed to land the code and doc changes into git honestly.

Phase changed from `execution` to `paused` because the short ratification round is closed, so the objective should return to paused until the next beta-hardening slice opens

Phase changed from `paused` to `execution` because Open a bounded b1 hardening slice to promote the minimum honest stable public response kernels.

Phase changed from `execution` to `paused` because The bounded b1 contract promotion slice is closed, so the active objective should return to paused until the next source-line release step opens.

Phase changed from `paused` to `execution` because Open the bounded 0.1.0b1 release-identity cut now that the selected b1 contract promotion is complete.

Phase changed from `execution` to `paused` because The 0.1.0b1 local beta release round is closed, so the objective returns to paused until the next bounded release slice opens.
