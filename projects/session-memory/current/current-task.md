# Current Task

## Goal

Turn `session-memory` into a stable phase-1 coding control system built on a
file-first memory substrate.

The immediate objective is:

- keep the design frozen around Markdown plus SQLite plus FTS5
- add first-class control-state files for objective, pivot, and workaround
- improve fresh-session context assembly quality
- compile handoff through active objective state instead of recency alone

## Current State

- Project: `session-memory`
- Objective id: `obj-2026-03-23-0002`
- Phase: `execution`
- Workspace id: `ws-1490b759`
- Workspace root: `C:/Users/terryzzb/Desktop/session-memory`
- Branch: `master`
- HEAD anchor: `0d603f3e2ed77feed60c71812169593f982cbaad`
- Phase-1 baseline already exists:
  - multi-project schema is documented
  - `wind-agent` is indexed as the first project sample
  - SQLite plus FTS5 build/query/assemble path is working
  - unified CLI and smoke command exist
- Control-system framing is now explicit:
  - durable docs define objective, pivot, and workaround as first-class objects
  - this project is the first real sample for a hard pivot in objective line
- Current work is focused on:
  - validating the first real control-state sample under `projects/session-memory/control/`
  - tightening packet shape now that `assemble` reads active objective and pivot lineage

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
- The project direction is now clarified:
  - from multi-project coding-agent memory
  - to coding control system built on top of that memory substrate
- `assemble_context.py` now compiles:
  - active objective
  - pivot lineage
  - workaround ledger when present

## Important Files

- `C:/Users/terryzzb/Desktop/session-memory/DESIGN_PRINCIPLES.md`
- `C:/Users/terryzzb/Desktop/session-memory/ARCHITECTURE.md`
- `C:/Users/terryzzb/Desktop/session-memory/CONTROL_SYSTEM.md`
- `C:/Users/terryzzb/Desktop/session-memory/SCHEMA.md`
- `C:/Users/terryzzb/Desktop/session-memory/IMPLEMENTATION_PLAN.md`
- `C:/Users/terryzzb/Desktop/session-memory/EVALUATION.md`
- `C:/Users/terryzzb/Desktop/session-memory/projects/session-memory/control/active-objective.md`
- `C:/Users/terryzzb/Desktop/session-memory/projects/session-memory/control/pivot-log.md`
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
- The new control schema can still drift into prompt vocabulary if later
  implementation fails to ground it in concrete files and evidence.
- The evaluation protocol is still a biased pilot because the evaluator already
  knows the project context.

## Next Steps

1. Keep compressing assembled context so it acts like a handoff packet instead
   of a file dump.
2. Decide whether active constitution belongs in assembled context or should
   stay recall-only.
3. Run and record the first bootstrap control-vs-treatment experiment against
   live project state.
4. Add a first real workaround or validation-report sample only when a live
   implementation round creates one honestly.
