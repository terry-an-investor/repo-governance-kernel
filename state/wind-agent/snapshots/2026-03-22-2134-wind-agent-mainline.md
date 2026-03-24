---
id: snap-2026-03-22-2134-wind-agent-mainline
type: handoff
title: Wind-agent mainline after query-surface live proof and broader convergence drift
project_id: wind-agent
workspace_id: ws-8c2176c3
workspace_root: C:/Users/terryzzb/Desktop/wind-agent
branch: master
git_sha: 765c444c9dcd04ba09c58cd7e637ccd7a4669cca
paths:
  - .round/
  - docs/
  - src/wind/
  - src/native/
  - native/WindNativeExecutor/
  - tests/cli/
thread_ids: []
created_at: 2026-03-22T21:34:57+08:00
updated_at: 2026-03-22T21:34:57+08:00
tags:
  - handoff
  - wind-agent
  - query-surface
  - substrate-convergence
  - governance-drift
---

## Goal

Capture the first real session-memory handoff for the current `wind-agent` mainline so a fresh
session can recover:

- what the declared round is
- what has been actually proven
- how the dirty worktree has already expanded past that round
- what should happen next

## Completed Work

- The active round contract was defined for `query-surface-producer-consumer-contract`.
- A real Wind query prepare -> commit flow was successfully validated.
- Prepared query context was proven reusable through the public `query_surface` consumer path.
- Canonical docs were rewritten around shared substrate, owner-layer contracts, dispatch proof,
  freshness/applicability, and convergence debt.
- The uncommitted mainline also broadened beyond the original round into:
  - broader `src/wind/` state-machine and substrate changes
  - `src/native/` and native executor changes
  - new seam-check and dispatch-proof related test coverage

## Validated Facts

- Active round file:
  - `C:/Users/terryzzb/Desktop/wind-agent/.round/active.json`
- Active round id:
  - `query-surface-producer-consumer-contract`
- Latest recorded live validation:
  - `pass`
- Validation command:
  - `node tests/cli/run_query_surface_prepared_context_live.js --query edb --candidate-text 经济数据库 --expected-state edb --verify-texts 经济数据库 --vision-mode live --capture-ocr true`
- Validation artifact root:
  - `C:/Users/terryzzb/Desktop/wind-agent/outputs/query-surface-prepared-context-live-20260322-194431/`
- HEAD anchor:
  - `765c444c9dcd04ba09c58cd7e637ccd7a4669cca`
- Current dirty diff summary:
  - `54 files changed, 3208 insertions, 1884 deletions`

## Rejected Approaches

- Re-observing the popup immediately before candidate commit as the default consumer path.
- Keeping query transient-surface logic as page-local glue instead of a reusable producer-consumer
  contract.
- Treating dispatch success as equivalent to verified business success.
- Treating raw observation/debug payloads as parallel owner truth once canonical observation/state
  exists.

## Blockers

- The active round contract is narrower than the actual worktree.
- Native and CLI changes currently exceed the declared allowed paths for the active round.
- Live validation coverage is narrower than the current dirty diff.
- Governance artifacts have not been refreshed to reflect the broadened mainline.

## Important Files

- `C:/Users/terryzzb/Desktop/wind-agent/.round/active.json`
- `C:/Users/terryzzb/Desktop/wind-agent/.round/last_live_validation.json`
- `C:/Users/terryzzb/Desktop/wind-agent/docs/ARCHITECTURE.md`
- `C:/Users/terryzzb/Desktop/wind-agent/docs/TECH_DEBT.md`
- `C:/Users/terryzzb/Desktop/wind-agent/docs/TOOL_DESIGN.md`
- `C:/Users/terryzzb/Desktop/wind-agent/docs/VOCABULARY.md`
- `C:/Users/terryzzb/Desktop/wind-agent/src/wind/query/surface.js`
- `C:/Users/terryzzb/Desktop/wind-agent/src/wind/state_machine/adapters.js`
- `C:/Users/terryzzb/Desktop/wind-agent/src/wind/substrate/sink_registry.js`
- `C:/Users/terryzzb/Desktop/wind-agent/src/wind/observation_manager.js`
- `C:/Users/terryzzb/Desktop/wind-agent/src/wind/wind_actions.js`
- `C:/Users/terryzzb/Desktop/wind-agent/src/wind/workspace_actions.js`
- `C:/Users/terryzzb/Desktop/wind-agent/src/native/native_executor.js`
- `C:/Users/terryzzb/Desktop/wind-agent/native/WindNativeExecutor/UiaDumpService.cs`

## Next Steps

1. Split or amend the active round so the contract matches the real owner layers in the diff.
2. Run the smallest credible tests for each broadened owner seam instead of assuming the one live
   query proof covers the rest.
3. After scope is honest again, refresh preflight/gate artifacts.
4. Extract durable memory items from this snapshot:
   - one decision about prepared query-context reuse
   - one failure about round-contract drift versus real worktree drift
