---
id: snap-2026-03-23-0744-linked-memory-proof
type: handoff
title: Session-memory after first real linked-memory proof
project_id: session-memory
workspace_id: ws-1490b759
workspace_root: C:/Users/terryzzb/Desktop/session-memory
branch: master
git_sha: 0d603f3e2ed77feed60c71812169593f982cbaad
paths:
  - scripts/build_index.py
  - scripts/smoke_phase1.py
  - projects/session-memory/current/
  - projects/session-memory/memory/decisions/
  - artifacts/evaluation/
thread_ids: []
created_at: 2026-03-23T07:44:04+08:00
updated_at: 2026-03-23T07:44:04+08:00
tags:
  - handoff
  - session-memory
  - linked-memory
  - evaluation
---

## Goal

Capture the state after proving the first real linked-memory path in
`session-memory`.

## Completed Work

- Added a superseded decision for the earlier project-scoped framing.
- Added an active decision that supersedes it with the multi-project,
  workspace-aware framing.
- Tightened smoke validation so `memory_links` must be non-zero.
- Froze the first bootstrap evaluation task and scoring protocol.

## Validated Facts

- The first linked-memory pair is real, not synthetic filler.
- The supersession reflects an actual project history transition:
  - from project-scoped
  - to multi-project and workspace-aware
- Validation should now prove `memory_links > 0`.

## Rejected Approaches

- Add fake placeholder link records only to exercise the table.
- Treat one design rewrite as enough proof without preserving the superseded
  historical object.

## Blockers

- The current evaluation remains a pilot with evaluator contamination.
- Cross-project patterns still need more than one experiment result.

## Important Files

- `C:/Users/terryzzb/Desktop/session-memory/projects/session-memory/memory/decisions/2026-03-22-project-scoped-scope.md`
- `C:/Users/terryzzb/Desktop/session-memory/projects/session-memory/memory/decisions/2026-03-23-multi-project-workspace-aware-scope.md`
- `C:/Users/terryzzb/Desktop/session-memory/scripts/build_index.py`
- `C:/Users/terryzzb/Desktop/session-memory/scripts/smoke_phase1.py`
- `C:/Users/terryzzb/Desktop/session-memory/docs/evaluation/EVALUATION.md`

## Next Steps

1. Rebuild the index and confirm `memory_links` is populated.
2. Run the bootstrap pilot through the updated smoke path.
3. Record control and treatment arm results in evaluation artifacts.
