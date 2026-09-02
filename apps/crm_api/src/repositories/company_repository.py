from __future__ import annotations

from typing import Any

from src.database.base import DatabaseAdapter
from src.models.company import Company


class CompanyRepository:
    """Repository for Company entity persistence and raw SQL query operations."""

    def __init__(self, database: DatabaseAdapter) -> None:
        """Initialize CompanyRepository with DatabaseAdapter.

        Args:
            database: Pre-configured DatabaseAdapter instance.
        """
        self.database = database

    def list(
        self,
        query: str | None = None,
        industry: str | None = None,
        limit: int = 50,
        offset: int = 0,
    ) -> list[Company]:
        """Fetch list of companies with optional search query and industry filtering.

        Args:
            query: Name or website text search term.
            industry: Filter by industry category.
            limit: Maximum items to return.
            offset: Pagination offset.

        Returns:
            List of Company domain models.
        """
        sql = "SELECT id, name, website_url, linkedin_url, headquarters, offices_summary, geographic_coverage, industry, business_type, employee_range, founded_year, ownership, created_at, updated_at FROM companies WHERE 1=1"
        params: list[Any] = []

        if query:
            sql += " AND (name LIKE ? OR website_url LIKE ?)"
            term = f"%{query}%"
            params.extend([term, term])

        if industry:
            sql += " AND industry = ?"
            params.append(industry)

        sql += " ORDER BY id ASC LIMIT ? OFFSET ?"
        params.extend([limit, offset])

        rows = self.database.execute(sql, params)
        return [Company.from_row(row) for row in rows]

    def get_by_id(self, company_id: int) -> Company | None:
        """Fetch a single company by primary key ID.

        Args:
            company_id: Primary key integer ID.

        Returns:
            Company domain model or None if not found.
        """
        rows = self.database.execute(
            "SELECT id, name, website_url, linkedin_url, headquarters, offices_summary, geographic_coverage, industry, business_type, employee_range, founded_year, ownership, created_at, updated_at FROM companies WHERE id = ?",
            [company_id],
        )
        if not rows:
            return None
        return Company.from_row(rows[0])

    def create(self, company: Company) -> Company:
        """Create a new company record.

        Args:
            company: Company object to persist.

        Returns:
            Company object populated with generated primary key ID.
        """
        sql = """
            INSERT INTO companies (
                name, website_url, linkedin_url, headquarters, offices_summary,
                geographic_coverage, industry, business_type, employee_range,
                founded_year, ownership
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        params = [
            company.name,
            company.website_url,
            company.linkedin_url,
            company.headquarters,
            company.offices_summary,
            company.geographic_coverage,
            company.industry,
            company.business_type,
            company.employee_range,
            company.founded_year,
            company.ownership,
        ]
        inserted = self.database.execute(sql, params)
        if inserted and "id" in inserted[0]:
            company.id = inserted[0]["id"]
        return company

    def update(self, company: Company) -> Company | None:
        """Update an existing company record.

        Args:
            company: Company model with updated fields.

        Returns:
            Updated Company model or None if record did not exist.
        """
        if company.id is None:
            return None

        sql = """
            UPDATE companies SET
                name = ?, website_url = ?, linkedin_url = ?, headquarters = ?,
                offices_summary = ?, geographic_coverage = ?, industry = ?,
                business_type = ?, employee_range = ?, founded_year = ?,
                ownership = ?, updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
        """
        params = [
            company.name,
            company.website_url,
            company.linkedin_url,
            company.headquarters,
            company.offices_summary,
            company.geographic_coverage,
            company.industry,
            company.business_type,
            company.employee_range,
            company.founded_year,
            company.ownership,
            company.id,
        ]
        self.database.execute(sql, params)
        return self.get_by_id(company.id)

    def delete(self, company_id: int) -> bool:
        """Delete a company record by primary key ID.

        Args:
            company_id: Primary key ID to delete.

        Returns:
            True if deletion was executed.
        """
        self.database.execute("DELETE FROM companies WHERE id = ?", [company_id])
        return True
