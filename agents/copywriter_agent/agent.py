"""Compatibilidad: el código vive en ``modules.creative.agents.copywriter_agent.agent``."""

import sys
from pathlib import Path

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from modules.creative.agents.copywriter_agent.agent import *  # noqa: F401,F403

if __name__ == "__main__":
    raise SystemExit(main())
