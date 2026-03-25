---
id: taskc-2026-03-24-2111-separate-alpha-single-assessment-artifacts-and-add-package-smoke
type: task-contract
title: "Separate alpha single-assessment artifacts and add package smoke"
status: completed
project_id: session-memory
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
  - task-contract
  - control-plane
confidence: high
created_at: 2026-03-24T21:11:05+08:00
updated_at: 2026-03-25T08:42:59+08:00
objective_id: obj-2026-03-23-0002
phase: execution
round_id: "round-2026-03-24-2110-stabilize-package-first-single-assessment-alpha-surface"
supersedes: []
superseded_by: []
---

## Summary

Separate alpha single-assessment artifacts, keep the install-first proof path honest, and migrate canonical host state into state/<project_id>.

## Intent

Make the 0.1.0a2 alpha surface more product-like by keeping draft/report artifact semantics distinct, proving one installed wheel can bootstrap a disposable governed host and complete one governed external-target single assessment, and replacing the old projects/<project_id> state layout with one canonical state/<project_id> tree.

## Allowed Changes

- Split draft and assessment artifact owner semantics in the registry, runtime, and docs without widening mutation authority.
- Keep one package-first smoke that builds or consumes the current wheel, installs it into an isolated environment, bootstraps a disposable host repo, and proves one governed external-target single assessment without mutating the target repo.
- Migrate the canonical host state layout from projects/<project_id> to state/<project_id> and retarget repo-facing audit, runtime, navigation, and durable reference surfaces to that live tree.

## Forbidden Changes

- Do not broaden the natural-language surface into free-form orchestration or monitoring.
- Do not claim general live-host mutation or continuous monitoring support.

## Completion Criteria

- Draft and assessment commands no longer share one overloaded artifact owner label.
- One package-first smoke proves an installed wheel can bootstrap a disposable governed host and complete one governed external-target single assessment without mutating the external target repo.
- The repository root keeps only entrypoint docs while canonical host state lives under state/<project_id> and no runtime or durable reference still depends on projects/<project_id>.
- Repo audit and enforcement remain clean after the alpha-surface tightening and state-root migration.

## Resolution

- Canonical project state now lives under state/<project_id> and no runtime or live documentation surface depends on projects/<project_id>.
- Package-first validation still proves installed-wheel bootstrap plus one bounded external-target single assessment.
- audit-control-state, enforce-worktree, smoke_phase1, and smoke_kernel_bootstrap all passed on the committed migration baseline.

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

Task contract rewritten because The active task now executes the real state-root migration, so it must cover the shared runtime resolver, broad scripts/kernel consumers, the retiring projects tree, and the new state tree together.

Task contract rewritten because The state-root migration is now real, so the active task must drop the retired projects tree and explicitly target state/<project_id> as the only live host-state layout.

Task contract rewritten because The state-root migration also repairs the derived-index contract read surface, so the active task must cover index alongside the runtime and canonical docs it now describes.

active -> completed: The state-root migration, package-first proof, and canonical-doc cleanup all landed and validated cleanly, so this task contract is resolved.

resolution recorded:
- Canonical project state now lives under state/<project_id> and no runtime or live documentation surface depends on projects/<project_id>.
- Package-first validation still proves installed-wheel bootstrap plus one bounded external-target single assessment.
- audit-control-state, enforce-worktree, smoke_phase1, and smoke_kernel_bootstrap all passed on the committed migration baseline.
