# Repo Governance Kernel Public Alpha Surface

This file is the package-facing summary of the current `0.1.0a4` public alpha
surface.

This entrypoint set remains unchanged from the surface first frozen in
`0.1.0a3`.

On source head, the next planned `0.1.0a5` line keeps this same command set and
standardizes the result envelope for the highest-frequency one-task flows.

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
