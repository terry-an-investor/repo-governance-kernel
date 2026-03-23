# Constitution

This file is the project-law layer for `wind-agent`.
It should stay short, explicit, and architecture-shaped.
It is not a backlog, roadmap, or prose summary.

## Product Boundaries

- `wind-agent` is a Wind-first desktop agent stack for turning a legacy Windows
  GUI into a verifiable capability surface for an external agent.
- The repo is not a generic desktop automation framework, generic RPA product,
  or provider-owned automation loop.
- The architecture unit is the reusable loop:
  `observe -> resolve owner -> resolve target -> choose honest sink -> dispatch one bounded action -> verify observed effect -> persist reusable knowledge`.
- Business labels such as `EDB`, `CPI`, or `NEWS` are evidence samples inside
  that loop, not architecture units.
- Providers may contribute evidence only. They do not own success, workflow
  completion, or canonical state truth.

## Architecture Invariants

- `canonical_observation` is the only owner-facing observation truth.
  Owner paths must not quietly fall back to raw `elements`, raw
  `snapshotText`, raw `vision`, or ad hoc preview blobs as parallel truth.
- `resolved_target` is the only owner-facing actionable-target truth.
  Sink choice belongs to `execution_sink_registry`, not owner-local helpers.
- `interaction_wait_pump` is the only owner for bounded wait, settle,
  materialization, retry, and recovery loops.
- `interaction_state_machine` owns next-state reduction, evidence freshness,
  applicability, and dispatch truth. Shared consumers should reject stale or
  inapplicable state by default.
- `dispatch_proof` must remain first-class state/evidence. Transport success or
  `ok` flags are not a substitute for bounded dispatch proof.
- Owner-layer tests must expose `di_seam` at honest lower-layer boundaries.
  Module-cache mutation and export reassignment are not architecture seams.

## Quality Bar

- Query and context work should be reviewed against producer-consumer contract
  fidelity, not against whether one page-local helper happened to succeed once.
- Mainline architecture work must converge toward state-first evidence
  consumption, not add new page-local patches, hidden recovery glue, or raw
  payload-shaped shortcuts.
- Owner-facing state and result contracts should stay canonical and compact.
  Producer-debug detail must be explicitly named as debug material, not allowed
  to drift back into owner truth.
- Round governance must stay honest. If the dirty worktree expands beyond the
  declared round, the round must be split or amended immediately instead of
  letting one narrow pass stand in for the broader mainline.

## Validation Rules

- The required validation ladder is:
  primitive self-test -> live primitive probe -> end-to-end task-chain proof.
- If a business chain fails, reduce it to the lowest failing primitive family,
  prove that primitive, then rerun the higher chain.
- Query-family debugging must start from primitive probes such as
  `focus_query_input`, `query_input_sink`, `query_input_readback`, and
  `query_popup_materialization`, not from composed task chains alone.
- Popup appearance, transport dispatch, screenshot existence, or weak submit
  evidence do not count as text-effect proof.
- Query popup/input commit paths should be local-first. Cropped visual/live
  evidence is escalation or strengthening evidence, not the default synchronous
  gate.
- Validation claims must stay aligned with the actual round scope. A narrow
  live proof cannot be used to claim broader substrate/native/CLI convergence.

## Forbidden Shortcuts

- Do not rebuild owner truth from raw `afterEvidence`, `surfacePreview`,
  `selectorPreview`, raw `snapshotText`, or provider payloads once canonical
  observation/state already exists.
- Do not bypass `resolved_target -> execution_sink_registry` with owner-local
  dispatch language for the same target family.
- Do not add private wait/retry loops where `interaction_wait_pump` should own
  the behavior.
- Do not treat provider output, popup visibility, or dismissal-like signals as
  canonical success without the stronger owner-facing verification contract.
- Do not hide broader `src/native/`, `native/`, or `src/cli/` work behind a
  still-open narrow query-only round.
