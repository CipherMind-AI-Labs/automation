from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass
class ResearchSource:
    """Domain model representing a research citation or reference source."""

    id: int | None = None
    research_profile_id: int | None = None
    source_type: str | None = None
    source_name: str | None = None
    source_url: str | None = None
    notes: str | None = None
    created_at: str | None = None

    @classmethod
    def from_row(cls, row: dict[str, Any]) -> ResearchSource:
        """Construct ResearchSource from database row dict."""
        return cls(
            id=row.get("id"),
            research_profile_id=row.get("research_profile_id"),
            source_type=row.get("source_type"),
            source_name=row.get("source_name") or "",
            source_url=row.get("source_url"),
            notes=row.get("notes"),
            created_at=row.get("created_at"),
        )

    def to_dict(self) -> dict[str, Any]:
        """Serialize ResearchSource into a dictionary."""
        return {
            "id": self.id,
            "research_profile_id": self.research_profile_id,
            "source_type": self.source_type,
            "source_name": self.source_name,
            "source_url": self.source_url,
            "notes": self.notes,
            "created_at": self.created_at,
        }
