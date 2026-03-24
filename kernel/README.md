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
- git-hook installation glue
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

Repo-local compatibility entrypoints still exist under `scripts/`, but they are
adapter surfaces rather than the canonical kernel implementation layer.
