# Current Task

## Goal

Turn `session-memory` from a design-only workspace into a stable phase-1 system
for multi-project coding-agent memory.

The immediate objective is:

- keep the design frozen around Markdown plus SQLite plus FTS5
- improve fresh-session context assembly quality
- validate the schema on more than one project sample
- prove the first real linked-memory path with `supersedes` / `superseded_by`

## Current State

- Project: `session-memory`
- Workspace id: `ws-1490b759`
- Workspace root: `C:/Users/terryzzb/Desktop/session-memory`
- Branch: `master`
- HEAD anchor: `0d603f3e2ed77feed60c71812169593f982cbaad`
- Phase-1 baseline already exists:
  - multi-project schema is documented
  - `wind-agent` is indexed as the first project sample
  - SQLite plus FTS5 build/query/assemble path is working
  - unified CLI and smoke command exist
- Current dirty work is focused on:
  - validating the first real linked-memory sample
  - preserving clean multi-project evaluation artifacts

## Validated Facts

- The latest committed baseline is:
  - `0d603f3 Implement phase-1 SQLite FTS5 memory pipeline`
- `uv run python scripts/session_memory.py smoke` passed on the committed
  baseline.
- Current index baseline before adding this project sample was:
  - `memory_items = 6`
  - `memory_paths = 17`
  - `memory_evidence_refs = 8`
  - `memory_fts = 6`
- The first real linked-memory pair now exists in `projects/session-memory/`.

## Important Files

- `C:/Users/terryzzb/Desktop/session-memory/DESIGN_PRINCIPLES.md`
- `C:/Users/terryzzb/Desktop/session-memory/ARCHITECTURE.md`
- `C:/Users/terryzzb/Desktop/session-memory/SCHEMA.md`
- `C:/Users/terryzzb/Desktop/session-memory/IMPLEMENTATION_PLAN.md`
- `C:/Users/terryzzb/Desktop/session-memory/EVALUATION.md`
- `C:/Users/terryzzb/Desktop/session-memory/scripts/build_index.py`
- `C:/Users/terryzzb/Desktop/session-memory/scripts/query_index.py`
- `C:/Users/terryzzb/Desktop/session-memory/scripts/assemble_context.py`
- `C:/Users/terryzzb/Desktop/session-memory/scripts/session_memory.py`
- `C:/Users/terryzzb/Desktop/session-memory/scripts/smoke_phase1.py`
- `C:/Users/terryzzb/Desktop/session-memory/projects/session-memory/memory/decisions/2026-03-22-project-scoped-scope.md`
- `C:/Users/terryzzb/Desktop/session-memory/projects/session-memory/memory/decisions/2026-03-23-multi-project-workspace-aware-scope.md`

## Active Risks

- The current assembler still risks over-including repeated information when
  current-task and snapshot overlap.
- The repo has only one committed project sample so far; without a second
  sample, multi-project claims are still under-proven.
- The evaluation protocol is still a biased pilot because the evaluator already
  knows the project context.

## Next Steps

1. Rebuild and validate the index across both projects after the linked-memory
   sample lands.
2. Keep compressing assembled context so it acts like a handoff packet instead
   of a file dump.
3. Run and record the first bootstrap control-vs-treatment experiment.
4. Add the first cross-project pattern only if the evaluation produces a stable
   lesson.
