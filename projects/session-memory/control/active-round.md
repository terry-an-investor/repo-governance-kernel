# Active Round

- Round id: `round-2026-03-23-1814-broaden-enforcement-coverage-beyond-first-worktree-gate`
- Objective id: `obj-2026-03-23-0002`
- Status: `active`

## Scope

- Add a machine-readable transition registry for the currently implemented command surface and bounded adjudication plan families.
- Wire executor and adjudication plan compiler support lists to the registry instead of hard-coded local sets.
- Teach control audit to detect registry drift against the canonical documented command surface.

## Deliverable

A repo-owned transition registry that becomes the single machine-readable source for supported transition commands and bounded adjudication plan families.

## Validation Plan

Validate registry listing and audit checks, rerun adjudication smoke and full phase-1 smoke, then rerun audit-control-state and enforce-worktree on the real project.

## Active Risks

- A partial registry could create false confidence if scripts still quietly keep private support lists outside the owner-layer registry.
- Registry drift checks may still be too shallow if they only compare names and not full guard or side-effect semantics yet.

## Blockers

_none recorded_
