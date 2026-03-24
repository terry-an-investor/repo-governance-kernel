---
id: round-2026-03-24-1151-land-m3-owner-layer-rewrite-semantics-and-unified-transition-engine-foundation
type: round-contract
title: "Land M3 owner-layer rewrite semantics and unified transition engine foundation"
status: closed
project_id: session-memory
workspace_id: ws-1490b759
workspace_root: C:/Users/terryzzb/Desktop/session-memory
branch: master
git_sha: 207551be1ebb034ee505574879036a7d8c73db08
paths:
  - scripts/
  - state/session-memory/control/
  - state/session-memory/current/
  - state/session-memory/memory/
  - CONTROL_SYSTEM.md
  - IMPLEMENTATION_PLAN.md
  - STATE_MACHINE.md
  - TRANSITION_COMMANDS.md
  - PRODUCT.md
  - ARCHITECTURE.md
  - DESIGN_PRINCIPLES.md
  - kernel/
  - pyproject.toml
  - .gitignore
  - RELEASE.md
  - uv.lock
  - README.md
thread_ids: []
evidence_refs: []
tags:
  - round
  - control-plane
confidence: high
created_at: 2026-03-24T11:51:07+08:00
updated_at: 2026-03-24T18:47:45+08:00
objective_id: obj-2026-03-23-0002
phase: execution
supersedes: []
superseded_by: []
---

## Summary

A new M3 slice that broadens rewrite semantics honestly and lands the first unified transition-engine foundation.

## Scope

- Extend registry-owned adjudication rewrite semantics beyond the current bounded round/task/exception slice without inventing new private executor branches.
- Extract shared execution-building primitives so owner-layer commands stop accumulating one-off if/else dispatch paths.
- Kernelize canonical product and control docs so the repo is framed as a repo governance kernel instead of a broader memory/autonomy system.
- Physically separate reusable governance runtime modules into kernel/ while keeping sample project data under state/session-memory/.
- Prepare kernel for alpha release with independent package metadata, release notes, and sample-downscoped host-repo positioning.

## Deliverable

A new M3 slice that broadens rewrite semantics honestly and lands the first unified transition-engine foundation.

## Validation Plan

Targeted py_compile, audit-control-state, enforce-worktree, and focused smoke coverage pass on the M3 path.
uv run python scripts/smoke_kernel_bootstrap.py
uv run python scripts/smoke_wind_agent_snapshot_adoption.py
uv run python scripts/smoke_brooks_semantic_research_snapshot_adoption.py
uv build
artifacts/preview-install/.venv/Scripts/python.exe -m kernel.cli --help
artifacts/preview-install/.venv/Scripts/repo-governance-kernel.exe --help
uv run python -m kernel.cli audit-control-state --project-id session-memory
uv run python -m kernel.cli enforce-worktree --project-id session-memory

## Active Risks

- Expanding rewrite semantics too fast could reintroduce private owner-layer behavior under a cleaner name.
- A premature unified engine abstraction could hide domain differences instead of making them explicit.

## Blockers

_none recorded_

## Status Notes

_none recorded_

Round rewritten because canonical docs now need to be kernelized so product, architecture, control, and machine-semantic docs match the registry-first governance stance already implemented

Round rewritten because the current milestone now includes physically separating reusable governance runtime modules into a kernel package while keeping scripts as CLI entrypoints and compatibility wrappers

Round rewritten because the milestone now includes kernel alpha release preparation and explicitly downgrading the host sample to dogfood/example status in canonical docs

Round rewritten because alpha packaging preparation now also owns release metadata and derived package-build hygiene for uv package mode

Round rewritten because Preview release packaging now owns the repository root README because setuptools readme metadata and package-facing preview framing must stay inside the governed release surface.

Round rewritten because preview packaging now includes root README metadata and package-facing preview framing.

active -> validation_pending: Preview release validation is complete across control audit, worktree enforcement, external frozen-host adoption smokes, package build, and installed CLI checks.

validation_pending -> captured: Preview release evidence is recorded in release notes, built artifacts, and frozen-host reports, so the validated release-prep round can be captured.

validated by:
- uv run python scripts/smoke_kernel_bootstrap.py
- uv run python scripts/smoke_wind_agent_snapshot_adoption.py
- uv run python scripts/smoke_brooks_semantic_research_snapshot_adoption.py
- uv build
- artifacts/preview-install/.venv/Scripts/python.exe -m kernel.cli --help
- artifacts/preview-install/.venv/Scripts/repo-governance-kernel.exe --help
- uv run python -m kernel.cli audit-control-state --project-id session-memory
- uv run python -m kernel.cli enforce-worktree --project-id session-memory

captured -> closed: Alpha preview release preparation is complete and the round can close on recorded evidence.

