---
id: taskc-2026-03-25-0946-land-package-first-repo-onboarding
type: task-contract
title: "Land package-first repo onboarding"
status: completed
project_id: session-memory
workspace_id: ws-1490b759
workspace_root: C:/Users/terryzzb/Desktop/session-memory
branch: master
git_sha: afad3f1b796dd2cb73421997d577eacb1635334e
paths:
  - kernel
  - scripts
  - docs
  - README.md
thread_ids: []
evidence_refs: []
tags:
  - task-contract
  - control-plane
confidence: high
created_at: 2026-03-25T09:46:59+08:00
updated_at: 2026-03-25T10:12:03+08:00
objective_id: obj-2026-03-23-0002
phase: execution
round_id: "round-2026-03-25-0946-make-package-first-repo-onboarding-real"
supersedes: []
superseded_by: []
---

## Summary

Add one owner-layer onboarding command that bootstraps a repo and, when real non-control dirty paths exist, opens the first honest objective/round/task setup for that host.

## Intent

Reduce package-first adoption friction by replacing the current manual bootstrap plus authoring sequence with one bounded onboarding surface that still respects registry-owned guards and real dirty-path scope.

## Allowed Changes

- Add one package-facing onboarding command or bounded workflow that composes existing owner-layer primitives instead of relying on smoke-only setup helpers.
- Add one focused proof showing a disposable host repo can bootstrap, open its first honest control objects from real dirty paths, refresh the anchor, and remain audit-clean.
- Update package-facing docs so a new user can find and understand the onboarding path without reverse-engineering smoke scripts.

## Forbidden Changes

- Do not broaden into continuous monitoring, background services, or freeform autonomous mutation.
- Do not fabricate round or task scope on a clean repo just to make onboarding look smoother than the real repo state.

## Completion Criteria

- A package-facing onboarding surface exists and can create the first honest governance setup for a disposable repo with real dirty paths.
- A focused smoke proves the onboarding surface from a fresh host repo rather than from repo-local helper setup.
- Audit, enforcement, and package-facing docs remain clean after the onboarding path lands.

## Resolution

- Added one package-facing onboard-repo wrapper backed by registry-owned bootstrap and onboarding bundle semantics.
- Focused onboarding smoke and installed-wheel bootstrap proof now both use the same onboarding surface and finish audit-clean plus enforce-clean.

## Active Risks

_none recorded_

## Status Notes

active -> completed: The package-facing repo onboarding surface, bundle registry wiring, docs, and smoke proof now land as one coherent onboarding path.

resolution recorded:
- Added one package-facing onboard-repo wrapper backed by registry-owned bootstrap and onboarding bundle semantics.
- Focused onboarding smoke and installed-wheel bootstrap proof now both use the same onboarding surface and finish audit-clean plus enforce-clean.
