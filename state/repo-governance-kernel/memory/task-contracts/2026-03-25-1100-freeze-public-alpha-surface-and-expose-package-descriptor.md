---
id: taskc-2026-03-25-1100-freeze-public-alpha-surface-and-expose-package-descriptor
type: task-contract
title: "Freeze public alpha surface and expose package descriptor"
status: completed
project_id: repo-governance-kernel
workspace_id: ws-1490b759
workspace_root: C:/Users/terryzzb/Desktop/session-memory
branch: master
git_sha: 0fcdc4fc4110039273ff0f761eebe95870db9551
paths:
  - kernel
  - scripts
  - docs
  - README.md
  - kernel/README.md
  - skills
thread_ids: []
evidence_refs: []
tags:
  - task-contract
  - control-plane
confidence: high
created_at: 2026-03-25T11:00:57+08:00
updated_at: 2026-03-25T11:06:14+08:00
objective_id: obj-2026-03-23-0002
phase: execution
round_id: "round-2026-03-25-0946-make-package-first-repo-onboarding-real"
supersedes: []
superseded_by: []
---

## Summary

Turn the agreed a3 public alpha surface into one machine-readable package contract, wire one descriptor command, and align package docs and package proof around that contract.

## Intent

Make the public alpha surface a registry-owned truth source instead of a set of loosely synchronized prose sections.

## Allowed Changes

- Add one machine-readable public alpha surface registry for the bounded package entrypoints and repo-owned agent wrappers.
- Expose that registry through one package-facing descriptor command and installed-package proof.
- Update canonical and package docs so public alpha surface, repo-owned agent packaging, and internal host-local surfaces are clearly separated.

## Forbidden Changes

- Do not broaden public alpha authority beyond already implemented bounded entrypoints.
- Do not add monitoring, server behavior, or generic natural-language mutation routing.

## Completion Criteria

- One installed package command can describe the public alpha surface as structured data.
- Docs and skill packaging clearly separate public alpha surface from internal or host-local surfaces.
- The package proof covers the public alpha descriptor and repo audits remain clean.

## Resolution

- Added one public-alpha surface registry plus the describe-public-alpha-surface package command.
- Added canonical and package-facing public-alpha surface docs and aligned entry docs around that split.
- Updated the installed-wheel smoke to validate the public alpha descriptor and expected command set.

## Active Risks

_none recorded_

## Status Notes

active -> completed: The public alpha surface is now frozen as one machine-readable package contract and is covered by the installed-package proof.

resolution recorded:
- Added one public-alpha surface registry plus the describe-public-alpha-surface package command.
- Added canonical and package-facing public-alpha surface docs and aligned entry docs around that split.
- Updated the installed-wheel smoke to validate the public alpha descriptor and expected command set.

