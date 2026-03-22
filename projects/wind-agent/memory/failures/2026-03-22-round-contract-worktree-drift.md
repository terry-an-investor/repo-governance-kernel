---
id: mem-2026-03-22-0002
type: failure
title: Active round contract drifted behind the real worktree
status: active
project_id: wind-agent
workspace_id: ws-8c2176c3
workspace_root: C:/Users/terryzzb/Desktop/wind-agent
branch: master
git_sha: 765c444c9dcd04ba09c58cd7e637ccd7a4669cca
paths:
  - .round/active.json
  - .round/progress.json
  - src/wind/
  - src/native/
  - native/WindNativeExecutor/
  - src/cli/run_seam_check.js
thread_ids: []
evidence_refs:
  - type: round_contract
    ref: C:/Users/terryzzb/Desktop/wind-agent/.round/active.json
  - type: round_progress
    ref: C:/Users/terryzzb/Desktop/wind-agent/.round/progress.json
  - type: task_state
    ref: C:/Users/terryzzb/Desktop/session-memory/projects/wind-agent/current/current-task.md
  - type: snapshot
    ref: C:/Users/terryzzb/Desktop/session-memory/projects/wind-agent/snapshots/2026-03-22-2134-wind-agent-mainline.md
tags:
  - governance
  - round-contract
  - scope-drift
  - validation-gap
confidence: high
created_at: 2026-03-22T21:34:57+08:00
updated_at: 2026-03-22T21:34:57+08:00
supersedes: []
superseded_by: []
---

## Summary

The active round remained scoped as a `src/wind/` query-surface contract cleanup, while the actual
dirty mainline expanded into native, substrate, CLI seam-check, docs, and broader state-machine
changes. The round metadata stopped describing the real work.

## Trigger

While extracting the first real `session-memory` snapshot, the current `wind-agent` worktree was
checked against `.round/active.json`, `.round/progress.json`, `git status`, and the live validation
artifact.

## Bad Assumption

The bad assumption was that a live pass for the narrow query-surface contract, plus a still-open
round file, was sufficient to describe the state of the full mainline.

That assumption failed because:

- the dirty diff had already spread to `src/native/`, `native/`, and `src/cli/`
- `.round/progress.json` still showed only initialization-era status
- the live validation proved one narrow path, not the entire broadened convergence work

## Evidence

- `.round/active.json` allows `src/wind/`, `docs/`, and `tests/`, and forbids broader owner-layer
  drift.
- `.round/progress.json` still reports the round as `initialized`.
- The extracted current-task state records a large dirty diff touching broader areas than the round
  declares.
- The first handoff snapshot records that the live proof passed while governance artifacts still
  lagged behind the code reality.

## Follow-up

- When the worktree expands beyond the current round, either split the work into a new round or
  amend the active contract immediately.
- Do not let one narrow live proof stand in for broader substrate or native convergence.
- Store this as a durable failure because round-governance drift is likely to recur in long coding
  sessions and is exactly the sort of state a fresh session should recover quickly.
