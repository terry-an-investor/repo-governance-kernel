# Session Memory Design Principles

Date: 2026-03-24
Scope: repo governance kernel

## Goal

Build a repo governance kernel that helps a fresh coding session recover the
real control state of a repository without replaying entire transcripts.

See [`PRODUCT.md`](./PRODUCT.md) for the canonical product definition.

## Core Position

The product should optimize for repository control, not chat recall.

Memory matters because control objects and evidence need durable storage. But
the system becomes useful only when it can prevent drift, not merely remember
it afterward.

## Principles

### 1. Control before recall

The highest-value question is not "what was said before" but:

- what objective is active
- what round is open
- what task contract authorizes the current slice
- what exception contract legitimizes temporary deviation
- what enforcement gate will block dishonest promotion

Recall without this layer only accelerates confusion.

### 2. Files are authority

Canonical truth should live in visible files.

Why:

- humans can inspect control objects directly
- git versions the control plane naturally
- audits and enforcement can compare durable truth with projections
- no hidden service becomes the source of authority

### 3. Product prose is not executable authority

Natural language can define intent, but machine behavior must still flow
through explicit owner-layer semantics:

- state domains
- transition commands
- guards
- write targets
- payload semantics
- governed bundle semantics

Without this rule, "documentation first" degrades back into prompt folklore.

### 4. One honest owner layer at a time

The system should not jump from round-level intent straight to arbitrary code
rewrite.

The honest layers are:

- objective
- round
- task contract
- exception contract
- adjudication

Each layer should become consumable before the next automation claim is made.

### 5. No private semantics

A semantic surface is not real until the repo owns it explicitly.

That means:

- no hidden bundle handlers
- no compiler-local free-string plan semantics
- no executor-only payload admission
- no command-local rewrite rules that bypass the registry

This principle is stricter than "write careful code". It is a structural ban on
private authority.

### 6. Bundles are allowed only when governed

Bundles are not forbidden. Private bundles are forbidden.

A bundle is acceptable only when it is:

- registry-owned
- bounded
- composed from existing governed steps
- audit-visible
- smoke-proven

Otherwise it is just a hidden orchestration layer.

### 7. Audit, adjudication, and projection must stay separate

These jobs are easy to blur and expensive to untangle later:

- audit detects dishonesty
- adjudication chooses authoritative durable truth
- projection rebuilds compact current-state files

Repair code must not quietly become judge and jury.

### 8. Enforcement is part of the product

The kernel is not complete when docs exist. It is complete when dishonest
advancement is blocked by repo-owned commands.

That means:

- `captured` and `closed` should hit enforcement gates
- git hooks and CI should reuse the same owner-layer commands
- live blocking should outrank smoke optimism

### 9. Kernel and sample must be distinguishable

Self-hosting is useful, but self-hosting also inflates complexity.

The repo therefore needs a clear conceptual split between:

- reusable governance kernel
- `session-memory` as the dogfood/sample project

Without that split, sample complexity looks like kernel necessity.

### 10. Start narrow and reusable

The right product is not a general AI development platform.

The right product is a small hard kernel that can be reused across repos:

- explicit control objects
- bounded legal transitions
- audit and enforcement
- bounded registry-owned execution

Broader autonomy comes later, if ever, and only after the lower layer is
already trustworthy.

## Design Consequence

The preferred direction is:

- keep the product framed as a repo governance kernel
- let memory remain substrate and evidence support
- continue promoting semantics into the registry
- strengthen enforcement before broadening automation
- separate kernel concerns from sample-specific dogfood history
