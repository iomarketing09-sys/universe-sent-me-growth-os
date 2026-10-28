"""Compatibilidad: el código vive en ``modules.intelligence.historical_baseline``."""

from modules.intelligence.historical_baseline import *  # noqa: F401,F403

if __name__ == "__main__":
    import runpy
    import sys

    # Evita el RuntimeWarning de runpy: el shim ya importó el módulo real.
    sys.modules.pop("modules.intelligence.historical_baseline", None)
    runpy.run_module("modules.intelligence.historical_baseline", run_name="__main__")
