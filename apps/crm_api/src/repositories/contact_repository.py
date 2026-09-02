from __future__ import annotations

from typing import Any

from src.database.base import DatabaseAdapter
from src.models.contact import Contact


class ContactRepository:
    """Repository for Contact entity SQL operations."""

    def __init__(self, database: DatabaseAdapter) -> None:
        """Initialize repository with DatabaseAdapter."""
        self.database = database

    def list(
        self,
        company_id: int | None = None,
        search: str | None = None,
        is_decision_maker: int | None = None,
        limit: int = 50,
        offset: int = 0,
    ) -> list[Contact]:
        """List contacts with optional filtering by company, search term, or decision maker status.

        Args:
            company_id: Optional company ID filter.
            search: Name or email search term.
            is_decision_maker: Filter by 0 or 1.
            limit: Page size.
            offset: Page offset.

        Returns:
            List of Contact domain models.
        """
        sql = "SELECT id, company_id, first_name, last_name, full_name, job_title, email, phone, linkedin_url, is_decision_maker, notes, created_at, updated_at FROM contacts WHERE 1=1"
        params: list[Any] = []

        if company_id is not None:
            sql += " AND company_id = ?"
            params.append(company_id)

        if search:
            sql += " AND (full_name LIKE ? OR email LIKE ?)"
            term = f"%{search}%"
            params.extend([term, term])

        if is_decision_maker is not None:
            sql += " AND is_decision_maker = ?"
            params.append(is_decision_maker)

        sql += " ORDER BY id ASC LIMIT ? OFFSET ?"
        params.extend([limit, offset])

        rows = self.database.execute(sql, params)
        return [Contact.from_row(row) for row in rows]

    def get_by_id(self, contact_id: int) -> Contact | None:
        """Fetch Contact by primary key ID.

        Args:
            contact_id: Contact ID.

        Returns:
            Contact domain model or None.
        """
        rows = self.database.execute(
            "SELECT id, company_id, first_name, last_name, full_name, job_title, email, phone, linkedin_url, is_decision_maker, notes, created_at, updated_at FROM contacts WHERE id = ?",
            [contact_id],
        )
        if not rows:
            return None
        return Contact.from_row(rows[0])

    def create(self, contact: Contact) -> Contact:
        """Create a new contact record.

        Args:
            contact: Contact model to persist.

        Returns:
            Contact model populated with generated ID.
        """
        sql = """
            INSERT INTO contacts (
                company_id, first_name, last_name, full_name, job_title,
                email, phone, linkedin_url, is_decision_maker, notes
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        params = [
            contact.company_id,
            contact.first_name,
            contact.last_name,
            contact.full_name or f"{contact.first_name or ''} {contact.last_name or ''}".strip(),
            contact.job_title,
            contact.email,
            contact.phone,
            contact.linkedin_url,
            contact.is_decision_maker,
            contact.notes,
        ]
        inserted = self.database.execute(sql, params)
        if inserted and "id" in inserted[0]:
            contact.id = inserted[0]["id"]
        return contact

    def update(self, contact: Contact) -> Contact | None:
        """Update an existing contact record.

        Args:
            contact: Contact model with updated values.

        Returns:
            Updated Contact model or None.
        """
        if contact.id is None:
            return None

        sql = """
            UPDATE contacts SET
                company_id = ?, first_name = ?, last_name = ?, full_name = ?,
                job_title = ?, email = ?, phone = ?, linkedin_url = ?,
                is_decision_maker = ?, notes = ?, updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
        """
        params = [
            contact.company_id,
            contact.first_name,
            contact.last_name,
            contact.full_name,
            contact.job_title,
            contact.email,
            contact.phone,
            contact.linkedin_url,
            contact.is_decision_maker,
            contact.notes,
            contact.id,
        ]
        self.database.execute(sql, params)
        return self.get_by_id(contact.id)

    def delete(self, contact_id: int) -> bool:
        """Delete contact by ID.

        Args:
            contact_id: Target ID.

        Returns:
            True if deletion was executed.
        """
        self.database.execute("DELETE FROM contacts WHERE id = ?", [contact_id])
        return True
