---
id: taskc-2026-03-24-2111-separate-alpha-single-assessment-artifacts-and-add-package-smoke
type: task-contract
title: "Separate alpha single-assessment artifacts and add package smoke"
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
  - task-contract
  - control-plane
confidence: high
created_at: 2026-03-24T21:11:05+08:00
updated_at: 2026-03-24T21:23:38+08:00
objective_id: obj-2026-03-23-0002
phase: execution
round_id: "round-2026-03-24-2110-stabilize-package-first-single-assessment-alpha-surface"
supersedes: []
superseded_by: []
---

## Summary

Tighten the package-facing single-assessment slice by splitting draft/report artifact semantics, proving installed-wheel bootstrap, and cleaning auxiliary docs out of the root.

## Intent

Make the 0.1.0a2 alpha surface more product-like by splitting external-target drafting from shadow assessment reporting at the owner layer, proving installed-wheel bootstrap and audit, and reducing root-doc clutter without moving canonical kernel docs out of the repository root.

## Allowed Changes

- Split draft and assessment artifact owner semantics in the registry, runtime, and docs without widening mutation authority.
- Add one package-first smoke that builds or consumes the current wheel, installs it into an isolated environment, bootstraps a disposable host repo, and audits that host.
- Move weakly-coupled auxiliary markdown docs out of the root into docs/ and update the small set of durable references that still need those paths.

## Forbidden Changes

- Do not broaden the natural-language surface into free-form orchestration or monitoring.
- Do not claim general live-host mutation or continuous monitoring support.

## Completion Criteria

- Draft and assessment commands no longer share one overloaded artifact owner label.
- One package-first smoke proves installed-wheel bootstrap and host-side audit from a disposable repo.
- The repository root keeps canonical kernel docs while moved auxiliary docs remain reachable through updated references under docs/.
- Repo audit and enforcement remain clean after the alpha-surface tightening and root-doc cleanup.

## Resolution

_none recorded_

## Active Risks

- The first package smoke may validate bootstrap and audit but still leave external-target single assessment under package-install coverage for a later slice.

## Status Notes

Task contract rewritten because The install-first package smoke will be registered in the smoke manifest and suite surfaces, so the task boundary must include those real harness paths.

Task contract rewritten because Root markdown cleanup now includes moving weakly-coupled auxiliary docs and updating durable references, so the task boundary must cover the real doc-topology write set.

Task contract rewritten because Root doc cleanup deletes the old auxiliary paths after migrating them into docs/, so the task boundary must cover both the new docs tree and the retiring root files.
