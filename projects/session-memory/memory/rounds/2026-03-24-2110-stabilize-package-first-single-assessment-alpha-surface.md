---
id: round-2026-03-24-2110-stabilize-package-first-single-assessment-alpha-surface
type: round-contract
title: "Stabilize package-first single-assessment alpha surface"
status: active
project_id: session-memory
workspace_id: ws-1490b759
workspace_root: C:/Users/terryzzb/Desktop/session-memory
branch: master
git_sha: 1247367251bd312354fa45329f09fe545c8fa866
paths:
  - kernel
  - scripts/smoke_kernel_bootstrap.py
  - scripts/session_memory.py
  - scripts/smoke_manifest.py
  - scripts/run_smoke_suite.py
  - README.md
  - RELEASE.md
  - TRANSITION_COMMANDS.md
  - ARCHITECTURE.md
  - docs
  - 2026-03-22-notes.md
  - HARNESS.md
  - WIND_AGENT_EVAL_PLAN.md
  - projects/session-memory/memory/decisions
  - kernel/README.md
  - kernel/docs/TRANSITION_COMMANDS.md
thread_ids: []
evidence_refs: []
tags:
  - round
  - control-plane
confidence: high
created_at: 2026-03-24T21:10:50+08:00
updated_at: 2026-03-24T21:23:24+08:00
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
- Clean up root markdown topology by keeping canonical kernel docs at the root and moving weakly-coupled auxiliary docs into docs/.

## Deliverable

A cleaner alpha single-assessment surface with distinct draft/report artifact semantics, one install-first wheel smoke, and a less cluttered root doc topology.

## Validation Plan

Run the focused package-first smoke, product-doc audit, audit-control-state, and enforce-worktree after the artifact split and root-doc cleanup land.

## Active Risks

- The first package-first smoke could stay too bootstrap-only and fail to prove the most important package-facing surface.

## Blockers

_none recorded_

## Status Notes

_none recorded_

Round rewritten because The install-first package smoke will be registered in the smoke manifest, so the round must cover the real harness paths before implementation begins.

Round rewritten because Root markdown cleanup now includes creating a docs hierarchy and moving weakly-coupled auxiliary docs out of the repository root, so the round must cover the real doc-topology write set.

Round rewritten because Root doc cleanup deletes the old auxiliary paths after migrating them into docs/, so the round must cover both the new docs tree and the retiring root files.
