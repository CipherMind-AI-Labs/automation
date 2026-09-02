from __future__ import annotations

from typing import Any

from src.database.base import DatabaseAdapter
from src.models.research_source import ResearchSource


class ResearchSourceRepository:
    """Repository for ResearchSource operations."""

    def __init__(self, database: DatabaseAdapter) -> None:
        """Initialize repository with DatabaseAdapter."""
        self.database = database

    def list_by_profile_id(self, research_profile_id: int) -> list[ResearchSource]:
        """Fetch list of research sources for a research profile.

        Args:
            research_profile_id: Target profile ID.

        Returns:
            List of ResearchSource models.
        """
        rows = self.database.execute(
            "SELECT id, research_profile_id, source_type, source_name, source_url, notes, created_at FROM research_sources WHERE research_profile_id = ? ORDER BY id ASC",
            [research_profile_id],
        )
        return [ResearchSource.from_row(row) for row in rows]

    def get_by_id(self, source_id: int) -> ResearchSource | None:
        """Fetch ResearchSource by primary key ID.

        Args:
            source_id: Source record ID.

        Returns:
            ResearchSource model or None.
        """
        rows = self.database.execute(
            "SELECT id, research_profile_id, source_type, source_name, source_url, notes, created_at FROM research_sources WHERE id = ?",
            [source_id],
        )
        if not rows:
            return None
        return ResearchSource.from_row(rows[0])

    def create(self, source: ResearchSource) -> ResearchSource:
        """Create a new research source record.

        Args:
            source: ResearchSource to persist.

        Returns:
            ResearchSource model with created ID.
        """
        sql = """
            INSERT INTO research_sources (
                research_profile_id, source_type, source_name, source_url, notes
            ) VALUES (?, ?, ?, ?, ?)
        """
        params = [
            source.research_profile_id,
            source.source_type,
            source.source_name,
            source.source_url,
            source.notes,
        ]
        inserted = self.database.execute(sql, params)
        if inserted and "id" in inserted[0]:
            source.id = inserted[0]["id"]
        return source

    def delete(self, source_id: int) -> bool:
        """Delete research source by ID.

        Args:
            source_id: Target source ID.

        Returns:
            True if deletion was executed.
        """
        self.database.execute("DELETE FROM research_sources WHERE id = ?", [source_id])
        return True
