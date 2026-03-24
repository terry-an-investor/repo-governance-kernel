# Repo Governance Kernel

This directory is the reusable repo-governance kernel prepared for alpha
packaging.

It owns:

- machine-readable transition semantics
- shared control runtime
- audit and enforcement logic
- generic command implementations
- the reusable kernel CLI

It does not own:

- `projects/session-memory/` dogfood control state
- repo-local smoke/eval harnesses
- this repository's sample-specific history and fixtures

## Kernel Surfaces

- `kernel/transition_specs.py`
- `kernel/round_control.py`
- `kernel/control_enforcement.py`
- `kernel/resolver_runtime.py`
- `kernel/executor_command_builder.py`
- `kernel/executor_runtime.py`
- `kernel/audit_control_state.py`
- `kernel/product_semantics.py`
- `kernel/commands/`
- `kernel/cli.py`

## Invocation

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

This bootstrap path now creates the minimum host-governance surface needed for
an honest first audit:

- `projects/<project_id>/control/constitution.md`
- `projects/<project_id>/control/pivot-log.md`
- `projects/<project_id>/control/exception-ledger.md`
- `projects/<project_id>/current/current-task.md`
- `.githooks/pre-commit`
- `.githooks/pre-push`

The current validation path now covers both:

- a brand-new disposable git repo
- a frozen copied `wind-agent` host snapshot

Both surfaces bootstrap and pass host-side `audit-control-state` without
touching the live source repository.

The frozen `wind-agent` path also proves the next adoption truth:

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

Run the bounded natural-language entry for the same path:

```powershell
repo-governance-kernel --repo-root C:/path/to/governed/host/repo assess-external-target-from-intent --project-id my-repo --request "Assess C:/path/to/external/repo current changes, set scope first, then give me the verdict."
```

This natural-language surface stays narrow on purpose:

- it only compiles one-time external-target assessment intents
- it still routes into the governed bundle-backed workflow instead of bypassing owner-layer controls
- it rejects continuous monitoring requests rather than pretending the current product supports them

Install or refresh repo-local hooks:

```powershell
repo-governance-kernel --repo-root C:/path/to/host/repo install-hooks --project-id my-repo
```

Repo-local compatibility entrypoints still exist under `scripts/`, but they are
adapter surfaces rather than the canonical kernel implementation layer.
