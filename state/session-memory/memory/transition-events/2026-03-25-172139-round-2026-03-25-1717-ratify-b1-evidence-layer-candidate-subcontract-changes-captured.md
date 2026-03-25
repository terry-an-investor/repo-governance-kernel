---
id: trans-2026-03-25-172139-update-round-status-updated-round-round-2026-03-25-1717-ratify-b1-evidence-layer-candidate-subcontract-changes-to-captured
type: transition-event
title: "Updated round round-2026-03-25-1717-ratify-b1-evidence-layer-candidate-subcontract-changes to captured"
status: recorded
project_id: session-memory
workspace_id: ws-1490b759
workspace_root: C:/Users/terryzzb/Desktop/session-memory
branch: master
git_sha: a47358d96bde31269421b6cc5815b713daba7e8f
paths:
  - round-2026-03-25-1717-ratify-b1-evidence-layer-candidate-subcontract-changes
  - obj-2026-03-23-0002
thread_ids: []
evidence_refs: []
tags:
  - transition-event
  - update-round-status
confidence: high
created_at: 2026-03-25T17:21:39+08:00
updated_at: 2026-03-25T17:21:39+08:00
supersedes: []
superseded_by: []
---

## Summary

Updated round round-2026-03-25-1717-ratify-b1-evidence-layer-candidate-subcontract-changes to captured

## Command

update-round-status

## Previous State

round `round-2026-03-25-1717-ratify-b1-evidence-layer-candidate-subcontract-changes` status `validation_pending`

## Next State

round `round-2026-03-25-1717-ratify-b1-evidence-layer-candidate-subcontract-changes` is now `captured`

## Guards

- round `round-2026-03-25-1717-ratify-b1-evidence-layer-candidate-subcontract-changes` exists
- transition `validation_pending -> captured` is legal
- captured or closed promotion passes worktree enforcement when required
- captured status includes at least one validation record when capture is requested
- no draft or active task contract remains attached to the round before it leaves open execution

## Side Effects

- updated durable round contract `session-memory/memory/rounds/2026-03-25-1717-ratify-b1-evidence-layer-candidate-subcontract-changes.md`
- removed active round projection `session-memory/control/active-round.md`

## Evidence

- the ratification round is now durably recorded in git commit a47358d
- git commit a47358d
