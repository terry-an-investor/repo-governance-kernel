# Repo Governance Kernel Public Surface

This file is the package-facing summary of the current `0.1.0b0` public beta
surface.

This beta line freezes the first stable package-facing compatibility promise.

It covers:

- the public command set
- the machine-readable public surface descriptor
- the stable public flow field contract for the four highest-frequency flows

That `0.1.0b0` descriptor includes:

- stable command metadata
- stable top-level flow result fields by entrypoint and status
- stable blocked-detail fields
- stable nested subcontract fields for `flow_contract` and
  `intent_compilation`

It still does not promise stable nested shapes for `execution`, `outcome`, or
`postconditions`.

The current source tree now also records `b1-target` candidate subcontracts for
the smallest repeated kernels inside those evidence-layer objects so agents and
smokes can consume one owner-layer promotion target instead of inferring shape
from payload examples.

Current candidate targets:

- onboarding:
  - `execution`
  - `execution.compiled_bundle`
  - `outcome`
  - `outcome.created_control_state`
  - `postconditions`
- external-target assessment:
  - `execution`
  - `outcome`
  - `postconditions`

Those candidate entries are not yet part of the released `0.1.0b0` stable
promise. They are the current beta-hardening promotion targets for the next
cut.

Use these commands as the intended direct package entrypoints:

- `describe-config`
- `describe-public-surface`
- `audit-control-state`
- `enforce-worktree`
- `bootstrap-repo`
- `onboard-repo`
- `onboard-repo-from-intent`
- `assess-external-target-once`
- `assess-external-target-from-intent`

Lower-level owner-layer commands such as `assess-host-adoption`,
`draft-external-target-shadow-scope`, and `execute-adjudication-followups`
remain implemented, but they are not the frozen public beta promise.

Machine-readable descriptor:

```powershell
repo-governance-kernel describe-public-surface
```

Canonical source:

- [`docs/canonical/PUBLIC_SURFACE.md`](../../docs/canonical/PUBLIC_SURFACE.md)
