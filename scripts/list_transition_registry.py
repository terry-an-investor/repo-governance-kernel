#!/usr/bin/env python3
from __future__ import annotations

import json

from transition_specs import export_transition_registry


def main() -> int:
    print(json.dumps(export_transition_registry(), ensure_ascii=True, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
