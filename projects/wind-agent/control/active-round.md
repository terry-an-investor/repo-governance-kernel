# Active Round

- Round id: `round-2026-03-23-1431-bootstrap-broadened-wind-agent-execution-round`
- Objective id: `obj-2026-03-23-1243-split-proven-query-surface-recovery-from-broader-convergence-governance`
- Status: `active`

## Scope

- reconcile the broadened wind-agent mainline into one honest bounded round
- cover the current query-surface plus substrate/native/CLI convergence slice explicitly instead of pretending the old narrow round still fits
- restore round-level governance so future review and validation gates match the actual owner layers in flight

## Deliverable

A durable active round contract that matches the broadened wind-agent mainline and can be used as the honest control boundary for the next validation slice.

## Validation Plan

Re-establish one durable round that matches the real dirty mainline, then validate the broadened slice in small owner-layer checks before claiming broader convergence is proven.

## Active Risks

- The broadened round can still be too large if unrelated debt is mixed into the same contract.
- Live validation remains narrower than the broadened implementation surface until follow-up checks are run.

## Blockers

_none recorded_
