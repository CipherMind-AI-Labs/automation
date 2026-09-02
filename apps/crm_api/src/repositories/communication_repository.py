from __future__ import annotations

from typing import Any

from src.database.base import DatabaseAdapter
from src.models.communication import Communication
from src.models.communication_event import CommunicationEvent
from src.models.communication_thread import CommunicationThread


class CommunicationRepository:
    """Repository for communication threads, messages, and webhook event tracking."""

    def __init__(self, database: DatabaseAdapter) -> None:
        """Initialize repository with DatabaseAdapter."""
        self.database = database

    # --- Communication Threads ---

    def list_threads(
        self,
        company_id: int | None = None,
        opportunity_id: int | None = None,
        thread_status: str | None = None,
        limit: int = 50,
        offset: int = 0,
    ) -> list[CommunicationThread]:
        """List communication threads with optional filtering.

        Args:
            company_id: Optional company filter.
            opportunity_id: Optional opportunity filter.
            thread_status: Optional status filter.
            limit: Pagination limit.
            offset: Pagination offset.

        Returns:
            List of CommunicationThread models.
        """
        sql = "SELECT id, company_id, opportunity_id, channel, provider, provider_thread_id, subject, thread_status, last_outbound_at, last_inbound_at, reply_due_at, next_follow_up_due_at, closed_at, created_at, updated_at FROM communication_threads WHERE 1=1"
        params: list[Any] = []

        if company_id is not None:
            sql += " AND company_id = ?"
            params.append(company_id)

        if opportunity_id is not None:
            sql += " AND opportunity_id = ?"
            params.append(opportunity_id)

        if thread_status:
            sql += " AND thread_status = ?"
            params.append(thread_status)

        sql += " ORDER BY id DESC LIMIT ? OFFSET ?"
        params.extend([limit, offset])

        rows = self.database.execute(sql, params)
        return [CommunicationThread.from_row(row) for row in rows]

    def get_thread_by_id(self, thread_id: int) -> CommunicationThread | None:
        """Fetch communication thread by ID.

        Args:
            thread_id: Thread primary key ID.

        Returns:
            CommunicationThread or None.
        """
        rows = self.database.execute(
            "SELECT id, company_id, opportunity_id, channel, provider, provider_thread_id, subject, thread_status, last_outbound_at, last_inbound_at, reply_due_at, next_follow_up_due_at, closed_at, created_at, updated_at FROM communication_threads WHERE id = ?",
            [thread_id],
        )
        if not rows:
            return None
        return CommunicationThread.from_row(rows[0])

    def create_thread(self, thread: CommunicationThread) -> CommunicationThread:
        """Create a new communication thread record.

        Args:
            thread: CommunicationThread model.

        Returns:
            CommunicationThread with generated ID.
        """
        sql = """
            INSERT INTO communication_threads (
                company_id, opportunity_id, channel, provider, provider_thread_id,
                subject, thread_status, last_outbound_at, last_inbound_at,
                reply_due_at, next_follow_up_due_at, closed_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        params = [
            thread.company_id,
            thread.opportunity_id,
            thread.channel or "email",
            thread.provider,
            thread.provider_thread_id,
            thread.subject,
            thread.thread_status or "Open",
            thread.last_outbound_at,
            thread.last_inbound_at,
            thread.reply_due_at,
            thread.next_follow_up_due_at,
            thread.closed_at,
        ]
        inserted = self.database.execute(sql, params)
        if inserted and "id" in inserted[0]:
            thread.id = inserted[0]["id"]
        return thread

    def update_thread(self, thread: CommunicationThread) -> CommunicationThread | None:
        """Update an existing communication thread.

        Args:
            thread: CommunicationThread model with updated values.

        Returns:
            Updated CommunicationThread or None.
        """
        if thread.id is None:
            return None

        sql = """
            UPDATE communication_threads SET
                company_id = ?, opportunity_id = ?, channel = ?, provider = ?,
                provider_thread_id = ?, subject = ?, thread_status = ?,
                last_outbound_at = ?, last_inbound_at = ?, reply_due_at = ?,
                next_follow_up_due_at = ?, closed_at = ?, updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
        """
        params = [
            thread.company_id,
            thread.opportunity_id,
            thread.channel,
            thread.provider,
            thread.provider_thread_id,
            thread.subject,
            thread.thread_status,
            thread.last_outbound_at,
            thread.last_inbound_at,
            thread.reply_due_at,
            thread.next_follow_up_due_at,
            thread.closed_at,
            thread.id,
        ]
        self.database.execute(sql, params)
        return self.get_thread_by_id(thread.id)

    def delete_thread(self, thread_id: int) -> bool:
        """Delete communication thread by ID.

        Args:
            thread_id: Thread ID.

        Returns:
            True if deletion was executed.
        """
        self.database.execute("DELETE FROM communication_threads WHERE id = ?", [thread_id])
        return True

    # --- Communications (Messages) ---

    def list_communications(
        self,
        thread_id: int | None = None,
        contact_id: int | None = None,
        message_status: str | None = None,
        limit: int = 50,
        offset: int = 0,
    ) -> list[Communication]:
        """List communication messages with optional filtering.

        Args:
            thread_id: Thread ID filter.
            contact_id: Contact ID filter.
            message_status: Status filter.
            limit: Page size.
            offset: Page offset.

        Returns:
            List of Communication domain models.
        """
        sql = """
            SELECT id, thread_id, contact_id, channel, direction, provider,
                   provider_message_id, in_reply_to_provider_message_id, from_address,
                   to_addresses, cc_addresses, subject, body_text, body_html, message_status,
                   approval_status, approved_by, approved_at, scheduled_for, sent_at,
                   received_at, delivered_at, opened_at, bounced_at, failed_at,
                   created_at, updated_at
            FROM communications WHERE 1=1
        """
        params: list[Any] = []

        if thread_id is not None:
            sql += " AND thread_id = ?"
            params.append(thread_id)

        if contact_id is not None:
            sql += " AND contact_id = ?"
            params.append(contact_id)

        if message_status:
            sql += " AND message_status = ?"
            params.append(message_status)

        sql += " ORDER BY id ASC LIMIT ? OFFSET ?"
        params.extend([limit, offset])

        rows = self.database.execute(sql, params)
        return [Communication.from_row(row) for row in rows]

    def get_communication_by_id(self, comm_id: int) -> Communication | None:
        """Fetch individual communication message by ID.

        Args:
            comm_id: Message primary key ID.

        Returns:
            Communication model or None.
        """
        sql = """
            SELECT id, thread_id, contact_id, channel, direction, provider,
                   provider_message_id, in_reply_to_provider_message_id, from_address,
                   to_addresses, cc_addresses, subject, body_text, body_html, message_status,
                   approval_status, approved_by, approved_at, scheduled_for, sent_at,
                   received_at, delivered_at, opened_at, bounced_at, failed_at,
                   created_at, updated_at
            FROM communications WHERE id = ?
        """
        rows = self.database.execute(sql, [comm_id])
        if not rows:
            return None
        return Communication.from_row(rows[0])

    def create_communication(self, comm: Communication) -> Communication:
        """Create a new communication message record.

        Args:
            comm: Communication model to persist.

        Returns:
            Communication model with generated ID.
        """
        sql = """
            INSERT INTO communications (
                thread_id, contact_id, channel, direction, provider, provider_message_id,
                in_reply_to_provider_message_id, from_address, to_addresses, cc_addresses,
                subject, body_text, body_html, message_status, approval_status, approved_by,
                approved_at, scheduled_for, sent_at, received_at, delivered_at, opened_at,
                bounced_at, failed_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        params = [
            comm.thread_id,
            comm.contact_id,
            comm.channel or "email",
            comm.direction or "outbound",
            comm.provider,
            comm.provider_message_id,
            comm.in_reply_to_provider_message_id,
            comm.from_address,
            comm.to_addresses,
            comm.cc_addresses,
            comm.subject,
            comm.body_text,
            comm.body_html,
            comm.message_status or "draft",
            comm.approval_status or "not_required",
            comm.approved_by,
            comm.approved_at,
            comm.scheduled_for,
            comm.sent_at,
            comm.received_at,
            comm.delivered_at,
            comm.opened_at,
            comm.bounced_at,
            comm.failed_at,
        ]
        inserted = self.database.execute(sql, params)
        if inserted and "id" in inserted[0]:
            comm.id = inserted[0]["id"]
        return comm

    def update_communication(self, comm: Communication) -> Communication | None:
        """Update an existing communication message.

        Args:
            comm: Communication model with updated fields.

        Returns:
            Updated Communication model or None.
        """
        if comm.id is None:
            return None

        sql = """
            UPDATE communications SET
                thread_id = ?, contact_id = ?, channel = ?, direction = ?, provider = ?,
                provider_message_id = ?, in_reply_to_provider_message_id = ?, from_address = ?,
                to_addresses = ?, cc_addresses = ?, subject = ?, body_text = ?, body_html = ?,
                message_status = ?, approval_status = ?, approved_by = ?, approved_at = ?,
                scheduled_for = ?, sent_at = ?, received_at = ?, delivered_at = ?, opened_at = ?,
                bounced_at = ?, failed_at = ?, updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
        """
        params = [
            comm.thread_id,
            comm.contact_id,
            comm.channel,
            comm.direction,
            comm.provider,
            comm.provider_message_id,
            comm.in_reply_to_provider_message_id,
            comm.from_address,
            comm.to_addresses,
            comm.cc_addresses,
            comm.subject,
            comm.body_text,
            comm.body_html,
            comm.message_status,
            comm.approval_status,
            comm.approved_by,
            comm.approved_at,
            comm.scheduled_for,
            comm.sent_at,
            comm.received_at,
            comm.delivered_at,
            comm.opened_at,
            comm.bounced_at,
            comm.failed_at,
            comm.id,
        ]
        self.database.execute(sql, params)
        return self.get_communication_by_id(comm.id)

    def delete_communication(self, comm_id: int) -> bool:
        """Delete communication message by ID.

        Args:
            comm_id: Target message ID.

        Returns:
            True if deletion was executed.
        """
        self.database.execute("DELETE FROM communications WHERE id = ?", [comm_id])
        return True

    # --- Communication Events ---

    def list_events_by_communication_id(self, communication_id: int) -> list[CommunicationEvent]:
        """Fetch list of events for a given communication message.

        Args:
            communication_id: Communication message ID.

        Returns:
            List of CommunicationEvent models.
        """
        sql = "SELECT id, communication_id, event_type, occurred_at, provider_event_id, metadata_json, created_at FROM communication_events WHERE communication_id = ? ORDER BY id ASC"
        rows = self.database.execute(sql, [communication_id])
        return [CommunicationEvent.from_row(row) for row in rows]

    def create_event(self, event: CommunicationEvent) -> CommunicationEvent:
        """Record a communication event.

        Args:
            event: CommunicationEvent model.

        Returns:
            CommunicationEvent populated with ID.
        """
        sql = """
            INSERT INTO communication_events (
                communication_id, event_type, occurred_at, provider_event_id, metadata_json
            ) VALUES (?, ?, ?, ?, ?)
        """
        params = [
            event.communication_id,
            event.event_type,
            event.occurred_at,
            event.provider_event_id,
            event.metadata_json,
        ]
        inserted = self.database.execute(sql, params)
        if inserted and "id" in inserted[0]:
            event.id = inserted[0]["id"]
        return event
