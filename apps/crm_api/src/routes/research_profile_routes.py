from __future__ import annotations

from typing import Any

from src.routes.router import Router
from src.services.research_profile_service import ResearchProfileService
from src.utils.response import error_response, success_response


class ResearchProfileRoutes:
    """HTTP route handlers for research profiles and associated assessments."""

    def __init__(self, service: ResearchProfileService) -> None:
        """Initialize route handlers with service instance."""
        self.service = service

    def register(self, router: Router) -> None:
        """Register routes with HTTP router."""
        router.add_route("GET", "/api/research-profiles", self.list_profiles)
        router.add_route("POST", "/api/research-profiles", self.create_profile)
        router.add_route("GET", "/api/research-profiles/:id", self.get_profile)
        router.add_route("PUT", "/api/research-profiles/:id", self.update_profile)
        router.add_route("DELETE", "/api/research-profiles/:id", self.delete_profile)
        router.add_route("POST", "/api/research-profiles/:id/sources", self.add_source)

    def list_profiles(
        self,
        path_params: dict[str, str],
        query_params: dict[str, str],
        payload: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """GET /api/research-profiles"""
        company_id = int(query_params["company_id"]) if "company_id" in query_params else None
        limit = int(query_params.get("limit", "50"))
        offset = int(query_params.get("offset", "0"))

        profiles = self.service.list_profiles(company_id=company_id, limit=limit, offset=offset)
        return success_response(profiles)

    def get_profile(
        self,
        path_params: dict[str, str],
        query_params: dict[str, str],
        payload: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """GET /api/research-profiles/:id"""
        try:
            profile_id = int(path_params["id"])
        except ValueError:
            return error_response("invalid_profile_id", status_code=400)

        profile = self.service.get_profile(profile_id)
        if profile is None:
            return error_response("research_profile_not_found", status_code=404)
        return success_response(profile)

    def create_profile(
        self,
        path_params: dict[str, str],
        query_params: dict[str, str],
        payload: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """POST /api/research-profiles"""
        if not payload or not payload.get("company_id"):
            return error_response("validation_error", status_code=400, details="Field 'company_id' is required.")

        profile = self.service.create_profile(payload)
        return success_response(profile, status_code=201)

    def update_profile(
        self,
        path_params: dict[str, str],
        query_params: dict[str, str],
        payload: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """PUT /api/research-profiles/:id"""
        try:
            profile_id = int(path_params["id"])
        except ValueError:
            return error_response("invalid_profile_id", status_code=400)

        updated = self.service.update_profile(profile_id, payload or {})
        if updated is None:
            return error_response("research_profile_not_found", status_code=404)
        return success_response(updated)

    def delete_profile(
        self,
        path_params: dict[str, str],
        query_params: dict[str, str],
        payload: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """DELETE /api/research-profiles/:id"""
        try:
            profile_id = int(path_params["id"])
        except ValueError:
            return error_response("invalid_profile_id", status_code=400)

        deleted = self.service.delete_profile(profile_id)
        if not deleted:
            return error_response("research_profile_not_found", status_code=404)
        return success_response(None, status_code=204)

    def add_source(
        self,
        path_params: dict[str, str],
        query_params: dict[str, str],
        payload: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """POST /api/research-profiles/:id/sources"""
        try:
            profile_id = int(path_params["id"])
        except ValueError:
            return error_response("invalid_profile_id", status_code=400)

        if not payload or not payload.get("source_name"):
            return error_response("validation_error", status_code=400, details="Field 'source_name' is required.")

        source = self.service.add_source(profile_id, payload)
        if source is None:
            return error_response("research_profile_not_found", status_code=404)
        return success_response(source, status_code=201)
