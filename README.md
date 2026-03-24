# Repo Governance Kernel

`session-memory` is the source repository for the preview release of
`repo-governance-kernel`.

The product is a repo governance kernel: a control-first system that makes
repository work move through explicit objective, round, task-contract, audit,
and enforcement semantics instead of informal chat state or ad hoc scripts.

This repository contains both:

- the reusable package surface under [`kernel/`](./kernel/)
- the host-local dogfood sample under [`projects/session-memory/`](./projects/session-memory/)

The host sample is important evidence, but it is not the package contract.

## Current Status

- package: `repo-governance-kernel`
- current preview release: `0.1.0a1`
- release level: alpha / internal preview
- automation scope: bounded registry-owned execution
- autonomy boundary: not a general autonomous rewrite engine

Release notes and packaging status live in [`RELEASE.md`](./RELEASE.md).

## What The Kernel Already Does

The current preview already provides:

- durable control objects for objective lines, rounds, task contracts, exception
  contracts, and transition events
- projected control views for active objective, active round, current task, and
  related execution context
- control-state audit and live worktree enforcement
- registry-owned primitive transition commands with explicit guards and write
  ownership
- governed bundle execution for bounded multi-step workflows
- external-target shadow assessment support that can:
  - draft scope from the external repo's observed dirty paths
  - rewrite the active round and task contract through governed commands
  - refresh the current anchor
  - run one bounded single-assessment flow without mutating the target repo
- one bounded natural-language entry that compiles a narrow supported request
  into the same governed external-target assessment bundle
- package bootstrap proof from the source tree plus one installed-wheel external-target single assessment proof

## Quickstart

This repository is developed and validated with `uv` on Windows.

### 1. Set up the repo

```powershell
uv sync
uv run python scripts/install_hooks.py
```

### 2. Verify host control state

```powershell
uv run python -m kernel.cli audit-control-state --project-id session-memory
uv run python -m kernel.cli enforce-worktree --project-id session-memory
```

### 3. Run the package/bootstrap smoke

```powershell
uv run python scripts/smoke_kernel_bootstrap.py
```

### 4. Run one external-target single assessment

From the source tree, the governed flow can be exercised with:

```powershell
uv run python -m kernel.cli `
  --repo-root C:/Users/terryzzb/Desktop/session-memory `
  assess-external-target-once `
  --project-id session-memory `
  --workspace-root C:/Users/terryzzb/Desktop/git_repos/buffet
```

That flow drafts scope from the target repo's live dirty paths, rewrites the
active round and task contract through governed semantics, refreshes the
current anchor, and writes the final assessment report.

## Package And Repo Boundaries

The reusable package surface lives under [`kernel/`](./kernel/).

The following remain host-local and are not part of the package contract:

- [`projects/session-memory/`](./projects/session-memory/)
- [`scripts/`](./scripts/)
- [`.githooks/`](./.githooks/)
- [`.github/workflows/`](./.github/workflows/)
- repo-local smoke and evaluation harnesses

Package-facing usage notes live in [`kernel/README.md`](./kernel/README.md).

## Non-Goals

This preview does not promise:

- continuous monitoring of external repositories
- a background server control plane
- arbitrary natural-language mutation authority
- general live-host autonomous rewrite
- stable public compatibility across all command surfaces

## Repository Map

- [`kernel/`](./kernel/): reusable kernel package, commands, docs, and
  transition semantics
- [`projects/session-memory/`](./projects/session-memory/): host-local dogfood
  control state and memory objects
- [`scripts/`](./scripts/): repo-local smoke, bootstrap, and validation entry
  points
- [`docs/`](./docs/README.md): auxiliary notes, operations docs, and evaluation
  plans that do not need to stay at the repository root

## Documentation Guide

- [`PRODUCT.md`](./PRODUCT.md): canonical product definition and positioning
- [`CONTROL_SYSTEM.md`](./CONTROL_SYSTEM.md): durable truth, projection, audit,
  and enforcement model
- [`STATE_MACHINE.md`](./STATE_MACHINE.md): legal state domains and transition
  lifecycle
- [`TRANSITION_COMMANDS.md`](./TRANSITION_COMMANDS.md): canonical command,
  bundle, and intent surface
- [`ARCHITECTURE.md`](./ARCHITECTURE.md): repository structure and ownership
  boundaries
- [`RELEASE.md`](./RELEASE.md): current preview evidence, caveats, and release
  target
- [`kernel/README.md`](./kernel/README.md): package-facing usage and support
  boundary
- [`docs/README.md`](./docs/README.md): index for auxiliary repository
  documentation

## Practical Reading Order

For a first pass through the repo:

1. Read [`README.md`](./README.md) for orientation.
2. Read [`PRODUCT.md`](./PRODUCT.md) and [`CONTROL_SYSTEM.md`](./CONTROL_SYSTEM.md)
   for the product and control model.
3. Read [`TRANSITION_COMMANDS.md`](./TRANSITION_COMMANDS.md) for the bounded
   execution surface.
4. Read [`kernel/README.md`](./kernel/README.md) for package-facing usage.
