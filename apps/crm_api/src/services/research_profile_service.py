from __future__ import annotations

from typing import Any

from src.models.digital_assessment import DigitalAssessment
from src.models.product_assessment import ProductAssessment
from src.models.research_profile import ResearchProfile
from src.models.research_source import ResearchSource
from src.repositories.digital_assessment_repository import DigitalAssessmentRepository
from src.repositories.product_assessment_repository import ProductAssessmentRepository
from src.repositories.research_profile_repository import ResearchProfileRepository
from src.repositories.research_source_repository import ResearchSourceRepository


class ResearchProfileService:
    """Business operations service for research profiles, assessments, and research sources."""

    def __init__(
        self,
        profile_repo: ResearchProfileRepository,
        digital_repo: DigitalAssessmentRepository,
        product_repo: ProductAssessmentRepository,
        source_repo: ResearchSourceRepository,
    ) -> None:
        """Initialize service with repositories.

        Args:
            profile_repo: ResearchProfileRepository instance.
            digital_repo: DigitalAssessmentRepository instance.
            product_repo: ProductAssessmentRepository instance.
            source_repo: ResearchSourceRepository instance.
        """
        self.profile_repo = profile_repo
        self.digital_repo = digital_repo
        self.product_repo = product_repo
        self.source_repo = source_repo

    def list_profiles(self, company_id: int | None = None, limit: int = 50, offset: int = 0) -> list[dict[str, Any]]:
        """List research profiles with composite assessment and source data.

        Args:
            company_id: Company filter ID.
            limit: Page size.
            offset: Page offset.

        Returns:
            List of dictionary profiles.
        """
        profiles = self.profile_repo.list(company_id=company_id, limit=limit, offset=offset)
        result: list[dict[str, Any]] = []
        for p in profiles:
            p_dict = p.to_dict()
            if p.id is not None:
                digital = self.digital_repo.get_by_profile_id(p.id)
                product = self.product_repo.get_by_profile_id(p.id)
                sources = self.source_repo.list_by_profile_id(p.id)
                p_dict["digital_assessment"] = digital.to_dict() if digital else None
                p_dict["product_assessment"] = product.to_dict() if product else None
                p_dict["sources"] = [s.to_dict() for s in sources]
            result.append(p_dict)
        return result

    def get_profile(self, profile_id: int) -> dict[str, Any] | None:
        """Fetch research profile with digital assessment, product assessment, and sources.

        Args:
            profile_id: Profile ID.

        Returns:
            Complete research profile dictionary or None.
        """
        profile = self.profile_repo.get_by_id(profile_id)
        if profile is None or profile.id is None:
            return None

        p_dict = profile.to_dict()
        digital = self.digital_repo.get_by_profile_id(profile.id)
        product = self.product_repo.get_by_profile_id(profile.id)
        sources = self.source_repo.list_by_profile_id(profile.id)

        p_dict["digital_assessment"] = digital.to_dict() if digital else None
        p_dict["product_assessment"] = product.to_dict() if product else None
        p_dict["sources"] = [s.to_dict() for s in sources]
        return p_dict

    def create_profile(self, payload: dict[str, Any]) -> dict[str, Any]:
        """Create a new research profile with optional digital/product assessments and sources.

        Args:
            payload: Input dictionary.

        Returns:
            Created research profile dictionary with full child records.
        """
        digital_data = payload.pop("digital_assessment", None)
        product_data = payload.pop("product_assessment", None)
        sources_data = payload.pop("sources", [])

        profile = ResearchProfile.from_row(payload)
        created_profile = self.profile_repo.create(profile)
        profile_id = created_profile.id

        if profile_id is not None:
            if digital_data:
                digital = DigitalAssessment.from_row({**digital_data, "research_profile_id": profile_id})
                self.digital_repo.create_or_update(digital)

            if product_data:
                product = ProductAssessment.from_row({**product_data, "research_profile_id": profile_id})
                self.product_repo.create_or_update(product)

            if isinstance(sources_data, list):
                for s_data in sources_data:
                    source = ResearchSource.from_row({**s_data, "research_profile_id": profile_id})
                    self.source_repo.create(source)

        return self.get_profile(profile_id) or created_profile.to_dict()  # type: ignore[arg-type]

    def update_profile(self, profile_id: int, payload: dict[str, Any]) -> dict[str, Any] | None:
        """Update an existing research profile and nested assessments.

        Args:
            profile_id: Profile ID.
            payload: Update fields payload dictionary.

        Returns:
            Updated profile dictionary or None if profile does not exist.
        """
        existing = self.profile_repo.get_by_id(profile_id)
        if existing is None:
            return None

        digital_data = payload.pop("digital_assessment", None)
        product_data = payload.pop("product_assessment", None)

        update_data = {**existing.to_dict(), **payload, "id": profile_id}
        profile = ResearchProfile.from_row(update_data)
        self.profile_repo.update(profile)

        if digital_data:
            digital = DigitalAssessment.from_row({**digital_data, "research_profile_id": profile_id})
            self.digital_repo.create_or_update(digital)

        if product_data:
            product = ProductAssessment.from_row({**product_data, "research_profile_id": profile_id})
            self.product_repo.create_or_update(product)

        return self.get_profile(profile_id)

    def delete_profile(self, profile_id: int) -> bool:
        """Delete a research profile.

        Args:
            profile_id: Target profile ID.

        Returns:
            True if profile was deleted.
        """
        existing = self.profile_repo.get_by_id(profile_id)
        if existing is None:
            return False
        return self.profile_repo.delete(profile_id)

    def add_source(self, profile_id: int, source_payload: dict[str, Any]) -> dict[str, Any] | None:
        """Add a research citation source to a profile.

        Args:
            profile_id: Target research profile ID.
            source_payload: Citation metadata.

        Returns:
            Created ResearchSource dict or None if profile not found.
        """
        existing = self.profile_repo.get_by_id(profile_id)
        if existing is None:
            return None
        source = ResearchSource.from_row({**source_payload, "research_profile_id": profile_id})
        created = self.source_repo.create(source)
        return created.to_dict()
