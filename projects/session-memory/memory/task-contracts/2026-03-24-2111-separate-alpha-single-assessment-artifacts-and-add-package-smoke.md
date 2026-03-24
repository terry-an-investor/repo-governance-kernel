---
id: taskc-2026-03-24-2111-separate-alpha-single-assessment-artifacts-and-add-package-smoke
type: task-contract
title: "Separate alpha single-assessment artifacts and add package smoke"
status: active
project_id: session-memory
workspace_id: ws-1490b759
workspace_root: C:/Users/terryzzb/Desktop/session-memory
branch: master
git_sha: 1212345248b7910d6feb2bf2b4de3482b32bd7c6
paths:
  - kernel
  - scripts/smoke_kernel_bootstrap.py
  - scripts/session_memory.py
  - scripts/smoke_manifest.py
  - scripts/run_smoke_suite.py
  - README.md
  - RELEASE.md
  - TRANSITION_COMMANDS.md
  - kernel/README.md
  - kernel/docs/TRANSITION_COMMANDS.md
thread_ids: []
evidence_refs: []
tags:
  - task-contract
  - control-plane
confidence: high
created_at: 2026-03-24T21:11:05+08:00
updated_at: 2026-03-24T21:12:12+08:00
objective_id: obj-2026-03-23-0002
phase: execution
round_id: "round-2026-03-24-2110-stabilize-package-first-single-assessment-alpha-surface"
supersedes: []
superseded_by: []
---

## Summary

Tighten the first package-facing single-assessment slice by separating draft/report artifact semantics and proving installed-wheel bootstrap from a disposable host.

## Intent

Make the 0.1.0a2 alpha surface more product-like by splitting external-target drafting from shadow assessment reporting at the owner layer, then adding one install-first smoke that validates kernel bootstrap and audit from an installed wheel.

## Allowed Changes

- Split draft and assessment artifact owner semantics in the registry, runtime, and docs without widening mutation authority.
- Add one package-first smoke that builds or consumes the current wheel, installs it into an isolated environment, bootstraps a disposable host repo, and audits that host.
- Update package-facing docs and release notes to describe the cleaner artifact split and package-first validation path.

## Forbidden Changes

- Do not broaden the natural-language surface into free-form orchestration or monitoring.
- Do not claim general live-host mutation or continuous monitoring support.

## Completion Criteria

- Draft and assessment commands no longer share one overloaded artifact owner label.
- One package-first smoke proves installed-wheel bootstrap and host-side audit from a disposable repo.
- Repo audit and enforcement remain clean after the alpha-surface tightening.

## Resolution

_none recorded_

## Active Risks

- The first package smoke may validate bootstrap and audit but still leave external-target single assessment under package-install coverage for a later slice.

## Status Notes

Task contract rewritten because The install-first package smoke will be registered in the smoke manifest and suite surfaces, so the task boundary must include those real harness paths.
