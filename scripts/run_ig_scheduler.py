#!/usr/bin/env python3
"""Entrypoint del timer de Instagram.

Evita el doble import de ``python -m`` (modules.social ya importa el módulo).
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from modules.social.ig_scheduler import main

if __name__ == "__main__":
    raise SystemExit(main() or 0)
