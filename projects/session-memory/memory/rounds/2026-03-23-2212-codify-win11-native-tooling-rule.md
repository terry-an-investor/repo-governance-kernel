---
id: round-2026-03-23-2212-codify-win11-native-tooling-rule
type: round-contract
title: "Codify Win11-native tooling rule"
status: active
project_id: session-memory
workspace_id: ws-1490b759
workspace_root: C:/Users/terryzzb/Desktop/session-memory
branch: master
git_sha: 745e42622fe1c9245eb8d72687ebfff2a170dad8
paths:
  - AGENTS.md
  - projects/session-memory/current/current-task.md
thread_ids: []
evidence_refs: []
tags:
  - round
  - control-plane
confidence: high
created_at: 2026-03-23T22:12:50+08:00
updated_at: 2026-03-23T22:13:34+08:00
objective_id: obj-2026-03-23-0002
phase: execution
supersedes: []
superseded_by: []
---

## Summary

A committed repository rule that directs agents to use Win11-native tooling for this repo.

## Scope

- Record repository-local tooling policy that this repo uses PowerShell and Windows Git rather than WSL shells.

## Deliverable

A committed repository rule that directs agents to use Win11-native tooling for this repo.

## Validation Plan

Run audit_control_state and enforce_worktree after the rule lands, then close the round and return the objective to paused.

## Active Risks

_none recorded_

## Blockers

_none recorded_

## Status Notes

_none recorded_

Round rewritten because Refresh current-task anchor so the active round is honestly reflected in control orientation before commit.
