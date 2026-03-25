# Active Round

- Round id: `round-2026-03-25-1500-require-local-sync-before-remote-push`
- Objective id: `obj-2026-03-23-0002`
- Status: `active`

## Scope

- Add a local repo rule that requires local control-state sync before any git push.
- Align the canonical release checklist to tag locally, close the release round locally, and only then push branch and tag.

## Deliverable

One durable push-order rule aligned across repo execution rules and release docs.

## Validation Plan

Run audit_product_docs, audit-control-state, and enforce-worktree after the doc update.

## Active Risks

_none recorded_

## Blockers

_none recorded_
