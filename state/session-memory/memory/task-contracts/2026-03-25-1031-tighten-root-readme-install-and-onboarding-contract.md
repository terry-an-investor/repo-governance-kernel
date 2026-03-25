---
id: taskc-2026-03-25-1031-tighten-root-readme-install-and-onboarding-contract
type: task-contract
title: "Tighten root README install and onboarding contract"
status: completed
project_id: session-memory
workspace_id: ws-1490b759
workspace_root: C:/Users/terryzzb/Desktop/session-memory
branch: master
git_sha: ecd54dbc378ce752bc782b16b6d9a071710437db
paths:
  - README.md
thread_ids: []
evidence_refs: []
tags:
  - task-contract
  - control-plane
confidence: high
created_at: 2026-03-25T10:31:19+08:00
updated_at: 2026-03-25T10:31:36+08:00
objective_id: obj-2026-03-23-0002
phase: execution
round_id: "round-2026-03-25-0946-make-package-first-repo-onboarding-real"
supersedes: []
superseded_by: []
---

## Summary

Make the root README sufficient for an agent to install the package and initialize a fresh governed host repo without relying on kernel/README for the minimal path.

## Intent

Refine the root README so one entry document gives agents the exact install, onboard, and immediate follow-up commands for package-first repo initialization.

## Allowed Changes

- Clarify the isolated environment install path in the root README.
- Document the bounded onboard-repo and onboard-repo-from-intent initialization path in the root README.
- Document the minimal post-onboarding audit and enforcement follow-up commands in the root README.

## Forbidden Changes

- Do not change command semantics or broaden authority beyond the existing onboarding surface.
- Do not turn the README into a second full package reference.

## Completion Criteria

- An agent can read the root README alone and recover the minimal install and initialization path.
- Root README remains consistent with package-facing command semantics and product docs.

## Resolution

- Added isolated-environment package install steps to the root README.
- Added bounded onboard-repo and onboard-repo-from-intent initialization examples and preconditions to the root README.
- Added minimal post-onboarding audit and enforce follow-up commands to the root README.

## Active Risks

_none recorded_

## Status Notes

active -> completed: Root README now carries the minimal package install and onboarding contract for agent callers.

resolution recorded:
- Added isolated-environment package install steps to the root README.
- Added bounded onboard-repo and onboard-repo-from-intent initialization examples and preconditions to the root README.
- Added minimal post-onboarding audit and enforce follow-up commands to the root README.
