"""GrowthOS configuration using Pydantic Settings."""

from functools import lru_cache
from pathlib import Path
from typing import Optional

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings with environment variable support."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # Core
    USE_SQLITE: bool = Field(
        default=False,
        description="Enable SQLite read/write (default: False, CSV only)",
    )
    DATABASE_URL: str = Field(
        default="sqlite:///data/growthos.db",
        description="SQLite database URL",
    )

    # Feature flags (all False by default for safe rollout)
    USE_GROWTHOS_CALENDAR: bool = Field(default=False)
    USE_GROWTHOS_PUBLISH: bool = Field(default=False)
    USE_GROWTHOS_METRICS: bool = Field(default=False)
    USE_GROWTHOS_RECONCILE: bool = Field(default=False)
    USE_GROWTHOS_REELS: bool = Field(default=False)
    USE_GROWTHOS_COMMUNITY: bool = Field(default=False)
    USE_GROWTHOS_AFFILIATES: bool = Field(default=False)

    # Meta Graph API (configured but not used until Phase 3)
    META_ACCESS_TOKEN: Optional[str] = Field(default=None)
    META_APP_SECRET: Optional[str] = Field(default=None)
    META_PAGE_ID: str = Field(default="1036844829507460")
    META_IG_USER_ID: Optional[str] = Field(default=None)

    # Behavior
    MOCK_META_API: bool = Field(default=True, description="Mock Meta API calls for dev/test")
    CSV_ROUNDTRIP_STRICT: bool = Field(default=True, description="Validate semantic CSV round-trip")
    LOG_LEVEL: str = Field(default="INFO")

    # Paths
    ROOT_DIR: Path = Field(default_factory=lambda: Path(__file__).resolve().parents[2])
    DATA_DIR: Path = Field(default_factory=lambda: Path(__file__).resolve().parents[2] / "data")
    GROWTHOS_DIR: Path = Field(default_factory=lambda: Path(__file__).resolve().parents[2] / "GrowthOS")
    OPERATIONS_DIR: Path = Field(default_factory=lambda: Path(__file__).resolve().parents[2] / "Operations")

    @property
    def sqlite_path(self) -> Path:
        """Extract file path from sqlite:/// URL."""
        if self.DATABASE_URL.startswith("sqlite:///"):
            return Path(self.DATABASE_URL.replace("sqlite:///", ""))
        return self.DATA_DIR / "growthos.db"


@lru_cache
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()


settings = get_settings()
