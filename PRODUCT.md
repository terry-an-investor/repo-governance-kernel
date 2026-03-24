---
id: product-session-memory
product_name: session-memory
product_category: "repo governance kernel"
product_approach: "control-first on top of a memory substrate"
positioning_phrase: "repo governance kernel"
automation_scope: "bounded registry-owned execution"
autonomy_boundary: "not a general autonomous rewrite engine"
current_stage: "kernelization phase"
target_user_segments:
  - vibe coding builders
  - non-senior engineers
  - AI-native technical leads
canonical_semantics_surfaces:
  - PRODUCT.md frontmatter
  - CONTROL_SYSTEM.md
  - STATE_MACHINE.md
  - TRANSITION_COMMANDS.md
  - kernel/transition_specs.py
  - scripts/audit_product_docs.py
  - kernel/audit_control_state.py
---
# Session Memory Product

Date: 2026-03-24
Scope: Canonical product definition for the repository

## Product Definition

`session-memory` is a repo governance kernel.

Its job is not to write code for a repository. Its job is to make repository
development pass through explicit control objects, legal transitions, audit,
and enforcement before progress is accepted.

Memory still matters, but memory is the substrate rather than the product
center. The product center is development control:

- what objective line is active
- what round is currently allowed to move the repo
- what task contract currently authorizes one concrete implementation slice
- what exception contracts temporarily legitimize guarded deviation
- what adjudications resolve conflicting durable control truth
- what enforcement gates block dishonest advancement

## Target Users

Primary users today:

- vibe coding builders who can generate code quickly but lose project control
  across sessions
- non-senior engineers who need explicit scope, state, and closure discipline
  while working with LLM-heavy workflows
- AI-native technical leads who need auditable control objects instead of
  transcript archaeology

## User Pain

The repeated pain is not missing chat history. The repeated pain is losing
control of a live repository.

Common failure modes:

- the real objective line disappears after several high-speed sessions
- scope expands because no bounded control object owns the change
- agents smuggle private semantics into scripts and bundle handlers
- work is narrated as done while the worktree or control files are blocked
- a fresh session cannot tell which state is durable truth and which state is
  stale projection

## Product Promise

The product promise is:

- keep the active development line explicit across sessions and handoffs
- force implementation to move inside bounded round and task contracts
- make temporary deviation explicit and recoverable
- block dishonest promotion and closure automatically
- allow only the registry-owned automatic subset the repo has already declared

## Current Capabilities

Today the product already provides:

- durable objective, pivot, round, task-contract, exception-contract, and
  adjudication records
- projected control files for active objective, active round, pivot log, and
  exception ledger
- registry-owned transition command semantics for the implemented bounded
  command subset
- registry-owned governed bundle semantics for the implemented bounded bundle
  subset
- control audit and worktree enforcement
- assembled and role-specific contexts that surface active control state
- bounded adjudication follow-up execution for the explicit safe subset
- multi-project operation with `session-memory` and `wind-agent`

## Product Boundaries

The current automation scope is bounded registry-owned execution.

The current autonomy boundary is not a general autonomous rewrite engine.

That means:

- execution is allowed only where command, guard, write-target, payload, and
  bundle semantics are already registry-owned
- prose does not authorize durable rewrite
- task contracts make task intent auditable, but they do not by themselves
  authorize arbitrary automatic code rewrite
- governed bundles are allowed only when they remain bounded, audit-visible,
  smoke-proven, and composed from existing governed primitives
- new automation surfaces must be promoted into owner-layer semantics before
  they are allowed to execute

## Product To Semantics Path

Product docs should influence machine behavior only through explicit owner-layer
surfaces, never through free-form natural-language inference.

The required path is:

1. `PRODUCT.md` defines the product contract and boundary
2. canonical docs translate that contract into control, architecture, and state
   language
3. `STATE_MACHINE.md` freezes the legal state domains and transition intent
4. `TRANSITION_COMMANDS.md` freezes the legal bounded command and bundle
   surface
5. `kernel/transition_specs.py` owns the executable machine semantics for the
   implemented subset
6. audits fail when the product contract, canonical docs, and executable
   registry drift apart

This is how "start from product" becomes auditable machine behavior instead of
prompt folklore.

## Current Stage

Current stage: `kernelization phase`

This stage is about narrowing the repository into a reusable governance kernel
with one self-hosted sample, instead of broadening it into a larger autonomous
system.

## Roadmap

Near-term product milestones:

- stabilize the kernel framing across canonical docs and machine-readable
  product metadata
- make task-contract a real execution gate rather than only a durable note
- strengthen enforcement so promotion and closure paths all reuse the same
  owner-layer blockers
- continue lifting private semantics into the transition registry and governed
  runtime
- separate reusable kernel surfaces from `session-memory` dogfood/sample
  surfaces
- validate the kernel on more non-self-hosted repositories before broadening
  automation
