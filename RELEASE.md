# Release Plan

Date: 2026-03-24
Scope: alpha release preparation for the reusable kernel

## Release Target

Current target:

- package name: `repo-governance-kernel`
- version: `0.1.0a0`
- release level: alpha / internal preview

## What Ships

The alpha package should ship:

- `kernel/`
- `kernel/commands/`
- `kernel/docs/`
- `repo-governance-kernel` console entrypoint

It should not claim that repo-local smoke/eval workflows are part of the
package contract.

## What Stays Host-Local

The host repository continues to own:

- `projects/session-memory/` dogfood sample state
- `scripts/` compatibility and adapter entrypoints
- `.githooks/`
- `.github/workflows/`
- repo-local smoke/eval harnesses

## Alpha Caveats

This alpha is not yet a stable compatibility promise.

Known reasons:

- public command/API stability is not frozen
- host repo and package still live in one repository
- kernel-only smoke coverage is still thinner than host-repo smoke coverage
- task-contract as a hard execution gate is still incomplete

## Promotion Bar

Do not promote beyond alpha until:

- kernel-only validation is explicit and repeatable
- public command contract is frozen
- package-facing docs include quickstart and support boundary
- host/sample adapters no longer look like canonical kernel ownership

## Preview Evidence

Preview validation completed on 2026-03-24.

- `uv run python scripts/smoke_kernel_bootstrap.py`
  - disposable bootstrap host passes `audit-control-state`
- `uv run python scripts/smoke_wind_agent_snapshot_adoption.py`
  - frozen `wind-agent` host adoption produces a readable shadow-adoption report and isolates remaining blocked verdicts to host bootstrap/support noise
- `uv run python scripts/smoke_brooks_semantic_research_snapshot_adoption.py`
  - frozen `brooks-semantic-research` host adoption produces a readable shadow-adoption report and isolates remaining blocked verdicts to host bootstrap/support noise
- `uv build`
  - produced:
    - `dist/repo_governance_kernel-0.1.0a0.tar.gz`
    - `dist/repo_governance_kernel-0.1.0a0-py3-none-any.whl`
- installed-package check
  - `uv pip install --python artifacts/preview-install/.venv/Scripts/python.exe --force-reinstall dist/repo_governance_kernel-0.1.0a0-py3-none-any.whl`
  - `.venv/Scripts/python.exe -m kernel.cli --help` succeeds from an isolated install root
  - package-installed `kernel.docs/TRANSITION_COMMANDS.md` is present

## Preview Residual Risks

- frozen-host adoption proof is honest preview evidence, not yet live-host shadow-mode proof
- host repo and package still share one source repository, so preview packaging hygiene can still regress if repo-local docs and package docs drift
