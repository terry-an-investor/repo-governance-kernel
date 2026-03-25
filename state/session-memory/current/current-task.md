# Current Task

## Goal

Turn `session-memory` into a stable phase-1 memory-driven repo governance
control plane built on a file-first memory substrate.

The immediate objective is:

- keep the design frozen around Markdown plus SQLite plus FTS5
- add first-class control-state files for objective, pivot, and exception-contract
- improve fresh-session context assembly quality
- compile handoff through active objective state instead of recency alone

## Current State

- Project: `session-memory`
- Objective id: `obj-2026-03-23-0002`
- Active round id: `round-2026-03-25-1348-add-release-publication-verifier-and-checklist`
- Phase: `execution`
- Workspace id: `ws-1490b759`
- Workspace root: `C:/Users/terryzzb/Desktop/session-memory`
- Phase-1 baseline already exists:
  - multi-project schema is documented
  - `wind-agent` is indexed as the first project sample
  - SQLite plus FTS5 build/query/assemble path is working
  - unified CLI and smoke command exist
- Control-system framing is now explicit:
  - durable docs define objective, pivot, and exception-contract as first-class objects
  - this project is the first real sample for hard pivot, soft pivot, and explicit objective close semantics
- Current work is focused on:
  - turning task-contract from a static durable object into a bounded lifecycle with explicit rewrite and status transitions
  - making assembled and role-specific contexts consume active task contracts instead of leaving the layer invisible
  - tightening round and objective honesty rules so active task contracts cannot be stranded across closure or pivot

## Validated Facts

- This round started from committed baseline:
  - `9740ecd Start M3 rewrite semantics unification`
- `PRODUCT.md` is now being introduced as the canonical product truth source
  for:
  - target users
  - product promise
  - capability boundaries
  - the product-to-machine-semantics path
- `uv run python scripts/session_memory.py smoke` passes on the current working tree after frontmatter `executor_followups` and the prose-only blocked boundary landed.
- `uv run python scripts/smoke_adjudication_followups.py` now passes with the first bounded multi-step bundle:
  - `round-close-chain`
  - `active -> validation_pending -> captured -> closed`
- `uv run python scripts/smoke_adjudication_followups.py` now also proves bounded exception-contract plan compilation:
  - retire one invalidated exception contract from adjudication durable truth
  - invalidate one invalidated exception contract from adjudication durable truth
  - keep one prose-only exception follow-up blocked instead of guessing a durable rewrite
- `uv run python scripts/smoke_adjudication_followups.py` now also proves bounded phase-side-effect compilation:
  - enter `execution` for one exploration objective through an adjudication plan contract
  - auto-open one bounded round from adjudication durable `round_*` bootstrap fields
- `uv run python scripts/smoke_adjudication_followups.py` now also proves bounded phase fallback compilation:
  - leave `execution` for `paused` through an adjudication plan contract
  - rewrite the still-open round through the same governed `set-phase` primitive
  - keep compile/execute on registry-declared `set-phase` payload semantics instead of a phase-local private executor branch
- `uv run python scripts/smoke_adjudication_followups.py` now also proves bounded hard-pivot replacement compilation:
  - compile one governed `round-close-chain-then-hard-pivot` payload from adjudication durable truth
  - close one blocked predecessor round before recording the hard pivot
  - leave the previous objective superseded and the successor objective active through the same bounded bundle family
- `uv run python scripts/smoke_adjudication_followups.py` now also proves bounded objective rewrite compilation:
  - compile one adjudication objective rewrite plan into `record-soft-pivot`
  - preserve objective identity while rewriting the active objective line
  - rewrite one still-open round through the same soft-pivot command so round and objective truth stay aligned
- `uv run python scripts/run_smoke_suite.py --list` now prints the canonical disposable smoke manifest:
  - registered smoke names
  - owned fixture project ids
  - parallel-safety flags
  - shared resource declarations
- `uv run python scripts/run_smoke_suite.py --smoke adjudication_followups --smoke phase_scope_controls` now passes under one suite runner:
  - serial execution replaces ad hoc parallel invocation
  - fixture leak checks run before and after each smoke
- `uv run python scripts/list_transition_registry.py` now exports the canonical machine-readable transition registry:
  - transition command names
  - command domains
  - implementation status
  - required inputs
  - guard codes
  - guard rendering semantics
  - write-target semantics
  - write targets
  - side-effect codes
  - transition-command side-effect semantics
  - bounded command mutable-field semantics for governed rewrite primitives
  - executor-supported commands
  - bounded adjudication plan family names
  - adjudication target-resolution semantics
  - adjudication binding-resolver semantics
  - adjudication plan side-effect semantics
- `uv run python scripts/audit_control_state.py --project-id session-memory` now checks registry name coverage and semantic coverage against `TRANSITION_COMMANDS.md`
- `uv run python scripts/audit_control_state.py --project-id session-memory` now also checks round-domain registry consumer coverage against the shared owner-layer helper
- `uv run python scripts/audit_control_state.py --project-id session-memory` now also treats bundle-consumer coverage as a registry concern:
  - bundle route states and step templates are audited from `transition_specs.py`
  - audit no longer depends on bundle handler names exported from the executor implementation
- adjudication plan compilation no longer resolves plan payload bindings through one local `if/elif` ladder:
  - binding resolvers are now explicit registry-owned semantics
  - plan target-resolution names are now explicit registry-owned semantics
  - plan side-effect names are now explicit registry-owned semantics instead of unchecked free strings
- compile and execute now also share one resolver runtime layer:
  - `kernel/resolver_runtime.py` now owns the bounded round / task-contract / exception-contract target resolution helpers
  - bundle `state_resolver` names are now declared in `kernel/transition_specs.py` and consumed at runtime
  - adjudication `plan_spec.target_resolution` is now an explicit runtime gate instead of a doc-only registry field
  - close-capable round target resolution and hard-pivot bundle state resolution now also live in the same shared runtime instead of bundle-local branching
- round-domain commands now consume one shared registry-backed owner-layer helper for:
  - guard coverage
  - guard rendering semantics
  - transition-command side-effect semantics
  - write-target coverage
  - transition-event expectations
- `rewrite-open-round` mutable field declarations are now being lifted into the registry so:
  - the rewrite script consumes one registry-owned field surface
  - adjudication rewrite execution can reject undeclared private payload keys
- supported automatic executor commands now also have a first registry-owned
  payload-field surface for:
  - payload key admission
  - CLI flag binding
  - required runtime executor fields
- command contract assertions and executor-surface validation now share one
  runtime-input alias layer for command-facing pluralization differences such as:
  - `success_criterion` / `success_criteria`
  - `non_goal` / `non_goals`
  - `allowed_change` / `allowed_changes`
  - `forbidden_change` / `forbidden_changes`
  - `completion_criterion` / `completion_criteria`
  - `path` / `paths`
- mutable rewrite executor command-building now also flows through one shared
  repo-owned builder:
  - `rewrite-open-round`
  - `rewrite-open-task-contract`
  - `record-soft-pivot` executor payloads now ride the same owner-layer surface
- `open-round` is now also on the executor-supported shared payload surface:
  - registry-owned executor payload fields now cover bounded round bootstrap inputs too
  - nested phase/bootstrap and soft-pivot follow-up consumers no longer need one private round-open CLI builder branch
- nested command execution now also has one shared runtime layer:
  - adjudication follow-up execution
  - `set-phase` auto-open / rewrite-open-round follow-ups
  - `record-soft-pivot` bounded round rewrite follow-up
- `round-close-chain` bundle execution now also consumes the same shared
  registry/runtime path:
  - the bundle now composes registry payloads for `update-round-status` instead
    of hand-building nested script CLIs
  - executor smoke now proves `update-round-status` through
    `kernel/executor_runtime.py` with explicit registry-owned payload fields
- governed bundle step-selection semantics are now also registry-owned:
  - bundle route states are declared in `kernel/transition_specs.py`
  - bundle step templates are declared in `kernel/transition_specs.py`
  - `scripts/execute_adjudication_followups.py` now runs one generic governed-bundle engine instead of one private handler per bundle
  - governed bundle steps can now also compose other governed bundles through the same owner-layer execution path instead of falling back to private nested orchestration
- the reusable unified CLI now exists at:
  - `uv run python -m kernel.cli ...`
  - `scripts/session_memory.py` now behaves as a host-repo adapter that forwards generic kernel commands and keeps repo-local smoke/eval commands local
- kernel release preparation is now in progress:
  - package target is `repo-governance-kernel`
  - current intended release level is `0.1.0a0` alpha
  - `state/session-memory/` is now treated as dogfood/example evidence rather than the product center
- more already-implemented primitive commands now also declare executor payload semantics:
  - `open-objective`
  - `record-hard-pivot`
  - `open-task-contract`
  - `activate-exception-contract`
- bundle wrapper admission is now being pulled into one explicit governance
  surface so executor and plan validation stop carrying hidden bundle exception
  literals
- executor bundle consumption now flows through one generic governed-bundle
  engine so adding a bundle requires registry route/step semantics instead of a
  new private handler branch
- A deliberate protocol violation now fails honestly:
  - running one disposable adjudication smoke while `smoke_phase1.py` tries to start the suite causes `fixture_leak_before_run`
  - this is now a visible harness-protocol failure instead of a silent flaky test
- `uv run python scripts/smoke_phase1.py` passes after the `round-close-chain` milestone landed.
- `uv run python scripts/session_memory.py smoke` passes after the `round-close-chain` milestone landed.
- The governed objective-close bundle round was abandoned before implementation:
  - `round-2026-03-23-1711-govern-objective-close-adjudication-bundles`
- The first automatic enforcement milestone is now closed:
  - `round-2026-03-23-1732-implement-automatic-code-control-enforcement-gates`
- A successor enforcement round is now active:
  - `round-2026-03-23-1814-broaden-enforcement-coverage-beyond-first-worktree-gate`
- Current index baseline before adding this project sample was:
  - `memory_items = 6`
  - `memory_paths = 17`
  - `memory_evidence_refs = 8`
  - `memory_fts = 6`
- The first real linked-memory pair now exists in `state/session-memory/`.
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
- Repository-local automatic enforcement now exists:
  - `scripts/control_enforcement.py` is the owner-layer enforcement primitive
  - `scripts/enforce_worktree.py` exposes the same checks as a CLI gate
  - `scripts/install_hooks.py` installs `.githooks/` through `git config core.hooksPath`
  - `.githooks/pre-commit` runs worktree enforcement before commit
  - `.githooks/pre-push` runs worktree enforcement plus control-state audit before push
  - `.github/workflows/control-enforcement.yml` reuses the same owner-layer commands in CI
- Automatic enforcement now has a second real blocked-state class:
  - constitution-declared guarded exception paths can be marked as temporary-deviation zones
  - dirty paths inside those zones are blocked unless one active exception contract explicitly covers them
  - the path matching is now workspace-aware instead of assuming the repo root is always the project workspace
- Round promotion is now partially punitive instead of advisory:
  - `update_round_status.py` blocks `captured` and `closed` when worktree enforcement fails
  - enforcement can validate against an explicit `round_id`, so honest `captured -> closed` still works after the active round is projected away
- The first enforcement slice has been validated on the real project:
  - `uv run python scripts/enforce_worktree.py --project-id session-memory` passed after round scope was corrected to include `AGENTS.md` and `.githooks/`
  - `uv run python scripts/audit_control_state.py --project-id session-memory` passed on the enforced control state
  - round transition gating was exercised across:
    - `active -> validation_pending`
    - `validation_pending -> captured`
    - `captured -> closed`
- Disposable guarded-exception fixture validation now exercises:
  - blocked enforcement when one guarded dirty path exists without any active exception contract
  - allowed enforcement once one active exception contract explicitly covers the same guarded path
  - `validation_pending -> captured -> closed` while the covering contract remains active
  - retirement of the covering contract after round closure
  - guarded-path cleanup and explicit phase fallback so final audit ends `ok`
- The project now has durable round history across multiple real control slices:
  - `state/session-memory/memory/rounds/2026-03-23-1213-implement-first-transition-slice.md`
  - `state/session-memory/memory/rounds/2026-03-23-1516-implement-exception-contract-transition-slice.md`
  - `state/session-memory/memory/rounds/2026-03-23-1530-extract-shared-transition-engine-primitive.md`
  - `state/session-memory/memory/rounds/2026-03-23-1548-implement-remaining-objective-line-transitions.md`
- The objective-line slice now exists end to end:
  - `open-objective`
  - `close-objective`
  - `record-soft-pivot`
  - `record-hard-pivot`
- The round and exception-control slices remain live:
  - `open-round`
  - `refresh-round-scope`
  - `rewrite-open-round`
  - `update-round-status`
  - `activate-exception-contract`
  - `retire-exception-contract`
  - `invalidate-exception-contract`
- Explicit phase control now exists:
  - `set-phase`
  - entering `execution` can bootstrap one bounded round in the same guarded transition
  - leaving `execution` requires explicit review notes when open rounds still exist
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
  - adjudication frontmatter can now carry bounded higher-level `executor_plan_contracts`
    that the repo compiler expands into explicit executor payloads
  - adjudication frontmatter `executor_followups` can call bounded existing transition commands
  - bounded exception-contract plans can now compile directly from adjudication
    `Objects Invalidated` instead of requiring one hand-authored low-level
    exception payload per contract
  - bounded phase-side-effect plans can now compile `set-phase --auto-open-round`
    from adjudication durable `round_*` bootstrap fields
  - current supported automatic execution covers:
    - `round-close-chain`
    - `refresh-round-scope`
    - `rewrite-open-round`
    - `set-phase`
    - `update-round-status`
    - `retire-exception-contract`
    - `invalidate-exception-contract`
    - `close-objective`
  - `rewrite-open-round` is now the owner-layer primitive for durable round-contract mutation without changing round identity
  - `compile-adjudication-executor-plan` now exists as the repo-owned compiler for bounded adjudication plan contracts
  - `round-close-chain` is the first bounded multi-step executor bundle:
    - legal path today is `active -> validation_pending -> captured -> closed`
    - can resume from `validation_pending` or `captured`
    - still refuses unsupported statuses instead of guessing
  - structured round bootstrap can still open one successor round after those rewrites
- Disposable adjudication-followup fixture validation now exercises:
  - compile a bounded adjudication rewrite plan contract into explicit executor followups
  - rewrite a predecessor round through the compiled adjudication plan before closure
  - close a pre-adjudication round through a structured close chain
  - retire an active exception contract through a bounded exception plan contract
  - invalidate an active exception contract through a bounded exception plan contract
  - enter execution and open one bounded round through a bounded phase-side-effect plan contract
  - leave execution and rewrite one still-open round through a bounded phase fallback plan contract
  - close one blocked predecessor round and then record one hard pivot through a bounded replacement bundle plan contract
  - open a successor round from adjudication bootstrap fields
  - block one prose-only follow-up instead of guessing a durable rewrite
  - finish with clean control audit
- The remaining objective-line round is now closed after validation.
- Disposable fixture validation now exercises:
  - `activate -> retire`
  - `activate -> invalidate`
  - exception-ledger projection and audit on a temporary project
- Disposable objective-line fixture validation now exercises:
  - open objective -> set phase into execution with auto-opened round -> soft pivot with the same objective id plus durable open-round rewrite
  - round closure before objective close
  - explicit objective close with zero active objectives and clean audit
- Disposable phase/scope-control fixture validation now exercises:
  - `set-phase --auto-open-round`
  - blocked enforcement when one dirty source path remains outside round scope
  - `refresh-round-scope` rewriting durable round `paths`
  - clean enforcement and audit after scope refresh
- The active real-project round has now been durably rewritten in place:
  - same round id retained
  - round title, summary, scope, deliverable, and validation plan updated through `rewrite-open-round`
  - sample control files now track the machine-readable transition-registry milestone instead of the earlier harness-law milestone
- The first adjudication follow-up rewrite round is now closed after validation.
- The adjudication executor broadening round is now closed after validation.
- The adjudication rewrite-bundle round is now closed after full validation:
  - `round-2026-03-23-1649-expand-adjudication-rewrite-bundles`
- The objective-close bundle governance round was explicitly abandoned:
  - `round-2026-03-23-1711-govern-objective-close-adjudication-bundles`

## Important Files

- `C:/Users/terryzzb/Desktop/session-memory/docs/canonical/DESIGN_PRINCIPLES.md`
- `C:/Users/terryzzb/Desktop/session-memory/docs/canonical/ARCHITECTURE.md`
- `C:/Users/terryzzb/Desktop/session-memory/docs/canonical/CONTROL_SYSTEM.md`
- `C:/Users/terryzzb/Desktop/session-memory/docs/canonical/STATE_MACHINE.md`
- `C:/Users/terryzzb/Desktop/session-memory/docs/canonical/TRANSITION_COMMANDS.md`
- `C:/Users/terryzzb/Desktop/session-memory/docs/canonical/SCHEMA.md`
- `C:/Users/terryzzb/Desktop/session-memory/docs/canonical/IMPLEMENTATION_PLAN.md`
- `C:/Users/terryzzb/Desktop/session-memory/docs/evaluation/EVALUATION.md`
- `C:/Users/terryzzb/Desktop/session-memory/docs/evaluation/ROLE_CONTEXT_EVALUATION.md`
- `C:/Users/terryzzb/Desktop/session-memory/state/session-memory/control/active-objective.md`
- `C:/Users/terryzzb/Desktop/session-memory/state/session-memory/control/active-round.md`
- `C:/Users/terryzzb/Desktop/session-memory/state/session-memory/control/pivot-log.md`
- `C:/Users/terryzzb/Desktop/session-memory/kernel/build_index.py`
- `C:/Users/terryzzb/Desktop/session-memory/scripts/query_index.py`
- `C:/Users/terryzzb/Desktop/session-memory/kernel/assemble_context.py`
- `C:/Users/terryzzb/Desktop/session-memory/scripts/compile_role_context.py`
- `C:/Users/terryzzb/Desktop/session-memory/scripts/compile_adjudication_executor_plan.py`
- `C:/Users/terryzzb/Desktop/session-memory/scripts/close_objective.py`
- `C:/Users/terryzzb/Desktop/session-memory/scripts/activate_exception_contract.py`
- `C:/Users/terryzzb/Desktop/session-memory/scripts/retire_exception_contract.py`
- `C:/Users/terryzzb/Desktop/session-memory/scripts/invalidate_exception_contract.py`
- `C:/Users/terryzzb/Desktop/session-memory/scripts/execute_adjudication_followups.py`
- `C:/Users/terryzzb/Desktop/session-memory/scripts/open_round.py`
- `C:/Users/terryzzb/Desktop/session-memory/scripts/open_objective.py`
- `C:/Users/terryzzb/Desktop/session-memory/scripts/prepare_role_eval_bundle.py`
- `C:/Users/terryzzb/Desktop/session-memory/scripts/refresh_round_scope.py`
- `C:/Users/terryzzb/Desktop/session-memory/scripts/record_hard_pivot.py`
- `C:/Users/terryzzb/Desktop/session-memory/scripts/record_soft_pivot.py`
- `C:/Users/terryzzb/Desktop/session-memory/scripts/reconcile_control_state.py`
- `C:/Users/terryzzb/Desktop/session-memory/scripts/rewrite_open_round.py`
- `C:/Users/terryzzb/Desktop/session-memory/kernel/round_control.py`
- `C:/Users/terryzzb/Desktop/session-memory/scripts/session_memory.py`
- `C:/Users/terryzzb/Desktop/session-memory/scripts/smoke_adjudication_followups.py`
- `C:/Users/terryzzb/Desktop/session-memory/scripts/smoke_exception_contracts.py`
- `C:/Users/terryzzb/Desktop/session-memory/scripts/smoke_objective_line.py`
- `C:/Users/terryzzb/Desktop/session-memory/scripts/smoke_phase1.py`
- `C:/Users/terryzzb/Desktop/session-memory/scripts/smoke_phase_scope_controls.py`
- `C:/Users/terryzzb/Desktop/session-memory/scripts/set_phase.py`
- `C:/Users/terryzzb/Desktop/session-memory/scripts/update_round_status.py`
- `C:/Users/terryzzb/Desktop/session-memory/state/session-memory/control/exception-ledger.md`
- `C:/Users/terryzzb/Desktop/session-memory/state/session-memory/memory/exception-contracts/2026-03-23-1524-transition-logic-remains-split-across-per-command-scripts.md`
- `C:/Users/terryzzb/Desktop/session-memory/scripts/smoke_transition_engine.py`
- `C:/Users/terryzzb/Desktop/session-memory/state/session-memory/memory/decisions/2026-03-22-project-scoped-scope.md`
- `C:/Users/terryzzb/Desktop/session-memory/state/session-memory/memory/decisions/2026-03-23-multi-project-workspace-aware-scope.md`

## Active Risks

- The current assembler still risks over-including repeated information when
  current-task and snapshot overlap.
- The new control schema can still drift into prompt vocabulary if later
  implementation fails to ground it in concrete files and evidence.
- The evaluation protocol is still a biased pilot because the evaluator already
  knows the project context.
- Adjudication follow-ups now execute a bounded structured subset, but they
  still cannot infer rewrites from verdict prose or handle broader multi-object
  rewrite plans automatically beyond explicit bounded command contracts.
- The new adjudication compiler will still be narrow at first:
  - only supported bounded plan types should compile
  - broader multi-object verdict execution still remains outside the safe automatic subset
- Exception-contract plan resolution is now more capable, but it still assumes
  one adjudication object set maps deterministically to a bounded set of active
  exception contracts; broader mixed-object verdict plans still need clearer
  contracts before they should compile automatically.
- Phase-side-effect planning now compiles execution bootstrap honestly, but it
  now also covers bounded execution fallback with open-round rewrite, while
  hard-pivot replacement now has one bounded predecessor-round close-chain path;
  broader multi-round replacement bundles still remain outside the bounded
  automatic subset.
- The new harness law now governs disposable fixture project leakage, but it
  still only checks declared fixture paths; richer contamination classes such as
  shared artifact collisions or index reuse policy remain outside the current suite runner.
- The transition registry now owns guards, write targets, side effects, and the
  first bounded rewrite-field semantics, but broader field-level mutation
  semantics and multi-object rewrite contracts still remain outside the current
  machine-readable owner layer.
- The compiler/executor boundary can still drift if future changes let in-place
  compilation overwrite explicit payloads, admit undeclared command-specific
  keys, or execute the same payload twice.
- broader bundle payload semantics are still intentionally narrow:
  - the repo now governs wrapper admission explicitly
  - but bundle route/state semantics should not expand casually while this
    governance layer is still settling
- Product positioning can still drift if canonical docs slide back into
  describing the repo as only a memory substrate, only a control system, or an
  overclaimed autonomous rewrite product.
- Automatic enforcement is still only partially implemented:
  - owner-layer enforcement now covers scope drift, projection drift, and guarded exception-path dishonesty, but broader abusive change classes still need explicit durable law instead of heuristics
  - round scope refresh, bounded phase fallback, and one bounded hard-pivot replacement bundle now exist, but broader multi-round replacement still is not automatic
- Phase transitions are now explicit, but phase-side effects are still conservative:
  - the system records review notes, optional bootstrap, and bounded round rewrites, but it still does not auto-close or auto-re-scope open rounds without explicit rewrite inputs

## Next Steps

1. Land `PRODUCT.md` as the canonical product truth source and align the major
   docs to the same product positioning.
2. Add an explicit audit path so product docs and machine-semantic docs stop
   drifting silently.
3. Continue broadening bounded plan and bundle families only where the
   underlying command semantics are already registry-owned and auditable.
4. Register the next bounded family around broader multi-object adjudication
   surfaces without introducing private bundle semantics.
5. Decide which additional resolver families deserve first-class machine
   semantics before expanding beyond one predecessor-round replacement path.
6. Validate the product on more non-self-hosted repositories after the product
   positioning and owner-layer contracts stabilize.