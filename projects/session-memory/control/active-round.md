# Active Round

- Round id: `round-2026-03-24-1928-land-live-host-shadow-assessment-and-adoption-report-owner-layer`
- Objective id: `obj-2026-03-23-0002`
- Status: `active`

## Scope

- Promote host adoption assessment and report generation into the kernel owner layer.
- Keep live-host rollout in shadow mode by producing honest assessment output before any broader automation claim.

## Deliverable

A kernel command and helper surface that can assess a host adoption state and write a readable shadow-adoption report.

## Validation Plan

Run focused host-adoption smokes plus audit-control-state and enforce-worktree on the repo after the owner-layer command lands.

## Active Risks

- The first command surface could stay too frozen-host-specific and fail to generalize to live-host shadow assessment.

## Blockers

_none recorded_
