"""Repository classes for GrowthOS entities using CSV storage."""

import sys
from pathlib import Path
from typing import List, Type, TypeVar, Optional

# Add the project root to sys.path to allow absolute imports
REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.append(str(REPO_ROOT))

from core.models import Piece, Publication, Experiment, CommunityEngagement, MetricsSnapshot, AssetAlias
from storage.csv_adapter import PieceCSVAdapter, CSVAdapter

T = TypeVar('T')


class BaseRepository:
    """Base repository with common CRUD operations using CSV."""

    def __init__(self, csv_path: Path, account_id: Optional[str] = None):
        self.account_id = account_id
        # Modify path to include account_id if provided
        if account_id:
            # Insert account_id before the file extension
            stem = csv_path.stem
            suffix = csv_path.suffix
            self.csv_path = csv_path.parent / f"{stem}_{account_id}{suffix}"
        else:
            self.csv_path = csv_path
        self.adapter = CSVAdapter(self.csv_path)

    def count(self) -> int:
        """Count rows in CSV file."""
        return len(self.read_all())

    def exists(self, **kwargs) -> bool:
        """Check if record exists matching kwargs."""
        records = self.read_all()
        for record in records:
            match = True
            for key, value in kwargs.items():
                if getattr(record, key, None) != value:
                    match = False
                    break
            if match:
                return True
        return False

    def read_all(self) -> List[T]:
        """Read all records from CSV."""
        # This should be overridden by subclasses
        raise NotImplementedError

    def save(self, record: T) -> None:
        """Save record to CSV (append or update)."""
        records = self.read_all()
        # Remove existing record with same ID if it exists
        # For simplicity, we'll just append and deduplicate on read
        # In a real implementation, we'd want to update in place
        records.append(record)
        self._write_all(records)

    def get_all(self) -> List[T]:
        """Get all records."""
        return self.read_all()

    def _write_all(self, records: List[T]) -> None:
        """Write all records to CSV."""
        # This should be overridden by subclasses
        raise NotImplementedError


class PieceRepository(BaseRepository):
    """Repository for Piece entities using CSV."""

    def __init__(self, csv_path: Path, account_id: Optional[str] = None):
        super().__init__(csv_path, account_id)
        self.adapter = PieceCSVAdapter(self.csv_path)

    def read_all(self) -> List[Piece]:
        """Read all pieces from CSV."""
        return self.adapter.read_all(Piece)

    def _write_all(self, records: List[Piece]) -> None:
        """Write all pieces to CSV."""
        self.adapter.write_all(Piece, records)


class PublicationRepository(BaseRepository):
    """Repository for Publication entities using CSV."""

    def __init__(self, csv_path: Path, account_id: Optional[str] = None):
        super().__init__(csv_path, account_id)

    def read_all(self) -> List[Publication]:
        """Read all publications from CSV."""
        return self.adapter.read_all(Publication)

    def _write_all(self, records: List[Publication]) -> None:
        """Write all publications to CSV."""
        self.adapter.write_all(Publication, records)


class ExperimentRepository(BaseRepository):
    """Repository for Experiment entities using CSV."""

    def __init__(self, csv_path: Path, account_id: Optional[str] = None):
        super().__init__(csv_path, account_id)

    def read_all(self) -> List[Experiment]:
        """Read all experiments from CSV."""
        return self.adapter.read_all(Experiment)

    def _write_all(self, records: List[Experiment]) -> None:
        """Write all experiments to CSV."""
        self.adapter.write_all(Experiment, records)


class CommunityEngagementRepository(BaseRepository):
    """Repository for Community Engagement entities using CSV."""

    def __init__(self, csv_path: Path, account_id: Optional[str] = None):
        super().__init__(csv_path, account_id)

    def read_all(self) -> List[CommunityEngagement]:
        """Read all community engagements from CSV."""
        return self.adapter.read_all(CommunityEngagement)

    def _write_all(self, records: List[CommunityEngagement]) -> None:
        """Write all community engagements to CSV."""
        self.adapter.write_all(CommunityEngagement, records)


class MetricsSnapshotRepository(BaseRepository):
    """Repository for Metrics Snapshot entities using CSV."""

    def __init__(self, csv_path: Path, account_id: Optional[str] = None):
        super().__init__(csv_path, account_id)

    def read_all(self) -> List[MetricsSnapshot]:
        """Read all metrics snapshots from CSV."""
        return self.adapter.read_all(MetricsSnapshot)

    def _write_all(self, records: List[MetricsSnapshot]) -> None:
        """Write all metrics snapshots to CSV."""
        self.adapter.write_all(MetricsSnapshot, records)


class AssetAliasRepository(BaseRepository):
    """Repository for Asset Alias entities using CSV."""

    def __init__(self, csv_path: Path, account_id: Optional[str] = None):
        super().__init__(csv_path, account_id)

    def read_all(self) -> List[AssetAlias]:
        """Read all asset aliases from CSV."""
        return self.adapter.read_all(AssetAlias)

    def _write_all(self, records: List[AssetAlias]) -> None:
        """Write all asset aliases to CSV."""
        self.adapter.write_all(AssetAlias, records)
