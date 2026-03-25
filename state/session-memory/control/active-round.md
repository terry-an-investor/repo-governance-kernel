# Active Round

- Round id: `round-2026-03-25-1332-correct-a4-release-semantics-and-cut-real-tag`
- Objective id: `obj-2026-03-23-0002`
- Status: `active`

## Scope

- Update release-facing version descriptors so the current package reports a4 while still noting that the entrypoint set was first frozen in a3.
- Cut the missing a4 git tag after docs and machine-readable surfaces are corrected and revalidated.

## Deliverable

One honest a4 release story: current public surfaces report a4, docs explain the a3 freeze lineage clearly, and origin carries an a4 tag.

## Validation Plan

Run focused doc/config validation, audit-control-state, enforce-worktree, then create and push the a4 tag.

## Active Risks

- If current release surfaces keep saying a3, users will not know which preview they are actually installing.

## Blockers

_none recorded_
