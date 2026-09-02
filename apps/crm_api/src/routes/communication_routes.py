from __future__ import annotations

from typing import Any

from src.routes.router import Router
from src.services.communication_service import CommunicationService
from src.utils.response import error_response, success_response


class CommunicationRoutes:
    """HTTP route handlers for communication threads, messages, and events."""

    def __init__(self, service: CommunicationService) -> None:
        """Initialize route handlers with CommunicationService."""
        self.service = service

    def register(self, router: Router) -> None:
        """Register communication endpoints on router."""
        router.add_route("GET", "/api/communication-threads", self.list_threads)
        router.add_route("POST", "/api/communication-threads", self.create_thread)
        router.add_route("GET", "/api/communication-threads/:id", self.get_thread)
        router.add_route("PUT", "/api/communication-threads/:id", self.update_thread)
        router.add_route("DELETE", "/api/communication-threads/:id", self.delete_thread)

        router.add_route("GET", "/api/communications", self.list_communications)
        router.add_route("POST", "/api/communications", self.create_communication)
        router.add_route("GET", "/api/communications/:id", self.get_communication)
        router.add_route("PUT", "/api/communications/:id", self.update_communication)
        router.add_route("DELETE", "/api/communications/:id", self.delete_communication)
        router.add_route("POST", "/api/communications/:id/events", self.create_event)

    # --- Communication Threads ---

    def list_threads(
        self,
        path_params: dict[str, str],
        query_params: dict[str, str],
        payload: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """GET /api/communication-threads"""
        company_id = int(query_params["company_id"]) if "company_id" in query_params else None
        opp_id = int(query_params["opportunity_id"]) if "opportunity_id" in query_params else None
        status = query_params.get("thread_status")
        limit = int(query_params.get("limit", "50"))
        offset = int(query_params.get("offset", "0"))

        threads = self.service.list_threads(
            company_id=company_id,
            opportunity_id=opp_id,
            thread_status=status,
            limit=limit,
            offset=offset,
        )
        return success_response([t.to_dict() for t in threads])

    def get_thread(
        self,
        path_params: dict[str, str],
        query_params: dict[str, str],
        payload: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """GET /api/communication-threads/:id"""
        try:
            thread_id = int(path_params["id"])
        except ValueError:
            return error_response("invalid_thread_id", status_code=400)

        thread = self.service.get_thread(thread_id)
        if thread is None:
            return error_response("thread_not_found", status_code=404)
        return success_response(thread)

    def create_thread(
        self,
        path_params: dict[str, str],
        query_params: dict[str, str],
        payload: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """POST /api/communication-threads"""
        if not payload or not payload.get("company_id"):
            return error_response("validation_error", status_code=400, details="Field 'company_id' is required.")

        thread = self.service.create_thread(payload)
        return success_response(thread.to_dict(), status_code=201)

    def update_thread(
        self,
        path_params: dict[str, str],
        query_params: dict[str, str],
        payload: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """PUT /api/communication-threads/:id"""
        try:
            thread_id = int(path_params["id"])
        except ValueError:
            return error_response("invalid_thread_id", status_code=400)

        updated = self.service.update_thread(thread_id, payload or {})
        if updated is None:
            return error_response("thread_not_found", status_code=404)
        return success_response(updated.to_dict())

    def delete_thread(
        self,
        path_params: dict[str, str],
        query_params: dict[str, str],
        payload: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """DELETE /api/communication-threads/:id"""
        try:
            thread_id = int(path_params["id"])
        except ValueError:
            return error_response("invalid_thread_id", status_code=400)

        deleted = self.service.delete_thread(thread_id)
        if not deleted:
            return error_response("thread_not_found", status_code=404)
        return success_response(None, status_code=204)

    # --- Communications ---

    def list_communications(
        self,
        path_params: dict[str, str],
        query_params: dict[str, str],
        payload: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """GET /api/communications"""
        thread_id = int(query_params["thread_id"]) if "thread_id" in query_params else None
        contact_id = int(query_params["contact_id"]) if "contact_id" in query_params else None
        status = query_params.get("message_status")
        limit = int(query_params.get("limit", "50"))
        offset = int(query_params.get("offset", "0"))

        messages = self.service.list_communications(
            thread_id=thread_id,
            contact_id=contact_id,
            message_status=status,
            limit=limit,
            offset=offset,
        )
        return success_response([m.to_dict() for m in messages])

    def get_communication(
        self,
        path_params: dict[str, str],
        query_params: dict[str, str],
        payload: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """GET /api/communications/:id"""
        try:
            comm_id = int(path_params["id"])
        except ValueError:
            return error_response("invalid_communication_id", status_code=400)

        comm = self.service.get_communication(comm_id)
        if comm is None:
            return error_response("communication_not_found", status_code=404)
        return success_response(comm)

    def create_communication(
        self,
        path_params: dict[str, str],
        query_params: dict[str, str],
        payload: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """POST /api/communications"""
        if not payload or not payload.get("thread_id"):
            return error_response("validation_error", status_code=400, details="Field 'thread_id' is required.")

        comm = self.service.create_communication(payload)
        return success_response(comm.to_dict(), status_code=201)

    def update_communication(
        self,
        path_params: dict[str, str],
        query_params: dict[str, str],
        payload: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """PUT /api/communications/:id"""
        try:
            comm_id = int(path_params["id"])
        except ValueError:
            return error_response("invalid_communication_id", status_code=400)

        updated = self.service.update_communication(comm_id, payload or {})
        if updated is None:
            return error_response("communication_not_found", status_code=404)
        return success_response(updated.to_dict())

    def delete_communication(
        self,
        path_params: dict[str, str],
        query_params: dict[str, str],
        payload: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """DELETE /api/communications/:id"""
        try:
            comm_id = int(path_params["id"])
        except ValueError:
            return error_response("invalid_communication_id", status_code=400)

        deleted = self.service.delete_communication(comm_id)
        if not deleted:
            return error_response("communication_not_found", status_code=404)
        return success_response(None, status_code=204)

    def create_event(
        self,
        path_params: dict[str, str],
        query_params: dict[str, str],
        payload: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """POST /api/communications/:id/events"""
        try:
            comm_id = int(path_params["id"])
        except ValueError:
            return error_response("invalid_communication_id", status_code=400)

        if not payload or not payload.get("event_type") or not payload.get("occurred_at"):
            return error_response(
                "validation_error",
                status_code=400,
                details="Fields 'event_type' and 'occurred_at' are required.",
            )

        event = self.service.create_event(comm_id, payload)
        if event is None:
            return error_response("communication_not_found", status_code=404)
        return success_response(event.to_dict(), status_code=201)
