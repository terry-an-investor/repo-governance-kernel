---
id: round-2026-03-23-1814-broaden-enforcement-coverage-beyond-first-worktree-gate
type: round-contract
title: "Freeze machine-readable transition registry"
status: active
project_id: session-memory
workspace_id: ws-1490b759
workspace_root: C:/Users/terryzzb/Desktop/session-memory
branch: master
git_sha: cc53d54dcf8c3869205632429a68344133db1330
paths:
  - AGENTS.md
  - .githooks/
  - .github/
  - scripts/
  - CONTROL_SYSTEM.md
  - SCHEMA.md
  - STATE_MACHINE.md
  - TRANSITION_COMMANDS.md
  - projects/session-memory/control/
  - projects/session-memory/current/
  - DESIGN_PRINCIPLES.md
  - HARNESS.md
  - scripts/transition_specs.py
thread_ids: []
evidence_refs: []
tags:
  - round
  - control-plane
confidence: high
created_at: 2026-03-23T18:14:34+08:00
updated_at: 2026-03-23T20:59:13+08:00
objective_id: obj-2026-03-23-0002
phase: execution
supersedes: []
superseded_by: []
---

## Summary

Add a canonical transition registry that declares command domains, executor support, and adjudication plan families in one machine-readable owner-layer surface.

## Scope

- Add a machine-readable transition registry for the currently implemented command surface and bounded adjudication plan families.
- Wire executor and adjudication plan compiler support lists to the registry instead of hard-coded local sets.
- Teach control audit to detect registry drift against the canonical documented command surface.

## Deliverable

A repo-owned transition registry that becomes the single machine-readable source for supported transition commands and bounded adjudication plan families.

## Validation Plan

Validate registry listing and audit checks, rerun adjudication smoke and full phase-1 smoke, then rerun audit-control-state and enforce-worktree on the real project.

## Active Risks

- A partial registry could create false confidence if scripts still quietly keep private support lists outside the owner-layer registry.
- Registry drift checks may still be too shallow if they only compare names and not full guard or side-effect semantics yet.

## Blockers

_none recorded_

## Status Notes

Opened after closing the first automatic worktree enforcement slice.

Constitution-declared guarded exception paths are now enforced as a second blocked-state class.

The same owner-layer commands are now wired into GitHub Actions so local hook
gates and remote CI gates execute the same enforcement surface.

Explicit `set-phase` and `refresh-round-scope` commands now exist.

`open-round` now rejects non-`execution` objectives so execution contracts
cannot be opened from exploration by accident.

validated by:
- uv run python scripts/smoke_guarded_exception_enforcement.py
- uv run python scripts/smoke_phase_scope_controls.py
- uv run python scripts/audit_control_state.py --project-id session-memory
- uv run python scripts/enforce_worktree.py --project-id session-memory

Round rewritten because This round is now serving the durable open-round rewrite milestone, so the active round contract must be rewritten to match the current mainline work.

This round was durably rewritten from the earlier enforcement-expansion milestone into the open-round rewrite integration milestone.

Round rewritten because The previous rewrite used shell-sensitive quoting, so the durable round scope bullets must be rewritten into clean plain text.

Round rewritten because The active milestone is now adjudication plan compilation, so the open round contract must be rewritten to the current durable objective slice.

The active round was rewritten again to move from raw open-round rewrite integration into bounded adjudication plan compilation.

Round rewritten because The current milestone has moved from initial adjudication plan compilation to bounded exception-contract plan compilation, so the durable round contract must be rewritten to the current mainline.

The active round now targets bounded exception-contract plan compilation so adjudication can compile more of its durable verdict into repo-owned execution contracts.

Round rewritten because The exception-contract plan milestone is complete, and the next bounded durable rewrite family is adjudication-driven phase-side-effect bundling through existing round bootstrap fields.

The active round now targets bounded phase-side-effect plan compilation so adjudication can drive execution bootstrap through repo-owned plan expansion instead of hand-authored payloads.

Round rewritten because The active phase-side-effect plan milestone now includes canonical design-principle updates about front-loaded precision, so the round scope must include that canonical doc honestly.

Round rewritten because The phase-side-effect plan milestone is complete, and the next control slice is harness law for disposable smoke isolation and suite execution.

The active round now targets harness law so disposable smoke isolation and execution ordering stop depending on developer memory.

Round rewritten because The harness-law milestone is complete, and the next control slice is a machine-readable transition registry so command support stops drifting between docs, executor, and plan compiler.

The active round now targets a machine-readable transition registry so command support stops living partly in prose and partly in scattered script constants.
