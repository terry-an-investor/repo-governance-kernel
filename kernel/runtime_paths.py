from __future__ import annotations

import os
from pathlib import Path


REPO_ROOT_ENV_VAR = "REPO_GOVERNANCE_ROOT"
PACKAGE_ROOT = Path(__file__).resolve().parent.parent
STATE_ROOT_DIRNAME = "state"


def resolve_package_root() -> Path:
    return PACKAGE_ROOT


def resolve_repo_root() -> Path:
    override = os.environ.get(REPO_ROOT_ENV_VAR, "").strip()
    if override:
        return Path(override).expanduser().resolve()

    cwd = Path.cwd().resolve()
    if (cwd / ".git").exists() or (cwd / STATE_ROOT_DIRNAME).exists():
        return cwd

    return PACKAGE_ROOT


def resolve_state_root(repo_root: Path | None = None) -> Path:
    root = repo_root or resolve_repo_root()
    return root / STATE_ROOT_DIRNAME


def resolve_project_state_root(project_id: str, repo_root: Path | None = None) -> Path:
    return resolve_state_root(repo_root) / project_id


def render_project_state_prefix(project_id: str) -> str:
    return f"{STATE_ROOT_DIRNAME}/{project_id}/"


def resolve_index_path() -> Path:
    return resolve_repo_root() / "index" / "memory.sqlite"
