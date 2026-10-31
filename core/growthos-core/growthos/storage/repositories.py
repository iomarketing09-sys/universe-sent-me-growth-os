"""Repository classes for GrowthOS entities."""

import sqlite3
from typing import List, Optional, Type, TypeVar

from growthos.core.models import (
    Piece,
    Publication,
    Experiment,
    CommunityEngagement,
    MetricsSnapshot,
    AssetAlias,
    Deal,
)
from growthos.storage.database import Database

T = TypeVar("T")


class BaseRepository:
    """Base repository with common CRUD operations."""

    table_name: str = ""
    model: Type = None

    def __init__(self, db: Optional[Database] = None):
        self.db = db or Database()

    def count(self) -> int:
        """Count rows in table."""
        row = self.db.fetchone(f"SELECT COUNT(*) as c FROM {self.table_name}")
        return row["c"] if row else 0

    def exists(self, **kwargs) -> bool:
        """Check if row exists matching kwargs."""
        conditions = " AND ".join(f"{k} = ?" for k in kwargs)
        sql = f"SELECT 1 FROM {self.table_name} WHERE {conditions} LIMIT 1"
        return self.db.fetchone(sql, tuple(kwargs.values())) is not None


class PieceRepository(BaseRepository):
    """Repository for Piece entities."""

    table_name = "pieces"
    model = Piece

    def save(self, piece: Piece) -> None:
        """Save piece to database (insert or replace)."""
        data = piece.model_dump()
        # Keep only real table columns. Piece allows extra CSV fields, but
        # SQLite must not receive columns that are not part of the schema.
        table_columns = {
            row["name"]
            for row in self.db.fetchall(f"PRAGMA table_info({self.table_name})")
        }
        columns = [
            k for k, v in data.items()
            if v is not None and k in table_columns
        ]
        values = [data[k] for k in columns]

        placeholders = ", ".join("?" * len(columns))
        column_names = ", ".join(columns)

        sql = f"""
            INSERT OR REPLACE INTO {self.table_name} ({column_names})
            VALUES ({placeholders})
        """
        self.db.execute(sql, tuple(values))

    def get_by_id(self, id_pieza: str) -> Optional[Piece]:
        """Get piece by ID."""
        row = self.db.fetchone(
            f"SELECT * FROM {self.table_name} WHERE id_pieza = ?", (id_pieza,)
        )
        return self.model(**dict(row)) if row else None

    def get_all(self) -> List[Piece]:
        """Get all pieces."""
        rows = self.db.fetchall(f"SELECT * FROM {self.table_name}")
        return [self.model(**dict(r)) for r in rows]

    def get_approved_for_scheduling(self) -> List[Piece]:
        """Get pieces approved for scheduling."""
        rows = self.db.fetchall(
            f"SELECT * FROM {self.table_name} WHERE estado = 'Aprobado'"
        )
        return [self.model(**dict(r)) for r in rows]

    def get_reuse_candidates(self, reference_date=None) -> List[Piece]:
        """Get pieces eligible for reuse (30+ days since last publication)."""
        from growthos.core.validators import validate_30_day_rule

        all_pieces = self.get_all()
        candidates = []
        for piece in all_pieces:
            if validate_30_day_rule(piece, reference_date):
                candidates.append(piece)
        return candidates

    def count(self) -> int:
        row = self.db.fetchone(f"SELECT COUNT(*) as c FROM {self.table_name}")
        return row["c"] if row else 0


class PublicationRepository(BaseRepository):
    """Repository for Publication entities."""

    table_name = "publications"
    model = Publication

    def save(self, publication: Publication) -> None:
        data = publication.model_dump()
        columns = [k for k, v in data.items() if v is not None]
        values = [data[k] for k in columns]
        placeholders = ", ".join("?" * len(columns))
        column_names = ", ".join(columns)

        sql = f"""
            INSERT OR REPLACE INTO {self.table_name} ({column_names})
            VALUES ({placeholders})
        """
        self.db.execute(sql, tuple(values))

    def get_by_id(self, publicacion_id: str) -> Optional[Publication]:
        row = self.db.fetchone(
            f"SELECT * FROM {self.table_name} WHERE publicacion_id = ?",
            (publicacion_id,),
        )
        return self.model(**dict(row)) if row else None

    def get_by_meta_post_id(self, meta_post_id: str) -> Optional[Publication]:
        row = self.db.fetchone(
            f"SELECT * FROM {self.table_name} WHERE meta_post_id = ?",
            (meta_post_id,),
        )
        return self.model(**dict(row)) if row else None

    def get_all(self) -> List[Publication]:
        rows = self.db.fetchall(f"SELECT * FROM {self.table_name}")
        return [self.model(**dict(r)) for r in rows]


class ExperimentRepository(BaseRepository):
    """Repository for Experiment entities."""

    table_name = "experiments"
    model = Experiment

    def save(self, experiment: Experiment) -> None:
        data = experiment.model_dump()
        columns = [k for k, v in data.items() if v is not None]
        values = [data[k] for k in columns]
        placeholders = ", ".join("?" * len(columns))
        column_names = ", ".join(columns)

        sql = f"""
            INSERT OR REPLACE INTO {self.table_name} ({column_names})
            VALUES ({placeholders})
        """
        self.db.execute(sql, tuple(values))

    def get_all(self) -> List[Experiment]:
        rows = self.db.fetchall(f"SELECT * FROM {self.table_name}")
        return [self.model(**dict(r)) for r in rows]


class CommunityRepository(BaseRepository):
    """Repository for Community Engagement entities."""

    table_name = "community_engagement"
    model = CommunityEngagement

    def save(self, entry: CommunityEngagement) -> None:
        data = entry.model_dump()
        columns = [k for k, v in data.items() if v is not None]
        values = [data[k] for k in columns]
        placeholders = ", ".join("?" * len(columns))
        column_names = ", ".join(columns)

        sql = f"""
            INSERT OR REPLACE INTO {self.table_name} ({column_names})
            VALUES ({placeholders})
        """
        self.db.execute(sql, tuple(values))

    def get_all(self) -> List[CommunityEngagement]:
        rows = self.db.fetchall(f"SELECT * FROM {self.table_name}")
        return [self.model(**dict(r)) for r in rows]


class MetricsSnapshotRepository(BaseRepository):
    """Repository for Metrics Snapshot entities."""

    table_name = "metrics_snapshots"
    model = MetricsSnapshot

    def save(self, snapshot: MetricsSnapshot) -> None:
        data = snapshot.model_dump()
        columns = [k for k, v in data.items() if v is not None]
        values = [data[k] for k in columns]
        placeholders = ", ".join("?" * len(columns))
        column_names = ", ".join(columns)

        sql = f"""
            INSERT OR REPLACE INTO {self.table_name} ({column_names})
            VALUES ({placeholders})
        """
        self.db.execute(sql, tuple(values))

    def get_all(self) -> List[MetricsSnapshot]:
        rows = self.db.fetchall(f"SELECT * FROM {self.table_name}")
        return [self.model(**dict(r)) for r in rows]

    def get_valid_e0(self) -> List[MetricsSnapshot]:
        rows = self.db.fetchall(
            f"SELECT * FROM {self.table_name} WHERE validation_status = 'Valid_E0'"
        )
        return [self.model(**dict(r)) for r in rows]


class AssetAliasRepository(BaseRepository):
    """Repository for Asset Alias entities."""

    table_name = "asset_aliases"
    model = AssetAlias

    def save(self, alias: AssetAlias) -> None:
        data = alias.model_dump()
        columns = [k for k, v in data.items() if v is not None]
        values = [data[k] for k in columns]
        placeholders = ", ".join("?" * len(columns))
        column_names = ", ".join(columns)

        sql = f"""
            INSERT OR REPLACE INTO {self.table_name} ({column_names})
            VALUES ({placeholders})
        """
        self.db.execute(sql, tuple(values))

    def get_all(self) -> List[AssetAlias]:
        rows = self.db.fetchall(f"SELECT * FROM {self.table_name}")
        return [self.model(**dict(r)) for r in rows]


class DealRepository(BaseRepository):
    """Repository for revenue deals."""

    table_name = "deals"
    model = Deal

    def save(self, deal: Deal) -> None:
        data = deal.model_dump()
        columns = [key for key, value in data.items() if value is not None]
        values = [data[key] for key in columns]
        placeholders = ", ".join("?" * len(columns))
        column_names = ", ".join(columns)
        self.db.execute(
            f"INSERT OR REPLACE INTO {self.table_name} ({column_names}) VALUES ({placeholders})",
            tuple(values),
        )

    def get_by_id(self, deal_id: str) -> Optional[Deal]:
        row = self.db.fetchone(
            f"SELECT * FROM {self.table_name} WHERE deal_id = ?", (deal_id,)
        )
        return self.model(**dict(row)) if row else None

    def get_all(self) -> List[Deal]:
        rows = self.db.fetchall(f"SELECT * FROM {self.table_name}")
        return [self.model(**dict(row)) for row in rows]

    def get_by_tenant(self, tenant_id: str) -> List[Deal]:
        rows = self.db.fetchall(
            f"SELECT * FROM {self.table_name} WHERE tenant_id = ? ORDER BY created_at",
            (tenant_id,),
        )
        return [self.model(**dict(row)) for row in rows]

    def get_by_payment_status(self, payment_status: str) -> List[Deal]:
        rows = self.db.fetchall(
            f"SELECT * FROM {self.table_name} WHERE payment_status = ?",
            (payment_status,),
        )
        return [self.model(**dict(row)) for row in rows]
