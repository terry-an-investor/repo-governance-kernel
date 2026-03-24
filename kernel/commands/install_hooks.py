#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import subprocess
from pathlib import Path

from kernel.runtime_paths import resolve_repo_root


PRE_COMMIT_TEXT = """#!/usr/bin/env sh
set -eu

repo-governance-kernel --repo-root "{repo_root}" audit-control-state --project-id {project_id}
repo-governance-kernel --repo-root "{repo_root}" enforce-worktree --project-id {project_id}
"""

PRE_PUSH_TEXT = """#!/usr/bin/env sh
set -eu

repo-governance-kernel --repo-root "{repo_root}" audit-control-state --project-id {project_id}
repo-governance-kernel --repo-root "{repo_root}" enforce-worktree --project-id {project_id}
"""


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Install repo-local governance git hooks for one host project.")
    parser.add_argument("--project-id", required=True)
    return parser.parse_args()


def write_hook(path: Path, text: str) -> None:
    path.write_text(text, encoding="utf-8", newline="\n")
    path.chmod(0o755)


def install_repo_hooks(root: Path, project_id: str) -> dict[str, object]:
    git_dir = root / ".git"
    if not git_dir.exists():
        raise SystemExit(f"git repository not found at {root}")

    hooks_dir = root / ".githooks"
    hooks_dir.mkdir(parents=True, exist_ok=True)
    repo_root = str(root).replace("\\", "/")
    write_hook(hooks_dir / "pre-commit", PRE_COMMIT_TEXT.format(project_id=project_id, repo_root=repo_root))
    write_hook(hooks_dir / "pre-push", PRE_PUSH_TEXT.format(project_id=project_id, repo_root=repo_root))

    subprocess.run(
        ["git", "config", "core.hooksPath", str(hooks_dir)],
        cwd=str(root),
        check=True,
    )
    return {
        "status": "ok",
        "repo_root": str(root),
        "project_id": project_id,
        "hooks_path": str(hooks_dir),
        "installed_hooks": ["pre-commit", "pre-push"],
    }


def main() -> int:
    args = parse_args()
    root = resolve_repo_root()
    result = install_repo_hooks(root, args.project_id)

    print(
        json.dumps(result, ensure_ascii=True, indent=2)
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
