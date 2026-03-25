---
id: round-2026-03-25-1348-add-release-publication-verifier-and-checklist
type: round-contract
title: "Add release publication verifier and checklist"
status: closed
project_id: session-memory
workspace_id: ws-1490b759
workspace_root: C:/Users/terryzzb/Desktop/session-memory
branch: master
git_sha: 94badecd4ce4fa3ae52b8fcab8c9e58096927200
paths:
  - scripts
  - docs
  - README.md
  - .github
thread_ids: []
evidence_refs: []
tags:
  - round
  - control-plane
confidence: high
created_at: 2026-03-25T13:48:12+08:00
updated_at: 2026-03-25T13:52:50+08:00
objective_id: obj-2026-03-23-0002
phase: execution
supersedes: []
superseded_by: []
---

## Summary

One repo-owned release publication verifier and one canonical release checklist that make release completion auditable instead of implicit.

## Scope

- Add one script that verifies remote branch head, release tag, GitHub Release object, and expected assets for a version.
- Update canonical release docs so the version-cut flow explicitly includes commit push, tag push, release creation, and remote verification.

## Deliverable

One repo-owned release publication verifier and one canonical release checklist that make release completion auditable instead of implicit.

## Validation Plan

Run the release verifier against v0.1.0a4, then rerun audit_product_docs, audit-control-state, and enforce-worktree.
verify_release_publication.py
session_memory.py verify-release-publication
audit_product_docs
audit-control-state
enforce-worktree
verify_release_publication.py
session_memory.py verify-release-publication
audit_product_docs
audit-control-state
enforce-worktree
verify_release_publication.py
session_memory.py verify-release-publication
audit_product_docs
audit-control-state
enforce-worktree

## Active Risks

- If release publication remains a human-memory step, future cuts can again stop at push or tag and still be mistaken for complete releases.

## Blockers

_none recorded_

## Status Notes

active -> validation_pending: The release publication process fix is implemented and validated.

validated by:
- verify_release_publication.py
- session_memory.py verify-release-publication
- audit_product_docs
- audit-control-state
- enforce-worktree

validation_pending -> captured: The release publication process fix is validated and should now be captured.

validated by:
- verify_release_publication.py
- session_memory.py verify-release-publication
- audit_product_docs
- audit-control-state
- enforce-worktree

captured -> closed: The release publication process fix is complete and no further active work remains in this round.

validated by:
- verify_release_publication.py
- session_memory.py verify-release-publication
- audit_product_docs
- audit-control-state
- enforce-worktree
