#!/usr/bin/env python3
"""CLI para inspeccionar y liberar el estado de publicación de Social."""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from modules.social.publish_state import main


if __name__ == "__main__":
    raise SystemExit(main())
