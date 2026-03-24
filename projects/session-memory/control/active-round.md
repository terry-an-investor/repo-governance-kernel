# Active Round

- Round id: `round-2026-03-24-2110-stabilize-package-first-single-assessment-alpha-surface`
- Objective id: `obj-2026-03-23-0002`
- Status: `active`

## Scope

- Split external-target scope drafting and shadow assessment reporting into distinct artifact owner semantics.
- Add one package-first validation path that proves an installed wheel can bootstrap and audit a disposable governed host repo.
- Clean up root markdown topology by keeping canonical kernel docs at the root and moving weakly-coupled auxiliary docs into docs/.
- Split external-target drafting and shadow assessment reporting into distinct artifact owner semantics.
- Extend the package-first validation path so an installed wheel can bootstrap a disposable governed host and complete one governed external-target single assessment against a disposable external repo.
- Register the package-first smoke in the suite and tighten package-facing quickstart and release evidence around that same proof path.
- Keep canonical root docs in place while moving weakly-coupled auxiliary markdown into docs/.

## Deliverable

A cleaner alpha single-assessment surface with distinct artifact semantics, one install-first bootstrap-and-assess proof, one registered package smoke path, and aligned package-facing docs.

## Validation Plan

Run smoke_kernel_bootstrap, run_smoke_suite --smoke kernel_bootstrap, audit_product_docs, audit-control-state, and enforce-worktree after the package-facing proof path lands.

## Active Risks

- The first package-first smoke could stay too bootstrap-only and fail to prove the most important package-facing surface.

## Blockers

_none recorded_
