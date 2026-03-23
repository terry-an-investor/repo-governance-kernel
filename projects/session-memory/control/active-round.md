# Active Round

- Round id: `round-2026-03-23-1814-broaden-enforcement-coverage-beyond-first-worktree-gate`
- Objective id: `obj-2026-03-23-0002`
- Status: `active`

## Scope

- Add the next enforcement slice for workaround or exception-contract coverage instead of only scope and projection drift.
- Decide how CI and commit-time enforcement should share the same owner-layer checks.
- Keep the enforcement model project-agnostic while broadening what counts as blocked dishonest work.

## Deliverable

A successor enforcement milestone that extends automatic penalties beyond the first worktree gate.

## Validation Plan

Define the next blocked-state class, connect it to the same enforcement owner layer, and prove it with targeted validation before broader smoke.

## Active Risks

- Broader enforcement could become noisy if workaround detection is based on weak heuristics rather than explicit durable objects.

## Blockers

_none recorded_
