"""Compatibilidad: el código vive en ``modules.intelligence.planner``."""

from modules.intelligence.planner import *  # noqa: F401,F403

if __name__ == "__main__":
    import runpy
    import sys

    # Evita el RuntimeWarning de runpy: el shim ya importó el módulo real.
    sys.modules.pop("modules.intelligence.planner", None)
    runpy.run_module("modules.intelligence.planner", run_name="__main__")
