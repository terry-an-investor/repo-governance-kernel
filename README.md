# Repo Governance Kernel

`repo-governance-kernel` is a repo governance kernel.

It does not try to be a general autonomous coding agent. Its job is narrower:
make repository work pass through explicit control objects, legal transitions,
audit, and enforcement before progress is accepted.

This source repository contains both:

- the reusable package under [`kernel/`](./kernel/)
- the host-local dogfood sample under [`state/session-memory/`](./state/session-memory/)

The current preview release is `0.1.0a2`. The automation scope is
`bounded registry-owned execution`. The autonomy boundary is
`not a general autonomous rewrite engine`.

## What You Can Do Today

- model repository work with objectives, rounds, task contracts, exception
  contracts, and transition events
- audit control state and enforce live worktree honesty
- run registry-owned commands with explicit guards and write ownership
- use governed bundles for bounded multi-step workflows
- run one bounded external-target assessment flow that:
  - drafts scope from the target repo's live dirty paths
  - rewrites the active round and task contract through governed commands
  - refreshes the current anchor
  - writes an assessment report without mutating the target repo
- trigger that same external-target assessment flow from one narrow natural-language entry
- bootstrap and verify the package from source tree and installed wheel

## Quickstart

This repository is developed and validated with `uv` on Windows.

### Set up the repo

```powershell
uv sync
uv run python scripts/install_hooks.py
```

### Verify the host sample

```powershell
uv run python -m kernel.cli audit-control-state --project-id session-memory
uv run python -m kernel.cli enforce-worktree --project-id session-memory
```

### Prove the packaged path

```powershell
uv run python scripts/smoke_kernel_bootstrap.py
```

### Run one external-target assessment

```powershell
uv run python -m kernel.cli `
  --repo-root C:/Users/terryzzb/Desktop/session-memory `
  assess-external-target-once `
  --project-id session-memory `
  --workspace-root C:/Users/terryzzb/Desktop/git_repos/buffet
```

## What This Repo Is Not

This preview does not promise:

- continuous monitoring of external repositories
- a background server control plane
- arbitrary natural-language mutation authority
- general live-host autonomous rewrite
- stable compatibility across all command surfaces

## Package Boundary

The reusable package surface lives under [`kernel/`](./kernel/).

These remain host-local and are not part of the package contract:

- [`state/session-memory/`](./state/session-memory/)
- [`scripts/`](./scripts/)
- [`.githooks/`](./.githooks/)
- [`.github/workflows/`](./.github/workflows/)
- repo-local smoke and evaluation harnesses

## Read Next

- [`kernel/README.md`](./kernel/README.md): package-facing usage
- [`docs/canonical/RELEASE.md`](./docs/canonical/RELEASE.md): release status and validation evidence
- [`docs/canonical/PRODUCT.md`](./docs/canonical/PRODUCT.md): product definition and positioning
- [`docs/canonical/CONTROL_SYSTEM.md`](./docs/canonical/CONTROL_SYSTEM.md): durable truth, projections, audit, and enforcement
- [`docs/canonical/TRANSITION_COMMANDS.md`](./docs/canonical/TRANSITION_COMMANDS.md): command, bundle, and intent surface
- [`docs/README.md`](./docs/README.md): full docs index

