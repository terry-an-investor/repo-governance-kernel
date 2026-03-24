---
id: taskc-2026-03-24-2111-separate-alpha-single-assessment-artifacts-and-add-package-smoke
type: task-contract
title: "Separate alpha single-assessment artifacts and add package smoke"
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
  - task-contract
  - control-plane
confidence: high
created_at: 2026-03-24T21:11:05+08:00
updated_at: 2026-03-24T21:57:28+08:00
objective_id: obj-2026-03-23-0002
phase: execution
round_id: "round-2026-03-24-2110-stabilize-package-first-single-assessment-alpha-surface"
supersedes: []
superseded_by: []
---

## Summary

Separate alpha single-assessment artifacts and extend package smoke to installed-wheel external assessment.

## Intent

Make the 0.1.0a2 alpha surface more product-like by keeping draft/report artifact semantics distinct, proving one installed wheel can bootstrap a disposable governed host and complete one governed external-target single assessment, and tightening the package-facing quickstart around that same path.

## Allowed Changes

- Split draft and assessment artifact owner semantics in the registry, runtime, and docs without widening mutation authority.
- Add one package-first smoke that builds or consumes the current wheel, installs it into an isolated environment, bootstraps a disposable host repo, and audits that host.
- Move weakly-coupled auxiliary markdown docs out of the root into docs/ and update the small set of durable references that still need those paths.
- Extend the package-first smoke so an installed wheel bootstraps a disposable governed host, runs one governed external-target single assessment against a disposable external repo, and proves the target repo remains unmutated.
- Register that package-first smoke in the smoke manifest and suite and align package-facing quickstart and release evidence to the same installed-wheel proof path.
- Keep canonical kernel docs at the root while moving weakly-coupled auxiliary markdown into docs/ and updating the small durable reference set.

## Forbidden Changes

- Do not broaden the natural-language surface into free-form orchestration or monitoring.
- Do not claim general live-host mutation or continuous monitoring support.

## Completion Criteria

- Draft and assessment commands no longer share one overloaded artifact owner label.
- One package-first smoke proves installed-wheel bootstrap and host-side audit from a disposable repo.
- The repository root keeps canonical kernel docs while moved auxiliary docs remain reachable through updated references under docs/.
- Repo audit and enforcement remain clean after the alpha-surface tightening and root-doc cleanup.
- One package-first smoke proves an installed wheel can bootstrap a disposable governed host and complete one governed external-target single assessment without mutating the external target repo.
- That package-first smoke is registered in the smoke manifest/suite and package-facing docs point at the same bounded proof path.

## Resolution

_none recorded_

## Active Risks

- The first package smoke may validate bootstrap and audit but still leave external-target single assessment under package-install coverage for a later slice.

## Status Notes

Task contract rewritten because The install-first package smoke will be registered in the smoke manifest and suite surfaces, so the task boundary must include those real harness paths.

Task contract rewritten because Root markdown cleanup now includes moving weakly-coupled auxiliary docs and updating durable references, so the task boundary must cover the real doc-topology write set.

Task contract rewritten because Root doc cleanup deletes the old auxiliary paths after migrating them into docs/, so the task boundary must cover both the new docs tree and the retiring root files.

Task contract rewritten because The active task now needs to prove installed-wheel external-target single assessment and register that proof path in package-facing docs and smoke surfaces, so the task contract must describe that real execution boundary.

Task contract rewritten because The active task now also needs to repair GitHub Actions enforcement by passing an explicit runner workspace root through the owner-layer command surface, so the task must cover the workflow file and enforcement wrapper path.
