"""GrowthOS Package"""
import sys

# Import core submodules
from growthos.core import models
from growthos.core import enums
from growthos.core import validators

# Import storage submodules
from growthos.storage import csv_adapter
from growthos.storage import repositories
from growthos.storage import database

# Re-export core
from growthos.core import models as core_models
from growthos.core import enums as core_enums
from growthos.core import validators as core_validators

# Re-export storage
from growthos.storage import csv_adapter as storage_csv_adapter
from growthos.storage import repositories as storage_repositories
from growthos.storage import database as storage_database

# Alias for backward compatibility
core = type(sys)("growthos.core")
core.models = core_models
core.enums = core_enums
core.validators = core_validators

storage = type(sys)("growthos.storage")
storage.csv_adapter = storage_csv_adapter
storage.repositories = storage_repositories
storage.database = storage_database

__all__ = [
    "models",
    "enums",
    "validators",
    "csv_adapter",
    "repositories",
    "database",
    "core",
    "storage",
]

__version__ = "1.0.0"
