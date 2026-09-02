from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass
class Contact:
    """Domain model representing a person contact at a company."""

    id: int | None = None
    company_id: int | None = None
    first_name: str | None = None
    last_name: str | None = None
    full_name: str | None = None
    job_title: str | None = None
    email: str | None = None
    phone: str | None = None
    linkedin_url: str | None = None
    is_decision_maker: int = 0
    notes: str | None = None
    created_at: str | None = None
    updated_at: str | None = None

    @classmethod
    def from_row(cls, row: dict[str, Any]) -> Contact:
        """Construct Contact from database row dict."""
        return cls(
            id=row.get("id"),
            company_id=row.get("company_id"),
            first_name=row.get("first_name"),
            last_name=row.get("last_name"),
            full_name=row.get("full_name") or f"{row.get('first_name', '')} {row.get('last_name', '')}".strip(),
            job_title=row.get("job_title"),
            email=row.get("email"),
            phone=row.get("phone"),
            linkedin_url=row.get("linkedin_url"),
            is_decision_maker=row.get("is_decision_maker", 0),
            notes=row.get("notes"),
            created_at=row.get("created_at"),
            updated_at=row.get("updated_at"),
        )

    def to_dict(self) -> dict[str, Any]:
        """Serialize Contact into a dictionary."""
        return {
            "id": self.id,
            "company_id": self.company_id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "full_name": self.full_name,
            "job_title": self.job_title,
            "email": self.email,
            "phone": self.phone,
            "linkedin_url": self.linkedin_url,
            "is_decision_maker": self.is_decision_maker,
            "notes": self.notes,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }
