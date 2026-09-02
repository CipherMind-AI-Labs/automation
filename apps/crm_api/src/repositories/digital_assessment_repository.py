from __future__ import annotations

from src.database.base import DatabaseAdapter
from src.models.digital_assessment import DigitalAssessment


class DigitalAssessmentRepository:
    """Repository for DigitalAssessment operations (primary key `research_profile_id`)."""

    def __init__(self, database: DatabaseAdapter) -> None:
        """Initialize repository with DatabaseAdapter."""
        self.database = database

    def get_by_profile_id(self, research_profile_id: int) -> DigitalAssessment | None:
        """Fetch DigitalAssessment by research profile ID.

        Args:
            research_profile_id: Research profile foreign key PK.

        Returns:
            DigitalAssessment domain model or None.
        """
        rows = self.database.execute(
            "SELECT research_profile_id, website_quality_score, mobile_friendly, blog_status, product_search_status, product_filters_status, product_catalog_status, ecommerce_status, quote_request_method, public_pricing_status, cms, pim_detection, dam_detection, technology_clues, digital_maturity FROM digital_assessments WHERE research_profile_id = ?",
            [research_profile_id],
        )
        if not rows:
            return None
        return DigitalAssessment.from_row(rows[0])

    def create_or_update(self, assessment: DigitalAssessment) -> DigitalAssessment:
        """Upsert digital assessment record.

        Args:
            assessment: DigitalAssessment instance.

        Returns:
            Saved DigitalAssessment model.
        """
        existing = self.get_by_profile_id(assessment.research_profile_id)  # type: ignore[arg-type]
        if existing is None:
            sql = """
                INSERT INTO digital_assessments (
                    research_profile_id, website_quality_score, mobile_friendly, blog_status,
                    product_search_status, product_filters_status, product_catalog_status,
                    ecommerce_status, quote_request_method, public_pricing_status, cms,
                    pim_detection, dam_detection, technology_clues, digital_maturity
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """
            params = [
                assessment.research_profile_id,
                assessment.website_quality_score,
                assessment.mobile_friendly,
                assessment.blog_status,
                assessment.product_search_status,
                assessment.product_filters_status,
                assessment.product_catalog_status,
                assessment.ecommerce_status,
                assessment.quote_request_method,
                assessment.public_pricing_status,
                assessment.cms,
                assessment.pim_detection,
                assessment.dam_detection,
                assessment.technology_clues,
                assessment.digital_maturity,
            ]
            self.database.execute(sql, params)
        else:
            sql = """
                UPDATE digital_assessments SET
                    website_quality_score = ?, mobile_friendly = ?, blog_status = ?,
                    product_search_status = ?, product_filters_status = ?,
                    product_catalog_status = ?, ecommerce_status = ?,
                    quote_request_method = ?, public_pricing_status = ?, cms = ?,
                    pim_detection = ?, dam_detection = ?, technology_clues = ?,
                    digital_maturity = ?
                WHERE research_profile_id = ?
            """
            params = [
                assessment.website_quality_score,
                assessment.mobile_friendly,
                assessment.blog_status,
                assessment.product_search_status,
                assessment.product_filters_status,
                assessment.product_catalog_status,
                assessment.ecommerce_status,
                assessment.quote_request_method,
                assessment.public_pricing_status,
                assessment.cms,
                assessment.pim_detection,
                assessment.dam_detection,
                assessment.technology_clues,
                assessment.digital_maturity,
                assessment.research_profile_id,
            ]
            self.database.execute(sql, params)

        return self.get_by_profile_id(assessment.research_profile_id) or assessment  # type: ignore[arg-type]

    def delete(self, research_profile_id: int) -> bool:
        """Delete digital assessment record.

        Args:
            research_profile_id: Target profile ID.

        Returns:
            True if deletion was executed.
        """
        self.database.execute(
            "DELETE FROM digital_assessments WHERE research_profile_id = ?",
            [research_profile_id],
        )
        return True
