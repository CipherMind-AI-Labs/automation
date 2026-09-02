from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass
class ResearchProfile:
    """Domain model representing a company research snapshot."""

    id: int | None = None
    company_id: int | None = None
    company_overview: str | None = None
    owners_summary: str | None = None
    core_services: str | None = None
    primary_customers: str | None = None
    business_model: str | None = None
    competitive_position: str | None = None
    showroom_status: str | None = None
    growth_indicators: str | None = None
    research_confidence: str | None = None
    researched_on: str | None = None
    analyst_notes: str | None = None
    created_at: str | None = None

    @classmethod
    def from_row(cls, row: dict[str, Any]) -> ResearchProfile:
        """Construct ResearchProfile from database row dict."""
        return cls(
            id=row.get("id"),
            company_id=row.get("company_id"),
            company_overview=row.get("company_overview"),
            owners_summary=row.get("owners_summary"),
            core_services=row.get("core_services"),
            primary_customers=row.get("primary_customers"),
            business_model=row.get("business_model"),
            competitive_position=row.get("competitive_position"),
            showroom_status=row.get("showroom_status"),
            growth_indicators=row.get("growth_indicators"),
            research_confidence=row.get("research_confidence"),
            researched_on=row.get("researched_on"),
            analyst_notes=row.get("analyst_notes"),
            created_at=row.get("created_at"),
        )

    def to_dict(self) -> dict[str, Any]:
        """Serialize ResearchProfile into a dictionary."""
        return {
            "id": self.id,
            "company_id": self.company_id,
            "company_overview": self.company_overview,
            "owners_summary": self.owners_summary,
            "core_services": self.core_services,
            "primary_customers": self.primary_customers,
            "business_model": self.business_model,
            "competitive_position": self.competitive_position,
            "showroom_status": self.showroom_status,
            "growth_indicators": self.growth_indicators,
            "research_confidence": self.research_confidence,
            "researched_on": self.researched_on,
            "analyst_notes": self.analyst_notes,
            "created_at": self.created_at,
        }
