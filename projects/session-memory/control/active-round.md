# Active Round

- Round id: `round-2026-03-24-2110-stabilize-package-first-single-assessment-alpha-surface`
- Objective id: `obj-2026-03-23-0002`
- Status: `active`

## Scope

- Split external-target scope drafting and shadow assessment reporting into distinct artifact owner semantics.
- Keep the package-first validation path proving installed-wheel bootstrap and bounded external-target single assessment.
- Collapse host canonical product/control/release docs into docs/canonical and retarget repo-facing audit and navigation surfaces to that tree.

## Deliverable

A cleaner alpha single-assessment surface with distinct artifact semantics, one install-first bootstrap-and-assess proof, one registered package smoke path, and a root markdown layout reduced to entrypoint-only docs.

## Validation Plan

Run smoke_phase1, smoke_kernel_bootstrap, run_smoke_suite --smoke kernel_bootstrap, audit_product_docs, audit-control-state, and enforce-worktree after the canonical-doc migration lands.

## Active Risks

- The first package-first smoke could stay too bootstrap-only and fail to prove the most important package-facing surface.

## Blockers

_none recorded_
