---
id: obj-2026-03-23-1242-recover-and-control-broadened-wind-agent-mainline-convergence
type: objective
title: "Recover and control broadened wind-agent mainline convergence"
status: superseded
project_id: wind-agent
workspace_id: ws-8c2176c3
workspace_root: C:/Users/terryzzb/Desktop/wind-agent
branch: master
git_sha: 18b32a9ca0c1fd43da1d9ea9ce1ec6e002c464eb
paths:
  - .round/active.json
  - docs/ARCHITECTURE.md
  - src/wind/
  - src/native/
thread_ids: []
evidence_refs: []
tags:
  - objective
  - superseded
confidence: high
created_at: 2026-03-23T12:42:05+08:00
updated_at: 2026-03-23T12:43:13+08:00
phase: execution
supersedes: []
superseded_by:
  - obj-2026-03-23-1243-split-proven-query-surface-recovery-from-broader-convergence-governance
---

## Summary

Fresh sessions can recover one validated query-surface claim, but the current wind-agent mainline now spans broader substrate, native, CLI, and governance drift that no active control objective names explicitly.

## Problem

Fresh sessions can recover one validated query-surface claim, but the current wind-agent mainline now spans broader substrate, native, CLI, and governance drift that no active control objective names explicitly.

## Success Criteria

- Active objective state makes the broadened mainline scope explicit for fresh sessions and side roles.
- Future rounds and reviews can anchor to real convergence work instead of the stale narrow query-surface round.
- Control artifacts stop hiding scope and validation drift behind old round metadata.

## Non-Goals

- Replace wind-agent's own round tooling.
- Claim broad live validation that has not happened.
- Redefine wind-agent's product mission outside the current mainline convergence work.

## Why Now

wind-agent is the first non-self-hosted project sample, so it needs a real active objective before objective and pivot commands can be judged as project-agnostic control primitives.

## Current Phase

execution

## Active Risks

- The broadened convergence objective may still be too wide for one honest round and may need splitting.
- The session-memory view of wind-agent could overfit to current governance pain if later repo context contradicts it.

## Supersession Notes

Superseded by `obj-2026-03-23-1243-split-proven-query-surface-recovery-from-broader-convergence-governance` because the newly opened broad recovery objective is still too overloaded to guide honest round control, so the project representation needs a new active objective centered on explicit lane separation and governance recovery
