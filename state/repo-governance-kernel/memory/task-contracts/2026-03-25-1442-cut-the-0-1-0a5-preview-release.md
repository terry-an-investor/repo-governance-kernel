---
id: taskc-2026-03-25-1442-cut-the-0-1-0a5-preview-release
type: task-contract
title: "Cut the 0.1.0a5 preview release"
status: completed
project_id: repo-governance-kernel
workspace_id: ws-1490b759
workspace_root: C:/Users/terryzzb/Desktop/session-memory
branch: master
git_sha: c309b4a51f83650c178216be08b71f2263567910
paths:
  - pyproject.toml
  - uv.lock
  - README.md
  - kernel/README.md
  - docs/README.md
  - docs/canonical/IMPLEMENTATION_PLAN.md
  - docs/canonical/PUBLIC_ALPHA_SURFACE.md
  - docs/canonical/RELEASE.md
  - docs/canonical/TRANSITION_COMMANDS.md
  - kernel/docs/PUBLIC_ALPHA_SURFACE.md
  - kernel/docs/TRANSITION_COMMANDS.md
  - kernel/public_alpha_surface.py
thread_ids: []
evidence_refs: []
tags:
  - task-contract
  - control-plane
confidence: high
created_at: 2026-03-25T14:42:17+08:00
updated_at: 2026-03-25T14:50:46+08:00
objective_id: obj-2026-03-23-0002
phase: execution
round_id: "round-2026-03-25-1441-cut-the-0-1-0a5-preview-release"
supersedes: []
superseded_by: []
---

## Summary

Make a5 the current package release identity instead of only a source-head milestone.

## Intent

Align package metadata, machine-readable public-surface descriptors, and release-facing docs on 0.1.0a5, then validate the packaged path before push.

## Allowed Changes

- Update release-owned version strings, wheel-install examples, and release-plan prose to make 0.1.0a5 the current preview cut.
- Advance the next planned release target to 0.1.0b0 where package-facing docs speak in version-roadmap terms.
- Run package-facing validation and publication-prep checks that do not require remote mutation.

## Forbidden Changes

- Do not widen the public command set or add new product capability under the guise of a version cut.
- Do not mutate historical task-contract records that only document older release cuts.

## Completion Criteria

- Package metadata, machine-readable public-surface descriptors, and release-facing docs all report 0.1.0a5 as the current preview release.
- Installed-wheel proof and release-facing doc audit pass against the a5 cut.
- audit-control-state and enforce-worktree both return ok before the release commit is pushed.

## Resolution

- package metadata, public-surface descriptors, and release-facing docs now report 0.1.0a5 as the current preview release
- release-facing validation passed for audit-product-docs, onboarding smoke, assessment smoke, and installed-wheel bootstrap smoke

## Active Risks

_none recorded_

## Status Notes

active -> completed: the a5 preview release cut is complete in commit c309b4a and tagged as v0.1.0a5

resolution recorded:
- package metadata, public-surface descriptors, and release-facing docs now report 0.1.0a5 as the current preview release
- release-facing validation passed for audit-product-docs, onboarding smoke, assessment smoke, and installed-wheel bootstrap smoke

