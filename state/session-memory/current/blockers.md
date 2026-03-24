# Blockers

## Active

- Context assembly quality is improved but still needs pressure-testing across
  more than one project.
- The first evaluation run is still a biased pilot because the same evaluator
  knows the repository history.

## Waiting

- Additional cross-project patterns should wait until at least two project
  samples feel natural instead of forced.

## Cleared

- Phase-1 retrieval engine choice is settled:
  SQLite plus FTS5 is in, DuckDB is out of phase 1.
- The build/query/assemble path is no longer just design; it is implemented and
  smoke-checked.
- Linked-memory behavior is no longer schema-only.
  The first real `supersedes` / `superseded_by` pair now exists in
  `state/session-memory/memory/decisions/`.

