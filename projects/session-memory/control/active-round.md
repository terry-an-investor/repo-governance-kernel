# Active Round

- Round id: `round-2026-03-23-1814-broaden-enforcement-coverage-beyond-first-worktree-gate`
- Objective id: `obj-2026-03-23-0002`
- Status: `active`

## Scope

- Land rewrite-open-round as the owner-layer primitive for rewriting one open round contract without changing round identity.
- Integrate that primitive into record-soft-pivot, set-phase, and adjudication follow-up execution instead of leaving round review as prose only.
- Validate the rewrite path on disposable fixtures and update canonical control docs plus current project state to match the new capability.

## Deliverable

A durable round rewrite milestone with one reusable rewrite primitive, real integrations for soft pivot and adjudication follow-ups, and canonical docs plus sample state updated to match observed behavior.

## Validation Plan

Run targeted smokes for objective-line and adjudication rewrite flows, then rerun phase-1 smoke, worktree enforcement, and control audit on the real project.

## Active Risks

- The rewrite primitive could stay too narrow and only patch symptoms instead of becoming the reusable owner-layer mutation path.
- Project samples and canonical docs could drift from the new rewrite behavior if the round narrative is not durably updated in the same milestone.

## Blockers

_none recorded_
