# Docs Map

This directory holds non-canonical or auxiliary repository docs that do not
need to live at the repository root.

The root keeps the canonical kernel and release surfaces:

- `README.md`
- `RELEASE.md`
- `PRODUCT.md`
- `ARCHITECTURE.md`
- `CONTROL_SYSTEM.md`
- `STATE_MACHINE.md`
- `TRANSITION_COMMANDS.md`
- `SCHEMA.md`
- `DESIGN_PRINCIPLES.md`
- `IMPLEMENTATION_PLAN.md`

The root currently also keeps:

- `EVALUATION.md`
- `ROLE_CONTEXT_EVALUATION.md`

Those two remain at the root for now because active repo-facing evaluation
material and durable references still point at them directly.

Auxiliary docs now live here:

- `docs/history/`
  - historical design notes and one-off background material
- `docs/operations/`
  - harness and operational law docs that support the repo but are not package-facing root contracts
- `docs/evaluation/`
  - evaluation plans and supporting experiment docs
