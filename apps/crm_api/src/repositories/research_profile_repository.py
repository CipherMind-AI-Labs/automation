from __future__ import annotations

from typing import Any

from src.database.base import DatabaseAdapter
from src.models.research_profile import ResearchProfile


class ResearchProfileRepository:
    """Repository for ResearchProfile raw SQL operations."""

    def __init__(self, database: DatabaseAdapter) -> None:
        """Initialize repository with DatabaseAdapter instance."""
        self.database = database

    def list(self, company_id: int | None = None, limit: int = 50, offset: int = 0) -> list[ResearchProfile]:
        """List research profiles, optionally filtered by company ID.

        Args:
            company_id: Optional company ID filter.
            limit: Page size limit.
            offset: Page offset.

        Returns:
            List of ResearchProfile domain models.
        """
        sql = "SELECT id, company_id, company_overview, owners_summary, core_services, primary_customers, business_model, competitive_position, showroom_status, growth_indicators, research_confidence, researched_on, analyst_notes, created_at FROM research_profiles WHERE 1=1"
        params: list[Any] = []

        if company_id is not None:
            sql += " AND company_id = ?"
            params.append(company_id)

        sql += " ORDER BY id DESC LIMIT ? OFFSET ?"
        params.extend([limit, offset])

        rows = self.database.execute(sql, params)
        return [ResearchProfile.from_row(row) for row in rows]

    def get_by_id(self, profile_id: int) -> ResearchProfile | None:
        """Get a single research profile by primary key ID.

        Args:
            profile_id: Primary key ID.

        Returns:
            ResearchProfile or None.
        """
        rows = self.database.execute(
            "SELECT id, company_id, company_overview, owners_summary, core_services, primary_customers, business_model, competitive_position, showroom_status, growth_indicators, research_confidence, researched_on, analyst_notes, created_at FROM research_profiles WHERE id = ?",
            [profile_id],
        )
        if not rows:
            return None
        return ResearchProfile.from_row(rows[0])

    def create(self, profile: ResearchProfile) -> ResearchProfile:
        """Create a new research profile.

        Args:
            profile: ResearchProfile to persist.

        Returns:
            ResearchProfile populated with created ID.
        """
        sql = """
            INSERT INTO research_profiles (
                company_id, company_overview, owners_summary, core_services,
                primary_customers, business_model, competitive_position,
                showroom_status, growth_indicators, research_confidence,
                researched_on, analyst_notes
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        params = [
            profile.company_id,
            profile.company_overview,
            profile.owners_summary,
            profile.core_services,
            profile.primary_customers,
            profile.business_model,
            profile.competitive_position,
            profile.showroom_status,
            profile.growth_indicators,
            profile.research_confidence,
            profile.researched_on,
            profile.analyst_notes,
        ]
        inserted = self.database.execute(sql, params)
        if inserted and "id" in inserted[0]:
            profile.id = inserted[0]["id"]
        return profile

    def update(self, profile: ResearchProfile) -> ResearchProfile | None:
        """Update an existing research profile.

        Args:
            profile: ResearchProfile with updated fields.

        Returns:
            Updated ResearchProfile or None.
        """
        if profile.id is None:
            return None

        sql = """
            UPDATE research_profiles SET
                company_id = ?, company_overview = ?, owners_summary = ?,
                core_services = ?, primary_customers = ?, business_model = ?,
                competitive_position = ?, showroom_status = ?, growth_indicators = ?,
                research_confidence = ?, researched_on = ?, analyst_notes = ?
            WHERE id = ?
        """
        params = [
            profile.company_id,
            profile.company_overview,
            profile.owners_summary,
            profile.core_services,
            profile.primary_customers,
            profile.business_model,
            profile.competitive_position,
            profile.showroom_status,
            profile.growth_indicators,
            profile.research_confidence,
            profile.researched_on,
            profile.analyst_notes,
            profile.id,
        ]
        self.database.execute(sql, params)
        return self.get_by_id(profile.id)

    def delete(self, profile_id: int) -> bool:
        """Delete research profile by ID.

        Args:
            profile_id: Primary key ID to delete.

        Returns:
            True if deletion query executed.
        """
        self.database.execute("DELETE FROM research_profiles WHERE id = ?", [profile_id])
        return True
