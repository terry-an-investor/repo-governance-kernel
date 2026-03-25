#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os

from kernel.config_runtime import CONFIG_RESOLUTION_ENV_VAR, resolve_runtime_config


def main() -> int:
    parser = argparse.ArgumentParser(description="Describe resolved repo_root and project_id config sources.")
    parser.add_argument("--project-id", default="")
    args = parser.parse_args()

    precomputed = os.environ.get(CONFIG_RESOLUTION_ENV_VAR, "").strip()
    if precomputed:
        payload = json.loads(precomputed)
    else:
        payload = resolve_runtime_config(explicit_project_id=args.project_id.strip())
    print(json.dumps(payload, ensure_ascii=True, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
