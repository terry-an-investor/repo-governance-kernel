from __future__ import annotations

import os
from pathlib import Path


REPO_ROOT_ENV_VAR = "REPO_GOVERNANCE_ROOT"
PACKAGE_ROOT = Path(__file__).resolve().parent.parent


def resolve_repo_root() -> Path:
    override = os.environ.get(REPO_ROOT_ENV_VAR, "").strip()
    if override:
        return Path(override).expanduser().resolve()

    cwd = Path.cwd().resolve()
    if (cwd / ".git").exists() or (cwd / "projects").exists():
        return cwd

    return PACKAGE_ROOT


def resolve_index_path() -> Path:
    return resolve_repo_root() / "index" / "memory.sqlite"
