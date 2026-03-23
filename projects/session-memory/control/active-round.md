# Active Round

- Round id: `round-2026-03-23-1814-broaden-enforcement-coverage-beyond-first-worktree-gate`
- Objective id: `obj-2026-03-23-0002`
- Status: `active`

## Scope

- Add the next enforcement slice for workaround or exception-contract coverage instead of only scope and projection drift.
- Reuse the same owner-layer enforcement commands across local hooks and CI without adding a second policy implementation.
- Keep the enforcement model project-agnostic while broadening what counts as blocked dishonest work.
- Use constitution-declared guarded exception paths instead of heuristics so blocked workaround debt is backed by durable project law.

## Deliverable

A successor enforcement milestone that extends automatic penalties beyond the first worktree gate.

## Validation Plan

Define the next blocked-state class, connect it to the same enforcement owner layer, wire the same commands into CI, and prove it with targeted validation before broader smoke.
Prove one blocked case and one allowed case on a disposable fixture where guarded dirty paths only pass after an active exception contract explicitly covers them.

## Active Risks

- Broader enforcement could become noisy if workaround detection is based on weak heuristics rather than explicit durable objects.

## Blockers

_none recorded_
