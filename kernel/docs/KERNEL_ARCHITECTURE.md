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

That includes:

- registry-owned transition specs
- command entrypoints under `kernel/commands/`
- shared executor helpers under `kernel/executor_runtime.py`
- shared governed-bundle execution under `kernel/governed_bundle_runtime.py`
- bounded intent compilation when it lowers only into existing governed
  commands or bundles

The host repository may still provide:

- repo-local CLI wrappers under `scripts/`
- git hooks
- CI glue
- sample data and dogfood control objects

Those are adapter surfaces, not the canonical kernel implementation layer.
