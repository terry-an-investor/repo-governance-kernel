---
id: round-2026-03-25-1621-cut-the-0-1-0b0-beta-release
type: round-contract
title: "Cut the 0.1.0b0 beta release"
status: closed
project_id: session-memory
workspace_id: ws-1490b759
workspace_root: C:/Users/terryzzb/Desktop/session-memory
branch: master
git_sha: 5dd4f9ce31622b737f88f06b244500f790a1c726
paths:
  - pyproject.toml
  - README.md
  - kernel
  - docs
  - scripts/smoke_kernel_bootstrap.py
  - scripts/verify_release_publication.py
  - uv.lock
  - skills/use-repo-governance-kernel/SKILL.md
thread_ids: []
evidence_refs: []
tags:
  - round
  - control-plane
confidence: high
created_at: 2026-03-25T16:21:50+08:00
updated_at: 2026-03-25T16:38:57+08:00
objective_id: obj-2026-03-23-0002
phase: execution
supersedes: []
superseded_by: []
---

## Summary

A published 0.1.0b0 beta release with aligned package identity, validated artifacts, annotated tag, GitHub Release assets, and verified publication truth.

## Scope

- Replace stale alpha preview identity with the formal 0.1.0b0 beta package identity across code, docs, descriptor naming, and release records.
- Publish the beta cut only after local validation, local control-state close-out, git tag creation, remote push, GitHub Release creation, and publication verification all succeed.

## Deliverable

A published 0.1.0b0 beta release with aligned package identity, validated artifacts, annotated tag, GitHub Release assets, and verified publication truth.

## Validation Plan

Run focused docs and smoke validation, build the 0.1.0b0 sdist and wheel, verify local control-state closure, then verify remote publication after push and GitHub Release creation.
docs audit, smoke matrix, enforce-worktree, uv build, and annotated release tag v0.1.0b0
release commit 5dd4f9c, tag v0.1.0b0, docs audit, smoke matrix, enforce-worktree, uv build
release commit 5dd4f9c and tag v0.1.0b0

## Active Risks

_none recorded_

## Blockers

_none recorded_

## Status Notes

_none recorded_

Round rewritten because beta release truth also touches version-locked build metadata and the packaged repo skill entrypoint

Expanded beta release scope to include version-locked uv metadata and the packaged repo skill entrypoint so enforcement and user-facing command truth stay aligned with the renamed public surface.

active -> validation_pending: the beta release slice is implemented, validated, built, and tagged locally, so the round can enter validation-pending close-out

validated by:
- docs audit, smoke matrix, enforce-worktree, uv build, and annotated release tag v0.1.0b0

validation_pending -> captured: the beta release commit 5dd4f9c and annotated tag v0.1.0b0 durably capture the intended release state

validated by:
- release commit 5dd4f9c, tag v0.1.0b0, docs audit, smoke matrix, enforce-worktree, uv build

captured -> closed: the beta release state is captured by commit 5dd4f9c and tag v0.1.0b0, so the release round can close locally before remote publication

validated by:
- release commit 5dd4f9c and tag v0.1.0b0
