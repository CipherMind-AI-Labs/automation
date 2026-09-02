from __future__ import annotations

from typing import Any

from src.database.base import DatabaseAdapter
from src.models.follow_up_reminder import FollowUpReminder


class FollowUpReminderRepository:
    """Repository for FollowUpReminder entity SQL operations."""

    def __init__(self, database: DatabaseAdapter) -> None:
        """Initialize repository with DatabaseAdapter."""
        self.database = database

    def list(
        self,
        opportunity_id: int | None = None,
        status: str | None = None,
        limit: int = 50,
        offset: int = 0,
    ) -> list[FollowUpReminder]:
        """List follow up reminders with optional filtering.

        Args:
            opportunity_id: Opportunity ID filter.
            status: Status filter ('pending', 'completed', 'cancelled', 'overdue').
            limit: Page size.
            offset: Page offset.

        Returns:
            List of FollowUpReminder models.
        """
        sql = "SELECT id, opportunity_id, thread_id, contact_id, reminder_type, status, due_at, completed_at, last_notified_at, notes, created_at, updated_at FROM follow_up_reminders WHERE 1=1"
        params: list[Any] = []

        if opportunity_id is not None:
            sql += " AND opportunity_id = ?"
            params.append(opportunity_id)

        if status:
            sql += " AND status = ?"
            params.append(status)

        sql += " ORDER BY due_at ASC LIMIT ? OFFSET ?"
        params.extend([limit, offset])

        rows = self.database.execute(sql, params)
        return [FollowUpReminder.from_row(row) for row in rows]

    def get_by_id(self, reminder_id: int) -> FollowUpReminder | None:
        """Fetch reminder by primary key ID.

        Args:
            reminder_id: Target ID.

        Returns:
            FollowUpReminder model or None.
        """
        rows = self.database.execute(
            "SELECT id, opportunity_id, thread_id, contact_id, reminder_type, status, due_at, completed_at, last_notified_at, notes, created_at, updated_at FROM follow_up_reminders WHERE id = ?",
            [reminder_id],
        )
        if not rows:
            return None
        return FollowUpReminder.from_row(rows[0])

    def create(self, reminder: FollowUpReminder) -> FollowUpReminder:
        """Create a new follow up reminder.

        Args:
            reminder: FollowUpReminder model to persist.

        Returns:
            FollowUpReminder model with generated ID.
        """
        sql = """
            INSERT INTO follow_up_reminders (
                opportunity_id, thread_id, contact_id, reminder_type, status,
                due_at, completed_at, last_notified_at, notes
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        params = [
            reminder.opportunity_id,
            reminder.thread_id,
            reminder.contact_id,
            reminder.reminder_type or "follow_up",
            reminder.status or "pending",
            reminder.due_at,
            reminder.completed_at,
            reminder.last_notified_at,
            reminder.notes,
        ]
        inserted = self.database.execute(sql, params)
        if inserted and "id" in inserted[0]:
            reminder.id = inserted[0]["id"]
        return reminder

    def update(self, reminder: FollowUpReminder) -> FollowUpReminder | None:
        """Update an existing follow up reminder.

        Args:
            reminder: FollowUpReminder model with updated fields.

        Returns:
            Updated FollowUpReminder model or None.
        """
        if reminder.id is None:
            return None

        sql = """
            UPDATE follow_up_reminders SET
                opportunity_id = ?, thread_id = ?, contact_id = ?, reminder_type = ?,
                status = ?, due_at = ?, completed_at = ?, last_notified_at = ?,
                notes = ?, updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
        """
        params = [
            reminder.opportunity_id,
            reminder.thread_id,
            reminder.contact_id,
            reminder.reminder_type,
            reminder.status,
            reminder.due_at,
            reminder.completed_at,
            reminder.last_notified_at,
            reminder.notes,
            reminder.id,
        ]
        self.database.execute(sql, params)
        return self.get_by_id(reminder.id)

    def delete(self, reminder_id: int) -> bool:
        """Delete reminder by ID.

        Args:
            reminder_id: Target ID.

        Returns:
            True if deletion was executed.
        """
        self.database.execute("DELETE FROM follow_up_reminders WHERE id = ?", [reminder_id])
        return True
