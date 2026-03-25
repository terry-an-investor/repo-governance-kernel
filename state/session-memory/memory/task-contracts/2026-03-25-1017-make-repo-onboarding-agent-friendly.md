---
id: taskc-2026-03-25-1017-make-repo-onboarding-agent-friendly
type: task-contract
title: "Make repo onboarding agent-friendly"
status: completed
project_id: session-memory
workspace_id: ws-1490b759
workspace_root: C:/Users/terryzzb/Desktop/session-memory
branch: master
git_sha: dc6cbdf16176dc4b42ef33f01bb2ca5abb9611a1
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
created_at: 2026-03-25T10:17:14+08:00
updated_at: 2026-03-25T10:26:52+08:00
objective_id: obj-2026-03-23-0002
phase: execution
round_id: "round-2026-03-25-0946-make-package-first-repo-onboarding-real"
supersedes: []
superseded_by: []
---

## Summary

Stabilize onboard-repo output semantics and add one bounded onboarding intent surface.

## Intent

Improve the package-facing onboarding control plane so an agent can initialize a new repo through one bounded intent and consume stable structured results without reverse-engineering human docs.

## Allowed Changes

- Add one bounded onboarding intent wrapper that compiles only repo-initialization requests into onboard-repo.
- Tighten onboard-repo result structure and failure semantics so agent callers can rely on explicit ids, scope paths, statuses, and next actions.
- Update package-facing docs to document onboarding as an agent-facing command contract rather than a human step list.

## Forbidden Changes

- Do not add a setup wizard, background service, or freeform natural-language mutation authority.
- Do not broaden onboarding beyond bounded first-control-line initialization for a fresh governed host repo.

## Completion Criteria

- One bounded onboarding intent surface exists and compiles only repo-initialization requests into onboard-repo.
- onboard-repo returns stable structured fields that are sufficient for agent follow-up without parsing prose.
- Docs and smoke proof reflect the agent-facing onboarding surface and repo audits remain clean.

## Resolution

- Added bounded onboard-repo-from-intent wrapper that compiles only repo initialization requests into onboard-repo.
- Stabilized onboard-repo success and failure payloads so agents can consume structured ids, scope, postconditions, and next actions.
- Updated package-facing docs and smoke coverage for direct and intent-based onboarding flows.

## Active Risks

_none recorded_

## Status Notes

active -> completed: Agent-friendly onboarding surface landed and validated.

resolution recorded:
- Added bounded onboard-repo-from-intent wrapper that compiles only repo initialization requests into onboard-repo.
- Stabilized onboard-repo success and failure payloads so agents can consume structured ids, scope, postconditions, and next actions.
- Updated package-facing docs and smoke coverage for direct and intent-based onboarding flows.
