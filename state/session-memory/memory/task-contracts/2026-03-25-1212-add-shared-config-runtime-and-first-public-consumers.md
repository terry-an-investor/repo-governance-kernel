---
id: taskc-2026-03-25-1212-add-shared-config-runtime-and-first-public-consumers
type: task-contract
title: "Add shared config runtime and first public consumers"
status: completed
project_id: session-memory
workspace_id: ws-1490b759
workspace_root: C:/Users/terryzzb/Desktop/session-memory
branch: master
git_sha: 59745309e19dbca9365bc8c99e520c3a8ca467c9
paths:
  - kernel
  - docs
  - README.md
  - pyproject.toml
  - scripts
thread_ids: []
evidence_refs: []
tags:
  - task-contract
  - control-plane
confidence: high
created_at: 2026-03-25T12:12:07+08:00
updated_at: 2026-03-25T12:54:55+08:00
objective_id: obj-2026-03-23-0002
phase: execution
round_id: "round-2026-03-25-1116-start-explicit-package-config-layering-for-a4"
supersedes: []
superseded_by: []
---

## Summary

Add one owner-layer config runtime that resolves repo_root and project_id across flags, environment, user config, project config, and local override, then wire the first public-alpha consumers onto that shared surface instead of leaving config semantics implicit in each command.

## Intent

Add one owner-layer config runtime that resolves repo_root and project_id across flags, environment, user config, project config, and local override, then wire the first public-alpha consumers onto that shared surface instead of leaving config semantics implicit in each command.

## Allowed Changes

- Add one shared config runtime and one package-facing describe-config command that reports the resolved config surface and source precedence.
- Make the first public-alpha commands consume the shared config runtime for repo_root or project_id resolution instead of requiring only explicit flags.

## Forbidden Changes

- Do not scatter config precedence rules across individual commands after the shared runtime exists.
- Do not claim provider-level or model-level configuration before repo_root and project_id layering is proven and documented.

## Completion Criteria

- One machine-readable package-facing config command exists and reports the resolved repo_root and project_id surface with source attribution.
- At least one public-alpha consumer path uses the shared config runtime instead of only ad hoc flag parsing.
- The new config surface is covered by focused smoke plus repo-level audit and enforcement.

## Resolution

- Added kernel/config_runtime.py and the package-facing describe-config command with source-attributed repo_root/project_id resolution.
- Wired kernel.cli to resolve project_id through the shared runtime for public alpha commands such as audit-control-state.
- Added smoke_config_runtime, integrated it into repo acceptance smoke, and extended smoke_kernel_bootstrap with installed-package config proof.

## Active Risks

- If config precedence is ambiguous, installed-package behavior will still depend on repo-local knowledge or trial-and-error.
- If only one command uses the runtime and the rest keep private parsing, a4 will reintroduce semantics drift under a config label.

## Status Notes

active -> completed: The shared config runtime, describe-config surface, first public consumer wiring, and installed config proof are now committed.

resolution recorded:
- Added kernel/config_runtime.py and the package-facing describe-config command with source-attributed repo_root/project_id resolution.
- Wired kernel.cli to resolve project_id through the shared runtime for public alpha commands such as audit-control-state.
- Added smoke_config_runtime, integrated it into repo acceptance smoke, and extended smoke_kernel_bootstrap with installed-package config proof.
