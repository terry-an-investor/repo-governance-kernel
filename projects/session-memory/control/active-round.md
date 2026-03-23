# Active Round

- Round id: `round-2026-03-23-1814-broaden-enforcement-coverage-beyond-first-worktree-gate`
- Objective id: `obj-2026-03-23-0002`
- Status: `active`

## Scope

- Add a canonical smoke manifest that declares disposable fixture project ids, parallel-safety, and shared resources for each smoke script.
- Implement a suite runner that enforces fixture leak checks before and after each smoke and executes shared-fixture smokes serially.
- Wire the phase-1 smoke entrypoint through the suite runner and validate that the harness owner layer catches fixture contamination honestly.

## Deliverable

A repo-owned smoke harness layer with a manifest, suite runner, fixture leak checks, and a phase-1 smoke entrypoint that no longer ad hoc calls disposable fixture scripts.

## Validation Plan

List the smoke manifest, run a targeted smoke suite slice, rerun full phase-1 smoke, then rerun audit-control-state and enforce-worktree on the real project.

## Active Risks

- Harness law could drift into another undocumented side protocol if smoke metadata lives partly in scripts and partly in the suite runner.
- Suite-level leak checks currently focus on fixture project paths and may still miss other contamination classes such as shared artifact collisions.

## Blockers

_none recorded_
