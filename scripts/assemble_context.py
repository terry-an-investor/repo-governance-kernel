#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from kernel.assemble_context import *  # noqa: F401,F403
from kernel.assemble_context import main


if __name__ == "__main__":
    main()
