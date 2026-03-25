#!/usr/bin/env python3
from __future__ import annotations

import os
import shutil
from pathlib import Path


WINDOWS_GIT_CANDIDATES = (
    Path(r"C:\Program Files\Git\cmd\git.exe"),
    Path(r"C:\Program Files (x86)\Git\cmd\git.exe"),
)
GIT_OVERRIDE_ENV = "REPO_GOVERNANCE_GIT_EXE"


def resolve_git_executable() -> str:
    override = os.environ.get(GIT_OVERRIDE_ENV, "").strip()
    if override:
        return override

    if os.name == "nt":
        for candidate in WINDOWS_GIT_CANDIDATES:
            if candidate.exists():
                return str(candidate)

    for candidate_name in ("git", "git.exe"):
        resolved = shutil.which(candidate_name)
        if resolved:
            return resolved

    raise SystemExit(
        f"git executable not found; install git or set {GIT_OVERRIDE_ENV}"
    )


GIT_EXE = resolve_git_executable()
