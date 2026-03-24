---
id: taskc-2026-03-24-2111-separate-alpha-single-assessment-artifacts-and-add-package-smoke
type: task-contract
title: "Separate alpha single-assessment artifacts and add package smoke"
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
  - task-contract
  - control-plane
confidence: high
created_at: 2026-03-24T21:11:05+08:00
updated_at: 2026-03-24T22:31:56+08:00
objective_id: obj-2026-03-23-0002
phase: execution
round_id: "round-2026-03-24-2110-stabilize-package-first-single-assessment-alpha-surface"
supersedes: []
superseded_by: []
---

## Summary

Separate alpha single-assessment artifacts, keep the install-first proof path honest, and collapse canonical host docs into docs/canonical.

## Intent

Make the 0.1.0a2 alpha surface more product-like by keeping draft/report artifact semantics distinct, proving one installed wheel can bootstrap a disposable governed host and complete one governed external-target single assessment, and moving canonical host docs into one docs/canonical tree without leaving stale root references behind.

## Allowed Changes

- Split draft and assessment artifact owner semantics in the registry, runtime, and docs without widening mutation authority.
- Keep one package-first smoke that builds or consumes the current wheel, installs it into an isolated environment, bootstraps a disposable host repo, and proves one governed external-target single assessment without mutating the target repo.
- Move the remaining canonical host product/control/release docs into docs/canonical and retarget repo-facing audit, navigation, and durable reference surfaces to that live tree.

## Forbidden Changes

- Do not broaden the natural-language surface into free-form orchestration or monitoring.
- Do not claim general live-host mutation or continuous monitoring support.

## Completion Criteria

- Draft and assessment commands no longer share one overloaded artifact owner label.
- One package-first smoke proves an installed wheel can bootstrap a disposable governed host and complete one governed external-target single assessment without mutating the external target repo.
- The repository root keeps only entrypoint docs while canonical host product/control/release docs live under docs/canonical and remain reachable through updated references.
- Repo audit and enforcement remain clean after the alpha-surface tightening and canonical-doc migration.

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

Task contract rewritten because The active task now also needs to finish the root markdown migration by moving the remaining evaluation docs into docs/ and repairing the current-task and durable-objective references that still point at the old root paths.

Task contract rewritten because The root markdown migration now also repairs one historical snapshot reference before deleting the old root evaluation docs, so the task must cover snapshots as part of the same cleanup.

Task contract rewritten because The active task has finished migrating the weakly-coupled root docs into docs/, so the task path set should drop the retired root doc names and keep only the live docs tree and real reference consumers.

Task contract rewritten because The active task now also needs to make the smoke layer Python 3.11-compatible for GitHub Actions by fixing the shared fixture cleanup helper and the remaining snapshot/adoption smokes that still use shutil.rmtree onexc.

Task contract rewritten because The active task now also finishes the root canonical-doc collapse by moving the remaining product/control/release specs into docs/canonical and retargeting the product-doc audit helpers to the new canonical location.

Task contract rewritten because The canonical-doc migration is now removing the root spec files, so the active task must target docs/canonical as the live document surface instead of keeping the old root paths in its contract.
