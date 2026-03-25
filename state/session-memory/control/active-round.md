# Active Round

- Round id: `round-2026-03-25-1414-stabilize-public-flow-result-contracts-for-a5`
- Objective id: `obj-2026-03-23-0002`
- Status: `active`

## Scope

- Add one shared public-flow result contract layer for the highest-frequency package entrypoints.
- Rewrite onboarding and external-target assessment direct and intent wrappers to emit the same success and blocked categories.
- Update smoke coverage and package-facing docs to treat the shared result contract as the a5 product surface.

## Deliverable

One shared public-flow contract for onboarding and one-time external-target assessment, with stable success and blocked payloads proven by smoke.

## Validation Plan

Run smoke_repo_onboarding, smoke_assess_host_adoption, smoke_kernel_bootstrap, and smoke_repo_acceptance after the contract rewrite.

## Active Risks

_none recorded_

## Blockers

_none recorded_
