# Blockers

## Active

- Round contract drift:
  `.round/active.json` declares a `src/wind/` query-surface round, but the current dirty mainline
  also changes `src/native/`, `native/`, and `src/cli/`.
- Validation scope gap:
  the existing live pass proves prepared query-context reuse only, not the full broadened
  substrate/state-machine/native convergence currently in the worktree.
- Progress artifact drift:
  `.round/progress.json` still shows `initialized`, so governance metadata no longer summarizes the
  live state of the round.
- Mainline convergence debt is still open:
  canonical docs still mark parallel observation truth, visual-policy centralization,
  freshness/applicability, sink-registry adoption, and wait-pump convergence as active debt.

## Waiting

- Durable memory extraction is waiting on a cleaner boundary between:
  - the proven query-surface contract
  - the still-open broader substrate convergence work

## Cleared

- Prepared query context reuse is no longer just a design claim.
  Real validation passed on `2026-03-22`, with artifacts under
  `outputs/query-surface-prepared-context-live-20260322-194431/`.
