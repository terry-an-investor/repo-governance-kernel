#!/usr/bin/env python3
from __future__ import annotations

import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
HOOKS_DIR = ROOT / ".githooks"


def main() -> int:
    if not (ROOT / ".git").exists():
        raise SystemExit(f"git repository not found at {ROOT}")
    if not HOOKS_DIR.exists():
        raise SystemExit(f"hooks directory not found: {HOOKS_DIR}")

    subprocess.run(["git", "config", "core.hooksPath", str(HOOKS_DIR)], cwd=str(ROOT), check=True)
    print(
        json.dumps(
            {
                "status": "ok",
                "hooks_path": str(HOOKS_DIR),
            },
            ensure_ascii=True,
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
