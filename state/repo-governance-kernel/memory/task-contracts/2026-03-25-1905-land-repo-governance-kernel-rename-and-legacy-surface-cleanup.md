---
id: taskc-2026-03-25-1905-land-repo-governance-kernel-rename-and-legacy-surface-cleanup
type: task-contract
title: "Land repo-governance-kernel rename and legacy-surface cleanup"
status: active
project_id: repo-governance-kernel
workspace_id: ws-1490b759
workspace_root: C:/Users/terryzzb/Desktop/session-memory
branch: master
git_sha: ccf86ba6952d1ffe3fc12e96136f287de2ca3536
paths:
  - AGENTS.md
  - README.md
  - docs/
  - .github/
  - .githooks/
  - index/
  - kernel/
  - scripts/
  - state/
thread_ids: []
evidence_refs: []
tags:
  - task-contract
  - control-plane
confidence: high
created_at: 2026-03-25T19:05:20+08:00
updated_at: 2026-03-25T19:12:49+08:00
objective_id: obj-2026-03-23-0002
phase: execution
round_id: "round-2026-03-25-1904-retire-stale-product-identities-and-legacy-scaffolding"
supersedes: []
superseded_by: []
---

## Summary

Bring the live source tree, repo-owned state, and docs into alignment with the repo-governance-kernel identity and remove stale legacy surfaces.

## Intent

Retire stale repo-owned names, delete legacy-only surfaces, and keep the control line honest through validation.

## Allowed Changes

- Rename repo-owned legacy identity references to the repo-governance-kernel surface in live code, docs, and control projections.
- Delete stale legacy scripts, docs, state artifacts, and other host-repo surfaces that no longer belong to the product.
- Run bounded validation and refresh current-task anchors so the rename round closes honestly.

## Forbidden Changes

- Do not change the physical workspace root path C:/Users/terryzzb/Desktop/session-memory where it refers to the real local checkout.
- Do not add new product scope or new long-running monitoring behavior in this cleanup round.

## Completion Criteria

- Live repo surfaces no longer present stale retired names or demo-only framing as the product identity, and rename validation passes.

## Resolution

_none recorded_

## Active Risks

- Historical state files may need selective wording cleanup so current control projections stop inheriting stale legacy phrasing.

## Status Notes

Task remains the bounded owner layer for identity retirement and stale-surface cleanup.

Task contract rewritten because The active task contract must explicitly cover index documentation because the rename cleanup changed index/README.md too.

Task contract rewritten because The active task contract should describe legacy-name cleanup generically instead of repeating retired product names.

Task contract rewritten because The task contract path scope should use the real dot-prefixed directory names for repo-owned hook and CI surfaces.
