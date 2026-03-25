# Index

`memory.sqlite` is a derived artifact built from Markdown source files.

Current builder:

- `scripts/build_index.py`
- `scripts/query_index.py`
- `scripts/assemble_context.py`
- `scripts/repo_governance_kernel.py`

Current contract:

- scans `state/` and `cross-project/`
- parses frontmatter from Markdown memory objects
- writes:
  - `memory_items`
  - `memory_paths`
  - `memory_evidence_refs`

Rebuild command:

```powershell
uv run python scripts/build_index.py
```

Unified CLI:

```powershell
uv run python scripts/repo_governance_kernel.py build-index
```

Smoke check:

```powershell
uv run python scripts/repo_governance_kernel.py smoke
```

Example query:

```powershell
uv run python scripts/repo_governance_kernel.py query --project-id repo-governance-kernel --text workspace
```

Example context assembly:

```powershell
uv run python scripts/repo_governance_kernel.py assemble --project-id repo-governance-kernel --output artifacts/repo-governance-kernel/session-context.md
```
