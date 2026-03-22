# Current Task

## Goal

Anchor the current `wind-agent` mainline so a fresh coding session can recover the real
state of work without replaying the entire transcript.

For the repo itself, the current explicit round goal is still:

- close query transient-surface producer-consumer debt at the Wind access layer
- keep prepared query context reusable through the public `query_surface` consumer path
- prevent pre-commit re-observation drift

## Current State

- Project: `wind-agent`
- Workspace id: `ws-8c2176c3`
- Workspace root: `C:/Users/terryzzb/Desktop/wind-agent`
- Branch: `master`
- HEAD anchor: `765c444c9dcd04ba09c58cd7e637ccd7a4669cca`
- Active round contract: `.round/active.json`
  - `round_id`: `query-surface-producer-consumer-contract`
  - declared owner layer: `src/wind/`
  - declared validation mode: `real_required`
- Real validation already passed for the narrow query prepared-context path on
  `2026-03-22`.
- The working tree has expanded beyond that narrow round:
  - docs changed
  - `src/wind/` changed broadly
  - `src/native/` and `native/` changed
  - new CLI seam-check entrypoint exists
  - many owner tests changed
- Current uncommitted mainline is therefore broader than the active round contract.

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

- Round contract drift:
  the active round allows `src/wind/`, `docs/`, and `tests/`, but the current worktree also
  touches `src/native/`, `native/`, and `src/cli/`.
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

1. Reconcile round scope with the real worktree.
   Either narrow the diff back to the declared query-surface round or amend/split the round so
   governance matches the actual owner layers being changed.
2. Validate the broadened mainline in small slices.
   Start with changed owner seams around query surface, wind actions, workspace actions, dispatch
   proof, sink registry, and seam-check enforcement.
3. Refresh round artifacts.
   Run the appropriate preflight/gate flow only after the declared round matches the actual diff.
4. Continue pressure-testing the session-memory schema.
   Convert the current mainline into durable memory items for at least one decision and one failure
   once the current scope split is clarified.
