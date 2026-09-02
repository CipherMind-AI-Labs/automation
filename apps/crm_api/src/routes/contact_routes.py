from __future__ import annotations

from typing import Any

from src.routes.router import Router
from src.services.contact_service import ContactService
from src.utils.response import error_response, success_response


class ContactRoutes:
    """HTTP route handlers for contact resources."""

    def __init__(self, service: ContactService) -> None:
        """Initialize route handlers with ContactService."""
        self.service = service

    def register(self, router: Router) -> None:
        """Register contact endpoints on HTTP router."""
        router.add_route("GET", "/api/contacts", self.list_contacts)
        router.add_route("POST", "/api/contacts", self.create_contact)
        router.add_route("GET", "/api/contacts/:id", self.get_contact)
        router.add_route("PUT", "/api/contacts/:id", self.update_contact)
        router.add_route("DELETE", "/api/contacts/:id", self.delete_contact)

    def list_contacts(
        self,
        path_params: dict[str, str],
        query_params: dict[str, str],
        payload: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """GET /api/contacts"""
        company_id = int(query_params["company_id"]) if "company_id" in query_params else None
        search = query_params.get("q")
        is_dm = int(query_params["is_decision_maker"]) if "is_decision_maker" in query_params else None
        limit = int(query_params.get("limit", "50"))
        offset = int(query_params.get("offset", "0"))

        contacts = self.service.list_contacts(
            company_id=company_id,
            search=search,
            is_decision_maker=is_dm,
            limit=limit,
            offset=offset,
        )
        return success_response([c.to_dict() for c in contacts])

    def get_contact(
        self,
        path_params: dict[str, str],
        query_params: dict[str, str],
        payload: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """GET /api/contacts/:id"""
        try:
            contact_id = int(path_params["id"])
        except ValueError:
            return error_response("invalid_contact_id", status_code=400)

        contact = self.service.get_contact(contact_id)
        if contact is None:
            return error_response("contact_not_found", status_code=404)
        return success_response(contact.to_dict())

    def create_contact(
        self,
        path_params: dict[str, str],
        query_params: dict[str, str],
        payload: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """POST /api/contacts"""
        if not payload or not payload.get("company_id") or not (payload.get("full_name") or payload.get("first_name")):
            return error_response(
                "validation_error",
                status_code=400,
                details="Fields 'company_id' and contact name are required.",
            )

        contact = self.service.create_contact(payload)
        return success_response(contact.to_dict(), status_code=201)

    def update_contact(
        self,
        path_params: dict[str, str],
        query_params: dict[str, str],
        payload: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """PUT /api/contacts/:id"""
        try:
            contact_id = int(path_params["id"])
        except ValueError:
            return error_response("invalid_contact_id", status_code=400)

        updated = self.service.update_contact(contact_id, payload or {})
        if updated is None:
            return error_response("contact_not_found", status_code=404)
        return success_response(updated.to_dict())

    def delete_contact(
        self,
        path_params: dict[str, str],
        query_params: dict[str, str],
        payload: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """DELETE /api/contacts/:id"""
        try:
            contact_id = int(path_params["id"])
        except ValueError:
            return error_response("invalid_contact_id", status_code=400)

        deleted = self.service.delete_contact(contact_id)
        if not deleted:
            return error_response("contact_not_found", status_code=404)
        return success_response(None, status_code=204)
