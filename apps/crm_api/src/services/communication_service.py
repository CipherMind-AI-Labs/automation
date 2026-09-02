from __future__ import annotations

from typing import Any

from src.models.communication import Communication
from src.models.communication_event import CommunicationEvent
from src.models.communication_thread import CommunicationThread
from src.repositories.communication_repository import CommunicationRepository


class CommunicationService:
    """Business operations service for communication threads, messages, and events."""

    def __init__(self, repository: CommunicationRepository) -> None:
        """Initialize service with CommunicationRepository.

        Args:
            repository: CommunicationRepository instance.
        """
        self.repository = repository

    # --- Threads ---

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
            company_id: Optional company ID filter.
            opportunity_id: Optional opportunity ID filter.
            thread_status: Optional status string.
            limit: Page size.
            offset: Page offset.

        Returns:
            List of CommunicationThread models.
        """
        return self.repository.list_threads(
            company_id=company_id,
            opportunity_id=opportunity_id,
            thread_status=thread_status,
            limit=limit,
            offset=offset,
        )

    def get_thread(self, thread_id: int) -> dict[str, Any] | None:
        """Fetch communication thread with associated messages.

        Args:
            thread_id: Thread primary key ID.

        Returns:
            Thread payload dict with messages list or None.
        """
        thread = self.repository.get_thread_by_id(thread_id)
        if thread is None:
            return None

        thread_dict = thread.to_dict()
        messages = self.repository.list_communications(thread_id=thread_id)
        thread_dict["messages"] = [m.to_dict() for m in messages]
        return thread_dict

    def create_thread(self, payload: dict[str, Any]) -> CommunicationThread:
        """Create a new communication thread.

        Args:
            payload: Payload dict.

        Returns:
            Created CommunicationThread model.
        """
        thread = CommunicationThread.from_row(payload)
        return self.repository.create_thread(thread)

    def update_thread(self, thread_id: int, payload: dict[str, Any]) -> CommunicationThread | None:
        """Update an existing thread.

        Args:
            thread_id: Target ID.
            payload: Update fields.

        Returns:
            Updated CommunicationThread or None.
        """
        existing = self.repository.get_thread_by_id(thread_id)
        if existing is None:
            return None

        update_data = {**existing.to_dict(), **payload, "id": thread_id}
        thread = CommunicationThread.from_row(update_data)
        return self.repository.update_thread(thread)

    def delete_thread(self, thread_id: int) -> bool:
        """Delete thread.

        Args:
            thread_id: Target ID.

        Returns:
            True if deleted.
        """
        existing = self.repository.get_thread_by_id(thread_id)
        if existing is None:
            return False
        return self.repository.delete_thread(thread_id)

    # --- Communications ---

    def list_communications(
        self,
        thread_id: int | None = None,
        contact_id: int | None = None,
        message_status: str | None = None,
        limit: int = 50,
        offset: int = 0,
    ) -> list[Communication]:
        """List communication messages.

        Args:
            thread_id: Optional thread ID.
            contact_id: Optional contact ID.
            message_status: Status filter string.
            limit: Page limit.
            offset: Page offset.

        Returns:
            List of Communication models.
        """
        return self.repository.list_communications(
            thread_id=thread_id,
            contact_id=contact_id,
            message_status=message_status,
            limit=limit,
            offset=offset,
        )

    def get_communication(self, comm_id: int) -> dict[str, Any] | None:
        """Fetch message with list of webhook events.

        Args:
            comm_id: Message ID.

        Returns:
            Communication dict with events or None.
        """
        comm = self.repository.get_communication_by_id(comm_id)
        if comm is None:
            return None

        comm_dict = comm.to_dict()
        events = self.repository.list_events_by_communication_id(comm_id)
        comm_dict["events"] = [e.to_dict() for e in events]
        return comm_dict

    def create_communication(self, payload: dict[str, Any]) -> Communication:
        """Create a new communication message.

        Args:
            payload: Payload dict.

        Returns:
            Created Communication model.
        """
        comm = Communication.from_row(payload)
        return self.repository.create_communication(comm)

    def update_communication(self, comm_id: int, payload: dict[str, Any]) -> Communication | None:
        """Update an existing communication message.

        Args:
            comm_id: Target ID.
            payload: Updated fields dict.

        Returns:
            Updated Communication or None.
        """
        existing = self.repository.get_communication_by_id(comm_id)
        if existing is None:
            return None

        update_data = {**existing.to_dict(), **payload, "id": comm_id}
        comm = Communication.from_row(update_data)
        return self.repository.update_communication(comm)

    def delete_communication(self, comm_id: int) -> bool:
        """Delete communication message.

        Args:
            comm_id: Target ID.

        Returns:
            True if deleted.
        """
        existing = self.repository.get_communication_by_id(comm_id)
        if existing is None:
            return False
        return self.repository.delete_communication(comm_id)

    # --- Events ---

    def create_event(self, comm_id: int, event_payload: dict[str, Any]) -> CommunicationEvent | None:
        """Record a communication event.

        Args:
            comm_id: Communication message ID.
            event_payload: Event data dict.

        Returns:
            Created CommunicationEvent model or None if message not found.
        """
        existing = self.repository.get_communication_by_id(comm_id)
        if existing is None:
            return None

        event = CommunicationEvent.from_row({**event_payload, "communication_id": comm_id})
        return self.repository.create_event(event)
