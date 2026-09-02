from __future__ import annotations

from typing import Any

from src.models.follow_up_reminder import FollowUpReminder
from src.repositories.follow_up_reminder_repository import FollowUpReminderRepository


class FollowUpReminderService:
    """Business operations service for follow-up reminders."""

    def __init__(self, repository: FollowUpReminderRepository) -> None:
        """Initialize service with FollowUpReminderRepository.

        Args:
            repository: FollowUpReminderRepository instance.
        """
        self.repository = repository

    def list_reminders(
        self,
        opportunity_id: int | None = None,
        status: str | None = None,
        limit: int = 50,
        offset: int = 0,
    ) -> list[FollowUpReminder]:
        """List follow up reminders with optional filtering.

        Args:
            opportunity_id: Optional opportunity ID.
            status: Optional status string.
            limit: Page limit.
            offset: Page offset.

        Returns:
            List of FollowUpReminder models.
        """
        return self.repository.list(
            opportunity_id=opportunity_id,
            status=status,
            limit=limit,
            offset=offset,
        )

    def get_reminder(self, reminder_id: int) -> FollowUpReminder | None:
        """Fetch reminder by ID.

        Args:
            reminder_id: Primary key ID.

        Returns:
            FollowUpReminder model or None.
        """
        return self.repository.get_by_id(reminder_id)

    def create_reminder(self, payload: dict[str, Any]) -> FollowUpReminder:
        """Create a new follow-up reminder.

        Args:
            payload: Payload dict.

        Returns:
            Created FollowUpReminder instance.
        """
        reminder = FollowUpReminder.from_row(payload)
        return self.repository.create(reminder)

    def update_reminder(self, reminder_id: int, payload: dict[str, Any]) -> FollowUpReminder | None:
        """Update an existing reminder.

        Args:
            reminder_id: Target ID.
            payload: Update fields dict.

        Returns:
            Updated FollowUpReminder or None if not found.
        """
        existing = self.repository.get_by_id(reminder_id)
        if existing is None:
            return None

        update_data = {**existing.to_dict(), **payload, "id": reminder_id}
        reminder = FollowUpReminder.from_row(update_data)
        return self.repository.update(reminder)

    def delete_reminder(self, reminder_id: int) -> bool:
        """Delete reminder.

        Args:
            reminder_id: Target ID.

        Returns:
            True if deleted.
        """
        existing = self.repository.get_by_id(reminder_id)
        if existing is None:
            return False
        return self.repository.delete(reminder_id)
