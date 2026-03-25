# Repo Governance Kernel Public Alpha Surface

This file is the package-facing summary of the frozen `0.1.0a3` public alpha
surface.

The current preview release is `0.1.0a4`, but this command contract remains
the same frozen direct-entry surface.

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
