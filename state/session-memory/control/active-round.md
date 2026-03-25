# Active Round

- Round id: `round-2026-03-25-1116-start-explicit-package-config-layering-for-a4`
- Objective id: `obj-2026-03-23-0002`
- Status: `active`

## Scope

- Add one owner-layer config runtime so the package can resolve user, project, and local config without scattering path and precedence rules across commands.
- Expose the first package-facing config command and wire the first real public-alpha consumers onto that shared config surface.
- Fix the recurring submit escape by centralizing durable file-name budgeting for pivot and objective writes and aligning the repo-owned pre-push smoke gate with the CI phase-1 smoke surface.
- Keep the source-repo acceptance smoke compatible with the CI interpreter floor and rename the stale phase-1 acceptance surface to a clearer repo-acceptance entrypoint across repo-owned triggers and docs.

## Deliverable

One first a4 slice with layered config runtime, a Python-3.11-safe acceptance smoke path, one clearer repo-acceptance smoke entrypoint, and one smoke-proven consumer path.

## Validation Plan

Run focused Python-3.11 acceptance smoke plus audit-control-state, enforce-worktree, audit_product_docs, and any changed repo-owned trigger path after the rename and config slice land.

## Active Risks

- If config layering stays implicit, installability will keep depending on flags and repo-local knowledge instead of package-owned defaults.
- If config semantics are added directly inside individual commands, the a4 surface will recreate the same private semantics drift the kernel has been removing elsewhere.
- If local push gating remains weaker than CI, GitHub will keep being the first place phase-1 smoke regressions are discovered.
- If the top-level acceptance smoke keeps its stale phase-1 label, repo-owned hooks, CI, and docs will keep hiding what the script actually proves.

## Blockers

_none recorded_
