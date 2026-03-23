---
id: round-2026-03-23-1814-broaden-enforcement-coverage-beyond-first-worktree-gate
type: round-contract
title: "Govern disposable smoke harness law"
status: active
project_id: session-memory
workspace_id: ws-1490b759
workspace_root: C:/Users/terryzzb/Desktop/session-memory
branch: master
git_sha: 588e2a6d54623d51ea3cd1ce3728a92b8de732bb
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
thread_ids: []
evidence_refs: []
tags:
  - round
  - control-plane
confidence: high
created_at: 2026-03-23T18:14:34+08:00
updated_at: 2026-03-23T20:55:01+08:00
objective_id: obj-2026-03-23-0002
phase: execution
supersedes: []
superseded_by: []
---

## Summary

Add a canonical smoke manifest and suite runner so fixture leak checks, serial execution, and smoke selection become repo-owned harness law instead of oral discipline.

## Scope

- Add a canonical smoke manifest that declares disposable fixture project ids, parallel-safety, and shared resources for each smoke script.
- Implement a suite runner that enforces fixture leak checks before and after each smoke and executes shared-fixture smokes serially.
- Wire the phase-1 smoke entrypoint through the suite runner and validate that the harness owner layer catches fixture contamination honestly.

## Deliverable

A repo-owned smoke harness layer with a manifest, suite runner, fixture leak checks, and a phase-1 smoke entrypoint that no longer ad hoc calls disposable fixture scripts.

## Validation Plan

List the smoke manifest, run a targeted smoke suite slice, rerun full phase-1 smoke, then rerun audit-control-state and enforce-worktree on the real project.

## Active Risks

- Harness law could drift into another undocumented side protocol if smoke metadata lives partly in scripts and partly in the suite runner.
- Suite-level leak checks currently focus on fixture project paths and may still miss other contamination classes such as shared artifact collisions.

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
