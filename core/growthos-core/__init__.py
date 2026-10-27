"""GrowthOS Core Package
=====================

Core domain models, enums, storage, and integrations for Growth OS.
"""

import sys
from pathlib import Path

# Add the growthos package to path for absolute imports
_pkg_path = Path(__file__).parent
sys.path.insert(0, str(_pkg_path))

from growthos.core import models, enums
from growthos.storage import csv_adapter, repositories

__all__ = [
    "models",
    "enums", 
    "csv_adapter",
    "repositories",
]

__version__ = "1.0.0"
