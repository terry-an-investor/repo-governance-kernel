# Current Task

## Goal

Anchor the current `wind-agent` mainline so a fresh coding session can recover the real
state of work without replaying the entire transcript.

For the repo itself:

- the last fully proved repo-local round was the narrow query prepared-context path
- the current durable control round is broader and now covers query-surface plus
  substrate/native/CLI convergence governance
- the immediate task is to keep those two truths separate instead of letting the
  old narrow proof masquerade as current full-round coverage

## Current State

- Project: `wind-agent`
- Objective id: `obj-2026-03-23-1243-split-proven-query-surface-recovery-from-broader-convergence-governance`
- Active round id: `round-2026-03-23-1431-bootstrap-broadened-wind-agent-execution-round`
- Workspace id: `ws-8c2176c3`
- Workspace root: `C:/Users/terryzzb/Desktop/wind-agent`
- Branch: `master`
- HEAD anchor: `765c444c9dcd04ba09c58cd7e637ccd7a4669cca`
- Canonical control surface now lives in `session-memory/state/wind-agent/control/`.
- Active round contract: `.round/active.json`
  - `round_id`: `query-surface-producer-consumer-contract`
  - declared owner layer: `src/wind/`
  - declared validation mode: `real_required`
  - status: historical repo-local governance artifact, not the current durable
    control contract
- Real validation already passed for the narrow query prepared-context path on
  `2026-03-22`.
- The working tree has expanded beyond that narrow round:
  - docs changed
  - `src/wind/` changed broadly
  - `src/native/` and `native/` changed
  - new CLI seam-check entrypoint exists
  - many owner tests changed
- Current uncommitted mainline is broader than the repo-local `.round/active.json`
  contract and is now represented by the durable active round in session-memory.

The practical state is:

- one important live query contract is proven
- broader substrate/state-machine convergence work is in progress
- round governance artifacts are now behind the real code state

## Validated Facts

- `.round/last_live_validation.json` reports `pass`.
- The live proof command was:
  - `node tests/cli/run_query_surface_prepared_context_live.js --query edb --candidate-text 经济数据库 --expected-state edb --verify-texts 经济数据库 --vision-mode live --capture-ocr true`
- The validated claim was:
  - prepared query context returned by `wind_prepare_query` was consumed by
    `wind_commit_target(query_surface)` without a second pre-selection observation path
- Validation artifacts exist under:
  - `outputs/query-surface-prepared-context-live-20260322-194431/`
- The current dirty diff is large:
  - `54 files changed`
  - `3208 insertions`
  - `1884 deletions`
- The latest committed baseline before the dirty worktree is:
  - `765c444 Fix prepared query commit state reuse`

## Important Files

- `C:/Users/terryzzb/Desktop/wind-agent/.round/active.json`
- `C:/Users/terryzzb/Desktop/wind-agent/.round/last_live_validation.json`
- `C:/Users/terryzzb/Desktop/wind-agent/docs/ARCHITECTURE.md`
- `C:/Users/terryzzb/Desktop/wind-agent/docs/TECH_DEBT.md`
- `C:/Users/terryzzb/Desktop/wind-agent/src/wind/query/surface.js`
- `C:/Users/terryzzb/Desktop/wind-agent/src/wind/state_machine/adapters.js`
- `C:/Users/terryzzb/Desktop/wind-agent/src/wind/observation_manager.js`
- `C:/Users/terryzzb/Desktop/wind-agent/src/wind/substrate/sink_registry.js`
- `C:/Users/terryzzb/Desktop/wind-agent/src/wind/wind_actions.js`
- `C:/Users/terryzzb/Desktop/wind-agent/src/wind/wind_view.js`
- `C:/Users/terryzzb/Desktop/wind-agent/src/wind/workspace_actions.js`
- `C:/Users/terryzzb/Desktop/wind-agent/src/native/native_executor.js`
- `C:/Users/terryzzb/Desktop/wind-agent/native/WindNativeExecutor/UiaDumpService.cs`

## Active Risks

- Legacy governance drift:
  repo-local `.round/*` artifacts still describe the older narrow query round,
  while the durable active round already covers the broadened
  `docs/`, `src/wind/`, `src/native/`, `native/`, `src/cli/`, and `tests/cli/`
  surface.
- Validation coverage drift:
  the live pass proves the prepared-query consumer path only; it does not prove the broader
  native/substrate/state-machine changes.
- Governance drift:
  `.round/progress.json` still reflects round initialization, not the current state after live
  validation and broader edits.
- Mainline debt remains open:
  docs still identify parallel observation truth, incomplete visual-policy centralization,
  incomplete freshness/applicability, and incomplete sink-registry adoption as active debt.
- Repo hygiene noise:
  `git_repos/` is untracked inside the repo and can obscure status/gate review if left mixed with
  mainline work.

## Next Steps

1. Keep repo-local governance artifacts from being mistaken for current durable control.
   Treat `.round/active.json` as historical evidence for the narrow proved lane, not as the
   active execution contract for the broader mainline.
2. Validate the broadened mainline in small slices.
   Start with changed owner seams around query surface, wind actions, workspace actions, dispatch
   proof, sink registry, and seam-check enforcement.
3. Refresh round artifacts.
   Run the appropriate preflight/gate flow only after the declared round matches the actual diff.
4. Continue pressure-testing the session-memory schema.
   Convert the current mainline into durable memory items for at least one decision and one failure
   once the current scope split is clarified.

