---
id: obj-2026-03-23-1243-split-proven-query-surface-recovery-from-broader-convergence-governance
type: objective
title: "Split proven query-surface recovery from broader convergence governance"
status: active
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
  - active
confidence: high
created_at: 2026-03-23T12:43:13+08:00
updated_at: 2026-03-23T12:43:13+08:00
phase: execution
supersedes:
  - obj-2026-03-23-1242-recover-and-control-broadened-wind-agent-mainline-convergence
superseded_by: []
---

## Summary

The current wind-agent representation is still too broad: one objective is trying to cover both the already-proven prepared query path and the still-open broader substrate/native/CLI convergence debt, which makes future rounds and reviews less honest.

## Problem

The current wind-agent representation is still too broad: one objective is trying to cover both the already-proven prepared query path and the still-open broader substrate/native/CLI convergence debt, which makes future rounds and reviews less honest.

## Success Criteria

- The active objective explicitly prioritizes separating the proven query-surface lane from the still-open broader convergence lane.
- Future rounds can be scoped against one honest control boundary instead of one overloaded objective.
- Pivot lineage makes it clear why the broader recovery framing was replaced.

## Non-Goals

- Pretend the broader convergence work is already validated.
- Collapse wind-agent product direction into session-memory's own product framing.
- Rewrite wind-agent code or round artifacts automatically as part of the pivot.

## Why Now

The first wind-agent objective made the control need visible, but it is still too broad to serve as a stable execution line; the representation needs a narrower objective that distinguishes proven query behavior from still-open convergence debt.

## Current Phase

execution

## Active Risks

- The new objective may still need another split if substrate/native and query-surface work continue diverging.
- Without a matching round update, the new objective could still outrun the repo's existing governance artifacts.

## Supersession Notes

_none recorded_
