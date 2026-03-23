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
- Active round id: `round-2026-03-23-1711-govern-objective-close-adjudication-bundles`
- Phase: `execution`
- Workspace id: `ws-1490b759`
- Workspace root: `C:/Users/terryzzb/Desktop/session-memory`
- Branch: `master`
- HEAD anchor: `29a8c54cb9f1ec6a7b3854d33f509a8e05ed442d`
- Worktree state: `dirty`
- Changed path count: `13`
- Last anchor refresh: `2026-03-23T17:11:07+08:00`
- Phase-1 baseline already exists:
  - multi-project schema is documented
  - `wind-agent` is indexed as the first project sample
  - SQLite plus FTS5 build/query/assemble path is working
  - unified CLI and smoke command exist
- Control-system framing is now explicit:
  - durable docs define objective, pivot, and exception-contract as first-class objects
  - this project is the first real sample for hard pivot, soft pivot, and explicit objective close semantics
- Current work is focused on:
  - designing the next bounded adjudication bundle around governed objective-close paths
  - deciding whether `executor_followups` should remain serialized JSON strings or evolve into a richer structured contract
  - keeping the adjudication schema project-agnostic while broadening execution coverage

## Validated Facts

- The latest committed baseline is:
  - `543d211 Execute first adjudication follow-up slice`
- `uv run python scripts/session_memory.py smoke` passes on the current working tree after frontmatter `executor_followups` and the prose-only blocked boundary landed.
- `uv run python scripts/smoke_adjudication_followups.py` now passes with the first bounded multi-step bundle:
  - `round-close-chain`
  - `active -> validation_pending -> captured -> closed`
- `uv run python scripts/smoke_phase1.py` passes after the `round-close-chain` milestone landed.
- `uv run python scripts/session_memory.py smoke` passes after the `round-close-chain` milestone landed.
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
  - `projects/session-memory/memory/rounds/2026-03-23-1548-implement-remaining-objective-line-transitions.md`
- The objective-line slice now exists end to end:
  - `open-objective`
  - `close-objective`
  - `record-soft-pivot`
  - `record-hard-pivot`
- The round and exception-control slices remain live:
  - `open-round`
  - `update-round-status`
  - `activate-exception-contract`
  - `retire-exception-contract`
  - `invalidate-exception-contract`
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
  - reject close-objective when durable open rounds or active exception contracts still depend on the objective
  - reject soft-pivot when it would silently mutate objective shape under an open round without an explicit review path
- Explicit objective close is now a first-class honest state:
  - durable objective history may exist with zero active objectives
  - `control/active-objective.md` may be absent after explicit close or invalidation
  - `pivot-log.md` now projects an empty active lineage honestly instead of treating that state as corruption
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
- The former shared-transition-engine exception contract is now retired:
  - objective, round, exception, and hard-pivot commands now delegate shared
    write/projection/event work through `apply-transition-transaction`
- The shared transition-engine milestone round is now closed.
- Adjudication follow-up execution now has its first real durable rewrite slice:
  - adjudication frontmatter `executor_followups` can call bounded existing transition commands
  - current supported automatic execution covers:
    - `round-close-chain`
    - `update-round-status`
    - `retire-exception-contract`
    - `invalidate-exception-contract`
    - `close-objective`
  - `round-close-chain` is the first bounded multi-step executor bundle:
    - legal path today is `active -> validation_pending -> captured -> closed`
    - can resume from `validation_pending` or `captured`
    - still refuses unsupported statuses instead of guessing
  - structured round bootstrap can still open one successor round after those rewrites
- Disposable adjudication-followup fixture validation now exercises:
  - close a pre-adjudication round through a structured close chain
  - retire an active exception contract
  - open a successor round from adjudication bootstrap fields
  - block one prose-only follow-up instead of guessing a durable rewrite
  - finish with clean control audit
- The remaining objective-line round is now closed after validation.
- Disposable fixture validation now exercises:
  - `activate -> retire`
  - `activate -> invalidate`
  - exception-ledger projection and audit on a temporary project
- Disposable objective-line fixture validation now exercises:
  - open objective -> open round -> soft pivot with the same objective id
  - round closure before objective close
  - explicit objective close with zero active objectives and clean audit
- The first adjudication follow-up rewrite round is now closed after validation.
- The adjudication executor broadening round is now closed after validation.
- The adjudication rewrite-bundle round is now closed after full validation:
  - `round-2026-03-23-1649-expand-adjudication-rewrite-bundles`
- A successor round is now active to govern objective-close adjudication bundles:
  - `round-2026-03-23-1711-govern-objective-close-adjudication-bundles`

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
- `C:/Users/terryzzb/Desktop/session-memory/scripts/close_objective.py`
- `C:/Users/terryzzb/Desktop/session-memory/scripts/activate_exception_contract.py`
- `C:/Users/terryzzb/Desktop/session-memory/scripts/retire_exception_contract.py`
- `C:/Users/terryzzb/Desktop/session-memory/scripts/invalidate_exception_contract.py`
- `C:/Users/terryzzb/Desktop/session-memory/scripts/execute_adjudication_followups.py`
- `C:/Users/terryzzb/Desktop/session-memory/scripts/open_round.py`
- `C:/Users/terryzzb/Desktop/session-memory/scripts/open_objective.py`
- `C:/Users/terryzzb/Desktop/session-memory/scripts/prepare_role_eval_bundle.py`
- `C:/Users/terryzzb/Desktop/session-memory/scripts/record_hard_pivot.py`
- `C:/Users/terryzzb/Desktop/session-memory/scripts/record_soft_pivot.py`
- `C:/Users/terryzzb/Desktop/session-memory/scripts/reconcile_control_state.py`
- `C:/Users/terryzzb/Desktop/session-memory/scripts/round_control.py`
- `C:/Users/terryzzb/Desktop/session-memory/scripts/session_memory.py`
- `C:/Users/terryzzb/Desktop/session-memory/scripts/smoke_adjudication_followups.py`
- `C:/Users/terryzzb/Desktop/session-memory/scripts/smoke_exception_contracts.py`
- `C:/Users/terryzzb/Desktop/session-memory/scripts/smoke_objective_line.py`
- `C:/Users/terryzzb/Desktop/session-memory/scripts/smoke_phase1.py`
- `C:/Users/terryzzb/Desktop/session-memory/scripts/update_round_status.py`
- `C:/Users/terryzzb/Desktop/session-memory/projects/session-memory/control/exception-ledger.md`
- `C:/Users/terryzzb/Desktop/session-memory/projects/session-memory/memory/exception-contracts/2026-03-23-1524-transition-logic-remains-split-across-per-command-scripts.md`
- `C:/Users/terryzzb/Desktop/session-memory/scripts/smoke_transition_engine.py`
- `C:/Users/terryzzb/Desktop/session-memory/projects/session-memory/memory/decisions/2026-03-22-project-scoped-scope.md`
- `C:/Users/terryzzb/Desktop/session-memory/projects/session-memory/memory/decisions/2026-03-23-multi-project-workspace-aware-scope.md`

## Active Risks

- The current assembler still risks over-including repeated information when
  current-task and snapshot overlap.
- The new control schema can still drift into prompt vocabulary if later
  implementation fails to ground it in concrete files and evidence.
- The evaluation protocol is still a biased pilot because the evaluator already
  knows the project context.
- Adjudication follow-ups now execute a bounded structured subset, but they
  still cannot infer rewrites from verdict prose or handle broader multi-object
  rewrite plans automatically beyond the first bounded close-chain bundle.
- Phase transitions are still implicit in objective rewrites because `set-phase`
  does not exist yet as a first-class guarded command.

## Next Steps

1. Expand the adjudication executor beyond the first bounded close-chain bundle:
   define the next safe supported rewrite around governed objective-close
   paths without letting adjudication prose mutate durable truth.
2. Decide whether `executor_followups` should stay as serialized JSON payloads
   in frontmatter or evolve into a richer explicit contract shape.
3. Keep compressing assembled context so it acts like a handoff packet instead
   of a file dump.
4. Run the first serious external-target role-eval bundle for `wind-agent`.
5. Decide whether reviewer/orchestrator scoring should stay manual or gain
   partial automatic checks.
6. After the adjudication executor is broader, choose the next command gap:
   explicit phase transitions or reviewer/orchestrator automatic checks.
