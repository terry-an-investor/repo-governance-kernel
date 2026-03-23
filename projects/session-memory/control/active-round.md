# Active Round

- Round id: `round-2026-03-23-1814-broaden-enforcement-coverage-beyond-first-worktree-gate`
- Objective id: `obj-2026-03-23-0002`
- Status: `active`

## Scope

- Add a bounded adjudication plan type that compiles execution-phase bootstrap into an explicit set-phase auto-open-round payload using existing adjudication round bootstrap fields.
- Exercise the new phase-side-effect plan path in disposable adjudication smoke without falling back to hand-authored set-phase executor payloads.
- Validate that adjudication smoke, phase/scope smoke, full phase-1 smoke, audit-control-state, and enforce-worktree all pass after the phase-side-effect plan milestone lands.

## Deliverable

A bounded adjudication plan compiler that can compile execution-phase bootstrap side effects from durable adjudication fields alongside existing round and exception-contract plan bundles.

## Validation Plan

Run adjudication followup smoke with phase-side-effect plan input, rerun phase/scope smoke and full phase-1 smoke, then rerun audit-control-state and enforce-worktree on the real project.

## Active Risks

- Phase-side-effect plans could become a hidden parallel schema if the compiler stops reusing the existing adjudication round bootstrap fields and set-phase contract.
- Phase bootstrap compilation could conflict with later followups if phase entry and open-round side effects are not kept in one bounded deterministic bundle.

## Blockers

_none recorded_
