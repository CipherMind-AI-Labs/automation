from __future__ import annotations

from typing import Any

from src.models.contact import Contact
from src.repositories.contact_repository import ContactRepository


class ContactService:
    """Business operations service for managing contacts."""

    def __init__(self, repository: ContactRepository) -> None:
        """Initialize service with ContactRepository.

        Args:
            repository: ContactRepository instance.
        """
        self.repository = repository

    def list_contacts(
        self,
        company_id: int | None = None,
        search: str | None = None,
        is_decision_maker: int | None = None,
        limit: int = 50,
        offset: int = 0,
    ) -> list[Contact]:
        """List contacts with optional search query or filters.

        Args:
            company_id: Company filter.
            search: Name or email search term.
            is_decision_maker: Filter by 0 or 1.
            limit: Page size.
            offset: Page offset.

        Returns:
            List of Contact domain models.
        """
        return self.repository.list(
            company_id=company_id,
            search=search,
            is_decision_maker=is_decision_maker,
            limit=limit,
            offset=offset,
        )

    def get_contact(self, contact_id: int) -> Contact | None:
        """Fetch contact by ID.

        Args:
            contact_id: Target ID.

        Returns:
            Contact domain model or None.
        """
        return self.repository.get_by_id(contact_id)

    def create_contact(self, payload: dict[str, Any]) -> Contact:
        """Create a new contact record.

        Args:
            payload: Contact dictionary.

        Returns:
            Created Contact instance.
        """
        contact = Contact.from_row(payload)
        return self.repository.create(contact)

    def update_contact(self, contact_id: int, payload: dict[str, Any]) -> Contact | None:
        """Update an existing contact record.

        Args:
            contact_id: Target ID.
            payload: Update fields dictionary.

        Returns:
            Updated Contact model or None if not found.
        """
        existing = self.repository.get_by_id(contact_id)
        if existing is None:
            return None

        update_data = {**existing.to_dict(), **payload, "id": contact_id}
        contact = Contact.from_row(update_data)
        return self.repository.update(contact)

    def delete_contact(self, contact_id: int) -> bool:
        """Delete contact record.

        Args:
            contact_id: Target ID.

        Returns:
            True if contact deleted.
        """
        existing = self.repository.get_by_id(contact_id)
        if existing is None:
            return False
        return self.repository.delete(contact_id)
