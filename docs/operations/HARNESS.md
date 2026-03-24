# Session Memory Harness

Date: 2026-03-23
Scope: Smoke-suite execution law for the coding control system

## Goal

Make smoke validation itself a governed owner-layer surface instead of an
informal collection of disposable fixture scripts.

This document exists because smoke failures can be caused by two very different
things:

- a real product regression
- a harness protocol failure such as fixture leakage or parallel contamination

The system should distinguish those explicitly.

## Core Position

Smoke scripts are not only convenience checks.

They are part of the harness law that decides whether the repo has observed the
claimed effect honestly.

That means fixture isolation, cleanup guarantees, and execution ordering are
part of the product surface, not only test hygiene.

## Harness Objects

The current harness owner layer includes:

- `scripts/smoke_manifest.py`
  - canonical registry of disposable smoke fixtures
- `scripts/run_smoke_suite.py`
  - suite runner that enforces fixture leak checks and serial execution
- `scripts/smoke_phase1.py`
  - top-level phase-1 integration path that delegates disposable fixture work to
    the suite runner

## Canonical Rules

### 1. Disposable smoke fixtures must be declared

Each disposable smoke must declare in the manifest:

- its canonical smoke name
- the script path
- the owned fixture project ids
- whether it is parallel-safe
- shared resources that affect execution ordering

Undeclared disposable fixtures are harness drift.

### 2. Fixture leak checks are mandatory

Before a smoke starts:

- none of its declared fixture paths may already exist

After a smoke finishes:

- none of its declared fixture paths may remain

If either condition fails, the suite runner should report:

- `fixture_leak_before_run`
- `fixture_leak_after_run`

This is a harness failure, not a product-state success.

### 3. Shared fixture smokes run serially

Current disposable fixture smokes all mutate:

- `projects/__*_smoke__/`
- the repo worktree view used by enforcement

So they are not parallel-safe by default.

The suite runner must execute them serially until explicit proof exists that a
given smoke is isolated enough to run in parallel.

### 4. Harness contamination must stay visible

If a fixture's temporary files pollute:

- `enforce-worktree`
- audit assumptions
- another fixture's cleanup path

that is a harness protocol failure and should not be hidden as a product
regression.

The correct fix is to strengthen the harness law, not to hand-wave the failure
away.

### 5. Phase-1 integration should use the suite runner

Top-level integration should not call each disposable smoke script ad hoc.

It should call the canonical suite runner so:

- fixture ordering stays centralized
- leak checks stay mandatory
- smoke selection is explicit
- later CI and local execution share the same harness owner layer

## Current Limitations

The current harness law now guarantees:

- disposable smoke registration
- fixture leak checks before and after execution
- serial execution for shared fixture smokes

It does not yet guarantee:

- parallel execution for any smoke class
- machine-checked per-smoke cleanup contracts beyond fixture-path deletion
- richer contamination classes such as artifact collisions or index reuse policy
- automatic classification of harness failures versus product failures in every
  higher-level report

## Design Consequence

This project should treat harness engineering as first-class control work.

Spec defines what the system is allowed to claim.
Harness defines what the repo is willing to accept as observed truth.

Without that layer, even a good smoke script can still produce misleading
confidence.
