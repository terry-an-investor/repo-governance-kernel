# Repo Governance Kernel

This directory is the reusable package surface for `repo-governance-kernel`.

Use it when you want the package-facing view of the project: what the package
owns, how to install it, and which commands already form the supported alpha
surface.

The next planned release line is `0.1.0a4`: add explicit config layering and
installability polish on top of the now-frozen `0.1.0a3` public alpha surface.

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
uv venv artifacts/preview-install/.venv
uv pip install --python artifacts/preview-install/.venv/Scripts/python.exe --force-reinstall dist/repo_governance_kernel-0.1.0a3-py3-none-any.whl
artifacts/preview-install/.venv/Scripts/repo-governance-kernel.exe --help
```

### Bootstrap a governed host repo

```powershell
artifacts/preview-install/.venv/Scripts/repo-governance-kernel.exe --repo-root C:/path/to/host/repo bootstrap-repo --project-id my-repo
```

### Onboard a governed host repo into its first control line

```powershell
artifacts/preview-install/.venv/Scripts/repo-governance-kernel.exe --repo-root C:/path/to/host/repo onboard-repo --project-id my-repo
```

### Run one bounded external-target assessment

```powershell
artifacts/preview-install/.venv/Scripts/repo-governance-kernel.exe --repo-root C:/path/to/governed/host/repo assess-external-target-once --project-id my-repo --workspace-root C:/path/to/external/repo
```

The repo smoke at `scripts/smoke_kernel_bootstrap.py` proves this path end to
end: source-tree bootstrap, installed-wheel bootstrap, and installed-wheel
external-target single assessment.

## Alpha Surface

The frozen `0.1.0a3` public alpha surface is:

- `audit-control-state`
- `enforce-worktree`
- `bootstrap-repo`
- `onboard-repo`
- `onboard-repo-from-intent`
- `assess-external-target-once`
- `assess-external-target-from-intent`

Machine-readable descriptor:

```powershell
repo-governance-kernel describe-public-alpha-surface
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
remain available, but they are not the frozen public alpha promise.

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

- `onboarding_contract`
- `compiled_onboarding`
- `created_control_state`
- `postconditions`
- `next_actions`

That means an agent can read the returned ids, scope paths, validation status,
and immediate follow-up commands without scraping prose.

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

The canonical public-alpha contract is documented in:

- [`docs/canonical/PUBLIC_ALPHA_SURFACE.md`](../docs/canonical/PUBLIC_ALPHA_SURFACE.md)
- [`kernel/docs/PUBLIC_ALPHA_SURFACE.md`](./docs/PUBLIC_ALPHA_SURFACE.md)

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

