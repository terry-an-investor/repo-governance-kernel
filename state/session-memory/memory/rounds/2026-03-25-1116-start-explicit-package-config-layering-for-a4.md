---
id: round-2026-03-25-1116-start-explicit-package-config-layering-for-a4
type: round-contract
title: "Start explicit package config layering for a4"
status: active
project_id: session-memory
workspace_id: ws-1490b759
workspace_root: C:/Users/terryzzb/Desktop/session-memory
branch: master
git_sha: 80b47b322a49439cb9b79eb6884b8b6bdc8a89af
paths:
  - kernel
  - docs
  - README.md
  - pyproject.toml
  - scripts
  - .githooks
thread_ids: []
evidence_refs: []
tags:
  - round
  - control-plane
confidence: high
created_at: 2026-03-25T11:16:27+08:00
updated_at: 2026-03-25T11:26:42+08:00
objective_id: obj-2026-03-23-0002
phase: execution
supersedes: []
superseded_by: []
---

## Summary

Add one owner-layer config runtime and close the recurrent submit escape by aligning shared path budgeting and the local smoke gate with the same package-facing validation surface.

## Scope

- Add one owner-layer config runtime so the package can resolve user, project, and local config without scattering path and precedence rules across commands.
- Expose the first package-facing config command and wire the first real public-alpha consumers onto that shared config surface.
- Fix the recurring submit escape by centralizing durable file-name budgeting for pivot and objective writes and aligning the repo-owned pre-push smoke gate with the CI phase-1 smoke surface.

## Deliverable

One first a4 slice with layered config runtime, hardened durable file naming, one package-facing config entrypoint, and one smoke-proven consumer path.

## Validation Plan

Run focused filename-budget and transition smoke plus audit-control-state, enforce-worktree, audit_product_docs, and any changed package proof after the slice lands.

## Active Risks

- If config layering stays implicit, installability will keep depending on flags and repo-local knowledge instead of package-owned defaults.
- If config semantics are added directly inside individual commands, the a4 surface will recreate the same private semantics drift the kernel has been removing elsewhere.
- If local push gating remains weaker than CI, GitHub will keep being the first place phase-1 smoke regressions are discovered.

## Blockers

_none recorded_

## Status Notes

_none recorded_

Round rewritten because This a4 slice needs to change the repo-owned pre-push gate alongside the shared config and path-budget runtime, so the open round scope must honestly cover .githooks.
