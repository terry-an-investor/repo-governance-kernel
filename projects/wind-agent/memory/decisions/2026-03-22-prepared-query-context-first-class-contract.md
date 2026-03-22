---
id: mem-2026-03-22-0001
type: decision
title: Prepared query context must be a first-class consumer contract
status: active
project_id: wind-agent
workspace_id: ws-8c2176c3
workspace_root: C:/Users/terryzzb/Desktop/wind-agent
branch: master
git_sha: 765c444c9dcd04ba09c58cd7e637ccd7a4669cca
paths:
  - src/wind/query/surface.js
  - src/wind/query/contract.js
  - src/wind/state_machine/adapters.js
  - docs/ARCHITECTURE.md
  - docs/TOOL_DESIGN.md
thread_ids: []
evidence_refs:
  - type: round_contract
    ref: C:/Users/terryzzb/Desktop/wind-agent/.round/active.json
  - type: live_validation
    ref: C:/Users/terryzzb/Desktop/wind-agent/.round/last_live_validation.json
  - type: artifact
    ref: C:/Users/terryzzb/Desktop/wind-agent/outputs/query-surface-prepared-context-live-20260322-194431/summary.json
  - type: snapshot
    ref: C:/Users/terryzzb/Desktop/session-memory/projects/wind-agent/snapshots/2026-03-22-2134-wind-agent-mainline.md
tags:
  - query-surface
  - transient-surface
  - producer-consumer
  - contract
  - drift-control
confidence: high
created_at: 2026-03-22T21:34:57+08:00
updated_at: 2026-03-22T21:34:57+08:00
supersedes: []
superseded_by: []
---

## Summary

Prepared query popup state should not remain an internal transient blob or force a second
observation pass before commit. It must be exposed as a first-class consumer contract that later
query-surface actions can reuse directly.

## Context

The active `wind-agent` round was explicitly framed around query transient-surface
producer-consumer drift. The repeated failure mode was:

- prepare logic observes enough popup context to identify candidate state
- commit logic then re-observes or rebuilds context
- popup state drifts between the two steps
- consumer paths stop being deterministic and start depending on accidental timing

This is not just a query popup issue. It is the smallest honest example of a broader transient
surface problem where producer output must become reusable consumer input.

## Decision

The system should treat prepared query context as a first-class tool-facing contract.

That means:

- `wind_prepare_query` should emit a reusable prepared context object
- `wind_commit_target(query_surface)` should consume that object directly
- commit should not require a second pre-selection observation path when the prepared context is
  still applicable
- the same producer-consumer contract shape should later generalize to other transient-surface
  families

## Rejected Alternatives

- Re-observe the popup immediately before every candidate commit.
  This makes correctness depend on surface stability and timing instead of on an explicit contract.
- Keep prepared popup context as an internal implementation detail.
  That prevents replay, cross-tool reuse, and owner-layer validation.
- Solve drift with page-local glue or special-case commit helpers.
  That hides the real problem class and does not create a reusable primitive.

## Evidence

- The declared round contract in `.round/active.json` is specifically about prepared query context
  reuse through the public consumer path.
- `.round/last_live_validation.json` records a `pass` for the real proof command:
  `node tests/cli/run_query_surface_prepared_context_live.js --query edb --candidate-text 经济数据库 --expected-state edb --verify-texts 经济数据库 --vision-mode live --capture-ocr true`
- The validation summary under
  `outputs/query-surface-prepared-context-live-20260322-194431/summary.json` shows that prepared
  query context was returned by prepare and consumed by commit without a second pre-selection
  observation path.

## Consequences

- Query-surface work should now be reviewed in terms of producer-consumer contract fidelity, not
  in terms of whether one helper happened to succeed.
- Future transient-surface families should prefer the same reusable contract shape.
- Retrieval in this memory system should store this as a durable decision because it is a stable
  architectural rule, not a one-off session note.
