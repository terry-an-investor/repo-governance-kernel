---
id: taskc-2026-03-25-1221-rename-stale-phase-1-acceptance-smoke-surface
type: task-contract
title: "Rename stale phase-1 acceptance smoke surface"
status: completed
project_id: repo-governance-kernel
workspace_id: ws-1490b759
workspace_root: C:/Users/terryzzb/Desktop/session-memory
branch: master
git_sha: bb118b9346eae2b83714ffc5dd6d388aaebbd9b9
paths:
  - scripts
  - docs
  - README.md
  - .githooks
  - .github
thread_ids: []
evidence_refs: []
tags:
  - task-contract
  - control-plane
confidence: high
created_at: 2026-03-25T12:21:00+08:00
updated_at: 2026-03-25T12:29:09+08:00
objective_id: obj-2026-03-23-0002
phase: execution
round_id: "round-2026-03-25-1116-start-explicit-package-config-layering-for-a4"
supersedes: []
superseded_by: []
---

## Summary

Replace the stale smoke_phase1 name with a clearer repo-acceptance smoke entrypoint and update repo-owned triggers and docs so the validation surface says what it actually is.

## Intent

Replace the stale smoke_phase1 name with a clearer repo-acceptance smoke entrypoint and update repo-owned triggers and docs so the validation surface says what it actually is.

## Allowed Changes

- Rename the top-level acceptance smoke script and update repo-owned wrappers, hooks, CI, and release-facing docs to the new name in one round.
- Keep the acceptance command shape and validation semantics the same while changing only the naming and entrypoint references.

## Forbidden Changes

- Do not keep the old smoke_phase1 path around as a fallback alias.
- Do not broaden or narrow the acceptance smoke scope under the cover of a rename.

## Completion Criteria

- The top-level repo acceptance smoke has one new canonical path and repo-owned triggers no longer reference smoke_phase1.py.
- The renamed acceptance smoke passes under Python 3.11 and through the normal repo validation path.
- Canonical docs and repo-facing quickstart text stop describing the top-level acceptance smoke as phase-1.

## Resolution

- Renamed scripts/smoke_phase1.py to scripts/smoke_repo_acceptance.py and updated the repo smoke alias.
- Updated CI, pre-push, README, harness docs, and release docs to call the acceptance surface repo acceptance smoke.
- Validated the renamed script and scripts/repo_governance_kernel.py smoke under Python 3.11, then reran audit-control-state and enforce-worktree.

## Active Risks

- If the stale phase-1 label remains, CI and local hooks will keep obscuring what the acceptance script actually validates.
- If both names survive, the repo will drift into duplicate acceptance entrypoints and unclear trigger ownership.

## Status Notes

active -> completed: Renamed the stale phase-1 smoke surface to repo acceptance smoke, updated live references, and revalidated the renamed acceptance path under Python 3.11.

resolution recorded:
- Renamed scripts/smoke_phase1.py to scripts/smoke_repo_acceptance.py and updated the repo smoke alias.
- Updated CI, pre-push, README, harness docs, and release docs to call the acceptance surface repo acceptance smoke.
- Validated the renamed script and scripts/repo_governance_kernel.py smoke under Python 3.11, then reran audit-control-state and enforce-worktree.

