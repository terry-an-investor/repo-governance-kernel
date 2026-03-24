# Kernel Architecture

Date: 2026-03-24
Scope: reusable repo-governance kernel architecture

## Layers

1. durable control truth
2. projected control state
3. audit and enforcement
4. adjudication
5. bounded execution runtime

## Runtime Ownership

The kernel package owns the reusable Python implementation.

The host repository may still provide:

- repo-local CLI wrappers under `scripts/`
- git hooks
- CI glue
- sample data and dogfood control objects

Those are adapter surfaces, not the canonical kernel implementation layer.
