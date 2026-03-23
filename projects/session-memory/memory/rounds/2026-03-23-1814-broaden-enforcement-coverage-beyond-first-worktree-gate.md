---
id: round-2026-03-23-1814-broaden-enforcement-coverage-beyond-first-worktree-gate
type: round-contract
title: "Broaden enforcement coverage beyond first worktree gate"
status: active
project_id: session-memory
workspace_id: ws-1490b759
workspace_root: C:/Users/terryzzb/Desktop/session-memory
branch: master
git_sha: 5988e6c5379a0def14b1c1cfc47c19ddc6172c06
paths:
  - AGENTS.md
  - .githooks/
  - scripts/
  - CONTROL_SYSTEM.md
  - SCHEMA.md
  - STATE_MACHINE.md
  - TRANSITION_COMMANDS.md
  - projects/session-memory/control/
  - projects/session-memory/current/
thread_ids: []
evidence_refs: []
tags:
  - round
  - control-plane
confidence: high
created_at: 2026-03-23T18:14:34+08:00
updated_at: 2026-03-23T18:14:34+08:00
objective_id: obj-2026-03-23-0002
phase: execution
supersedes: []
superseded_by: []
---

## Summary

A successor enforcement milestone that extends automatic penalties beyond the first worktree gate.

## Scope

- Add the next enforcement slice for workaround or exception-contract coverage instead of only scope and projection drift.
- Decide how CI and commit-time enforcement should share the same owner-layer checks.
- Keep the enforcement model project-agnostic while broadening what counts as blocked dishonest work.
- Use constitution-declared guarded exception paths instead of heuristics so blocked workaround debt is backed by durable project law.

## Deliverable

A successor enforcement milestone that extends automatic penalties beyond the first worktree gate.

## Validation Plan

Define the next blocked-state class, connect it to the same enforcement owner layer, and prove it with targeted validation before broader smoke.
Prove one blocked case and one allowed case on a disposable fixture where guarded dirty paths only pass after an active exception contract explicitly covers them.

## Active Risks

- Broader enforcement could become noisy if workaround detection is based on weak heuristics rather than explicit durable objects.

## Blockers

_none recorded_

## Status Notes

Opened after closing the first automatic worktree enforcement slice.

Constitution-declared guarded exception paths are now enforced as a second blocked-state class.

validated by:
- uv run python scripts/smoke_guarded_exception_enforcement.py
- uv run python scripts/audit_control_state.py --project-id session-memory
- uv run python scripts/enforce_worktree.py --project-id session-memory
