# Release Plan

Date: 2026-03-25
Scope: alpha release preparation for the reusable kernel

## Release Target

Current target:

- package name: `repo-governance-kernel`
- current released version: `0.1.0a3`
- next target version: `0.1.0a4`
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

- `state/session-memory/` dogfood sample state
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
- the alpha command surface is still intentionally narrow and does not promise general autonomous rewrite

## Next Release Theme

The next planned cut is `0.1.0a4`.

Its purpose is not to broaden the kernel. Its purpose is to make external
installation and runtime configuration more predictable now that the `0.1.0a3`
public alpha surface is frozen.

Primary outcomes:

- explicit user/project/local config layering
- clearer provider/config resolution order
- stronger install-first proof that does not assume knowledge of this source repo
- stronger source-repo push gating so repo acceptance smoke regressions are
  caught locally before GitHub Actions

This means `0.1.0a4` is a config-layering and installability release, not a
monitoring, server, or general autonomous rewrite release.

## Promotion Bar

Do not promote beyond alpha until:

- kernel-only validation is explicit and repeatable
- public command contract is frozen
- package-facing docs include quickstart and support boundary
- host/sample adapters no longer look like canonical kernel ownership

## Preview Evidence

Preview validation completed on 2026-03-25.

- `uv run python scripts/smoke_kernel_bootstrap.py`
  - source-tree bootstrap still passes `audit-control-state`, and an installed wheel can both bootstrap a second disposable host and complete one bounded external-target single assessment from an isolated environment without mutating the target repo
- `uv run python scripts/smoke_task_contract_hard_gate.py`
  - unresolved task contracts block direct round promotion until the task contract is resolved
- `uv run python scripts/smoke_task_contract_bundle_gate.py`
  - `execute-adjudication-followups` plus the governed `round-close-chain` bundle still fails closed on unresolved task contracts and succeeds only after task resolution
- `uv run python scripts/smoke_wind_agent_snapshot_adoption.py`
  - frozen `wind-agent` host adoption produces a readable shadow-adoption report and isolates remaining blocked verdicts to host bootstrap/support noise
- `uv run python scripts/smoke_brooks_semantic_research_snapshot_adoption.py`
  - frozen `brooks-semantic-research` host adoption produces a readable shadow-adoption report and isolates remaining blocked verdicts to host bootstrap/support noise
- `uv run python -m kernel.cli --repo-root <governed-host> assess-host-adoption --project-id <project>`
  - owner-layer shadow adoption assessment writes a readable report from governed host control state plus live workspace inspection
- `uv run python -m kernel.cli --repo-root <governed-host> draft-external-target-shadow-scope --project-id <project> --workspace-root <external-repo>`
  - owner-layer external-target drafting writes a readable scope draft from the observed dirty paths before the real assessment command runs, and that draft artifact is now distinct from the later shadow-adoption report
- `uv run python -m kernel.cli --repo-root <governed-host> assess-external-target-once --project-id <project> --workspace-root <external-repo>`
  - bounded workflow wrapper now compiles into one governed bundle-backed external-target assessment flow
- `uv run python -m kernel.cli --repo-root <governed-host> assess-external-target-from-intent --project-id <project> --request \"Assess C:/path/to/external/repo current changes, set scope first, then give me the verdict.\"`
  - bounded natural-language entry compiles one supported intent into the same governed bundle-backed flow
- `uv build`
  - produced:
    - `dist/repo_governance_kernel-0.1.0a3.tar.gz`
    - `dist/repo_governance_kernel-0.1.0a3-py3-none-any.whl`
- installed-package check
  - `uv pip install --python artifacts/preview-install/.venv/Scripts/python.exe --force-reinstall dist/repo_governance_kernel-0.1.0a3-py3-none-any.whl`
  - `.venv/Scripts/python.exe -m kernel.cli --help` succeeds from an isolated install root
  - package-installed `kernel.docs/TRANSITION_COMMANDS.md` is present
  - installed `describe-public-alpha-surface` returns the frozen `0.1.0a3` public command set and repo-owned agent wrapper metadata

## Preview Residual Risks

- the package-facing command surface is still alpha and intentionally narrow; broader adjudication plan families and mutation authority are not a compatibility promise yet
- frozen-host adoption proof remains honest preview evidence for adopted host snapshots rather than the whole live-host story
- external-target shadow mode now has one smoke-proven owner-layer draft-plus-assessment path, one governed bundle-backed single-pass wrapper, one bounded natural-language entry, and one installed-wheel package proof, but it is still not a stable general live-host mutation contract
- host repo and package still share one source repository, so preview packaging hygiene can still regress if repo-local docs and package docs drift

