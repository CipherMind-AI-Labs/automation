from __future__ import annotations

from typing import Any

from src.routes.router import Router
from src.services.company_service import CompanyService
from src.utils.response import error_response, success_response


class CompanyRoutes:
    """HTTP route handlers for company resources."""

    def __init__(self, service: CompanyService) -> None:
        """Initialize company routes with service instance."""
        self.service = service

    def register(self, router: Router) -> None:
        """Register company endpoints on router instance.

        Args:
            router: Router instance.
        """
        router.add_route("GET", "/api/companies", self.list_companies)
        router.add_route("POST", "/api/companies", self.create_company)
        router.add_route("GET", "/api/companies/:id", self.get_company)
        router.add_route("PUT", "/api/companies/:id", self.update_company)
        router.add_route("DELETE", "/api/companies/:id", self.delete_company)

    def list_companies(
        self,
        path_params: dict[str, str],
        query_params: dict[str, str],
        payload: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """GET /api/companies"""
        query = query_params.get("q")
        industry = query_params.get("industry")
        limit = int(query_params.get("limit", "50"))
        offset = int(query_params.get("offset", "0"))

        companies = self.service.list_companies(query=query, industry=industry, limit=limit, offset=offset)
        return success_response([c.to_dict() for c in companies])

    def get_company(
        self,
        path_params: dict[str, str],
        query_params: dict[str, str],
        payload: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """GET /api/companies/:id"""
        try:
            company_id = int(path_params["id"])
        except ValueError:
            return error_response("invalid_company_id", status_code=400)

        company = self.service.get_company(company_id)
        if company is None:
            return error_response("company_not_found", status_code=404)
        return success_response(company.to_dict())

    def create_company(
        self,
        path_params: dict[str, str],
        query_params: dict[str, str],
        payload: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """POST /api/companies"""
        if not payload or not payload.get("name"):
            return error_response("validation_error", status_code=400, details="Field 'name' is required.")

        company = self.service.create_company(payload)
        return success_response(company.to_dict(), status_code=201)

    def update_company(
        self,
        path_params: dict[str, str],
        query_params: dict[str, str],
        payload: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """PUT /api/companies/:id"""
        try:
            company_id = int(path_params["id"])
        except ValueError:
            return error_response("invalid_company_id", status_code=400)

        updated = self.service.update_company(company_id, payload or {})
        if updated is None:
            return error_response("company_not_found", status_code=404)
        return success_response(updated.to_dict())

    def delete_company(
        self,
        path_params: dict[str, str],
        query_params: dict[str, str],
        payload: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """DELETE /api/companies/:id"""
        try:
            company_id = int(path_params["id"])
        except ValueError:
            return error_response("invalid_company_id", status_code=400)

        deleted = self.service.delete_company(company_id)
        if not deleted:
            return error_response("company_not_found", status_code=404)
        return success_response(None, status_code=204)
