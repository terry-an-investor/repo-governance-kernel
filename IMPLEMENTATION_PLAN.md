# Session Memory Implementation Plan

Date: 2026-03-22
Scope: Phase-1 implementation of the memory-driven repo governance control plane

## Goal

Implement the smallest honest retrieval and control loop for the
memory-driven repo governance control plane defined in [`PRODUCT.md`](./PRODUCT.md):

- Markdown files remain the source of truth
- SQLite is the local index store
- FTS5 is the phase-1 full-text engine
- retrieval stays structure-first, then FTS5
- control state stays file-first before automation expands

Product prose is not executable authority. Machine semantics should keep
flowing through explicit registries, audits, and transition contracts.

This phase is now partially state-machine enforced.

Its automation target remains bounded automatic execution.
It is not a general autonomous rewrite engine.

Today that enforcement is intentionally narrow:

- the objective-line domain can open a first active objective
- the objective-line domain can record a guarded hard pivot
- the round domain has real transition commands
- the repo is introducing a first task-contract owner layer under round governance
- illegal round-status transitions are rejected
- transition events are recorded as durable files
- control projections can be rebuilt from durable truth when the state is
  unambiguous
- one audit path can now report control dishonesty without mutating state

It is not yet a unified transition engine across every domain.
It now includes a bounded adjudication executor subset, but not a general
autonomous rewrite engine after a verdict is recorded.

## Phase 1 In Scope

- establish canonical control objects in files:
  - constitution
  - active objective
  - pivot log
  - exception ledger
- add a first file-first task-contract object model beneath active round governance
- add bounded task-contract lifecycle and context-consumption paths so the new
  owner layer is not only durable but also operable
- index Markdown memory files under `projects/` and `cross-project/`
- populate SQLite metadata tables
- populate one FTS5 table for recall
- support structured filters:
  - `project_id`
  - `workspace_id`
  - `type`
  - `path`
- support FTS5 text recall after structured narrowing
- assemble one fresh-session context packet from canonical files plus durable
  memory
- ensure assembled context compiles through active objective and freshness
  signals rather than raw recency alone
- add role-context compilation so reviewer / architect / orchestrator can read
  project control state instead of relying on prompt text alone
- add frozen role-eval bundle preparation so role-context quality can be judged
  with a fixed rubric instead of prose preference

## Phase 1 Out Of Scope

- DuckDB
- embeddings
- reranking
- automatic transcript extraction
- graph reasoning
- generalized memory ontology expansion
- automatic pivot detection beyond explicit operator-authored records
- unified transition engine with enforced guards and side effects
- task-contract-driven automatic rewrite from prose alone

## Current Implementation Gaps

### Control files

- add canonical project-agnostic control files under `projects/<project_id>/control/`
- make `assemble` read active objective and exception-contract state
- keep pivot handling explicit before any automation tries to infer it
- introduce task contracts as a repo-owned lower owner layer before claiming
  broader task-level rewrite semantics
- keep constitution out of the default handoff packet unless later evidence
  proves that always inlining it helps more than it bloats
- compile constitution into role-specific contexts instead
- define the future transition command surface before implementing enforcement
- first objective/pivot transition slice is now real:
  - `open-objective`
  - `record-hard-pivot`
  - only one durable active objective is allowed at a time
  - hard pivots now scan durable rounds and refuse to outrun still-open work tied to the old objective
- first round transition slice is now real:
  - `open-round`
  - `update-round-status`
  - rewrite path now preserves round metadata instead of degrading frontmatter
- repair support now exists:
  - `reconcile-control-state`
  - rebuilds control files from durable objective, pivot, and round records
  - refuses ambiguous durable state instead of guessing
- audit support now exists:
  - `audit-control-state`
  - reports projection drift, execution-without-round, and other control honesty
    failures
- first adjudication support now exists:
  - `adjudicate-control-state`
  - records durable adjudication verdicts from the live audit result
  - records bounded machine-readable plan contracts and explicit executor
    followups for the safe automatic subset
- first adjudication follow-up executor now exists:
  - `execute-adjudication-followups`
  - can scaffold safe missing control surfaces
  - can compile bounded objective rewrite, task-contract rewrite/status,
    round-close, exception-contract, and phase-bootstrap plan families from
    adjudication durable truth
  - can also compile bounded phase fallback plans that leave `execution`
    through the existing `set-phase` primitive while rewriting open-round
    contracts through declared owner-layer payload semantics
  - can also compile one bounded hard-pivot replacement plan that closes one
    predecessor round through governed bundle semantics before recording the
    hard pivot through the existing objective primitive
  - now treats plan target-resolution names, binding resolvers, and plan
    side-effect names as explicit registry-owned machine semantics
  - now routes mutable rewrite executor commands through one shared
    registry-backed builder foundation instead of keeping one private rewrite
    builder branch per command
  - now routes bounded round bootstrap/open-round executor payloads through the
    same shared registry-backed builder instead of phase-local CLI assembly
  - now routes nested command execution through one shared executor runtime
    helper instead of repeating per-caller subprocess/json handling
  - now routes `round-close-chain` bundle execution through registry-built
    `update-round-status` payloads on that same shared runtime instead of a
    bundle-local nested CLI path
  - now routes governed bundle step-selection through registry-owned route
    states and step templates instead of one private handler branch per bundle
  - now routes bounded resolver logic through one shared resolver runtime so
    bundle `state_resolver` names and adjudication `target_resolution` names
    are runtime-consumed owner-layer semantics
  - now extends executor payload semantics to more already-implemented
    primitive commands instead of leaving that coverage concentrated only on
    rewrite/status paths
  - keeps underspecified follow-ups blocked instead of guessing
- next enforcement slice should target:
  - broader multi-round and multi-object adjudication replacement semantics
  - a shared transition engine that consumes the same registry-backed machine
    semantics end to end
- future external-evidence slice should evaluate:
  - using `xurl` as a provider-agnostic read/query adapter for external agent
    session extraction
  - accepting `agents://...` references as evidence or context inputs
  - keeping governance, owner-layer semantics, and durable control state inside
    `session-memory` instead of outsourcing them to the adapter

### `scripts/build_index.py`

- keep:
  - project/cross-project scanning
  - frontmatter extraction
  - metadata table population
- must change:
  - add `memory_links`
  - add `memory_fts` as FTS5
  - ensure the schema matches `SCHEMA.md`

### `scripts/query_index.py`

- keep:
  - CLI shape for `project_id`, `workspace_id`, `type`, `path`
- must change:
  - replace `LIKE` text recall with FTS5-backed recall
  - preserve structure-first filtering

### `scripts/assemble_context.py`

- keep:
  - current-task / blockers / latest snapshot assembly
- may refine later:
  - tighter compaction
  - less duplicated structure

## Implementation Order

1. add canonical control files and objective-line semantics
2. align index schema with `SCHEMA.md`
3. add FTS5 population in the builder
4. switch query path from `LIKE` to FTS5
5. teach context assembly to compile through active objective state
6. add role-context compilers over the same control substrate
7. freeze the explicit state-machine design and transition semantics
8. rerun real builds and queries

## Validation Standard

Phase 1 is only considered working when:

- the SQLite file is rebuilt successfully from current Markdown memory
- metadata tables contain expected rows
- FTS5 recall returns real project records
- one fresh-session context packet is generated from indexed project memory
