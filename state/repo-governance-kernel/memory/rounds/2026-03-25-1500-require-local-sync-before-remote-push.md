---
id: round-2026-03-25-1500-require-local-sync-before-remote-push
type: round-contract
title: "Require local sync before remote push"
status: closed
project_id: repo-governance-kernel
workspace_id: ws-1490b759
workspace_root: C:/Users/terryzzb/Desktop/session-memory
branch: master
git_sha: dac91cb3add4232dd3f5167565a073ad020c5c29
paths:
  - AGENTS.md
  - docs/canonical/RELEASE.md
thread_ids: []
evidence_refs: []
tags:
  - round
  - control-plane
confidence: high
created_at: 2026-03-25T15:00:11+08:00
updated_at: 2026-03-25T15:02:56+08:00
objective_id: obj-2026-03-23-0002
phase: execution
supersedes: []
superseded_by: []
---

## Summary

One durable push-order rule aligned across repo execution rules and release docs.

## Scope

- Add a local repo rule that requires local control-state sync before any git push.
- Align the canonical release checklist to tag locally, close the release round locally, and only then push branch and tag.

## Deliverable

One durable push-order rule aligned across repo execution rules and release docs.

## Validation Plan

Run audit_product_docs, audit-control-state, and enforce-worktree after the doc update.
scripts/audit_product_docs.py
audit-control-state
enforce-worktree
commit dac91cb
commit dac91cb

## Active Risks

_none recorded_

## Blockers

_none recorded_

## Status Notes

active -> validation_pending: the push-order rule change passed local doc and control validation

validated by:
- scripts/audit_product_docs.py
- audit-control-state
- enforce-worktree

validation_pending -> captured: the push-order rule is durably recorded in commit dac91cb

validated by:
- commit dac91cb

captured -> closed: the push-order rule round is complete and no open implementation work remains in this boundary

validated by:
- commit dac91cb

