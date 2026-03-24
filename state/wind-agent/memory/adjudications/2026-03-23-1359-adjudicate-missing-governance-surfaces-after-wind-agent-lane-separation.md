---
id: adj-2026-03-23-1359-adjudicate-missing-governance-surfaces-after-wind-agent-lane-separation
type: adjudication
title: "Adjudicate missing governance surfaces after wind-agent lane separation"
status: recorded
project_id: wind-agent
workspace_id: ws-8c2176c3
workspace_root: C:/Users/terryzzb/Desktop/wind-agent
branch: master
git_sha: 52dd524464dfebe29c6d53a389bec8bcf731ea46
paths:
  - state/wind-agent/control/
  - state/wind-agent/memory/adjudications/
thread_ids: []
evidence_refs: []
tags:
  - adjudication
  - control-state
confidence: high
created_at: 2026-03-23T13:59:25+08:00
updated_at: 2026-03-23T13:59:25+08:00
objective_id: obj-2026-03-23-1243-split-proven-query-surface-recovery-from-broader-convergence-governance
phase: execution
supersedes: []
superseded_by: []
---

## Summary

Adjudication recorded against 3 current control-state issue(s) for project `wind-agent`.

## Conflict Set

- [warning] round-control/execution_without_open_round: the active objective is in execution phase, but no durable open round is present | evidence: obj-2026-03-23-1243-split-proven-query-surface-recovery-from-broader-convergence-governance
- [warning] constitution/missing_constitution_file: control/constitution.md is missing, so project-specific invariants cannot be compiled explicitly | evidence: C:\Users\terryzzb\Desktop\session-memory\state\wind-agent\control\constitution.md
- [warning] exception-contract/missing_exception_ledger: control/exception-ledger.md is missing, so temporary deviations have no canonical active ledger | evidence: C:\Users\terryzzb\Desktop\session-memory\state\wind-agent\control\exception-ledger.md

## Adjudication Question

Given the current execution-phase objective lacks a bounded round, constitution, and exception ledger, what remains the mainline and what must be restored before project-aware review and orchestration can be trusted?

## Verdict

Keep the current active objective as the mainline. Treat the missing round, constitution, and exception ledger as control-surface gaps, not as evidence for another pivot. Restore those governance surfaces before treating reviewer and orchestrator contexts as governance-complete.

## Objects Retained

- obj-2026-03-23-1243-split-proven-query-surface-recovery-from-broader-convergence-governance

## Objects Invalidated

_none recorded_

## Required Follow-Up Transitions

- open one bounded round against the active objective
- author control/constitution.md for wind-agent
- materialize control/exception-ledger.md for wind-agent
- rerun audit-control-state after the missing surfaces are restored

## Evidence

- audit status: warn
- audit check: durable objective-line selection
- audit check: durable round selection
- audit check: active objective projection and execution/round alignment
- audit check: active round projection and round honesty
- audit check: pivot lineage projection
- audit check: constitution and exception-contract control presence


