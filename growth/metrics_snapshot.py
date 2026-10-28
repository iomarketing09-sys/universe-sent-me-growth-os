"""Compatibilidad: el código vive en ``modules.intelligence.metrics_snapshot``."""

from modules.intelligence.metrics_snapshot import *  # noqa: F401,F403

if __name__ == "__main__":
    import runpy
    import sys

    # Evita el RuntimeWarning de runpy: el shim ya importó el módulo real.
    sys.modules.pop("modules.intelligence.metrics_snapshot", None)
    runpy.run_module("modules.intelligence.metrics_snapshot", run_name="__main__")
