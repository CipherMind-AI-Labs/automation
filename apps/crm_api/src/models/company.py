from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass
class Company:
    """Domain model representing a company in the CRM database."""

    id: int | None = None
    name: str | None = None
    website_url: str | None = None
    linkedin_url: str | None = None
    headquarters: str | None = None
    offices_summary: str | None = None
    geographic_coverage: str | None = None
    industry: str | None = None
    business_type: str | None = None
    employee_range: str | None = None
    founded_year: int | None = None
    ownership: str | None = None
    created_at: str | None = None
    updated_at: str | None = None

    @classmethod
    def from_row(cls, row: dict[str, Any]) -> Company:
        """Construct a Company instance from a database row dictionary."""
        return cls(
            id=row.get("id"),
            name=row.get("name"),
            website_url=row.get("website_url"),
            linkedin_url=row.get("linkedin_url"),
            headquarters=row.get("headquarters"),
            offices_summary=row.get("offices_summary"),
            geographic_coverage=row.get("geographic_coverage"),
            industry=row.get("industry"),
            business_type=row.get("business_type"),
            employee_range=row.get("employee_range"),
            founded_year=row.get("founded_year"),
            ownership=row.get("ownership"),
            created_at=row.get("created_at"),
            updated_at=row.get("updated_at"),
        )

    def to_dict(self) -> dict[str, Any]:
        """Serialize Company instance into a dictionary."""
        return {
            "id": self.id,
            "name": self.name,
            "website_url": self.website_url,
            "linkedin_url": self.linkedin_url,
            "headquarters": self.headquarters,
            "offices_summary": self.offices_summary,
            "geographic_coverage": self.geographic_coverage,
            "industry": self.industry,
            "business_type": self.business_type,
            "employee_range": self.employee_range,
            "founded_year": self.founded_year,
            "ownership": self.ownership,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }
