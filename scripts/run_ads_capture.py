#!/usr/bin/env python3
"""Entrypoint del timer de cortes de métricas para campañas de Ads."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from modules.intelligence.campaign_capture import main


if __name__ == "__main__":
    raise SystemExit(main())
