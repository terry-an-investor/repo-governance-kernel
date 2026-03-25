---
id: round-2026-03-25-1904-retire-stale-product-identities-and-legacy-scaffolding
type: round-contract
title: "Retire stale product identities and legacy scaffolding"
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
  - round
  - control-plane
confidence: high
created_at: 2026-03-25T19:04:56+08:00
updated_at: 2026-03-25T19:12:49+08:00
objective_id: obj-2026-03-23-0002
phase: execution
supersedes: []
superseded_by: []
---

## Summary

One honest repo-owned rename and cleanup round with legacy demo framing removed from the public source tree.

## Scope

- Remove stale legacy names from live repo-owned code, docs, and control projections.
- Delete stale evaluation files and legacy-only surfaces that no longer belong to the product.
- Revalidate audit, enforcement, and acceptance smoke under the repo-governance-kernel identity.

## Deliverable

One honest repo-owned rename and cleanup round with legacy demo framing removed from the public source tree.

## Validation Plan

Pass audit-control-state, enforce-worktree, and the smallest credible smoke set after the rename cleanup.

## Active Risks

- Historical control-state prose may still carry stale identity wording that conflicts with the current product boundary.
- Deleting stale evaluation and legacy artifacts can widen the real worktree scope beyond the previous paused state unless the round captures it explicitly.

## Blockers

_none recorded_

## Status Notes

Execution remains scoped to identity retirement and legacy-surface cleanup.

Round rewritten because The active round must explicitly cover index documentation because the rename cleanup changed index/README.md too.

Round rewritten because The durable round scope should describe legacy-name cleanup generically so the projection does not need manual edits.

Round rewritten because The active round must explicitly cover repo-owned hook and CI enforcement surfaces because this cleanup changed them too.

Round rewritten because The round path scope should use the real dot-prefixed directory names for repo-owned hook and CI surfaces.
