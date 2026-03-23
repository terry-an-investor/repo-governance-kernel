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
- Use Win11-native tooling for this repo: prefer PowerShell and `C:\Program Files\Git\cmd\git.exe`.
- Do not invoke `bash.exe`, WSL shells, `/usr/bin/git`, or `/mnt/...` paths for repository work.
- Treat Windows paths such as `C:/Users/...` as canonical in docs, scripts, and validation.
- Install and keep repository git hooks active through `uv run python scripts/install_hooks.py`.
- Treat `.githooks/pre-commit` and `.githooks/pre-push` as part of the control
  plane, not optional local convenience.
- Keep `.github/workflows/control-enforcement.yml` aligned with the same
  owner-layer enforcement commands used by local hooks.

## 6. Automatic Enforcement

- Do not hand-wave uncontrolled code changes as "just temporary".
- Dirty non-control paths outside the active round scope are a blocked state.
- Direct manual edits to projected control files such as `control/active-round.md`
  are a blocked state unless the file still exactly matches the durable
  projection rebuilt by commands.
- Dirty paths under constitution-declared guarded exception zones are a blocked
  state unless one active exception contract explicitly covers them.
- `captured` and `closed` round transitions must pass automatic worktree
  enforcement before promotion is allowed.
- Treat repository-local enforcement as the canonical owner layer.
- Treat CI as another trigger surface for the same owner-layer commands, not a
  separate policy implementation.
- Do not rely on Codex or Claude harness-specific native hooks for correctness.
- When a harness offers native hooks, use them only as an extra trigger path
  into the same repo-owned enforcement command.

## 7. Round Closure

- At the end of each meaningful round, inspect the current project for remaining
  problems before closing the turn.
- This close-out inspection must explicitly consider:
  - control-state drift or schema drift
  - guard or transition holes
  - sample-file pollution or fidelity regressions
  - validation gaps between claimed behavior and observed behavior
- Do not wait for the user to ask "what is still wrong"; surface the current
  problems proactively in the round close-out.
