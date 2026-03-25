---
id: round-2026-03-25-0946-make-package-first-repo-onboarding-real
type: round-contract
title: "Make package-first repo onboarding real"
status: active
project_id: session-memory
workspace_id: ws-1490b759
workspace_root: C:/Users/terryzzb/Desktop/session-memory
branch: master
git_sha: e8ee75f6e4f188e611fc07246a631e5a52eaf320
paths:
  - kernel
  - scripts
  - docs
  - README.md
  - skills
thread_ids: []
evidence_refs: []
tags:
  - round
  - control-plane
confidence: high
created_at: 2026-03-25T09:46:58+08:00
updated_at: 2026-03-25T10:55:40+08:00
objective_id: obj-2026-03-23-0002
phase: execution
supersedes: []
superseded_by: []
---

## Summary

Turn the landed onboarding and assessment primitives into a clearer package product surface by defining the next version roadmap and starting bounded agent packaging.

## Scope

- Create one package-facing onboarding primitive so a fresh host repo can move from bare bootstrap into an honest first governance setup without hand-opening every control object.
- Keep the onboarding path bounded and registry-owned instead of adding a freeform setup orchestrator.
- Define the next release sequence so the package surface, config layering, and one-task entrypoints are planned as explicit alpha milestones instead of informal chat guidance.
- Land the first repo-owned agent packaging surface so onboarding and single assessment can be invoked through a bounded skill rather than only through raw CLI knowledge.

## Deliverable

One canonical version roadmap plus the first repo-owned agent skill showing how to initialize and evaluate repos through the bounded package surface.

## Validation Plan

Run audit_product_docs, audit-control-state, enforce-worktree, and one focused skill-oriented proof or command example after the roadmap and first agent packaging surface land.

## Active Risks

- If onboarding still depends on smoke-only setup helpers, the package-first story will remain repo-local rather than product-facing.
- If onboarding invents placeholder control objects on a clean repo or absorbs bootstrap side effects dishonestly, it will make the first governance state look smoother than it is.
- If agent packaging is left implicit, the product will continue to feel like an internal kernel even after onboarding and assessment surfaces already exist.
- If the roadmap stays only in chat, package-facing priorities will drift and alpha release work will remain reactive instead of versioned.

## Blockers

_none recorded_

## Status Notes

_none recorded_

Round rewritten because The onboarding milestone is landed; the active round now needs to cover the next package-surface step: public alpha planning plus the first agent packaging surface.

The active round now extends from onboarding delivery into package-surface planning and first agent packaging.
