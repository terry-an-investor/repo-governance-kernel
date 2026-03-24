#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import subprocess
from pathlib import Path

from kernel.runtime_paths import resolve_repo_root


CONSTITUTION_TEXT = """# Constitution

## Product Boundaries

- Keep repo governance explicit and file-first.
- Do not allow uncontrolled scope expansion or hidden private semantics.

## Architecture Invariants

- Control truth lives under `projects/{project_id}/memory/`.
- Projected control state lives under `projects/{project_id}/control/` and `projects/{project_id}/current/`.
- Repo-local hooks and CI call the shared kernel rather than owning private policy logic.

## Quality Bar

- Promotion and closure require passing control audit and worktree enforcement.
- Dirty non-control paths must stay inside active round and active task scope when present.

## Validation Rules

### Audit Hooks

- current_task_mentions_active_objective
- current_task_mentions_active_round
- current_task_phase_matches_active_objective

## Forbidden Shortcuts

- Do not bypass repo-owned audit or worktree enforcement.
- Do not add private bundle or executor semantics outside the registry-owned owner layer.

## Guarded Exception Paths

_none recorded_
"""

CURRENT_TASK_TEXT = """# Current Task

## Goal

Bootstrap repo governance for this host repository.

## Current State

- Project: `{project_id}`
- Objective id: ``
- Active round id: ``
- Phase: ``
- Workspace root: `{workspace_root}`

## Validated Facts

- Governance bootstrap completed for this repository.
- Repo-local hooks were installed to call the shared kernel CLI.

## Active Risks

- Repo-specific policy still needs refinement beyond the bootstrap constitution.

## Next Steps

1. Open the first active objective.
2. Move the objective into execution and open the first bounded round.
3. Refine constitution invariants and guarded paths as real project evidence appears.
"""

PIVOT_LOG_TEXT = """# Pivot Log

_none recorded_
"""

EXCEPTION_LEDGER_TEXT = """# Exception Ledger

_none recorded_
"""


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Bootstrap the minimal repo-local governance surface for a host repository.")
    parser.add_argument("--project-id", required=True)
    parser.add_argument("--skip-hooks", action="store_true")
    return parser.parse_args()


def ensure_file(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not path.exists():
        path.write_text(text, encoding="utf-8", newline="\n")


def ensure_gitignore_line(path: Path, line: str) -> None:
    existing = path.read_text(encoding="utf-8") if path.exists() else ""
    lines = [candidate.rstrip("\n") for candidate in existing.splitlines()]
    if line not in lines:
        lines.append(line)
        path.write_text("\n".join(lines).strip() + "\n", encoding="utf-8", newline="\n")


def main() -> int:
    args = parse_args()
    root = resolve_repo_root()
    if not (root / ".git").exists():
        raise SystemExit(f"git repository not found at {root}")

    project_root = root / "projects" / args.project_id
    for relative in [
        "artifacts",
        "control",
        "current",
        "memory/objectives",
        "memory/rounds",
        "memory/task-contracts",
        "memory/exception-contracts",
        "memory/adjudications",
        "memory/pivots",
        "memory/transition-events",
        "memory/decisions",
        "memory/failures",
        "memory/handoffs",
        "memory/patterns",
        "memory/constraints",
        "snapshots",
    ]:
        (project_root / relative).mkdir(parents=True, exist_ok=True)

    ensure_file(
        project_root / "control" / "constitution.md",
        CONSTITUTION_TEXT.format(project_id=args.project_id),
    )
    ensure_file(project_root / "control" / "pivot-log.md", PIVOT_LOG_TEXT)
    ensure_file(project_root / "control" / "exception-ledger.md", EXCEPTION_LEDGER_TEXT)
    ensure_file(
        project_root / "current" / "current-task.md",
        CURRENT_TASK_TEXT.format(project_id=args.project_id, workspace_root=str(root).replace("\\", "/")),
    )
    ensure_file(project_root / "current" / "blockers.md", "# Blockers\n\n_none recorded_\n")
    ensure_file(project_root / "current" / "idea-inbox.md", "# Idea Inbox\n\n_none recorded_\n")
    ensure_file(root / "cross-project" / ".gitkeep", "")
    ensure_file(root / "index" / ".gitkeep", "")

    hook_result: dict[str, object] | None = None
    if not args.skip_hooks:
        completed = subprocess.run(
            [
                "repo-governance-kernel",
                "--repo-root",
                str(root),
                "install-hooks",
                "--project-id",
                args.project_id,
            ],
            cwd=str(root),
            capture_output=True,
            text=True,
            check=False,
        )
        if completed.returncode != 0:
            raise SystemExit(completed.stderr.strip() or completed.stdout.strip() or "failed to install hooks")
        hook_result = json.loads(completed.stdout)

    print(
        json.dumps(
            {
                "status": "ok",
                "repo_root": str(root),
                "project_id": args.project_id,
                "project_root": str(project_root),
                "installed_hooks": hook_result.get("installed_hooks", []) if hook_result else [],
                "bootstrap_created": [
                    "projects/<project_id>/control/constitution.md",
                    "projects/<project_id>/control/pivot-log.md",
                    "projects/<project_id>/control/exception-ledger.md",
                    "projects/<project_id>/current/current-task.md",
                    ".githooks/pre-commit",
                    ".githooks/pre-push",
                ],
            },
            ensure_ascii=True,
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
