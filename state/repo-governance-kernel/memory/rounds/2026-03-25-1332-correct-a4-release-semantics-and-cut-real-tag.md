---
id: round-2026-03-25-1332-correct-a4-release-semantics-and-cut-real-tag
type: round-contract
title: "Correct a4 release semantics and cut real tag"
status: closed
project_id: repo-governance-kernel
workspace_id: ws-1490b759
workspace_root: C:/Users/terryzzb/Desktop/session-memory
branch: master
git_sha: 092d70cbe011a40d730a23b365d4e357b4decb94
paths:
  - kernel
  - docs
  - README.md
  - pyproject.toml
  - uv.lock
  - .github
thread_ids: []
evidence_refs: []
tags:
  - round
  - control-plane
confidence: high
created_at: 2026-03-25T13:32:04+08:00
updated_at: 2026-03-25T13:37:47+08:00
objective_id: obj-2026-03-23-0002
phase: execution
supersedes: []
superseded_by: []
---

## Summary

One honest a4 release story: current public surfaces report a4, docs explain the a3 freeze lineage clearly, and origin carries an a4 tag.

## Scope

- Update release-facing version descriptors so the current package reports a4 while still noting that the entrypoint set was first frozen in a3.
- Cut the missing a4 git tag after docs and machine-readable surfaces are corrected and revalidated.

## Deliverable

One honest a4 release story: current public surfaces report a4, docs explain the a3 freeze lineage clearly, and origin carries an a4 tag.

## Validation Plan

Run focused doc/config validation, audit-control-state, enforce-worktree, then create and push the a4 tag.
describe-public-alpha-surface
audit_product_docs
smoke_kernel_bootstrap
audit-control-state
enforce-worktree
describe-public-alpha-surface
audit_product_docs
smoke_kernel_bootstrap
audit-control-state
enforce-worktree
describe-public-alpha-surface
audit_product_docs
smoke_kernel_bootstrap
audit-control-state
enforce-worktree

## Active Risks

- If current release surfaces keep saying a3, users will not know which preview they are actually installing.

## Blockers

_none recorded_

## Status Notes

active -> validation_pending: The a4 release-correction round is implemented and externally published.

validated by:
- describe-public-alpha-surface
- audit_product_docs
- smoke_kernel_bootstrap
- audit-control-state
- enforce-worktree

validation_pending -> captured: The a4 release-correction round is validated and should now be captured.

validated by:
- describe-public-alpha-surface
- audit_product_docs
- smoke_kernel_bootstrap
- audit-control-state
- enforce-worktree

captured -> closed: The a4 release-correction round is complete and no further active work remains in it.

validated by:
- describe-public-alpha-surface
- audit_product_docs
- smoke_kernel_bootstrap
- audit-control-state
- enforce-worktree

