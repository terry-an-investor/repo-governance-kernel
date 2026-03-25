---
id: trans-2026-03-25-101714-open-task-contract-opened-task-contract-taskc-2026-03-25-1017-make-repo-onboarding-agent-friendly
type: transition-event
title: "Opened task contract taskc-2026-03-25-1017-make-repo-onboarding-agent-friendly"
status: recorded
project_id: repo-governance-kernel
workspace_id: ws-1490b759
workspace_root: C:/Users/terryzzb/Desktop/session-memory
branch: master
git_sha: dc6cbdf16176dc4b42ef33f01bb2ca5abb9611a1
paths:
  - taskc-2026-03-25-1017-make-repo-onboarding-agent-friendly
  - round-2026-03-25-0946-make-package-first-repo-onboarding-real
  - obj-2026-03-23-0002
thread_ids: []
evidence_refs: []
tags:
  - transition-event
  - open-task-contract
confidence: high
created_at: 2026-03-25T10:17:14+08:00
updated_at: 2026-03-25T10:17:14+08:00
supersedes: []
superseded_by: []
---

## Summary

Opened task contract taskc-2026-03-25-1017-make-repo-onboarding-agent-friendly

## Command

open-task-contract

## Previous State

round `round-2026-03-25-0946-make-package-first-repo-onboarding-real` already had 1 durable task-contract record(s)

## Next State

task contract `taskc-2026-03-25-1017-make-repo-onboarding-agent-friendly` is now active beneath round `round-2026-03-25-0946-make-package-first-repo-onboarding-real`

## Guards

- round `round-2026-03-25-0946-make-package-first-repo-onboarding-real` exists and remains open for task attachment
- task-contract objective linkage matches the referenced round
- task intent is explicit
- task scope paths are explicit
- task scope paths stay inside the round scope
- allowed changes, forbidden changes, and completion criteria are all present

## Side Effects

- wrote durable task contract `repo-governance-kernel/memory/task-contracts/2026-03-25-1017-make-repo-onboarding-agent-friendly.md`

## Evidence

- Improve the package-facing onboarding control plane so an agent can initialize a new repo through one bounded intent and consume stable structured results without reverse-engineering human docs.
- One bounded onboarding intent surface exists and compiles only repo-initialization requests into onboard-repo.
- onboard-repo returns stable structured fields that are sufficient for agent follow-up without parsing prose.
- Docs and smoke proof reflect the agent-facing onboarding surface and repo audits remain clean.

