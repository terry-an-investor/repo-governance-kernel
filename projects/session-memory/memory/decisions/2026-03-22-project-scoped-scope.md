---
id: mem-2026-03-22-0003
type: decision
title: Project-scoped memory was the initial scope framing
status: superseded
project_id: session-memory
workspace_id: ws-1490b759
workspace_root: C:/Users/terryzzb/Desktop/session-memory
branch: master
git_sha: 0d603f3e2ed77feed60c71812169593f982cbaad
paths:
  - docs/history/2026-03-22-notes.md
  - docs/canonical/DESIGN_PRINCIPLES.md
  - docs/canonical/ARCHITECTURE.md
thread_ids: []
evidence_refs:
  - type: note
    ref: C:/Users/terryzzb/Desktop/session-memory/docs/history/2026-03-22-notes.md
tags:
  - scope
  - project-scoped
  - superseded
confidence: medium
created_at: 2026-03-23T07:44:04+08:00
updated_at: 2026-03-23T07:44:04+08:00
supersedes: []
superseded_by:
  - mem-2026-03-23-0002
---

## Summary

The initial framing narrowed the system to project-scoped coding memory before
the design was pressure-tested against the real requirement of working across
many repositories and local workspaces.

## Context

The earliest design pass was intentionally narrow to avoid overbuilding.
In that phase, the notes explicitly concluded that a coding-first,
project-scoped variant was the right immediate direction.

## Decision

Treat project-scoped coding memory as the temporary framing for the first design
pass.

## Rejected Alternatives

- Start immediately as a generalized Memory OS.
- Start with broad personal-memory categories instead of coding work state.

## Evidence

- `docs/history/2026-03-22-notes.md` explicitly concluded that a coding-first,
  project-scoped variant was appropriate at that stage.

## Consequences

- This framing helped keep the first design pass narrow.
- It later became too narrow once the requirement of multi-project continuity
  was made explicit.
