---
id: round-2026-03-24-2110-stabilize-package-first-single-assessment-alpha-surface
type: round-contract
title: "Stabilize package-first single-assessment alpha surface"
status: closed
project_id: repo-governance-kernel
workspace_id: ws-1490b759
workspace_root: C:/Users/terryzzb/Desktop/session-memory
branch: master
git_sha: f09a1bc6652290b312ea43a06e38410030bb9e1b
paths:
  - kernel
  - scripts
  - README.md
  - docs
  - index
  - state
  - .github/workflows
thread_ids: []
evidence_refs: []
tags:
  - round
  - control-plane
confidence: high
created_at: 2026-03-24T21:10:50+08:00
updated_at: 2026-03-25T08:43:22+08:00
objective_id: obj-2026-03-23-0002
phase: execution
supersedes: []
superseded_by: []
---

## Summary

Stabilize the alpha single-assessment surface by migrating canonical host state from projects/<project_id> to state/<project_id> and keeping package-facing proof, CI, and docs honest.

## Scope

- Split external-target scope drafting and shadow assessment reporting into distinct artifact owner semantics.
- Keep the package-first validation path proving installed-wheel bootstrap and bounded external-target single assessment.
- Migrate the canonical host state layout from projects/<project_id> to state/<project_id> and retarget runtime, docs, and durable references to that tree.

## Deliverable

A cleaner alpha single-assessment surface with distinct artifact semantics, one install-first bootstrap-and-assess proof, one registered package smoke path, and one canonical state/<project_id> layout with no remaining projects/ dependency.

## Validation Plan

Run smoke_phase1, smoke_kernel_bootstrap, run_smoke_suite --smoke kernel_bootstrap, audit_product_docs, audit-control-state, and enforce-worktree after the state-root migration lands.
uv run python scripts/smoke_phase1.py
uv run python scripts/smoke_kernel_bootstrap.py
uv run python -m kernel.cli audit-control-state --project-id repo-governance-kernel
uv run python -m kernel.cli enforce-worktree --project-id repo-governance-kernel --workspace-root C:/Users/terryzzb/Desktop/session-memory
uv run python scripts/smoke_phase1.py
uv run python scripts/smoke_kernel_bootstrap.py
uv run python -m kernel.cli audit-control-state --project-id repo-governance-kernel
uv run python -m kernel.cli enforce-worktree --project-id repo-governance-kernel --workspace-root C:/Users/terryzzb/Desktop/session-memory

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

Round rewritten because The canonical-doc migration now also updates the active pivot durable reference surface, so the round boundary must cover state/repo-governance-kernel/memory/pivots before the docs/canonical path swap is finalized.

Round rewritten because The root canonical-doc collapse is now real, so the active round must describe docs/canonical as the live canonical location instead of claiming the product/control/release specs still stay at the repo root.

Round rewritten because The next slice is a real state-layout migration from state/<project_id> to a new owner-layer state root, so the active round must cover kernel path resolution, bootstrap/audit/enforcement consumers, canonical docs, and both live sample state trees before any migration lands.

Round rewritten because The state-root migration is now the active deliverable, so the round contract must drop the retired projects tree and describe state/<project_id> as the canonical control-state layout.

Round rewritten because The state-root migration also repairs the derived-index contract read surface, so the active round must cover index alongside the runtime and canonical docs it now describes.

active -> validation_pending: The alpha-surface migration slice is implemented and ready for final round validation on the committed state-root baseline.

validated by:
- uv run python scripts/smoke_phase1.py
- uv run python scripts/smoke_kernel_bootstrap.py
- uv run python -m kernel.cli audit-control-state --project-id repo-governance-kernel
- uv run python -m kernel.cli enforce-worktree --project-id repo-governance-kernel --workspace-root C:/Users/terryzzb/Desktop/session-memory

validation_pending -> captured: The alpha-surface migration slice passed its declared validation set and can be durably captured.

validated by:
- uv run python scripts/smoke_phase1.py
- uv run python scripts/smoke_kernel_bootstrap.py
- uv run python -m kernel.cli audit-control-state --project-id repo-governance-kernel
- uv run python -m kernel.cli enforce-worktree --project-id repo-governance-kernel --workspace-root C:/Users/terryzzb/Desktop/session-memory

captured -> closed: The alpha-surface migration slice is captured and no open task contracts remain, so the round can close cleanly.

