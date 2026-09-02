from __future__ import annotations

from typing import Any

from src.routes.router import Router
from src.services.opportunity_service import OpportunityService
from src.utils.response import error_response, success_response


class OpportunityRoutes:
    """HTTP route handlers for commercial deal opportunities."""

    def __init__(self, service: OpportunityService) -> None:
        """Initialize route handlers with OpportunityService."""
        self.service = service

    def register(self, router: Router) -> None:
        """Register opportunity endpoints on HTTP router."""
        router.add_route("GET", "/api/opportunities", self.list_opportunities)
        router.add_route("POST", "/api/opportunities", self.create_opportunity)
        router.add_route("GET", "/api/opportunities/:id", self.get_opportunity)
        router.add_route("PUT", "/api/opportunities/:id", self.update_opportunity)
        router.add_route("DELETE", "/api/opportunities/:id", self.delete_opportunity)

    def list_opportunities(
        self,
        path_params: dict[str, str],
        query_params: dict[str, str],
        payload: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """GET /api/opportunities"""
        company_id = int(query_params["company_id"]) if "company_id" in query_params else None
        lead_status = query_params.get("lead_status")
        priority = query_params.get("priority")
        limit = int(query_params.get("limit", "50"))
        offset = int(query_params.get("offset", "0"))

        opportunities = self.service.list_opportunities(
            company_id=company_id,
            lead_status=lead_status,
            priority=priority,
            limit=limit,
            offset=offset,
        )
        return success_response([o.to_dict() for o in opportunities])

    def get_opportunity(
        self,
        path_params: dict[str, str],
        query_params: dict[str, str],
        payload: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """GET /api/opportunities/:id"""
        try:
            opp_id = int(path_params["id"])
        except ValueError:
            return error_response("invalid_opportunity_id", status_code=400)

        opportunity = self.service.get_opportunity(opp_id)
        if opportunity is None:
            return error_response("opportunity_not_found", status_code=404)
        return success_response(opportunity.to_dict())

    def create_opportunity(
        self,
        path_params: dict[str, str],
        query_params: dict[str, str],
        payload: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """POST /api/opportunities"""
        if not payload or not payload.get("company_id"):
            return error_response("validation_error", status_code=400, details="Field 'company_id' is required.")

        opportunity = self.service.create_opportunity(payload)
        return success_response(opportunity.to_dict(), status_code=201)

    def update_opportunity(
        self,
        path_params: dict[str, str],
        query_params: dict[str, str],
        payload: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """PUT /api/opportunities/:id"""
        try:
            opp_id = int(path_params["id"])
        except ValueError:
            return error_response("invalid_opportunity_id", status_code=400)

        updated = self.service.update_opportunity(opp_id, payload or {})
        if updated is None:
            return error_response("opportunity_not_found", status_code=404)
        return success_response(updated.to_dict())

    def delete_opportunity(
        self,
        path_params: dict[str, str],
        query_params: dict[str, str],
        payload: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """DELETE /api/opportunities/:id"""
        try:
            opp_id = int(path_params["id"])
        except ValueError:
            return error_response("invalid_opportunity_id", status_code=400)

        deleted = self.service.delete_opportunity(opp_id)
        if not deleted:
            return error_response("opportunity_not_found", status_code=404)
        return success_response(None, status_code=204)
