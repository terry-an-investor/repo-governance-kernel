---
id: taskc-2026-03-25-1055-land-a3-roadmap-and-first-repo-owned-agent-skill
type: task-contract
title: "Land a3 roadmap and first repo-owned agent skill"
status: completed
project_id: repo-governance-kernel
workspace_id: ws-1490b759
workspace_root: C:/Users/terryzzb/Desktop/session-memory
branch: master
git_sha: e8ee75f6e4f188e611fc07246a631e5a52eaf320
paths:
  - docs
  - README.md
  - kernel/README.md
  - skills
thread_ids: []
evidence_refs: []
tags:
  - task-contract
  - control-plane
confidence: high
created_at: 2026-03-25T10:55:52+08:00
updated_at: 2026-03-25T10:58:01+08:00
objective_id: obj-2026-03-23-0002
phase: execution
round_id: "round-2026-03-25-0946-make-package-first-repo-onboarding-real"
supersedes: []
superseded_by: []
---

## Summary

Write the next version roadmap into canonical docs and add one repo-owned agent skill for bounded onboarding and external-target assessment entrypoints.

## Intent

Turn the current package surface into a clearer product plan and a more explicit agent-facing entry by landing canonical roadmap truth plus one repo-owned skill.

## Allowed Changes

- Update canonical implementation and release planning docs with the a3-plus roadmap for public alpha surface, config layering, one-task productization, and beta freeze.
- Add one repo-owned skill that tells agents how to use bounded onboarding and single-assessment surfaces without widening authority.
- Update package-facing docs so the new skill and roadmap are discoverable from the main doc entrypoints.

## Forbidden Changes

- Do not add new broad mutation workflows, setup wizards, or monitoring/server behavior.
- Do not broaden the public command surface beyond already-implemented bounded entrypoints in this round.

## Completion Criteria

- Canonical docs record the agreed version roadmap from a3 through beta freeze.
- A repo-owned agent skill exists for bounded onboarding and single assessment and stays aligned with the current command surface.
- Docs, audit, and enforcement remain clean after the roadmap and skill land.

## Resolution

- Updated canonical implementation and release docs with the version roadmap from a3 through beta freeze.
- Added the first repo-owned agent skill for bounded onboarding and one-time external-target assessment.
- Updated the main doc entrypoints so the roadmap and repo-owned skill are discoverable.

## Active Risks

_none recorded_

## Status Notes

active -> completed: The a3-plus roadmap and the first repo-owned agent skill now exist in canonical docs and repo-owned packaging.

resolution recorded:
- Updated canonical implementation and release docs with the version roadmap from a3 through beta freeze.
- Added the first repo-owned agent skill for bounded onboarding and one-time external-target assessment.
- Updated the main doc entrypoints so the roadmap and repo-owned skill are discoverable.

