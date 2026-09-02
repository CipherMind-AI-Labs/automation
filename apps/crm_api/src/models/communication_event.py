from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass
class CommunicationEvent:
    """Domain model representing a webhook event associated with a communication message."""

    id: int | None = None
    communication_id: int | None = None
    event_type: str | None = None
    occurred_at: str | None = None
    provider_event_id: str | None = None
    metadata_json: str | None = None
    created_at: str | None = None

    @classmethod
    def from_row(cls, row: dict[str, Any]) -> CommunicationEvent:
        """Construct CommunicationEvent from database row dict."""
        return cls(
            id=row.get("id"),
            communication_id=row.get("communication_id"),
            event_type=row.get("event_type"),
            occurred_at=row.get("occurred_at"),
            provider_event_id=row.get("provider_event_id"),
            metadata_json=row.get("metadata_json"),
            created_at=row.get("created_at"),
        )

    def to_dict(self) -> dict[str, Any]:
        """Serialize CommunicationEvent into a dictionary."""
        return {
            "id": self.id,
            "communication_id": self.communication_id,
            "event_type": self.event_type,
            "occurred_at": self.occurred_at,
            "provider_event_id": self.provider_event_id,
            "metadata_json": self.metadata_json,
            "created_at": self.created_at,
        }
