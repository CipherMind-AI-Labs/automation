from __future__ import annotations

from src.database.base import DatabaseAdapter
from src.models.product_assessment import ProductAssessment


class ProductAssessmentRepository:
    """Repository for ProductAssessment operations (primary key `research_profile_id`)."""

    def __init__(self, database: DatabaseAdapter) -> None:
        """Initialize repository with DatabaseAdapter."""
        self.database = database

    def get_by_profile_id(self, research_profile_id: int) -> ProductAssessment | None:
        """Fetch ProductAssessment by research profile ID.

        Args:
            research_profile_id: Profile ID.

        Returns:
            ProductAssessment model or None.
        """
        rows = self.database.execute(
            "SELECT research_profile_id, manufacturers_represented, estimated_brands, product_pages, product_search_experience, product_filters_quality, images_status, product_descriptions_status, specifications_status, cad_revit_status, brochures_status, sustainability_warranty_docs_status, product_attributes_completeness_score, data_ownership, product_information_quality_score, estimated_catalog_size FROM product_assessments WHERE research_profile_id = ?",
            [research_profile_id],
        )
        if not rows:
            return None
        return ProductAssessment.from_row(rows[0])

    def create_or_update(self, assessment: ProductAssessment) -> ProductAssessment:
        """Upsert product assessment record.

        Args:
            assessment: ProductAssessment model to save.

        Returns:
            Saved ProductAssessment model.
        """
        existing = self.get_by_profile_id(assessment.research_profile_id)  # type: ignore[arg-type]
        if existing is None:
            sql = """
                INSERT INTO product_assessments (
                    research_profile_id, manufacturers_represented, estimated_brands,
                    product_pages, product_search_experience, product_filters_quality,
                    images_status, product_descriptions_status, specifications_status,
                    cad_revit_status, brochures_status, sustainability_warranty_docs_status,
                    product_attributes_completeness_score, data_ownership,
                    product_information_quality_score, estimated_catalog_size
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """
            params = [
                assessment.research_profile_id,
                assessment.manufacturers_represented,
                assessment.estimated_brands,
                assessment.product_pages,
                assessment.product_search_experience,
                assessment.product_filters_quality,
                assessment.images_status,
                assessment.product_descriptions_status,
                assessment.specifications_status,
                assessment.cad_revit_status,
                assessment.brochures_status,
                assessment.sustainability_warranty_docs_status,
                assessment.product_attributes_completeness_score,
                assessment.data_ownership,
                assessment.product_information_quality_score,
                assessment.estimated_catalog_size,
            ]
            self.database.execute(sql, params)
        else:
            sql = """
                UPDATE product_assessments SET
                    manufacturers_represented = ?, estimated_brands = ?, product_pages = ?,
                    product_search_experience = ?, product_filters_quality = ?, images_status = ?,
                    product_descriptions_status = ?, specifications_status = ?, cad_revit_status = ?,
                    brochures_status = ?, sustainability_warranty_docs_status = ?,
                    product_attributes_completeness_score = ?, data_ownership = ?,
                    product_information_quality_score = ?, estimated_catalog_size = ?
                WHERE research_profile_id = ?
            """
            params = [
                assessment.manufacturers_represented,
                assessment.estimated_brands,
                assessment.product_pages,
                assessment.product_search_experience,
                assessment.product_filters_quality,
                assessment.images_status,
                assessment.product_descriptions_status,
                assessment.specifications_status,
                assessment.cad_revit_status,
                assessment.brochures_status,
                assessment.sustainability_warranty_docs_status,
                assessment.product_attributes_completeness_score,
                assessment.data_ownership,
                assessment.product_information_quality_score,
                assessment.estimated_catalog_size,
                assessment.research_profile_id,
            ]
            self.database.execute(sql, params)

        return self.get_by_profile_id(assessment.research_profile_id) or assessment  # type: ignore[arg-type]

    def delete(self, research_profile_id: int) -> bool:
        """Delete product assessment record.

        Args:
            research_profile_id: Profile ID.

        Returns:
            True if deletion was executed.
        """
        self.database.execute(
            "DELETE FROM product_assessments WHERE research_profile_id = ?",
            [research_profile_id],
        )
        return True
