---
id: round-2026-03-23-1431-bootstrap-broadened-wind-agent-execution-round
type: round-contract
title: "Bootstrap broadened wind-agent execution round"
status: active
project_id: wind-agent
workspace_id: ws-8c2176c3
workspace_root: C:/Users/terryzzb/Desktop/wind-agent
branch: master
git_sha: 52dd524464dfebe29c6d53a389bec8bcf731ea46
paths:
  - docs/
  - src/wind/
  - src/native/
  - native/
  - src/cli/
thread_ids: []
evidence_refs: []
tags:
  - round
  - control-plane
confidence: high
created_at: 2026-03-23T14:31:07+08:00
updated_at: 2026-03-23T14:31:07+08:00
objective_id: obj-2026-03-23-1243-split-proven-query-surface-recovery-from-broader-convergence-governance
phase: execution
supersedes: []
superseded_by: []
---

## Summary

A durable active round contract that matches the broadened wind-agent mainline and can be used as the honest control boundary for the next validation slice.

## Scope

- reconcile the broadened wind-agent mainline into one honest bounded round
- cover the current query-surface plus substrate/native/CLI convergence slice explicitly instead of pretending the old narrow round still fits
- restore round-level governance so future review and validation gates match the actual owner layers in flight

## Deliverable

A durable active round contract that matches the broadened wind-agent mainline and can be used as the honest control boundary for the next validation slice.

## Validation Plan

Re-establish one durable round that matches the real dirty mainline, then validate the broadened slice in small owner-layer checks before claiming broader convergence is proven.

## Active Risks

- The broadened round can still be too large if unrelated debt is mixed into the same contract.
- Live validation remains narrower than the broadened implementation surface until follow-up checks are run.

## Blockers

_none recorded_

## Status Notes

Opened from adjudication so durable round control catches up to the broadened mainline already visible in current-task.
