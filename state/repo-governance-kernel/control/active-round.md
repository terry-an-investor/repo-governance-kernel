# Active Round

- Round id: `round-2026-03-25-1904-retire-stale-product-identities-and-legacy-scaffolding`
- Objective id: `obj-2026-03-23-0002`
- Status: `active`

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
