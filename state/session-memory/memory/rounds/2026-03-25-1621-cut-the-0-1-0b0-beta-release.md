---
id: round-2026-03-25-1621-cut-the-0-1-0b0-beta-release
type: round-contract
title: "Cut the 0.1.0b0 beta release"
status: active
project_id: session-memory
workspace_id: ws-1490b759
workspace_root: C:/Users/terryzzb/Desktop/session-memory
branch: master
git_sha: b1a95fbe9f5aa17a9dd59d9fbdda5c1629b6b8f1
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
updated_at: 2026-03-25T16:35:43+08:00
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

## Active Risks

_none recorded_

## Blockers

_none recorded_

## Status Notes

_none recorded_

Round rewritten because beta release truth also touches version-locked build metadata and the packaged repo skill entrypoint

Expanded beta release scope to include version-locked uv metadata and the packaged repo skill entrypoint so enforcement and user-facing command truth stay aligned with the renamed public surface.
