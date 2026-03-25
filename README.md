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
- attach the package to a fresh repo with one bounded onboarding flow that
  bootstraps governance and opens the first honest objective, round, and task
  contract
- trigger that same onboarding flow from one narrow natural-language request
  when the caller is an agent rather than a human shell user
- run one bounded external-target assessment flow that:
  - drafts scope from the target repo's live dirty paths
  - rewrites the active round and task contract through governed commands
  - refreshes the current anchor
  - writes an assessment report without mutating the target repo
- trigger that same external-target assessment flow from one narrow natural-language entry
- bootstrap and verify the package from source tree and installed wheel

## Quickstart

This repository is developed and validated with `uv` on Windows.

If an agent only reads one file, it should be able to do two things from this
README:

- install the package into an isolated environment
- initialize one fresh git repo through the bounded onboarding surface

### Set up this source repo

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

### Install the package into an isolated environment

```powershell
uv build
uv venv artifacts/preview-install/.venv
uv pip install --python artifacts/preview-install/.venv/Scripts/python.exe --force-reinstall dist/repo_governance_kernel-0.1.0a2-py3-none-any.whl
artifacts/preview-install/.venv/Scripts/repo-governance-kernel.exe --help
```

### Initialize one fresh host repo from the package

Preconditions:

- `C:/path/to/host/repo` already exists and is a git repo
- the target `project_id` does not already have durable objective, round, or task-contract history
- any pre-existing dirty repo paths will be carried into the first honest scope instead of being ignored

```powershell
artifacts/preview-install/.venv/Scripts/repo-governance-kernel.exe `
  --repo-root C:/path/to/host/repo `
  onboard-repo `
  --project-id my-repo
```

That one command bootstraps governance and opens the first bounded control line:

- one active objective
- one active execution round
- one active task contract
- current-task anchor bound to the governed host repo
- host-side `audit-control-state` and `enforce-worktree` required to end `ok`

The returned JSON is agent-facing. The important fields are:

- `onboarding_contract`
- `compiled_onboarding`
- `created_control_state`
- `postconditions`
- `next_actions`

### Let an agent say the same thing once

```powershell
artifacts/preview-install/.venv/Scripts/repo-governance-kernel.exe `
  --repo-root C:/path/to/host/repo `
  onboard-repo-from-intent `
  --project-id my-repo `
  --request "Initialize governance for this repo."
```

This wrapper is intentionally narrow:

- it only accepts first-control-line repo initialization requests
- it only compiles into `onboard-repo`
- it rejects assessment or monitoring requests instead of stretching authority

### Minimal follow-up after initialization

```powershell
artifacts/preview-install/.venv/Scripts/repo-governance-kernel.exe `
  --repo-root C:/path/to/host/repo `
  audit-control-state `
  --project-id my-repo

artifacts/preview-install/.venv/Scripts/repo-governance-kernel.exe `
  --repo-root C:/path/to/host/repo `
  enforce-worktree `
  --project-id my-repo `
  --workspace-root C:/path/to/host/repo
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

- [`kernel/README.md`](./kernel/README.md): full package-facing command reference beyond the minimal install/init path above
- [`docs/canonical/RELEASE.md`](./docs/canonical/RELEASE.md): release status and validation evidence
- [`docs/canonical/PRODUCT.md`](./docs/canonical/PRODUCT.md): product definition and positioning
- [`docs/canonical/CONTROL_SYSTEM.md`](./docs/canonical/CONTROL_SYSTEM.md): durable truth, projections, audit, and enforcement
- [`docs/canonical/TRANSITION_COMMANDS.md`](./docs/canonical/TRANSITION_COMMANDS.md): command, bundle, and intent surface
- [`docs/README.md`](./docs/README.md): full docs index

