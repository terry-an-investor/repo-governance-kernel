# Release Plan

Date: 2026-03-25
Scope: beta release preparation and publication for the reusable kernel

## Release Target

Current target:

- package name: `repo-governance-kernel`
- current released version: `0.1.0b0`
- previous released version: `0.1.0a5`
- next target version: `0.1.0b1`
- release level: beta

## What Ships

The beta package ships:

- `kernel/`
- `kernel/commands/`
- `kernel/docs/`
- `repo-governance-kernel` console entrypoint

It does not claim that repo-local smoke/eval workflows are part of the
package contract.

## What Stays Host-Local

The host repository continues to own:

- `state/session-memory/` dogfood sample state
- `scripts/` compatibility and adapter entrypoints
- `.githooks/`
- `.github/workflows/`
- repo-local smoke/eval harnesses

## Beta Boundary

This beta is the first stable compatibility promise for the bounded package
surface.

What is frozen in `0.1.0b0`:

- the public command set documented in [`PUBLIC_SURFACE.md`](./PUBLIC_SURFACE.md)
- the machine-readable `describe-public-surface` descriptor
- the stable public flow result contract for:
  - `onboard-repo`
  - `onboard-repo-from-intent`
  - `assess-external-target-once`
  - `assess-external-target-from-intent`
- the stable nested public subcontracts for:
  - `flow_contract`
  - `intent_compilation`

What is still explicitly out of scope:

- continuous monitoring of external repositories
- background server behavior
- general autonomous rewrite
- stable nested shapes for `execution`, `outcome`, or `postconditions`
- lower-level owner-layer commands not listed in the public surface

## Current Release Theme

The current beta cut is `0.1.0b0`.

Its purpose is to stop treating the package-facing surface as a moving preview
target and instead publish one formal beta identity with:

- aligned version truth across code, docs, and descriptors
- formal public-surface naming instead of alpha-preview naming
- frozen public command membership
- frozen public flow and subcontract truth
- repeatable package-install, onboarding, assessment, and gating validation

## Next Release Theme

The next planned cut is `0.1.0b1`.

Its purpose is beta hardening after the first compatibility promise, not a new
authority expansion.

Primary outcomes:

- tighten package docs and examples around the beta contract
- decide whether any evidence-layer response objects deserve promotion into the
  stable public contract
- keep CI and installed-package proof aligned with the beta surface

## Promotion Bar

Do not promote beyond beta until:

- public surface naming no longer carries stale alpha-preview semantics
- beta validation remains explicit and repeatable
- publication verification proves branch, tag, release object, and assets
- host-local adapter surfaces are visibly separate from package contract

## Publication Checklist

Treat a release as incomplete until all of the following are true:

1. the intended release commit exists locally
2. the annotated version tag exists locally and dereferences to the intended release commit
3. the release close-out commit is also landed locally and control-state returns to a clean paused state
4. `audit-control-state` and `enforce-worktree` both return `ok` after local close-out
5. `origin/master` contains the intended local branch head
6. the annotated version tag exists on origin and dereferences to the intended release commit
7. the GitHub Release object exists for that tag
8. the GitHub Release object carries the intended wheel and sdist assets

The repo-owned publication verifier for this checklist is:

- `uv run python scripts/verify_release_publication.py --repo terry-an-investor/repo-governance-kernel --version <version> --expected-sha <release-commit-sha> --asset repo_governance_kernel-<version>-py3-none-any.whl --asset repo_governance_kernel-<version>.tar.gz`

Use `--require-branch-head` only when the remote branch head is expected to
still equal the release commit itself. Omit it after a local close-out commit
has advanced `master` beyond the tagged release commit.

Recommended cut order:

1. land the beta release commit locally
2. `git tag -a v<version> <release-commit-sha> -m "repo-governance-kernel <version>"` locally against that exact release commit
3. close the release task/round locally, refresh the current-task anchor, and return the objective phase to `paused` if no open round remains
4. rerun `audit-control-state` and `enforce-worktree` and require both to return `ok` before any remote push
5. `git push origin master`
6. `git push origin v<version>`
7. `gh release create v<version> dist/repo_governance_kernel-<version>.tar.gz dist/repo_governance_kernel-<version>-py3-none-any.whl --repo terry-an-investor/repo-governance-kernel --title "repo-governance-kernel <version>"`
8. run `verify_release_publication.py` against the same version and tagged release commit before calling the cut complete

## Beta Evidence

Beta validation completed on 2026-03-25 for the `0.1.0b0` cut.

- `uv run python scripts/audit_product_docs.py`
  - package-facing and canonical docs agree on the formal beta identity and
    keep package contract separate from host-local surfaces
- `uv run python scripts/smoke_repo_onboarding.py`
  - direct and intent onboarding now satisfy the stable public flow contract,
    including the stable `flow_contract` and `intent_compilation` subcontracts
- `uv run python scripts/smoke_assess_host_adoption.py`
  - direct and intent one-time external-target assessment now satisfy the same
    stable public flow and subcontract truth
- `uv run python scripts/smoke_kernel_bootstrap.py`
  - source-tree bootstrap still passes `audit-control-state`, and an installed
    wheel can bootstrap a disposable host, resolve package config, expose the
    machine-readable beta public surface, and complete one bounded external
    assessment without mutating the target repo
- `uv run python scripts/smoke_task_contract_hard_gate.py`
  - unresolved task contracts still block direct round promotion until the task
    contract is resolved
- `uv run python scripts/smoke_task_contract_bundle_gate.py`
  - governed bundle promotion still fails closed on unresolved task contracts
- `uv run python scripts/smoke_repo_acceptance.py`
  - the repo-owned acceptance path still passes under the same release truth
- `uv build`
  - produced:
    - `dist/repo_governance_kernel-0.1.0b0.tar.gz`
    - `dist/repo_governance_kernel-0.1.0b0-py3-none-any.whl`

## Beta Residual Risks

- the beta contract is intentionally narrow; lower-level owner-layer commands
  remain implemented but are not part of the compatibility promise
- the package and dogfood sample still live in one repository, so docs and
  packaging hygiene still need active discipline
- evidence-layer response objects such as `execution`, `outcome`, and
  `postconditions` remain intentionally richer than the frozen minimum
  contract, so callers should not treat them as fully stable yet
