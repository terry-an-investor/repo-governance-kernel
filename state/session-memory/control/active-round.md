# Active Round

- Round id: `round-2026-03-25-1553-freeze-b0-public-flow-subcontracts`
- Objective id: `obj-2026-03-23-0002`
- Status: `active`

## Scope

- Define one owner-layer catalog for stable public subcontracts beneath the four public flow payloads.
- Freeze only flow_contract and intent_compilation nested fields in this slice; leave execution, outcome, and postconditions outside the stable minimum contract.

## Deliverable

One machine-readable b0 candidate subcontract catalog for stable nested public flow fields, exported through the public alpha surface and enforced by smoke.

## Validation Plan

Run py_compile, the public flow smokes, the kernel bootstrap smoke, product doc audit, audit-control-state, and enforce-worktree.

## Active Risks

_none recorded_

## Blockers

_none recorded_
