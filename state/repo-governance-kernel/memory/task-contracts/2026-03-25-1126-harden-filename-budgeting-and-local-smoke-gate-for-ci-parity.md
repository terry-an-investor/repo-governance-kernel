---
id: taskc-2026-03-25-1126-harden-filename-budgeting-and-local-smoke-gate-for-ci-parity
type: task-contract
title: "Harden filename budgeting and local smoke gate for CI parity"
status: completed
project_id: repo-governance-kernel
workspace_id: ws-1490b759
workspace_root: C:/Users/terryzzb/Desktop/session-memory
branch: master
git_sha: 80b47b322a49439cb9b79eb6884b8b6bdc8a89af
paths:
  - kernel
  - scripts
  - .githooks
  - docs
  - README.md
thread_ids: []
evidence_refs: []
tags:
  - task-contract
  - control-plane
confidence: high
created_at: 2026-03-25T11:26:55+08:00
updated_at: 2026-03-25T11:33:44+08:00
objective_id: obj-2026-03-23-0002
phase: execution
round_id: "round-2026-03-25-1116-start-explicit-package-config-layering-for-a4"
supersedes: []
superseded_by: []
---

## Summary

Fix the recurring submit regression by centralizing durable file-name budgeting for pivot/objective writes and aligning the local pre-push gate with the CI smoke surface that currently catches the escape.

## Intent

Fix the recurring submit regression by centralizing durable file-name budgeting for pivot/objective writes and aligning the local pre-push gate with the CI smoke surface that currently catches the escape.

## Allowed Changes

- Add one shared durable-file path budgeting helper and route pivot or objective durable writes through it instead of assembling long file names ad hoc in individual commands.
- Raise the local pre-push gate so phase-1 smoke regressions are blocked before push instead of surfacing only on GitHub Actions.

## Forbidden Changes

- Do not add compatibility shims that keep both budgeted and unbudgeted durable file naming semantics alive.
- Do not widen CI or hook policy in a way that diverges from the owner-layer commands already used by control-enforcement.

## Completion Criteria

- Shared durable file naming is reused by the pivot or objective write surfaces that currently assemble unbounded file names.
- The local pre-push hook and the documented release-facing validation surface both cover the smoke that caught the a3 escape.
- The changed path is validated by focused smoke plus the repo-level audit and enforcement commands.

## Resolution

- Added one shared durable_markdown_path helper in kernel/round_control.py and routed objective, round, task-contract, exception-contract, adjudication, and pivot writes through it across kernel commands and repo-local script entrypoints.
- Raised the source-repo .githooks/pre-push gate to run scripts/smoke_phase1.py so the same smoke surface runs locally before push instead of only on GitHub Actions.
- Validated the changed path with uv run python scripts/smoke_transition_engine.py, uv run python scripts/smoke_phase1.py, uv run python scripts/audit_product_docs.py, uv run python -m kernel.cli audit-control-state --project-id repo-governance-kernel, and uv run python -m kernel.cli enforce-worktree --project-id repo-governance-kernel --workspace-root C:/Users/terryzzb/Desktop/session-memory

## Active Risks

- If durable file names keep bypassing the shared path budget, Windows and deep fixture roots will continue to fail late and non-obviously.
- If the local hook stays weaker than CI, GitHub will keep being the first place smoke regressions are discovered.

## Status Notes

active -> completed: Shared durable filename budgeting now covers the direct memory-object write surfaces that were escaping into long-path failures, and the source-repo pre-push gate now runs the same phase-1 smoke surface that caught the a3 escape.

resolution recorded:
- Added one shared durable_markdown_path helper in kernel/round_control.py and routed objective, round, task-contract, exception-contract, adjudication, and pivot writes through it across kernel commands and repo-local script entrypoints.
- Raised the source-repo .githooks/pre-push gate to run scripts/smoke_phase1.py so the same smoke surface runs locally before push instead of only on GitHub Actions.
- Validated the changed path with uv run python scripts/smoke_transition_engine.py, uv run python scripts/smoke_phase1.py, uv run python scripts/audit_product_docs.py, uv run python -m kernel.cli audit-control-state --project-id repo-governance-kernel, and uv run python -m kernel.cli enforce-worktree --project-id repo-governance-kernel --workspace-root C:/Users/terryzzb/Desktop/session-memory

