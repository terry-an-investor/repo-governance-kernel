# Active Round

- Round id: `round-2026-03-25-0843-make-task-contract-a-real-hard-execution-gate`
- Objective id: `obj-2026-03-23-0002`
- Status: `active`

## Scope

- Prove governed bundle and adjudication follow-up surfaces fail closed when unresolved task contracts still block the round close chain.
- Cut the 0.1.0a2 alpha release by updating package metadata, release-facing docs, and release-grade validation evidence in one controlled round.

## Deliverable

One hard-gate-complete owner layer plus one 0.1.0a2 release cut with aligned versioning, docs, and release evidence.

## Validation Plan

Run focused bundle/adjudication hard-gate proof, smoke_phase1, smoke_kernel_bootstrap, audit-control-state, enforce-worktree, audit_product_docs, uv build, and installed-wheel verification after the release cut lands.

## Active Risks

- High-level workflow surfaces may still bypass the low-level task-contract gate unless one bundle-backed proof demonstrates the blocked path directly.
- The release cut can drift from the real package surface if version, docs, and installed-wheel evidence are not updated in the same round.

## Blockers

_none recorded_
