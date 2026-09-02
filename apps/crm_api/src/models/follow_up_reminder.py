from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass
class FollowUpReminder:
    """Domain model representing a scheduled follow-up reminder."""

    id: int | None = None
    opportunity_id: int | None = None
    thread_id: int | None = None
    contact_id: int | None = None
    reminder_type: str = "follow_up"
    status: str = "pending"
    due_at: str | None = None
    completed_at: str | None = None
    last_notified_at: str | None = None
    notes: str | None = None
    created_at: str | None = None
    updated_at: str | None = None

    @classmethod
    def from_row(cls, row: dict[str, Any]) -> FollowUpReminder:
        """Construct FollowUpReminder from database row dict."""
        return cls(
            id=row.get("id"),
            opportunity_id=row.get("opportunity_id"),
            thread_id=row.get("thread_id"),
            contact_id=row.get("contact_id"),
            reminder_type=row.get("reminder_type") or "follow_up",
            status=row.get("status") or "pending",
            due_at=row.get("due_at"),
            completed_at=row.get("completed_at"),
            last_notified_at=row.get("last_notified_at"),
            notes=row.get("notes"),
            created_at=row.get("created_at"),
            updated_at=row.get("updated_at"),
        )

    def to_dict(self) -> dict[str, Any]:
        """Serialize FollowUpReminder into a dictionary."""
        return {
            "id": self.id,
            "opportunity_id": self.opportunity_id,
            "thread_id": self.thread_id,
            "contact_id": self.contact_id,
            "reminder_type": self.reminder_type,
            "status": self.status,
            "due_at": self.due_at,
            "completed_at": self.completed_at,
            "last_notified_at": self.last_notified_at,
            "notes": self.notes,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }
