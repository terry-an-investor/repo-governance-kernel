# Repo Governance Kernel Public Surface

Date: 2026-03-25
Scope: current `0.1.0b0` public beta package surface

## Goal

Define the smallest public package contract that users and agents should depend
on directly during the current `0.1.0b0` beta line.

This document exists because "implemented command" and "frozen public beta
surface" are not the same thing.

The current beta release is `0.1.0b0`.

This is the first release that makes a beta compatibility promise about:

- which package-facing commands are stable
- which public flow fields are stable
- which nested public flow subobjects are stable
- which implemented owner-layer commands remain explicitly out of scope

The product remains a repo governance kernel as defined in
[`PRODUCT.md`](./PRODUCT.md). Its automation scope remains `bounded
registry-owned execution`. Its autonomy boundary remains `not a general
autonomous rewrite engine`.

## Public Beta Commands

These are the intended direct entrypoints for users and agent callers during
the current `0.1.0b0` line:

- `describe-config`
- `describe-public-surface`
- `audit-control-state`
- `enforce-worktree`
- `bootstrap-repo`
- `onboard-repo`
- `onboard-repo-from-intent`
- `assess-external-target-once`
- `assess-external-target-from-intent`

Why these and not more:

- they cover package-facing inspection, install-first bootstrap, first
  control-line onboarding, and one bounded external-target assessment
- they already represent the package's highest-frequency product tasks
- they have a clearer package-facing meaning than the lower-level owner-layer
  primitives they compose

## `0.1.0b0` Stable Public Flow Contract

The stable beta flow contract currently covers the four highest-frequency public
workflow entrypoints:

- `onboard-repo`
- `onboard-repo-from-intent`
- `assess-external-target-once`
- `assess-external-target-from-intent`

The owner-layer source of truth for their stable field contract now
lives in:

- `kernel/public_flow_contracts.py`

and is exported through:

- `describe-public-surface`

Current stable boundary:

- `result_contract` always carries one stable schema/version/entrypoint record
- each of the four entrypoints now has one owner-layer list of required
  top-level fields for `ok` and `blocked`
- blocked payloads now share one stable required detail shape:
  - `stage`
  - `code`
  - `message`
  - `meaning`
  - `suggested_next_actions`
- the two public interpretation subobjects that callers most directly depend on
  now also export stable nested field catalogs:
  - `flow_contract`
  - `intent_compilation`

Current stable nested subcontract boundary:

- `flow_contract` is the stable explanation object for direct workflows and for
  successful intent wrappers
- `intent_compilation` is the stable explanation object for intent wrappers,
  including blocked intent-compilation outcomes
- the descriptor records both:
  - which top-level statuses require each subobject
  - which nested fields are stable when that subobject is present
- `execution`, `outcome`, and `postconditions` remain outside the minimum
  stable beta contract in this release

This `0.1.0b0` promise is intentionally narrow. It freezes the public command
surface plus the minimum public flow contract, not every detail-rich evidence
object that may appear inside richer responses.

## `0.1.0b1` Hardening Candidates In The Current Source Line

The current source tree is now recording the next honest promotion targets for
the beta line without claiming that they are already part of the released
`0.1.0b0` stable promise.

These `b1-target` candidate subcontracts are also exported through
`describe-public-surface`.

Why this intermediate layer exists:

- agents already consume repeated kernels inside `execution`, `outcome`, and
  `postconditions`
- those kernels are more stable than the full evidence objects that contain
  them
- the owner layer should name those promotion targets explicitly before they
  are frozen into the next release promise

Current candidate promotion targets:

- onboarding:
  - `execution`
  - `execution.compiled_bundle`
  - `outcome`
  - `outcome.created_control_state`
  - `postconditions`
- external-target assessment:
  - `execution`
  - `outcome`
  - `postconditions`

These candidate entries do not widen authority and do not freeze full evidence
payloads. They only record the smallest repeated kernels that the current
source line is testing for promotion into the next beta cut.

## Package-Internal But Implemented

These commands remain real owner-layer surfaces, but they are not the frozen
public beta promise:

- `assess-host-adoption`
- `draft-external-target-shadow-scope`
- `execute-adjudication-followups`

They stay implemented because higher-level bounded workflows depend on them,
but users and agents should treat them as lower-level package internals unless
the public contract expands later.

## Repo-Owned Agent Packaging

The source repository now ships one repo-owned agent wrapper:

- `skills/use-repo-governance-kernel/SKILL.md`

This wrapper is part of the `a3` productization work, but it is a
repository-owned wrapper, not a wheel-installed package artifact. Its job is to
guide agents onto the same bounded public entrypoints instead of inventing new
authority.

## Host-Local And Internal Surfaces

The following remain out of the public beta package contract:

- `scripts/`
- `state/session-memory/`
- `.githooks/`
- `.github/workflows/`
- repo-local smoke and evaluation harnesses

These surfaces may continue to provide evidence, adapter entrypoints, or local
automation triggers, but they are not part of the user-facing package promise.

## Machine-Readable Descriptor

The public beta surface is also exported through:

- `describe-public-surface`

That command exists so package docs, installed-package proof, and agent
wrappers can consume one shared owner-layer truth instead of carrying slightly
different prose lists. The descriptor now carries both:

- the released `b0` stable contract
- the current `b1-target` candidate subcontract catalog for evidence-layer
  hardening
