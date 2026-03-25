# Repo Governance Kernel

This directory is the reusable package surface for `repo-governance-kernel`.

Use it when you want the package-facing view of the project: what the package
owns, how to install it, and which commands already form the supported beta
surface.

The current beta release is `0.1.0b0`.

Its release theme is the first formal beta compatibility promise for the
package-facing command and flow contract.

The current source line is now hardening that beta promise toward `0.1.0b1`
by recording explicit candidate subcontracts for the smallest reusable kernels
inside the evidence-layer response objects.

It owns:

- transition semantics
- shared control runtime
- audit and enforcement logic
- governed command and bundle implementations
- the reusable kernel CLI

It does not own:

- `state/session-memory/` dogfood control state
- repo-local smoke and evaluation harnesses
- this repository's sample-specific history

## Start Here

### Install the current wheel

```powershell
uv build
uv venv artifacts/beta-install/.venv
uv pip install --python artifacts/beta-install/.venv/Scripts/python.exe --force-reinstall dist/repo_governance_kernel-0.1.0b0-py3-none-any.whl
artifacts/beta-install/.venv/Scripts/repo-governance-kernel.exe --help
```

### Bootstrap a governed host repo

```powershell
artifacts/beta-install/.venv/Scripts/repo-governance-kernel.exe --repo-root C:/path/to/host/repo bootstrap-repo --project-id my-repo
```

### Onboard a governed host repo into its first control line

```powershell
artifacts/beta-install/.venv/Scripts/repo-governance-kernel.exe --repo-root C:/path/to/host/repo onboard-repo --project-id my-repo
```

### Run one bounded external-target assessment

```powershell
artifacts/beta-install/.venv/Scripts/repo-governance-kernel.exe --repo-root C:/path/to/governed/host/repo assess-external-target-once --project-id my-repo --workspace-root C:/path/to/external/repo
```

### Inspect shared config resolution

The current beta line keeps one shared config runtime for `repo_root` and
`project_id`.

Current precedence:

- `repo_root`: flag -> environment -> cwd discovery -> user config -> package default
- `project_id`: flag -> environment -> local override -> project config -> user config

Config file locations:

- user config: `%USERPROFILE%/.repo-governance-kernel/config.json`
- project config: `<repo_root>/.repo-governance-kernel/project.json`
- local override: `<repo_root>/.repo-governance-kernel/local.json`

Machine-readable inspection surface:

```powershell
repo-governance-kernel describe-config
```

The first public-beta consumer path now wired to this runtime is
`audit-control-state`. When `project_id` is present in config, the installed
entrypoint can resolve it without an explicit flag:

```powershell
repo-governance-kernel --repo-root C:/path/to/host/repo audit-control-state
```

The repo smoke at `scripts/smoke_kernel_bootstrap.py` proves this path end to
end: source-tree bootstrap, installed-wheel bootstrap, and installed-wheel
external-target single assessment.

## Public Surface

The current `0.1.0b0` public beta surface is:

- `describe-config`
- `describe-public-surface`
- `audit-control-state`
- `enforce-worktree`
- `bootstrap-repo`
- `onboard-repo`
- `onboard-repo-from-intent`
- `assess-external-target-once`
- `assess-external-target-from-intent`

Machine-readable descriptor:

```powershell
repo-governance-kernel describe-public-surface
```

The descriptor exists so installed-package proof, docs, and agent wrappers can
consume one shared package contract.

What matters is not the command count, but the boundary:

- execution is bounded
- semantics are registry-owned
- task-contract gating applies to both direct round promotion and governed close bundles
- external-target assessment does not mutate the target repo

Implemented lower-level owner-layer commands such as `assess-host-adoption`,
`draft-external-target-shadow-scope`, and `execute-adjudication-followups`
remain available, but they are not the frozen public beta promise.

## Common Commands

Generic kernel commands can run through:

```powershell
uv run python -m kernel.cli audit-control-state --project-id session-memory
```

Installed entrypoint target:

```powershell
repo-governance-kernel audit-control-state --project-id session-memory
```

Bootstrap a new host repo:

```powershell
repo-governance-kernel --repo-root C:/path/to/host/repo bootstrap-repo --project-id my-repo
```

This bootstrap path creates the minimum host-governance surface needed for an
honest first audit:

- `state/<project_id>/control/constitution.md`
- `state/<project_id>/control/pivot-log.md`
- `state/<project_id>/control/exception-ledger.md`
- `state/<project_id>/current/current-task.md`
- `.githooks/pre-commit`
- `.githooks/pre-push`

Move that host straight into its first honest governed boundary:

```powershell
repo-governance-kernel --repo-root C:/path/to/host/repo onboard-repo --project-id my-repo
```

This onboarding path exists to remove the manual bootstrap plus authoring gap:

- it bootstraps the governed host surface if needed
- it opens the first active objective, one execution round, and one active task contract
- it refreshes the current-task anchor to the governed host repo root
- it carries any pre-existing dirty repo paths into the first honest round/task boundary instead of dropping them
- it fails closed if the repo already has durable objective, round, or task-contract history for that project id

The `onboard-repo` result is now shaped as an agent-facing contract:

- `result_contract`
- `flow_contract`
- `execution`
- `outcome`
- `postconditions`
- `next_actions`

That means an agent can read the returned ids, scope paths, validation status,
and immediate follow-up commands without scraping prose.

The same machine-readable public surface now also records `b1-target`
candidate subcontracts for the smallest reusable kernels inside those
evidence-layer objects, instead of leaving that shape implicit in smoke code.

Run the same onboarding path from one bounded intent surface:

```powershell
repo-governance-kernel --repo-root C:/path/to/host/repo onboard-repo-from-intent --project-id my-repo --request "Initialize governance for this repo."
```

This intent wrapper stays narrow on purpose:

- it only accepts first-control-line repo initialization requests
- it compiles only into `onboard-repo`
- it rejects monitoring and assessment requests instead of stretching its authority

## Agent Packaging

The repository now carries one repo-owned agent wrapper at:

- [`skills/use-repo-governance-kernel/SKILL.md`](../skills/use-repo-governance-kernel/SKILL.md)

That skill is intentionally narrow:

- it teaches agents the bounded onboarding and one-time assessment surfaces
- it keeps agents on `onboard-repo`, `onboard-repo-from-intent`,
  `assess-external-target-once`, and `assess-external-target-from-intent`
- it does not claim monitoring, server behavior, or freeform mutation authority

The canonical public beta contract is documented in:

- [`docs/canonical/PUBLIC_SURFACE.md`](../docs/canonical/PUBLIC_SURFACE.md)
- [`kernel/docs/PUBLIC_SURFACE.md`](./docs/PUBLIC_SURFACE.md)

## Validation Evidence

The current release proof covers:

- a brand-new disposable git repo
- one disposable host repo with real pre-existing dirty paths onboarding through the package-facing surface
- the same bootstrap path from an installed wheel in an isolated environment
- one installed-wheel governed external-target single assessment against a disposable external repo without mutating that target repo
- one focused governed bundle proof showing `execute-adjudication-followups`
  plus `round-close-chain` still fails closed until the attached task contract
  is resolved
- a frozen copied `wind-agent` host snapshot

Both bootstrap surfaces pass host-side `audit-control-state` without touching
the live source repository.

The frozen `wind-agent` path also proves:

- `enforce-worktree` is expected to remain `blocked` until one explicit adopted
  round honestly covers the dirty host paths
- the kernel now writes one host-side adoption report that explains this blocked
  state and the next control actions instead of leaving only raw JSON
- after opening one host-side objective, adopted round, and task contract,
  host-side `audit-control-state` remains `ok`
- after that adoption step, `enforce-worktree` no longer fails for missing
  round authority; remaining `blocked` results now come from real scope law such
  as `dirty_paths_outside_scope_round` and
  `dirty_paths_outside_active_task_contracts`

## Assessment Commands

Assess a governed host for shadow adoption:

```powershell
repo-governance-kernel --repo-root C:/path/to/governed/host/repo assess-host-adoption --project-id my-repo
```

This assessment surface is for shadow mode:

- it requires an already-governed host with one active objective, one open round, and one active task contract
- it resolves either `governed-host-shadow` or `external-target-shadow`
- it interprets active round/task paths relative to the assessed workspace root, not relative to arbitrary host-doc locations
- it always produces a readable adoption report instead of claiming general live-host rewrite authority
- it can keep the report inside the governed host repo or write to an explicit external path

Draft one external-target shadow boundary before assessment:

```powershell
repo-governance-kernel --repo-root C:/path/to/governed/host/repo draft-external-target-shadow-scope --project-id my-repo --workspace-root C:/path/to/external/repo
```

This draft surface is for external-target setup:

- it inspects the external repo live and turns the observed dirty paths into suggested round/task scope
- it writes a readable draft artifact and suggested command sequence instead of mutating durable control truth automatically
- it keeps that draft artifact distinct from the later shadow-adoption report so authoring output and assessment output do not collapse into one owner label
- it exists to reduce hand-authored ambiguity before `assess-host-adoption` interprets the external target boundary

Run the bounded single-pass external-target workflow:

```powershell
repo-governance-kernel --repo-root C:/path/to/governed/host/repo assess-external-target-once --project-id my-repo --workspace-root C:/path/to/external/repo
```

This wrapper is intentionally narrow:

- it drafts scope from the observed external dirty paths
- it rewrites the current open round and current active task contract to that scope
- it refreshes the current-task anchor and then runs `assess-host-adoption`
- it now runs through one governed bundle instead of a private per-command script chain
- it stays inside existing owner-layer commands instead of inventing freeform mutation authority
- the installed-wheel smoke now proves this same workflow from the packaged console entrypoint, not only from the source tree

Run the bounded natural-language entry for the same path:

```powershell
repo-governance-kernel --repo-root C:/path/to/governed/host/repo assess-external-target-from-intent --project-id my-repo --request "Assess C:/path/to/external/repo current changes, set scope first, then give me the verdict."
```

This natural-language surface stays narrow on purpose:

- it only compiles one-time external-target assessment intents
- it still routes into the governed bundle-backed workflow instead of bypassing owner-layer controls
- it rejects continuous monitoring requests rather than pretending the current product supports them

## Repo Integration

Install or refresh repo-local hooks:

```powershell
repo-governance-kernel --repo-root C:/path/to/host/repo install-hooks --project-id my-repo
```

Repo-local compatibility entrypoints still exist under `scripts/`, but they are
adapter surfaces rather than the canonical kernel implementation layer.

