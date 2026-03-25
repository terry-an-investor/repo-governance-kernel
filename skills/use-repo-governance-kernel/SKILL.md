---
name: use-repo-governance-kernel
description: Use the bounded repo-governance-kernel package surface for fresh repo onboarding and one-time external-target assessment. Do not widen authority beyond the documented onboarding and assessment entrypoints.
---

# Repo Governance Kernel

Use this skill when the task is:

- initialize governance for a fresh host repo
- check whether a governed host repo is audit-clean
- run one bounded external-target assessment
- explain which bounded command to run next

Do not use this skill for:

- continuous monitoring
- background server behavior
- general autonomous code mutation
- commit message generation
- freeform control-state rewrites outside the bounded entrypoints below

## Default Command Surface

Use these commands as the primary entrypoints:

```powershell
repo-governance-kernel --repo-root C:/path/to/host/repo onboard-repo --project-id my-repo
repo-governance-kernel --repo-root C:/path/to/host/repo onboard-repo-from-intent --project-id my-repo --request "Initialize governance for this repo."
repo-governance-kernel --repo-root C:/path/to/host/repo audit-control-state --project-id my-repo
repo-governance-kernel --repo-root C:/path/to/host/repo enforce-worktree --project-id my-repo --workspace-root C:/path/to/host/repo
repo-governance-kernel --repo-root C:/path/to/governed/host/repo assess-external-target-once --project-id my-repo --workspace-root C:/path/to/external/repo
repo-governance-kernel --repo-root C:/path/to/governed/host/repo assess-external-target-from-intent --project-id my-repo --request "Assess C:/path/to/external/repo current changes, set scope first, then give me the verdict."
```

## Workflow

### 1. Fresh Repo Onboarding

If the repo is not yet governed, prefer:

```powershell
repo-governance-kernel --repo-root C:/path/to/host/repo onboard-repo --project-id my-repo
```

If the caller is speaking in one narrow natural-language request, prefer:

```powershell
repo-governance-kernel --repo-root C:/path/to/host/repo onboard-repo-from-intent --project-id my-repo --request "Initialize governance for this repo."
```

After onboarding, immediately run:

```powershell
repo-governance-kernel --repo-root C:/path/to/host/repo audit-control-state --project-id my-repo
repo-governance-kernel --repo-root C:/path/to/host/repo enforce-worktree --project-id my-repo --workspace-root C:/path/to/host/repo
```

### 2. One-Time External-Target Assessment

Use this only when the governed host repo already exists and the task is one
bounded assessment of another repo's current dirty state.

Preferred direct surface:

```powershell
repo-governance-kernel --repo-root C:/path/to/governed/host/repo assess-external-target-once --project-id my-repo --workspace-root C:/path/to/external/repo
```

Natural-language wrapper:

```powershell
repo-governance-kernel --repo-root C:/path/to/governed/host/repo assess-external-target-from-intent --project-id my-repo --request "Assess C:/path/to/external/repo current changes, set scope first, then give me the verdict."
```

## Rules

- Keep authority bounded to the command surface above.
- Prefer one-task entrypoints over manually stitching lower-level commands.
- Treat `audit-control-state` and `enforce-worktree` as the required follow-up checks after onboarding.
- Do not infer support for monitoring, daemonized control planes, or general live-host mutation.
- If the request falls outside onboarding or one-time assessment, say that the current public surface does not support it.

## Important Output Fields

When `onboard-repo` succeeds, read these JSON fields first:

- `onboarding_contract`
- `compiled_onboarding`
- `created_control_state`
- `postconditions`
- `next_actions`

When `onboard-repo-from-intent` succeeds, read:

- `compiled_intent`
- `workflow`

When one-time assessment succeeds, keep the assessment verdict and next command
sequence tied to the returned bounded workflow output instead of inventing
follow-up rewrites.

## Canonical References

- [`README.md`](../../README.md)
- [`kernel/README.md`](../../kernel/README.md)
- [`docs/canonical/TRANSITION_COMMANDS.md`](../../docs/canonical/TRANSITION_COMMANDS.md)
- [`docs/canonical/IMPLEMENTATION_PLAN.md`](../../docs/canonical/IMPLEMENTATION_PLAN.md)
