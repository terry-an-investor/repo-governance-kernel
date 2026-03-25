# Repo Governance Kernel Implementation Plan

Date: 2026-03-25
Scope: versioned roadmap for the repo governance kernel after the first beta cut

## Goal

Keep the product centered on the smallest honest reusable kernel for repository
governance defined in [`PRODUCT.md`](./PRODUCT.md):

- files remain the source of truth
- SQLite plus FTS5 remain retrieval support layers
- control objects remain file-first
- machine behavior remains registry-first

The product is a repo governance kernel, not a general autonomous rewrite
engine. Its automation target remains bounded registry-owned execution.

## Current State

The repository already has a meaningful bounded kernel slice and the first
package-facing workflows:

- objective, pivot, round, task-contract, exception-contract, adjudication, and
  transition-event files exist
- projected control files exist
- transition registry exists
- audit and worktree enforcement exist
- bounded adjudication follow-up execution exists
- governed bundle execution exists for the bounded implemented subset
- package-facing repo onboarding exists through `onboard-repo`
- bounded natural-language wrappers exist for onboarding and one-time
  external-target assessment
- task-contract hard gating now blocks both direct round promotion and governed
  close bundles

The current gap is no longer "can the kernel do anything real". The current gap
is "does the package feel like a small product that agents can use without
reverse-engineering host-local details".

## Version Roadmap

### `0.1.0a3` — Agent Packaging And Public Alpha Surface

Primary outcome:

- turn the current kernel entrypoints into a clearer public alpha surface

Needed work:

- define and freeze the first public alpha command set
- add one repo-owned agent skill for bounded onboarding and bounded
  single-assessment workflows
- separate public package docs from host-local/internal tool docs more clearly
- make one agent-readable entry path sufficient for install, onboarding, and
  first assessment handoff

Success standard:

- an agent can discover and use the intended bounded package entrypoints without
  reading smoke code or host-local docs

Current status:

- landed in the current preview line

### `0.1.0a4` — Config Layering And Installability Polish

Primary outcome:

- make external installation and runtime config resolution predictable

Needed work:

- add explicit user/project/local config layering for package-facing behavior
- define runtime config resolution order across flags, environment, config
  files, cwd discovery, and package defaults
- tighten installed-package proof so it does not depend on familiarity with this
  source repo
- keep package install docs and validation evidence aligned

Success standard:

- a new repo can install the package and understand how runtime configuration is
  resolved without reading the source tree

Current status:

- landed in the current preview line

### `0.1.0a5` — One-Task Productization

Primary outcome:

- make the highest-frequency flows feel like one-task product surfaces

Needed work:

- keep compressing common workflows into bounded one-command entrypoints
- stabilize JSON result contracts for those entrypoints
- make failure semantics explicit and machine-readable
- add one explanatory surface for blocked states if the current output still
  forces agents to infer too much

Success standard:

- the common flows complete through one command plus one structured response,
  not through command archaeology

Current status:

- landed in the current preview line
- the package-facing onboarding and one-time external-target assessment flows
  now converge on one shared public result envelope across direct and
  intent-wrapper entrypoints
- blocked outcomes for those flows are now explicit package-facing payloads
  instead of mixed plain-text failures and command-local json quirks

### `0.1.0b0` — Beta Contract Freeze

Primary outcome:

- freeze the first beta compatibility promise

Needed work:

- freeze public command contracts
- freeze package doc layering
- keep host-local evidence and package contract clearly separated
- prove the beta matrix across install, onboarding, assessment, gating, and CI

Success standard:

- the project can make a defensible beta promise about what surfaces are stable
  and what remains explicitly out of scope

Current status:

- landed in the current beta line
- the public surface is now exported through `describe-public-surface`
- the stable public flow contract now freezes both top-level flow fields and
  the stable `flow_contract` / `intent_compilation` subcontracts

### `0.1.0b1` — Beta Hardening

Primary outcome:

- harden the first beta promise without expanding product authority

Needed work:

- promote the selected `execution` / `postconditions` kernels into the stable
  public contract
- keep package docs, installed-package proof, and CI validation aligned with
  the `0.1.0b1` beta surface
- tighten examples and release tooling around the new public-surface naming

Success standard:

- the beta line stays coherent and boring under repeated install, onboarding,
  assessment, and publication checks

Current status:

- landed in the current beta line
- the released stable public contract now includes `execution` and
  `postconditions` across onboarding and one-time external-target assessment
- the owner layer still keeps the deeper `compiled_bundle`,
  `created_control_state`, and assessment `outcome` projections as explicit
  forward-looking `candidate` subcontracts instead of freezing those whole
  evidence objects
- the current gap is no longer the `0.1.0b1` cut itself; the current gap is
  deciding whether any remaining deeper evidence kernels deserve a later stable
  promotion

## Cross-Version Priorities

### 1. Stabilize the kernel surface

Keep the reusable kernel centered on:

- objective
- round
- task-contract
- exception-contract
- adjudication
- audit
- enforcement
- bounded transition runtime

Do not broaden the primitive surface unless the behavior cannot honestly remain
composition.

### 2. Strengthen task-contract as an execution gate

Task contracts should become more than durable notes.

Needed outcomes:

- enforcement narrows dirty implementation scope to active task contracts when
  they exist
- promotion and closure commands refuse to strand open task contracts
- context assembly and role contexts continue to surface active task contracts
  as current authority

### 3. Make enforcement the hard promotion gate

Important promotion and closure paths should converge on the same blockers:

- `audit-control-state`
- `enforce-worktree`

The system should not keep separate local notions of "good enough to proceed".

### 4. Continue eliminating private semantics

Keep moving these surfaces into the registry/runtime owner layer:

- command payload semantics
- mutable-field semantics
- bundle route/state semantics
- bundle payload semantics
- target resolution semantics
- compiler binding semantics

No new executor-local or compiler-local private authority should be added.

### 5. Separate kernel from sample

Make the conceptual split increasingly real:

- kernel
  - reusable governance semantics and runtime
- sample
  - `state/session-memory/...`
  - dogfood/example rounds, adjudications, and sample history

This can begin as documentation and module-boundary cleanup before it becomes a
physical repo split.

### 6. Prepare the kernel for alpha release

Needed outcomes:

- package metadata and console entrypoint exist
- kernel docs explain release boundary and support surface
- host repo docs stop treating the sample as the product center

### 7. Prove install-first host bootstrap on low-risk fixtures

Needed outcomes:

- one brand-new git repo can bootstrap the minimal governance surface through the kernel CLI
- bootstrap installs repo-local hooks that call the shared kernel entrypoint instead of repo-private policy code
- fixture validation proves the install path and host-side control audit before higher-risk host rollout
- real-host rollout proceeds in this order:
  - disposable fixture repo
  - frozen host snapshot
    - first proof now exists through a copied `wind-agent` working-tree snapshot that bootstraps and passes host-side control audit without touching the live repo
    - frozen-host enforcement now also returns the honest blocked verdict before adoption:
      - dirty worktree plus no adopted round means the host is not yet allowed to proceed
      - adoption should therefore continue through explicit objective/round capture before live shadow mode
  - shadow mode on a live host
  - hard-gated adoption on a lower-risk real repo

## Out Of Scope

The following should stay out of scope for this phase:

- general autonomous rewrite
- prose-driven durable rewrite inference
- arbitrary multi-object adjudication execution
- ontology expansion for its own sake
- new private bundle families
- product broadening back into a generic memory platform

## Immediate Order

1. keep the `0.1.0b1` beta command and flow contract aligned across code, docs, and release tooling
2. decide whether any remaining deeper evidence kernels should stay intentionally unstable or later graduate into another stable beta cut
3. continue hardening installation, validation, and publication proof without widening product authority

## Validation Standard

Kernelization is only considered real when:

- canonical docs agree on the product boundary
- product-doc audit stays clean
- control audit stays clean on the real project
- enforcement stays clean on the real project after the round closes
- newly added execution semantics are registry-owned, audit-visible, and
  smoke-proven
- sample-specific complexity is distinguishable from reusable kernel semantics

