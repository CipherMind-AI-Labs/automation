from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass
class DigitalAssessment:
    """Domain model representing digital capability audit details."""

    research_profile_id: int | None = None
    website_quality_score: int | None = None
    mobile_friendly: str | None = None
    blog_status: str | None = None
    product_search_status: str | None = None
    product_filters_status: str | None = None
    product_catalog_status: str | None = None
    ecommerce_status: str | None = None
    quote_request_method: str | None = None
    public_pricing_status: str | None = None
    cms: str | None = None
    pim_detection: str | None = None
    dam_detection: str | None = None
    technology_clues: str | None = None
    digital_maturity: str | None = None

    @classmethod
    def from_row(cls, row: dict[str, Any]) -> DigitalAssessment:
        """Construct DigitalAssessment from database row dict."""
        return cls(
            research_profile_id=row.get("research_profile_id"),
            website_quality_score=row.get("website_quality_score"),
            mobile_friendly=row.get("mobile_friendly"),
            blog_status=row.get("blog_status"),
            product_search_status=row.get("product_search_status"),
            product_filters_status=row.get("product_filters_status"),
            product_catalog_status=row.get("product_catalog_status"),
            ecommerce_status=row.get("ecommerce_status"),
            quote_request_method=row.get("quote_request_method"),
            public_pricing_status=row.get("public_pricing_status"),
            cms=row.get("cms"),
            pim_detection=row.get("pim_detection"),
            dam_detection=row.get("dam_detection"),
            technology_clues=row.get("technology_clues"),
            digital_maturity=row.get("digital_maturity"),
        )

    def to_dict(self) -> dict[str, Any]:
        """Serialize DigitalAssessment into a dictionary."""
        return {
            "research_profile_id": self.research_profile_id,
            "website_quality_score": self.website_quality_score,
            "mobile_friendly": self.mobile_friendly,
            "blog_status": self.blog_status,
            "product_search_status": self.product_search_status,
            "product_filters_status": self.product_filters_status,
            "product_catalog_status": self.product_catalog_status,
            "ecommerce_status": self.ecommerce_status,
            "quote_request_method": self.quote_request_method,
            "public_pricing_status": self.public_pricing_status,
            "cms": self.cms,
            "pim_detection": self.pim_detection,
            "dam_detection": self.dam_detection,
            "technology_clues": self.technology_clues,
            "digital_maturity": self.digital_maturity,
        }
