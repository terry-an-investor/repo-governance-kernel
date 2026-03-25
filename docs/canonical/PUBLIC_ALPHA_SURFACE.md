# Repo Governance Kernel Public Alpha Surface

Date: 2026-03-25
Scope: current `0.1.0a5` public alpha package surface

## Goal

Define the smallest public package contract that users and agents should depend
on directly during the current `0.1.0a5` alpha line.

This document exists because "implemented command" and "frozen public alpha
surface" are not the same thing.

The current preview release is `0.1.0a5`.

The direct package command contract remains the same entrypoint set first
frozen in `0.1.0a3`, but the live public preview release identity is now
`0.1.0a5`.

The command list is still stable across `a4` and `a5`. What changed in `a5` is
the package-facing result contract for the highest-frequency product flows:
shared success and blocked payload categories across the direct and
intent-wrapper entrypoints.

The product remains a repo governance kernel as defined in
[`PRODUCT.md`](./PRODUCT.md). Its automation scope remains `bounded
registry-owned execution`. Its autonomy boundary remains `not a general
autonomous rewrite engine`.

## Public Alpha Commands

These are the intended direct entrypoints for users and agent callers during
the current `0.1.0a5` line:

- `audit-control-state`
- `enforce-worktree`
- `bootstrap-repo`
- `onboard-repo`
- `onboard-repo-from-intent`
- `assess-external-target-once`
- `assess-external-target-from-intent`

Why these and not more:

- they cover install-first bootstrap, first control-line onboarding, and one
  bounded external-target assessment
- they already represent the package's highest-frequency product tasks
- they have a clearer package-facing meaning than the lower-level owner-layer
  primitives they compose

The `a5` productization focus for these same commands is:

- shared top-level result categories across direct and intent-wrapper entrypoints
- explicit machine-readable blocked payloads when the one-task workflow cannot finish cleanly

## Package-Internal But Implemented

These commands remain real owner-layer surfaces, but they are not the frozen
public alpha promise:

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

The following remain out of the public alpha package contract:

- `scripts/`
- `state/session-memory/`
- `.githooks/`
- `.github/workflows/`
- repo-local smoke and evaluation harnesses

These surfaces may continue to provide evidence, adapter entrypoints, or local
automation triggers, but they are not part of the user-facing package promise.

## Machine-Readable Descriptor

The public alpha surface is also exported through:

- `describe-public-alpha-surface`

That command exists so package docs, installed-package proof, and agent
wrappers can consume one shared owner-layer truth instead of carrying slightly
different prose lists.
