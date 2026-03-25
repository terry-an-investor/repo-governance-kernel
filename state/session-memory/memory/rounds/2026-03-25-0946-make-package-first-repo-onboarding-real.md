---
id: round-2026-03-25-0946-make-package-first-repo-onboarding-real
type: round-contract
title: "Make package-first repo onboarding real"
status: active
project_id: session-memory
workspace_id: ws-1490b759
workspace_root: C:/Users/terryzzb/Desktop/session-memory
branch: master
git_sha: afad3f1b796dd2cb73421997d577eacb1635334e
paths:
  - kernel
  - scripts
  - docs
  - README.md
thread_ids: []
evidence_refs: []
tags:
  - round
  - control-plane
confidence: high
created_at: 2026-03-25T09:46:58+08:00
updated_at: 2026-03-25T09:46:58+08:00
objective_id: obj-2026-03-23-0002
phase: execution
supersedes: []
superseded_by: []
---

## Summary

One package-facing repo onboarding flow with code, docs, and smoke proof showing a new host can bootstrap and enter its first honest governance setup.

## Scope

- Create one package-facing onboarding primitive so a fresh host repo can move from bare bootstrap into an honest first governance setup without hand-opening every control object.
- Keep the onboarding path bounded and registry-owned instead of adding a freeform setup orchestrator.

## Deliverable

One package-facing repo onboarding flow with code, docs, and smoke proof showing a new host can bootstrap and enter its first honest governance setup.

## Validation Plan

Run focused onboarding smoke plus audit-control-state, enforce-worktree, audit_product_docs, and package/bootstrap proof after the onboarding flow lands.

## Active Risks

- If onboarding still depends on smoke-only setup helpers, the package-first story will remain repo-local rather than product-facing.
- If onboarding invents placeholder control objects on a clean repo or absorbs bootstrap side effects dishonestly, it will make the first governance state look smoother than it is.

## Blockers

_none recorded_

## Status Notes

_none recorded_
