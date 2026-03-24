---
id: round-2026-03-24-2110-stabilize-package-first-single-assessment-alpha-surface
type: round-contract
title: "Stabilize package-first single-assessment alpha surface"
status: active
project_id: session-memory
workspace_id: ws-1490b759
workspace_root: C:/Users/terryzzb/Desktop/session-memory
branch: master
git_sha: 1212345248b7910d6feb2bf2b4de3482b32bd7c6
paths:
  - kernel
  - scripts/smoke_kernel_bootstrap.py
  - scripts/session_memory.py
  - scripts/smoke_manifest.py
  - scripts/run_smoke_suite.py
  - README.md
  - RELEASE.md
  - TRANSITION_COMMANDS.md
  - kernel/README.md
  - kernel/docs/TRANSITION_COMMANDS.md
thread_ids: []
evidence_refs: []
tags:
  - round
  - control-plane
confidence: high
created_at: 2026-03-24T21:10:50+08:00
updated_at: 2026-03-24T21:12:04+08:00
objective_id: obj-2026-03-23-0002
phase: execution
supersedes: []
superseded_by: []
---

## Summary

A cleaner alpha single-assessment surface with distinct draft/report artifact semantics plus one install-first wheel smoke for bootstrap and audit.

## Scope

- Split external-target scope drafting and shadow assessment reporting into distinct artifact owner semantics.
- Add one package-first validation path that proves an installed wheel can bootstrap and audit a disposable governed host repo.
- Refresh package-facing docs and release notes so the a2 single-assessment validation story matches the implemented surface.

## Deliverable

A cleaner alpha single-assessment surface with distinct draft/report artifact semantics plus one install-first wheel smoke for bootstrap and audit.

## Validation Plan

Run the focused package-first smoke, audit-control-state, and enforce-worktree on the real repo after the artifact split and smoke path land.

## Active Risks

- The first package-first smoke could stay too bootstrap-only and fail to prove the most important package-facing surface.

## Blockers

_none recorded_

## Status Notes

_none recorded_

Round rewritten because The install-first package smoke will be registered in the smoke manifest, so the round must cover the real harness paths before implementation begins.
