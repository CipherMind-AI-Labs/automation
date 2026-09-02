from __future__ import annotations

from typing import Any

from src.models.company import Company
from src.repositories.company_repository import CompanyRepository


class CompanyService:
    """Business operations service for managing Companies."""

    def __init__(self, repository: CompanyRepository) -> None:
        """Initialize CompanyService with repository.

        Args:
            repository: CompanyRepository instance.
        """
        self.repository = repository

    def list_companies(
        self,
        query: str | None = None,
        industry: str | None = None,
        limit: int = 50,
        offset: int = 0,
    ) -> list[Company]:
        """List companies matching optional search query or industry filter.

        Args:
            query: Name or URL search term.
            industry: Industry filter string.
            limit: Page size limit.
            offset: Page offset.

        Returns:
            List of Company domain models.
        """
        return self.repository.list(query=query, industry=industry, limit=limit, offset=offset)

    def get_company(self, company_id: int) -> Company | None:
        """Retrieve company by ID.

        Args:
            company_id: Primary key ID.

        Returns:
            Company domain model or None.
        """
        return self.repository.get_by_id(company_id)

    def create_company(self, payload: dict[str, Any]) -> Company:
        """Create and validate a new company record.

        Args:
            payload: Request dictionary payload.

        Returns:
            Created Company instance.
        """
        company = Company.from_row(payload)
        return self.repository.create(company)

    def update_company(self, company_id: int, payload: dict[str, Any]) -> Company | None:
        """Update an existing company record.

        Args:
            company_id: Primary key ID.
            payload: Update fields dictionary.

        Returns:
            Updated Company model or None if not found.
        """
        existing = self.repository.get_by_id(company_id)
        if existing is None:
            return None

        update_data = {**existing.to_dict(), **payload, "id": company_id}
        company = Company.from_row(update_data)
        return self.repository.update(company)

    def delete_company(self, company_id: int) -> bool:
        """Delete company record.

        Args:
            company_id: Primary key ID.

        Returns:
            True if existing record was deleted.
        """
        existing = self.repository.get_by_id(company_id)
        if existing is None:
            return False
        return self.repository.delete(company_id)
