---
id: round-2026-03-24-2110-stabilize-package-first-single-assessment-alpha-surface
type: round-contract
title: "Stabilize package-first single-assessment alpha surface"
status: active
project_id: session-memory
workspace_id: ws-1490b759
workspace_root: C:/Users/terryzzb/Desktop/session-memory
branch: master
git_sha: e7ebe4ebf8fff703ae06f6c12f627f7502db0300
paths:
  - kernel
  - scripts/smoke_kernel_bootstrap.py
  - scripts/session_memory.py
  - scripts/smoke_manifest.py
  - scripts/run_smoke_suite.py
  - scripts/enforce_worktree.py
  - scripts/smoke_fixture_lib.py
  - scripts/smoke_assess_host_adoption.py
  - scripts/smoke_brooks_semantic_research_snapshot_adoption.py
  - scripts/smoke_wind_agent_snapshot_bootstrap.py
  - scripts/smoke_wind_agent_snapshot_adoption.py
  - scripts/smoke_phase1.py
  - scripts/audit_product_docs.py
  - scripts/product_semantics.py
  - README.md
  - docs/canonical/PRODUCT.md
  - docs/canonical/RELEASE.md
  - docs/canonical/TRANSITION_COMMANDS.md
  - docs/canonical/ARCHITECTURE.md
  - docs/canonical/CONTROL_SYSTEM.md
  - docs/canonical/STATE_MACHINE.md
  - docs/canonical/SCHEMA.md
  - docs/canonical/DESIGN_PRINCIPLES.md
  - docs/canonical/IMPLEMENTATION_PLAN.md
  - docs
  - projects/session-memory/current/current-task.md
  - projects/session-memory/memory/objectives
  - projects/session-memory/memory/decisions
  - projects/session-memory/memory/pivots
  - projects/session-memory/snapshots
  - kernel/README.md
  - kernel/docs/TRANSITION_COMMANDS.md
  - .github/workflows
thread_ids: []
evidence_refs: []
tags:
  - round
  - control-plane
confidence: high
created_at: 2026-03-24T21:10:50+08:00
updated_at: 2026-03-24T22:32:14+08:00
objective_id: obj-2026-03-23-0002
phase: execution
supersedes: []
superseded_by: []
---

## Summary

Stabilize the alpha single-assessment surface while collapsing canonical host docs into docs/canonical and keeping package-facing proof and CI honest.

## Scope

- Split external-target scope drafting and shadow assessment reporting into distinct artifact owner semantics.
- Keep the package-first validation path proving installed-wheel bootstrap and bounded external-target single assessment.
- Collapse host canonical product/control/release docs into docs/canonical and retarget repo-facing audit and navigation surfaces to that tree.

## Deliverable

A cleaner alpha single-assessment surface with distinct artifact semantics, one install-first bootstrap-and-assess proof, one registered package smoke path, and a root markdown layout reduced to entrypoint-only docs.

## Validation Plan

Run smoke_phase1, smoke_kernel_bootstrap, run_smoke_suite --smoke kernel_bootstrap, audit_product_docs, audit-control-state, and enforce-worktree after the canonical-doc migration lands.

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

Round rewritten because The root-doc cleanup now fully migrates the remaining evaluation docs out of the repository root, so the round must cover their real references in current-task, docs navigation, and the durable objective that still names the old root path.

Round rewritten because The remaining evaluation-doc migration also touches one historical snapshot that still points at the retiring root path, so the round boundary must cover snapshots before the old files are removed.

Round rewritten because The root-doc migration is now complete enough to retire the old root evaluation and auxiliary doc paths from the active round, so the round path set should collapse to the live docs tree instead of keeping stale retired roots.

Round rewritten because GitHub Actions now fails inside phase-1 smoke on Python 3.11 compatibility, so the round boundary must cover the shared smoke fixture helper and the snapshot/adoption smokes that still use the unsupported shutil.rmtree onexc parameter.

Round rewritten because Root canonical-doc cleanup now moves the remaining root product/control/release specs into docs/canonical, so the round boundary must cover those retiring root files plus the product-doc audit helpers that enforce their new location.

Round rewritten because The canonical-doc migration now also updates the active pivot durable reference surface, so the round boundary must cover projects/session-memory/memory/pivots before the docs/canonical path swap is finalized.

Round rewritten because The root canonical-doc collapse is now real, so the active round must describe docs/canonical as the live canonical location instead of claiming the product/control/release specs still stay at the repo root.
