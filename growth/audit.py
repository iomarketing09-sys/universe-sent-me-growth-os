"""Compatibilidad: el código vive en ``modules.intelligence.audit``."""

from modules.intelligence.audit import *  # noqa: F401,F403

if __name__ == "__main__":
    import runpy

    runpy.run_module("modules.intelligence.audit", run_name="__main__")
