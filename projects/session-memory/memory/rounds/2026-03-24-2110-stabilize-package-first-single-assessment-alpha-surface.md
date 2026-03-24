---
id: round-2026-03-24-2110-stabilize-package-first-single-assessment-alpha-surface
type: round-contract
title: "Stabilize package-first single-assessment alpha surface"
status: active
project_id: session-memory
workspace_id: ws-1490b759
workspace_root: C:/Users/terryzzb/Desktop/session-memory
branch: master
git_sha: e93c10d47b4be2445bb73d8deb0e65d8661959a1
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
  - scripts/enforce_worktree.py
  - .github/workflows
thread_ids: []
evidence_refs: []
tags:
  - round
  - control-plane
confidence: high
created_at: 2026-03-24T21:10:50+08:00
updated_at: 2026-03-24T21:57:28+08:00
objective_id: obj-2026-03-23-0002
phase: execution
supersedes: []
superseded_by: []
---

## Summary

A tighter alpha single-assessment surface with distinct draft/report semantics, one install-first bootstrap-and-assess proof, and cleaner package/root docs.

## Scope

- Split external-target scope drafting and shadow assessment reporting into distinct artifact owner semantics.
- Add one package-first validation path that proves an installed wheel can bootstrap and audit a disposable governed host repo.
- Clean up root markdown topology by keeping canonical kernel docs at the root and moving weakly-coupled auxiliary docs into docs/.
- Split external-target drafting and shadow assessment reporting into distinct artifact owner semantics.
- Extend the package-first validation path so an installed wheel can bootstrap a disposable governed host and complete one governed external-target single assessment against a disposable external repo.
- Register the package-first smoke in the suite and tighten package-facing quickstart and release evidence around that same proof path.
- Keep canonical root docs in place while moving weakly-coupled auxiliary markdown into docs/.

## Deliverable

A cleaner alpha single-assessment surface with distinct artifact semantics, one install-first bootstrap-and-assess proof, one registered package smoke path, and aligned package-facing docs.

## Validation Plan

Run smoke_kernel_bootstrap, run_smoke_suite --smoke kernel_bootstrap, audit_product_docs, audit-control-state, and enforce-worktree after the package-facing proof path lands.

## Active Risks

- The first package-first smoke could stay too bootstrap-only and fail to prove the most important package-facing surface.

## Blockers

_none recorded_

## Status Notes

_none recorded_

Round rewritten because The install-first package smoke will be registered in the smoke manifest, so the round must cover the real harness paths before implementation begins.

Round rewritten because Root markdown cleanup now includes creating a docs hierarchy and moving weakly-coupled auxiliary docs out of the repository root, so the round must cover the real doc-topology write set.

Round rewritten because Root doc cleanup deletes the old auxiliary paths after migrating them into docs/, so the round must cover both the new docs tree and the retiring root files.

Round rewritten because The a2 package-first slice now extends from installed-wheel bootstrap and audit to installed-wheel external-target single assessment proof plus package-facing smoke registration, so the round contract must describe the real proof path.

Round rewritten because CI now needs a cross-environment workspace-root override for owner-layer enforcement, so the round boundary must cover the workflow surface and the repo-local enforcement wrapper that consume that override.
