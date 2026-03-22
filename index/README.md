# Index

`memory.sqlite` is a derived artifact built from Markdown source files.

Current builder:

- `scripts/build_index.py`
- `scripts/query_index.py`
- `scripts/assemble_context.py`
- `scripts/session_memory.py`

Current contract:

- scans `projects/` and `cross-project/`
- parses frontmatter from Markdown memory objects
- writes:
  - `memory_items`
  - `memory_paths`
  - `memory_evidence_refs`

Rebuild command:

```bash
uv run python scripts/build_index.py
```

Unified CLI:

```bash
uv run python scripts/session_memory.py build-index
```

Smoke check:

```bash
uv run python scripts/session_memory.py smoke
```

Example query:

```bash
uv run python scripts/session_memory.py query --project-id wind-agent --type decision
```

Example context assembly:

```bash
uv run python scripts/session_memory.py assemble --project-id wind-agent --output artifacts/wind-agent/session-context.md
```
