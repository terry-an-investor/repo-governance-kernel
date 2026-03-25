# Active Round

- Round id: `round-2026-03-25-1348-add-release-publication-verifier-and-checklist`
- Objective id: `obj-2026-03-23-0002`
- Status: `active`

## Scope

- Add one script that verifies remote branch head, release tag, GitHub Release object, and expected assets for a version.
- Update canonical release docs so the version-cut flow explicitly includes commit push, tag push, release creation, and remote verification.

## Deliverable

One repo-owned release publication verifier and one canonical release checklist that make release completion auditable instead of implicit.

## Validation Plan

Run the release verifier against v0.1.0a4, then rerun audit_product_docs, audit-control-state, and enforce-worktree.

## Active Risks

- If release publication remains a human-memory step, future cuts can again stop at push or tag and still be mistaken for complete releases.

## Blockers

_none recorded_
