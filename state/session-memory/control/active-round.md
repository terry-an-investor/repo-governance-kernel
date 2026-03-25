# Active Round

- Round id: `round-2026-03-25-1441-cut-the-0-1-0a5-preview-release`
- Objective id: `obj-2026-03-23-0002`
- Status: `active`

## Scope

- Bump release-owned version metadata and package-facing docs from 0.1.0a4 to 0.1.0a5.
- Advance the next planned release line from 0.1.0a5 to 0.1.0b0 where docs currently speak in release terms.
- Rebuild the package proof and re-run release-facing validation before push.

## Deliverable

One clean a5 preview release commit with aligned version truth and validated package proof.

## Validation Plan

Run audit-product-docs, smoke_kernel_bootstrap, audit-control-state, and enforce-worktree after the version cut.

## Active Risks

_none recorded_

## Blockers

_none recorded_
