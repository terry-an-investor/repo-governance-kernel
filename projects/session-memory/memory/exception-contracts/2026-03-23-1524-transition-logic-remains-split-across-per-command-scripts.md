---
id: exc-2026-03-23-1524-transition-logic-remains-split-across-per-command-scripts
type: exception-contract
title: "Transition logic remains split across per-command scripts"
status: active
project_id: session-memory
workspace_id: ws-1490b759
workspace_root: C:/Users/terryzzb/Desktop/session-memory
branch: master
git_sha: 41f9d2e9e3d3caaaae16446b43d74b2ace393ccf
paths:
  - scripts/open_objective.py
  - scripts/open_round.py
  - scripts/update_round_status.py
  - scripts/activate_exception_contract.py
  - scripts/retire_exception_contract.py
  - scripts/invalidate_exception_contract.py
  - scripts/round_control.py
  - TRANSITION_COMMANDS.md
thread_ids: []
evidence_refs: []
tags:
  - exception-contract
  - control-plane
confidence: high
created_at: 2026-03-23T15:24:00+08:00
updated_at: 2026-03-23T15:24:00+08:00
objective_id: obj-2026-03-23-0002
phase: execution
supersedes: []
superseded_by: []
---

## Summary

The control plane still accepts duplicated transition-writing logic across command-specific scripts while the shared transition engine remains unimplemented.

## Reason

The repo has real enforced slices now, but objective, round, and exception transitions still land through separate command owners instead of one shared engine.

## Temporary Behavior

Commands such as open-objective, open-round, update-round-status, and the new exception-contract commands still own overlapping transition-writing logic locally rather than delegating to one shared transition engine.

## Risk

Duplicated transition logic can drift in guard semantics, projection side effects, and transition-event fidelity across command families.

## Exit Condition

Retire this contract once objective, round, and exception-contract transitions share one owner-layer transition engine or a materially equivalent common primitive.

## Owner Scope

- scripts/open_objective.py
- scripts/open_round.py
- scripts/update_round_status.py
- scripts/activate_exception_contract.py
- scripts/retire_exception_contract.py
- scripts/invalidate_exception_contract.py

## Evidence

- current objective still lists a shared transition engine as future work
- multiple command scripts currently write durable objects and transition events directly

## Resolution

_none recorded_
