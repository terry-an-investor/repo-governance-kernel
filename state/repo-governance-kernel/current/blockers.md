# Blockers

## Active

- Rename and namespace cleanup can leave stale legacy-name strings in
  repo-local docs or historical projections if the sweep is incomplete.
- Sample-specific scripts and docs must be deleted or rewritten together so the
  repo does not keep dangling entrypoints after the cleanup.

## Waiting

- Any broader multi-repo evidence should wait until the core self-hosted path
  stays honest without stale scaffolding.

## Cleared

- Phase-1 retrieval engine choice is settled:
  SQLite plus FTS5 is in, DuckDB is out of phase 1.
- The build/query/assemble path is no longer just design; it is implemented and
  smoke-checked.
- Linked-memory behavior is no longer schema-only.
  The first real `supersedes` / `superseded_by` pair now exists in
  `state/repo-governance-kernel/memory/decisions/`.


