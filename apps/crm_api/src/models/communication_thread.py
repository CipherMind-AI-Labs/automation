from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass
class CommunicationThread:
    """Domain model representing an email/message communication thread."""

    id: int | None = None
    company_id: int | None = None
    opportunity_id: int | None = None
    channel: str = "email"
    provider: str | None = None
    provider_thread_id: str | None = None
    subject: str | None = None
    thread_status: str = "Open"
    last_outbound_at: str | None = None
    last_inbound_at: str | None = None
    reply_due_at: str | None = None
    next_follow_up_due_at: str | None = None
    closed_at: str | None = None
    created_at: str | None = None
    updated_at: str | None = None

    @classmethod
    def from_row(cls, row: dict[str, Any]) -> CommunicationThread:
        """Construct CommunicationThread from database row dict."""
        return cls(
            id=row.get("id"),
            company_id=row.get("company_id"),
            opportunity_id=row.get("opportunity_id"),
            channel=row.get("channel") or "email",
            provider=row.get("provider"),
            provider_thread_id=row.get("provider_thread_id"),
            subject=row.get("subject"),
            thread_status=row.get("thread_status") or "Open",
            last_outbound_at=row.get("last_outbound_at"),
            last_inbound_at=row.get("last_inbound_at"),
            reply_due_at=row.get("reply_due_at"),
            next_follow_up_due_at=row.get("next_follow_up_due_at"),
            closed_at=row.get("closed_at"),
            created_at=row.get("created_at"),
            updated_at=row.get("updated_at"),
        )

    def to_dict(self) -> dict[str, Any]:
        """Serialize CommunicationThread into a dictionary."""
        return {
            "id": self.id,
            "company_id": self.company_id,
            "opportunity_id": self.opportunity_id,
            "channel": self.channel,
            "provider": self.provider,
            "provider_thread_id": self.provider_thread_id,
            "subject": self.subject,
            "thread_status": self.thread_status,
            "last_outbound_at": self.last_outbound_at,
            "last_inbound_at": self.last_inbound_at,
            "reply_due_at": self.reply_due_at,
            "next_follow_up_due_at": self.next_follow_up_due_at,
            "closed_at": self.closed_at,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }
