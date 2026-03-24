---
id: round-2026-03-24-0907-lift-rewrite-open-round-field-semantics-into-registry-owned-owner-layer-contracts
type: round-contract
title: "Define product positioning and align governance docs to it"
status: active
project_id: session-memory
workspace_id: ws-1490b759
workspace_root: C:/Users/terryzzb/Desktop/session-memory
branch: master
git_sha: 3ccabebc4819d82e2fc5994e79dffd7c4a5d20e9
paths:
  - scripts/transition_specs.py
  - scripts/execute_adjudication_followups.py
  - scripts/audit_control_state.py
  - CONTROL_SYSTEM.md
  - TRANSITION_COMMANDS.md
  - projects/session-memory/current/current-task.md
  - .githooks/pre-push
  - .github/workflows/control-enforcement.yml
  - ARCHITECTURE.md
  - DESIGN_PRINCIPLES.md
  - IMPLEMENTATION_PLAN.md
  - STATE_MACHINE.md
  - PRODUCT.md
  - scripts/audit_product_docs.py
  - scripts/product_semantics.py
thread_ids: []
evidence_refs: []
tags:
  - round
  - control-plane
confidence: high
created_at: 2026-03-24T09:07:16+08:00
updated_at: 2026-03-24T10:12:46+08:00
objective_id: obj-2026-03-23-0002
phase: execution
supersedes: []
superseded_by: []
---

## Summary

Establish one canonical product document for session-memory as a memory-driven repo governance control plane, align major canonical docs to that positioning, and define how machine semantics should follow product docs without turning prose into hidden authority.

## Scope

- Create one canonical product document that states target users, product promise, value proposition, boundaries, and roadmap for session-memory.
- Align major canonical docs so architecture, control-system framing, and implementation plan describe the same product rather than drifting between memory tool, control system, and autonomous rewrite narratives.
- Define and begin codifying the owner-layer path by which machine semantics should follow canonical product docs through explicit machine-readable contracts and audits instead of prose-only interpretation.

## Deliverable

Session-memory has one canonical product definition, the main governance docs read consistently from that product stance, and the repo gains an explicit documented mechanism for turning canonical product intent into auditable machine semantics.

## Validation Plan

Read the aligned product/control docs, run targeted doc drift checks or audit additions if introduced, refresh current-task anchor, and run control audit plus worktree enforcement before commit.

## Active Risks

_none recorded_

## Blockers

_none recorded_

## Status Notes

_none recorded_

Round rewritten because Scope shifted from continuing bundle-semantic registration to bundle governance institutionalization.

Round rewritten because Scope shifted from bundle-governance law to product-definition alignment and doc-driven semantics governance.

Round rewritten because Product-definition alignment round expanded to additional canonical docs, product semantics audit scripts, and enforcement entrypoints that must be explicitly in round scope.
