# Blockers

## Active

- The project has not yet proven linked-memory behavior with real `supersedes`
  or `superseded_by` examples.
- Context assembly quality is improved but still needs pressure-testing across
  more than one project.

## Waiting

- Additional cross-project patterns should wait until at least two project
  samples feel natural instead of forced.

## Cleared

- Phase-1 retrieval engine choice is settled:
  SQLite plus FTS5 is in, DuckDB is out of phase 1.
- The build/query/assemble path is no longer just design; it is implemented and
  smoke-checked.
