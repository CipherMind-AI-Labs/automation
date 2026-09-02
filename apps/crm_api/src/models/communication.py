from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass
class Communication:
    """Domain model representing an individual communication message."""

    id: int | None = None
    thread_id: int | None = None
    contact_id: int | None = None
    channel: str = "email"
    direction: str = "outbound"
    provider: str | None = None
    provider_message_id: str | None = None
    in_reply_to_provider_message_id: str | None = None
    from_address: str | None = None
    to_addresses: str | None = None
    cc_addresses: str | None = None
    subject: str | None = None
    body_text: str | None = None
    body_html: str | None = None
    message_status: str = "draft"
    approval_status: str = "not_required"
    approved_by: str | None = None
    approved_at: str | None = None
    scheduled_for: str | None = None
    sent_at: str | None = None
    received_at: str | None = None
    delivered_at: str | None = None
    opened_at: str | None = None
    bounced_at: str | None = None
    failed_at: str | None = None
    created_at: str | None = None
    updated_at: str | None = None

    @classmethod
    def from_row(cls, row: dict[str, Any]) -> Communication:
        """Construct Communication from database row dict."""
        return cls(
            id=row.get("id"),
            thread_id=row.get("thread_id"),
            contact_id=row.get("contact_id"),
            channel=row.get("channel") or "email",
            direction=row.get("direction") or "outbound",
            provider=row.get("provider"),
            provider_message_id=row.get("provider_message_id"),
            in_reply_to_provider_message_id=row.get("in_reply_to_provider_message_id"),
            from_address=row.get("from_address"),
            to_addresses=row.get("to_addresses"),
            cc_addresses=row.get("cc_addresses"),
            subject=row.get("subject"),
            body_text=row.get("body_text"),
            body_html=row.get("body_html"),
            message_status=row.get("message_status") or "draft",
            approval_status=row.get("approval_status") or "not_required",
            approved_by=row.get("approved_by"),
            approved_at=row.get("approved_at"),
            scheduled_for=row.get("scheduled_for"),
            sent_at=row.get("sent_at"),
            received_at=row.get("received_at"),
            delivered_at=row.get("delivered_at"),
            opened_at=row.get("opened_at"),
            bounced_at=row.get("bounced_at"),
            failed_at=row.get("failed_at"),
            created_at=row.get("created_at"),
            updated_at=row.get("updated_at"),
        )

    def to_dict(self) -> dict[str, Any]:
        """Serialize Communication into a dictionary."""
        return {
            "id": self.id,
            "thread_id": self.thread_id,
            "contact_id": self.contact_id,
            "channel": self.channel,
            "direction": self.direction,
            "provider": self.provider,
            "provider_message_id": self.provider_message_id,
            "in_reply_to_provider_message_id": self.in_reply_to_provider_message_id,
            "from_address": self.from_address,
            "to_addresses": self.to_addresses,
            "cc_addresses": self.cc_addresses,
            "subject": self.subject,
            "body_text": self.body_text,
            "body_html": self.body_html,
            "message_status": self.message_status,
            "approval_status": self.approval_status,
            "approved_by": self.approved_by,
            "approved_at": self.approved_at,
            "scheduled_for": self.scheduled_for,
            "sent_at": self.sent_at,
            "received_at": self.received_at,
            "delivered_at": self.delivered_at,
            "opened_at": self.opened_at,
            "bounced_at": self.bounced_at,
            "failed_at": self.failed_at,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }
