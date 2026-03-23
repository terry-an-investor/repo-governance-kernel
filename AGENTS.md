# Session Memory Local Rules

These rules apply inside `C:/Users/terryzzb/Desktop/session-memory`.

## 1. Editing Style

- Do not use one giant `apply_patch` for large doc or schema rewrites.
- Prefer small, reviewable patches grouped by file or by one coherent change.
- For broad restructures, land changes in this order:
  1. update canonical docs
  2. create new target paths
  3. migrate real sample files
  4. delete obsolete paths last

## 2. Migration Safety

- When changing directory layout, prefer additive migration first.
- Do not delete the old path until the new path exists and has been checked.
- Keep one canonical location for each memory object after migration completes.

## 3. Schema Discipline

- Keep the global schema project-agnostic.
- Project-specific workflow objects may appear in `evidence_refs`, but they must
  not become mandatory global fields.
- Prefer `project_id`, `workspace_id`, and `workspace_root` over repo-specific
  assumptions.

## 4. Implementation Order

- Do not start embeddings before file workflow and indexing are proven useful.
- Pressure-test schema changes on real sample files before adding new machinery.
- Prefer the smallest working indexing and recall path before broader features.

## 5. Tooling

- Manage Python execution in this project with `uv`.
- Prefer `uv run python ...` over direct `python ...`.

## 6. Round Closure

- At the end of each meaningful round, inspect the current project for remaining
  problems before closing the turn.
- This close-out inspection must explicitly consider:
  - control-state drift or schema drift
  - guard or transition holes
  - sample-file pollution or fidelity regressions
  - validation gaps between claimed behavior and observed behavior
- Do not wait for the user to ask "what is still wrong"; surface the current
  problems proactively in the round close-out.
