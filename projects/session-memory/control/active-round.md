# Active Round

- Round id: `round-2026-03-24-2110-stabilize-package-first-single-assessment-alpha-surface`
- Objective id: `obj-2026-03-23-0002`
- Status: `active`

## Scope

- Split external-target scope drafting and shadow assessment reporting into distinct artifact owner semantics.
- Add one package-first validation path that proves an installed wheel can bootstrap and audit a disposable governed host repo.
- Refresh package-facing docs and release notes so the a2 single-assessment validation story matches the implemented surface.

## Deliverable

A cleaner alpha single-assessment surface with distinct draft/report artifact semantics plus one install-first wheel smoke for bootstrap and audit.

## Validation Plan

Run the focused package-first smoke, audit-control-state, and enforce-worktree on the real repo after the artifact split and smoke path land.

## Active Risks

- The first package-first smoke could stay too bootstrap-only and fail to prove the most important package-facing surface.

## Blockers

_none recorded_
