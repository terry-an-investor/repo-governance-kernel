# Repo Governance Kernel Public Alpha Surface

This file is the package-facing summary of the current `0.1.0a5` public alpha
surface.

This entrypoint set remains unchanged from the surface first frozen in
`0.1.0a3`.

This `0.1.0a5` line keeps the same command set and standardizes the result
envelope for the highest-frequency one-task flows.

For the `0.1.0b0` freeze line, the candidate stable field contract for those
four public flow entrypoints is now exported through the same machine-readable
descriptor instead of living only in prose and smoke assertions.

That `b0` candidate descriptor now includes:

- stable top-level result fields by entrypoint and status
- stable blocked-detail fields
- stable nested subcontract fields for `flow_contract` and
  `intent_compilation`

It still does not promise stable nested shapes for `execution`, `outcome`, or
`postconditions`.

Use these commands as the intended direct package entrypoints:

- `audit-control-state`
- `enforce-worktree`
- `bootstrap-repo`
- `onboard-repo`
- `onboard-repo-from-intent`
- `assess-external-target-once`
- `assess-external-target-from-intent`

Lower-level owner-layer commands such as `assess-host-adoption`,
`draft-external-target-shadow-scope`, and `execute-adjudication-followups`
remain implemented, but they are not the frozen public alpha promise.

Machine-readable descriptor:

```powershell
repo-governance-kernel describe-public-alpha-surface
```

Canonical source:

- [`docs/canonical/PUBLIC_ALPHA_SURFACE.md`](../../docs/canonical/PUBLIC_ALPHA_SURFACE.md)
