# Current Task

## Goal

Keep `repo-governance-kernel` honest as a repo governance kernel with one
repo-owned control line, not a stale demo pile and not a memory-first demo.

## Current State

- Project: `repo-governance-kernel`
- Objective id: `obj-2026-03-23-0002`
- Active round id: `round-2026-03-25-1904-retire-stale-product-identities-and-legacy-scaffolding`
- Phase: `execution`
- Workspace id: `ws-1490b759`
- Workspace root: `C:/Users/terryzzb/Desktop/session-memory`
- The `0.1.0b1` local beta identity has already been cut and closed.
- The package-facing public surface is centered on:
  - bounded onboarding
  - one-time external-target assessment
  - audit and worktree enforcement
- Repo-local state now lives under `state/repo-governance-kernel/`.
- Early legacy-specific material is being removed so the source repo no longer
  presents stale historical names as active product identities.

## Validated Facts

- `uv run python -m kernel.cli describe-public-surface` reports:
  - released version `0.1.0b1`
  - status `public-beta-b1`
- The `0.1.0b1` release round is closed and the active objective is paused.
- Before this rename/cleanup round started, the source repo was clean and both:
  - `uv run python -m kernel.cli audit-control-state --project-id repo-governance-kernel`
  - `uv run python -m kernel.cli enforce-worktree --project-id repo-governance-kernel --workspace-root C:/Users/terryzzb/Desktop/session-memory`
  returned `ok`.
- The package validation matrix for the current beta line has already passed:
  - docs audit
  - onboarding smoke
  - external-target assessment smoke
  - kernel bootstrap smoke
  - task-contract hard gate smoke
  - task-contract bundle gate smoke
  - repo acceptance smoke
  - `uv build`

## Important Files

- `C:/Users/terryzzb/Desktop/session-memory/README.md`
- `C:/Users/terryzzb/Desktop/session-memory/kernel/README.md`
- `C:/Users/terryzzb/Desktop/session-memory/docs/canonical/PRODUCT.md`
- `C:/Users/terryzzb/Desktop/session-memory/docs/canonical/ARCHITECTURE.md`
- `C:/Users/terryzzb/Desktop/session-memory/docs/canonical/CONTROL_SYSTEM.md`
- `C:/Users/terryzzb/Desktop/session-memory/docs/canonical/PUBLIC_SURFACE.md`
- `C:/Users/terryzzb/Desktop/session-memory/kernel/public_surface.py`
- `C:/Users/terryzzb/Desktop/session-memory/scripts/repo_governance_kernel.py`
- `C:/Users/terryzzb/Desktop/session-memory/scripts/smoke_repo_acceptance.py`
- `C:/Users/terryzzb/Desktop/session-memory/state/repo-governance-kernel/control/active-objective.md`

## Active Risks

- Legacy naming can still survive in historical docs or state artifacts after
  the namespace move.
- Legacy-oriented documentation can drift behind the actual package boundary if
  canonical docs and repo-local adapters are not updated together.

## Next Steps

1. Finish removing remaining live legacy-name references from repo-local
   scripts, canonical docs, and current control projections.
2. Re-run `audit-control-state`, `enforce-worktree`, and the smallest credible
   smoke set after the rename/delete sweep.
3. Land the rename and legacy-surface cleanup as one honest repo-local round.
