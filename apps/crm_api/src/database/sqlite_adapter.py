from __future__ import annotations

from pathlib import Path
import sqlite3
from typing import Any

from src.database.base import DatabaseAdapter
from src.utils.logger import log_info


def create_sqlite_connection(db_path: str = ":memory:") -> sqlite3.Connection:
    """Create a sqlite3 connection configured with row dictionary factory and foreign keys enabled.

    Args:
        db_path: Database filepath or ":memory:".

    Returns:
        Configured `sqlite3.Connection`.
    """
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn


def apply_migrations(conn: sqlite3.Connection, migrations_dir: Path | str | None = None) -> None:
    """Apply all repository SQL migration files in sequence to the SQLite database.

    Args:
        conn: Target `sqlite3.Connection`.
        migrations_dir: Path to directory containing migration .sql files.
    """
    if migrations_dir is None:
        # Search parent directories for migrations folder
        curr = Path(__file__).resolve()
        for parent in curr.parents:
            candidate = parent / "migrations"
            if candidate.exists() and candidate.is_dir():
                migrations_dir = candidate
                break

    if migrations_dir is None:
        log_info("Migrations directory not found, skipping migration application.")
        return

    migrations_path = Path(migrations_dir)
    sql_files = sorted(migrations_path.glob("*.sql"))
    cursor = conn.cursor()
    for sql_file in sql_files:
        log_info(f"Applying database migration: {sql_file.name}")
        sql_script = sql_file.read_text(encoding="utf-8")
        cursor.executescript(sql_script)
    conn.commit()


def get_test_database_adapter() -> DatabaseAdapter:
    """Instantiate a DatabaseAdapter backed by an in-memory SQLite database pre-loaded with schema migrations.

    Returns:
        Pre-configured `DatabaseAdapter`.
    """
    conn = create_sqlite_connection(":memory:")
    apply_migrations(conn)
    return DatabaseAdapter(connection=conn)
