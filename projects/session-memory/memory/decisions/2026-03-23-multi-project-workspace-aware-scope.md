---
id: mem-2026-03-23-0002
type: decision
title: Multi-project workspace-aware scope replaces the earlier project-scoped framing
status: active
project_id: session-memory
workspace_id: ws-1490b759
workspace_root: C:/Users/terryzzb/Desktop/session-memory
branch: master
git_sha: 0d603f3e2ed77feed60c71812169593f982cbaad
paths:
  - DESIGN_PRINCIPLES.md
  - ARCHITECTURE.md
  - SCHEMA.md
  - projects/session-memory/
thread_ids: []
evidence_refs:
  - type: note
    ref: C:/Users/terryzzb/Desktop/session-memory/docs/history/2026-03-22-notes.md
  - type: doc
    ref: C:/Users/terryzzb/Desktop/session-memory/DESIGN_PRINCIPLES.md
  - type: doc
    ref: C:/Users/terryzzb/Desktop/session-memory/ARCHITECTURE.md
  - type: doc
    ref: C:/Users/terryzzb/Desktop/session-memory/SCHEMA.md
tags:
  - scope
  - multi-project
  - workspace-aware
  - supersession
confidence: high
created_at: 2026-03-23T07:44:04+08:00
updated_at: 2026-03-23T07:44:04+08:00
supersedes:
  - mem-2026-03-22-0003
superseded_by: []
---

## Summary

The system scope must be multi-project and workspace-aware rather than
project-scoped, because the real user requirement is continuity across many
repositories and local workspaces.

## Context

After the first design pass, the project was corrected explicitly:

- the user would not stay in one repository forever
- same-project parallel workspaces would otherwise collide
- project-specific governance could not become the global ontology

This made the earlier project-scoped framing too narrow.

## Decision

Replace the project-scoped framing with:

- multi-project memory
- workspace-aware identity
- project-local plus cross-project memory layout

## Rejected Alternatives

- Keep the system centered on one long-lived repo.
- Treat `wind-agent` as the schema owner instead of as the first sample.
- Delay the scope correction until after more implementation accumulated.

## Evidence

- The project notes captured the earlier project-scoped conclusion.
- The later canonical docs explicitly changed the design to multi-project and
  workspace-aware.
- The current repository now has two real project samples: `wind-agent` and
  `session-memory`.

## Consequences

- `project_id`, `workspace_id`, and `workspace_root` are now first-class.
- `projects/<project_id>/...` is the canonical layout.
- The earlier project-scoped framing is preserved as history, not deleted.
