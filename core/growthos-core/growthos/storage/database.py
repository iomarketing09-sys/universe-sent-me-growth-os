"""SQLite database connection and migration management."""

import sqlite3
from contextlib import contextmanager
from pathlib import Path
from typing import Generator, Optional

from growthos.config import settings


class Database:
    """SQLite database wrapper with connection pooling."""

    def __init__(self, db_path: Optional[Path] = None):
        self.db_path = db_path or settings.sqlite_path
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._conn: Optional[sqlite3.Connection] = None

    def connect(self) -> sqlite3.Connection:
        """Get or create database connection."""
        if self._conn is None:
            self._conn = sqlite3.connect(
                self.db_path,
                detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES,
            )
            self._conn.row_factory = sqlite3.Row
            self._conn.execute("PRAGMA foreign_keys = ON")
            self._conn.execute("PRAGMA journal_mode = WAL")
        return self._conn

    def close(self) -> None:
        """Close database connection."""
        if self._conn:
            self._conn.close()
            self._conn = None

    @contextmanager
    def transaction(self) -> Generator[sqlite3.Connection, None, None]:
        """Context manager for database transactions."""
        conn = self.connect()
        try:
            yield conn
            conn.commit()
        except Exception:
            conn.rollback()
            raise

    def execute(self, sql: str, params: tuple = ()) -> sqlite3.Cursor:
        """Execute a single SQL statement."""
        conn = self.connect()
        return conn.execute(sql, params)

    def executemany(self, sql: str, params: list[tuple]) -> sqlite3.Cursor:
        """Execute many SQL statements."""
        conn = self.connect()
        return conn.executemany(sql, params)

    def fetchone(self, sql: str, params: tuple = ()) -> Optional[sqlite3.Row]:
        """Fetch single row."""
        return self.connect().execute(sql, params).fetchone()

    def fetchall(self, sql: str, params: tuple = ()) -> list[sqlite3.Row]:
        """Fetch all rows."""
        return self.connect().execute(sql, params).fetchall()

    def init_schema(self) -> None:
        """Initialize database schema from migration files."""
        migrations_dir = Path(__file__).parent / "migrations"
        if not migrations_dir.exists():
            return

        # Create schema_version table if not exists
        self.execute("""
            CREATE TABLE IF NOT EXISTS schema_version (
                version INTEGER PRIMARY KEY,
                applied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # Get applied migrations
        applied = {row["version"] for row in self.fetchall("SELECT version FROM schema_version")}

        # Apply pending migrations in order
        for migration_file in sorted(migrations_dir.glob("*.sql")):
            version_str = migration_file.stem.split("_")[0]
            try:
                version = int(version_str)
            except ValueError:
                continue

            if version in applied:
                continue

            sql = migration_file.read_text(encoding="utf-8")
            with self.transaction() as conn:
                conn.executescript(sql)
                conn.execute("INSERT INTO schema_version (version) VALUES (?)", (version,))


# Global database instance
_db: Optional[Database] = None


def get_db() -> Database:
    """Get global database instance."""
    global _db
    if _db is None:
        _db = Database()
    return _db


def init_db() -> Database:
    """Initialize database and run migrations."""
    db = get_db()
    db.init_schema()
    return db
