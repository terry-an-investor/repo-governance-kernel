# Exception Ledger

## Active

- None recorded yet.

## Retired

- `exc-2026-03-23-1524-transition-logic-remains-split-across-per-command-scripts`: Transition logic remains split across per-command scripts
  - objective: `obj-2026-03-23-0002`
  - owner scope: scripts/open_objective.py
  - exit condition: Retire this contract once objective, round, and exception-contract transitions share one owner-layer transition engine or a materially equivalent common primitive.
  - resolution: active -> retired: objective, round, and exception commands now delegate shared write/projection/event work through apply-transition-transaction evidence: - uv run python scripts/smoke_exception_contracts.py - uv run python scripts/repo_governance_kernel.py smoke

## Invalidated

- None recorded yet.

