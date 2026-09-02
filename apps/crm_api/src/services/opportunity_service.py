from __future__ import annotations

from typing import Any

from src.models.opportunity import Opportunity
from src.repositories.opportunity_repository import OpportunityRepository


class OpportunityService:
    """Business operations service for commercial deal opportunities."""

    def __init__(self, repository: OpportunityRepository) -> None:
        """Initialize service with OpportunityRepository.

        Args:
            repository: OpportunityRepository instance.
        """
        self.repository = repository

    def list_opportunities(
        self,
        company_id: int | None = None,
        lead_status: str | None = None,
        priority: str | None = None,
        limit: int = 50,
        offset: int = 0,
    ) -> list[Opportunity]:
        """List opportunities with optional status, priority, or company filtering.

        Args:
            company_id: Company ID filter.
            lead_status: Lead status filter.
            priority: Priority filter.
            limit: Page size.
            offset: Page offset.

        Returns:
            List of Opportunity models.
        """
        return self.repository.list(
            company_id=company_id,
            lead_status=lead_status,
            priority=priority,
            limit=limit,
            offset=offset,
        )

    def get_opportunity(self, opportunity_id: int) -> Opportunity | None:
        """Fetch opportunity by ID.

        Args:
            opportunity_id: Primary key ID.

        Returns:
            Opportunity domain model or None.
        """
        return self.repository.get_by_id(opportunity_id)

    def create_opportunity(self, payload: dict[str, Any]) -> Opportunity:
        """Create a new commercial deal opportunity.

        Args:
            payload: Payload dictionary.

        Returns:
            Created Opportunity instance.
        """
        opp = Opportunity.from_row(payload)
        return self.repository.create(opp)

    def update_opportunity(self, opportunity_id: int, payload: dict[str, Any]) -> Opportunity | None:
        """Update an existing opportunity record.

        Args:
            opportunity_id: Target ID.
            payload: Updated fields.

        Returns:
            Updated Opportunity model or None if not found.
        """
        existing = self.repository.get_by_id(opportunity_id)
        if existing is None:
            return None

        update_data = {**existing.to_dict(), **payload, "id": opportunity_id}
        opp = Opportunity.from_row(update_data)
        return self.repository.update(opp)

    def delete_opportunity(self, opportunity_id: int) -> bool:
        """Delete opportunity record.

        Args:
            opportunity_id: Target ID.

        Returns:
            True if opportunity deleted.
        """
        existing = self.repository.get_by_id(opportunity_id)
        if existing is None:
            return False
        return self.repository.delete(opportunity_id)
