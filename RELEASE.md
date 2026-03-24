# Release Plan

Date: 2026-03-24
Scope: alpha release preparation for the reusable kernel

## Release Target

Current target:

- package name: `repo-governance-kernel`
- version: `0.1.0a0`
- release level: alpha / internal preview

## What Ships

The alpha package should ship:

- `kernel/`
- `kernel/commands/`
- `kernel/docs/`
- `repo-governance-kernel` console entrypoint

It should not claim that repo-local smoke/eval workflows are part of the
package contract.

## What Stays Host-Local

The host repository continues to own:

- `projects/session-memory/` dogfood sample state
- `scripts/` compatibility and adapter entrypoints
- `.githooks/`
- `.github/workflows/`
- repo-local smoke/eval harnesses

## Alpha Caveats

This alpha is not yet a stable compatibility promise.

Known reasons:

- public command/API stability is not frozen
- host repo and package still live in one repository
- kernel-only smoke coverage is still thinner than host-repo smoke coverage
- task-contract as a hard execution gate is still incomplete

## Promotion Bar

Do not promote beyond alpha until:

- kernel-only validation is explicit and repeatable
- public command contract is frozen
- package-facing docs include quickstart and support boundary
- host/sample adapters no longer look like canonical kernel ownership
