# Current Task

## Goal

Turn `session-memory` into a stable phase-1 coding control system built on a
file-first memory substrate.

The immediate objective is:

- keep the design frozen around Markdown plus SQLite plus FTS5
- add first-class control-state files for objective, pivot, and exception-contract
- improve fresh-session context assembly quality
- compile handoff through active objective state instead of recency alone

## Current State

- Project: `session-memory`
- Objective id: `obj-2026-03-23-0002`
- Active round id: `round-2026-03-23-1530-extract-shared-transition-engine-primitive`
- Phase: `execution`
- Workspace id: `ws-1490b759`
- Workspace root: `C:/Users/terryzzb/Desktop/session-memory`
- Branch: `master`
- HEAD anchor: `72ab90077f2b18968f6deecc11f8215c1f220aa8`
- Phase-1 baseline already exists:
  - multi-project schema is documented
  - `wind-agent` is indexed as the first project sample
  - SQLite plus FTS5 build/query/assemble path is working
  - unified CLI and smoke command exist
- Control-system framing is now explicit:
  - durable docs define objective, pivot, and exception-contract as first-class objects
  - this project is the first real sample for a hard pivot in objective line
- Current work is focused on:
  - extracting one shared transition-engine primitive from the duplicated command implementations
  - shrinking the active exception contract around split transition logic instead of leaving it as standing debt
  - keeping objective, round, and exception-command regressions visible while shared ownership is introduced

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
  - exception ledger when present
- `compile_role_context.py` now exists for:
  - reviewer
  - architect
  - orchestrator
- Constitution routing is now explicit:
  - excluded from the default handoff packet
  - included in role-specific compiled contexts
- Role-context compilation also degrades cleanly on `wind-agent`:
  - no `control/` directory required
  - current-task, blockers, snapshot, and durable memory still compile
- `prepare_role_eval_bundle.py` now prepares frozen role-eval bundles with:
  - snapshot
  - task
  - role-context
  - score template
  - run config
- The first external-target reviewer bundle was prepared successfully for
  `wind-agent`.
- `STATE_MACHINE.md` now makes the design explicit:
  - current system is state-machine oriented
  - current system is partially state-machine enforced
- `TRANSITION_COMMANDS.md` now freezes:
  - canonical transition names
  - guards
  - side effects
  - primary write targets
- The project now has durable round history across multiple real control slices:
  - `projects/session-memory/memory/rounds/2026-03-23-1213-implement-first-transition-slice.md`
  - `projects/session-memory/memory/rounds/2026-03-23-1516-implement-exception-contract-transition-slice.md`
  - `projects/session-memory/memory/rounds/2026-03-23-1530-extract-shared-transition-engine-primitive.md`
- The first enforced transition slice now exists:
  - `open-objective`
  - `record-hard-pivot`
  - `open-round`
  - `update-round-status`
- `wind-agent` now has a real control substrate as a second project sample:
  - `control/active-objective.md`
  - `control/pivot-log.md`
  - durable objective and pivot records
- The first non-self-hosted objective-line lifecycle has been exercised:
  - initial active objective opened on `wind-agent`
  - guarded hard pivot recorded on `wind-agent`
- Hard pivots now have one explicit honesty guard:
  - reject pivot when an active round is still tied to the previous objective
- Objective-line guards are now anchored to durable truth, not only control files:
  - reject opening a second active objective from orphaned durable state
  - reject hard pivot when durable still-open rounds remain on the old objective
- Control projection repair now exists:
  - `reconcile-control-state`
  - rebuilds `active-objective.md`, `pivot-log.md`, and `active-round.md` from durable truth
- Real repair validation has been exercised:
  - deleted `session-memory/control/active-round.md` and restored it from durable round state
  - deleted `wind-agent/control/active-objective.md` and restored it from durable objective state
- The first real round lifecycle has been exercised:
  - `active -> validation_pending -> captured -> closed`
  - successor round opened with transition-event records
- The round rewrite path has now been re-validated on the active round:
  - `active -> blocked -> active`
  - frontmatter fidelity survived the rewrite
- Exception-contract control now has a real enforced slice:
  - `activate-exception-contract`
  - `retire-exception-contract`
  - `invalidate-exception-contract`
- Exception-contract commands now project `control/exception-ledger.md` from
  durable truth instead of leaving the ledger as a manually maintained stub.
- A real active exception contract now exists for `session-memory`:
  - transition logic remains split across per-command scripts until a shared
    transition engine exists
- The exception-contract milestone round is now closed and a successor round is
  active for shared transition-engine extraction.
- Disposable fixture validation now exercises:
  - `activate -> retire`
  - `activate -> invalidate`
  - exception-ledger projection and audit on a temporary project

## Important Files

- `C:/Users/terryzzb/Desktop/session-memory/DESIGN_PRINCIPLES.md`
- `C:/Users/terryzzb/Desktop/session-memory/ARCHITECTURE.md`
- `C:/Users/terryzzb/Desktop/session-memory/CONTROL_SYSTEM.md`
- `C:/Users/terryzzb/Desktop/session-memory/STATE_MACHINE.md`
- `C:/Users/terryzzb/Desktop/session-memory/TRANSITION_COMMANDS.md`
- `C:/Users/terryzzb/Desktop/session-memory/SCHEMA.md`
- `C:/Users/terryzzb/Desktop/session-memory/IMPLEMENTATION_PLAN.md`
- `C:/Users/terryzzb/Desktop/session-memory/EVALUATION.md`
- `C:/Users/terryzzb/Desktop/session-memory/ROLE_CONTEXT_EVALUATION.md`
- `C:/Users/terryzzb/Desktop/session-memory/projects/session-memory/control/active-objective.md`
- `C:/Users/terryzzb/Desktop/session-memory/projects/session-memory/control/active-round.md`
- `C:/Users/terryzzb/Desktop/session-memory/projects/session-memory/control/pivot-log.md`
- `C:/Users/terryzzb/Desktop/session-memory/scripts/build_index.py`
- `C:/Users/terryzzb/Desktop/session-memory/scripts/query_index.py`
- `C:/Users/terryzzb/Desktop/session-memory/scripts/assemble_context.py`
- `C:/Users/terryzzb/Desktop/session-memory/scripts/compile_role_context.py`
- `C:/Users/terryzzb/Desktop/session-memory/scripts/activate_exception_contract.py`
- `C:/Users/terryzzb/Desktop/session-memory/scripts/retire_exception_contract.py`
- `C:/Users/terryzzb/Desktop/session-memory/scripts/invalidate_exception_contract.py`
- `C:/Users/terryzzb/Desktop/session-memory/scripts/open_round.py`
- `C:/Users/terryzzb/Desktop/session-memory/scripts/open_objective.py`
- `C:/Users/terryzzb/Desktop/session-memory/scripts/prepare_role_eval_bundle.py`
- `C:/Users/terryzzb/Desktop/session-memory/scripts/record_hard_pivot.py`
- `C:/Users/terryzzb/Desktop/session-memory/scripts/reconcile_control_state.py`
- `C:/Users/terryzzb/Desktop/session-memory/scripts/round_control.py`
- `C:/Users/terryzzb/Desktop/session-memory/scripts/session_memory.py`
- `C:/Users/terryzzb/Desktop/session-memory/scripts/smoke_exception_contracts.py`
- `C:/Users/terryzzb/Desktop/session-memory/scripts/smoke_phase1.py`
- `C:/Users/terryzzb/Desktop/session-memory/scripts/update_round_status.py`
- `C:/Users/terryzzb/Desktop/session-memory/projects/session-memory/control/exception-ledger.md`
- `C:/Users/terryzzb/Desktop/session-memory/projects/session-memory/memory/exception-contracts/2026-03-23-1524-transition-logic-remains-split-across-per-command-scripts.md`
- `C:/Users/terryzzb/Desktop/session-memory/projects/session-memory/memory/decisions/2026-03-22-project-scoped-scope.md`
- `C:/Users/terryzzb/Desktop/session-memory/projects/session-memory/memory/decisions/2026-03-23-multi-project-workspace-aware-scope.md`

## Active Risks

- The current assembler still risks over-including repeated information when
  current-task and snapshot overlap.
- The new control schema can still drift into prompt vocabulary if later
  implementation fails to ground it in concrete files and evidence.
- The evaluation protocol is still a biased pilot because the evaluator already
  knows the project context.
- The shared transition engine still does not exist yet, so transition logic is
  intentionally duplicated across command scripts under one explicit exception
  contract.

## Next Steps

1. Keep compressing assembled context so it acts like a handoff packet instead
   of a file dump.
2. Run the first serious external-target role-eval bundle for `wind-agent`.
3. Extract the shared transition engine.
   Pull the duplicated file-write and transition-event responsibilities out of
   objective, round, and exception commands into one owner-layer primitive.
4. Decide whether reviewer/orchestrator scoring should stay manual or gain
   partial automatic checks.
5. Run and record the first bootstrap control-vs-treatment experiment against
   live project state.
6. Reassess the active exception contract after the shared engine lands.
   Retire it only if duplicated transition ownership is materially reduced for
   the command families it currently covers.
