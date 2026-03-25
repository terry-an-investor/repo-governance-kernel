# Active Round

- Round id: `round-2026-03-25-1402-make-smoke-git-resolution-ci-portable`
- Objective id: `obj-2026-03-23-0002`
- Status: `active`

## Scope

- Add one shared git executable resolver for repo-owned smoke and release verification scripts.
- Rewrite each affected smoke or release verifier entrypoint to consume the shared resolver instead of a hardcoded Windows path.
- Validate the changed paths with direct smoke runs and the repo acceptance smoke.

## Deliverable

A repo-owned cross-platform git resolution layer with passing smoke validation for the affected script surfaces.

## Validation Plan

Run smoke_config_runtime, smoke_repo_onboarding, smoke_kernel_bootstrap, verify_release_publication --help, and smoke_repo_acceptance after the resolver rewrite.

## Active Risks

_none recorded_

## Blockers

_none recorded_
