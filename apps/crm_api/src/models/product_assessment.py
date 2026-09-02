from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass
class ProductAssessment:
    """Domain model representing product data maturity audit details."""

    research_profile_id: int | None = None
    manufacturers_represented: str | None = None
    estimated_brands: str | None = None
    product_pages: str | None = None
    product_search_experience: str | None = None
    product_filters_quality: str | None = None
    images_status: str | None = None
    product_descriptions_status: str | None = None
    specifications_status: str | None = None
    cad_revit_status: str | None = None
    brochures_status: str | None = None
    sustainability_warranty_docs_status: str | None = None
    product_attributes_completeness_score: int | None = None
    data_ownership: str | None = None
    product_information_quality_score: int | None = None
    estimated_catalog_size: str | None = None

    @classmethod
    def from_row(cls, row: dict[str, Any]) -> ProductAssessment:
        """Construct ProductAssessment from database row dict."""
        return cls(
            research_profile_id=row.get("research_profile_id"),
            manufacturers_represented=row.get("manufacturers_represented"),
            estimated_brands=row.get("estimated_brands"),
            product_pages=row.get("product_pages"),
            product_search_experience=row.get("product_search_experience"),
            product_filters_quality=row.get("product_filters_quality"),
            images_status=row.get("images_status"),
            product_descriptions_status=row.get("product_descriptions_status"),
            specifications_status=row.get("specifications_status"),
            cad_revit_status=row.get("cad_revit_status"),
            brochures_status=row.get("brochures_status"),
            sustainability_warranty_docs_status=row.get("sustainability_warranty_docs_status"),
            product_attributes_completeness_score=row.get("product_attributes_completeness_score"),
            data_ownership=row.get("data_ownership"),
            product_information_quality_score=row.get("product_information_quality_score"),
            estimated_catalog_size=row.get("estimated_catalog_size"),
        )

    def to_dict(self) -> dict[str, Any]:
        """Serialize ProductAssessment into a dictionary."""
        return {
            "research_profile_id": self.research_profile_id,
            "manufacturers_represented": self.manufacturers_represented,
            "estimated_brands": self.estimated_brands,
            "product_pages": self.product_pages,
            "product_search_experience": self.product_search_experience,
            "product_filters_quality": self.product_filters_quality,
            "images_status": self.images_status,
            "product_descriptions_status": self.product_descriptions_status,
            "specifications_status": self.specifications_status,
            "cad_revit_status": self.cad_revit_status,
            "brochures_status": self.brochures_status,
            "sustainability_warranty_docs_status": self.sustainability_warranty_docs_status,
            "product_attributes_completeness_score": self.product_attributes_completeness_score,
            "data_ownership": self.data_ownership,
            "product_information_quality_score": self.product_information_quality_score,
            "estimated_catalog_size": self.estimated_catalog_size,
        }
