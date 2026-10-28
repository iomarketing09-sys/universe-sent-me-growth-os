"""Compatibilidad: el código vive en ``modules.intelligence.experiment_log``."""

from modules.intelligence.experiment_log import *  # noqa: F401,F403

if __name__ == "__main__":
    import runpy
    import sys

    # Evita el RuntimeWarning de runpy: el shim ya importó el módulo real.
    sys.modules.pop("modules.intelligence.experiment_log", None)
    runpy.run_module("modules.intelligence.experiment_log", run_name="__main__")
