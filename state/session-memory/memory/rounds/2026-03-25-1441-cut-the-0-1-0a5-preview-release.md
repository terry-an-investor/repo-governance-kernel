---
id: round-2026-03-25-1441-cut-the-0-1-0a5-preview-release
type: round-contract
title: "Cut the 0.1.0a5 preview release"
status: active
project_id: session-memory
workspace_id: ws-1490b759
workspace_root: C:/Users/terryzzb/Desktop/session-memory
branch: master
git_sha: 7ff723b146ea86ea7c9751c8e99257a920ae272a
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
  - round
  - control-plane
confidence: high
created_at: 2026-03-25T14:41:24+08:00
updated_at: 2026-03-25T14:41:24+08:00
objective_id: obj-2026-03-23-0002
phase: execution
supersedes: []
superseded_by: []
---

## Summary

One clean a5 preview release commit with aligned version truth and validated package proof.

## Scope

- Bump release-owned version metadata and package-facing docs from 0.1.0a4 to 0.1.0a5.
- Advance the next planned release line from 0.1.0a5 to 0.1.0b0 where docs currently speak in release terms.
- Rebuild the package proof and re-run release-facing validation before push.

## Deliverable

One clean a5 preview release commit with aligned version truth and validated package proof.

## Validation Plan

Run audit-product-docs, smoke_kernel_bootstrap, audit-control-state, and enforce-worktree after the version cut.

## Active Risks

_none recorded_

## Blockers

_none recorded_

## Status Notes

_none recorded_
