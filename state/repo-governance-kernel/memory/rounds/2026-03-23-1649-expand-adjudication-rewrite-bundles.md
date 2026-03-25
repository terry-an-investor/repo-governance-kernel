---
id: round-2026-03-23-1649-expand-adjudication-rewrite-bundles
type: round-contract
title: "Expand adjudication rewrite bundles"
status: closed
project_id: repo-governance-kernel
workspace_id: ws-1490b759
workspace_root: C:/Users/terryzzb/Desktop/session-memory
branch: master
git_sha: 29a8c54cb9f1ec6a7b3854d33f509a8e05ed442d
paths:
  - scripts/execute_adjudication_followups.py
  - scripts/adjudicate_control_state.py
  - scripts/smoke_adjudication_followups.py
  - state/repo-governance-kernel/
thread_ids: []
evidence_refs: []
tags:
  - round
  - control-plane
confidence: high
created_at: 2026-03-23T16:49:58+08:00
updated_at: 2026-03-23T17:10:55+08:00
objective_id: obj-2026-03-23-0002
phase: execution
supersedes: []
superseded_by: []
---

## Summary

A broader adjudication execution layer that can apply one additional multi-step rewrite bundle while preserving honest blocked boundaries.

## Scope

- Add one more safe adjudication execution bundle beyond the current structured subset, such as a multi-step round close chain or a governed objective close bundle.
- Keep machine-executable follow-up contracts explicit and bounded instead of inferring them from verdict prose.
- Validate at least one richer adjudication rewrite bundle on disposable fixtures and the live control state.

## Deliverable

A broader adjudication execution layer that can apply one additional multi-step rewrite bundle while preserving honest blocked boundaries.

## Validation Plan

Add targeted bundle regression, rerun audit-control-state, then rerun full phase-1 smoke.
uv run python scripts/smoke_adjudication_followups.py
uv run python scripts/smoke_phase1.py
uv run python scripts/repo_governance_kernel.py smoke

## Active Risks

- The executor now has one real multi-step bundle, but broader adjudication bundles still do not exist for objective-close governance or round splitting.

## Blockers

_none recorded_

## Status Notes

Implementation landed for the first bounded multi-step adjudication bundle as `round-close-chain`.

Targeted adjudication smoke passed on a disposable fixture. Full round closure still must go through formal transition commands after audit and full smoke validation.

active -> validation_pending: Milestone implementation and full smoke validation completed for the first bounded adjudication rewrite bundle.

validation_pending -> captured: Round-close-chain milestone captured after targeted smoke, phase smoke, and full smoke all passed.

validated by:
- uv run python scripts/smoke_adjudication_followups.py
- uv run python scripts/smoke_phase1.py
- uv run python scripts/repo_governance_kernel.py smoke

captured -> closed: First bounded multi-step adjudication bundle landed and validated; successor milestone should move to governed objective-close bundles.


