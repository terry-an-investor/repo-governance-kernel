# Release Plan

Date: 2026-03-25
Scope: alpha release preparation for the reusable kernel

## Release Target

Current target:

- package name: `repo-governance-kernel`
- current released version: `0.1.0a4`
- next target version: `0.1.0a5`
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

## Current Release Theme

The current preview cut is `0.1.0a4`.

Its purpose was not to broaden the kernel. Its purpose was to make external
installation and runtime configuration more predictable while keeping the same
public alpha command set first frozen in `0.1.0a3`.

Delivered outcomes:

- explicit user/project/local config layering for `repo_root` and `project_id`
- one package-facing `describe-config` surface with source attribution
- the first public command consumer of shared `project_id` resolution
- stronger install-first proof that does not assume prior knowledge of this
  source repo
- stronger source-repo push gating so repo acceptance smoke regressions are
  caught locally before GitHub Actions

This means `0.1.0a4` is a config-layering and installability release, not a
monitoring, server, provider-selection, or general autonomous rewrite release.

## Next Release Theme

The next planned cut is `0.1.0a5`.

Its purpose is to make the highest-frequency package flows feel like one-task
product surfaces instead of command archaeology.

Primary outcomes:

- keep compressing common flows into bounded one-command entrypoints
- stabilize JSON result contracts for those entrypoints
- make blocked-state explanations easier for agents to consume directly

Source-head progress already landed for the planned `0.1.0a5` cut:

- `onboard-repo` and `onboard-repo-from-intent` now share one public result envelope
- `assess-external-target-once` and `assess-external-target-from-intent` now share the same top-level result categories
- blocked outcomes for those flows now stay machine-readable instead of falling back to plain string failures

## Promotion Bar

Do not promote beyond alpha until:

- kernel-only validation is explicit and repeatable
- public command contract is frozen
- package-facing docs include quickstart and support boundary
- host/sample adapters no longer look like canonical kernel ownership

## Publication Checklist

Treat a release as incomplete until all of the following are true:

1. the release commit is on `origin/master`
2. the annotated version tag exists on origin and dereferences to the intended release commit
3. the GitHub Release object exists for that tag
4. the GitHub Release object carries the intended wheel and sdist assets

The repo-owned publication verifier for this checklist is:

- `uv run python scripts/verify_release_publication.py --repo terry-an-investor/repo-governance-kernel --version <version> --expected-sha <release-commit-sha> --asset repo_governance_kernel-<version>-py3-none-any.whl --asset repo_governance_kernel-<version>.tar.gz`

Use `--require-branch-head` during the release cut itself when `origin/master`
should still equal the release commit. Omit it later when auditing an older
release after newer commits have already advanced `master`.

Recommended cut order:

1. land the release commit locally
2. `git push origin master`
3. `git tag -a v<version> <release-commit-sha> -m "repo-governance-kernel <version>"`
4. `git push origin v<version>`
5. `gh release create v<version> dist/repo_governance_kernel-<version>.tar.gz dist/repo_governance_kernel-<version>-py3-none-any.whl --repo terry-an-investor/repo-governance-kernel --title "repo-governance-kernel <version>"`
6. run `verify_release_publication.py --require-branch-head` against the same version and release commit before calling the cut complete

## Preview Evidence

Preview validation completed on 2026-03-25 for the `0.1.0a4` cut.

- `uv run python scripts/smoke_config_runtime.py`
  - focused config runtime proof now covers user config, project config, local
    override, environment override, and explicit-flag precedence for
    `repo_root` and `project_id`
- `uv run python scripts/smoke_repo_acceptance.py`
  - the renamed source-repo acceptance smoke now passes under Python 3.11 and
    includes the focused config runtime proof in the same repo-owned gate
- `uv run python scripts/audit_product_docs.py`
  - package-facing and canonical docs stay aligned on the `0.1.0a4` release
    boundary and clearly separate the current release identity from the older
    `0.1.0a3` freeze point for the unchanged command set

- `uv run python scripts/smoke_kernel_bootstrap.py`
  - source-tree bootstrap still passes `audit-control-state`, and an installed
    wheel can both bootstrap a second disposable host and complete one bounded
    external-target single assessment from an isolated environment without
    mutating the target repo
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
    - `dist/repo_governance_kernel-0.1.0a4.tar.gz`
    - `dist/repo_governance_kernel-0.1.0a4-py3-none-any.whl`
- installed-package check
  - `uv pip install --python artifacts/preview-install/.venv/Scripts/python.exe --force-reinstall dist/repo_governance_kernel-0.1.0a4-py3-none-any.whl`
  - `.venv/Scripts/python.exe -m kernel.cli --help` succeeds from an isolated install root
  - package-installed `kernel.docs/TRANSITION_COMMANDS.md` is present
  - installed `describe-public-alpha-surface` returns the current `0.1.0a4`
    public release identity plus the `0.1.0a3` freeze lineage for the unchanged
    command set and repo-owned agent wrapper metadata
  - installed `describe-config` reports resolved `repo_root` and `project_id` with source attribution, and installed `audit-control-state` can resolve `project_id` from `<repo_root>/.repo-governance-kernel/project.json` without an explicit flag

## Preview Residual Risks

- the package-facing command surface is still alpha and intentionally narrow; broader adjudication plan families and mutation authority are not a compatibility promise yet
- frozen-host adoption proof remains honest preview evidence for adopted host snapshots rather than the whole live-host story
- external-target shadow mode now has one smoke-proven owner-layer draft-plus-assessment path, one governed bundle-backed single-pass wrapper, one bounded natural-language entry, and one installed-wheel package proof, but it is still not a stable general live-host mutation contract
- host repo and package still share one source repository, so preview packaging hygiene can still regress if repo-local docs and package docs drift

