#!/usr/bin/env python3
from __future__ import annotations

import json

from kernel.public_alpha_surface import describe_public_alpha_surface


def main() -> int:
    print(json.dumps(describe_public_alpha_surface(), ensure_ascii=True, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
