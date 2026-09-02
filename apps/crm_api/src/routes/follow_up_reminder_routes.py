from __future__ import annotations

from typing import Any

from src.routes.router import Router
from src.services.follow_up_reminder_service import FollowUpReminderService
from src.utils.response import error_response, success_response


class FollowUpReminderRoutes:
    """HTTP route handlers for follow-up reminders."""

    def __init__(self, service: FollowUpReminderService) -> None:
        """Initialize route handlers with FollowUpReminderService."""
        self.service = service

    def register(self, router: Router) -> None:
        """Register reminder endpoints on router."""
        router.add_route("GET", "/api/reminders", self.list_reminders)
        router.add_route("POST", "/api/reminders", self.create_reminder)
        router.add_route("GET", "/api/reminders/:id", self.get_reminder)
        router.add_route("PUT", "/api/reminders/:id", self.update_reminder)
        router.add_route("DELETE", "/api/reminders/:id", self.delete_reminder)

    def list_reminders(
        self,
        path_params: dict[str, str],
        query_params: dict[str, str],
        payload: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """GET /api/reminders"""
        opp_id = int(query_params["opportunity_id"]) if "opportunity_id" in query_params else None
        status = query_params.get("status")
        limit = int(query_params.get("limit", "50"))
        offset = int(query_params.get("offset", "0"))

        reminders = self.service.list_reminders(
            opportunity_id=opp_id,
            status=status,
            limit=limit,
            offset=offset,
        )
        return success_response([r.to_dict() for r in reminders])

    def get_reminder(
        self,
        path_params: dict[str, str],
        query_params: dict[str, str],
        payload: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """GET /api/reminders/:id"""
        try:
            reminder_id = int(path_params["id"])
        except ValueError:
            return error_response("invalid_reminder_id", status_code=400)

        reminder = self.service.get_reminder(reminder_id)
        if reminder is None:
            return error_response("reminder_not_found", status_code=404)
        return success_response(reminder.to_dict())

    def create_reminder(
        self,
        path_params: dict[str, str],
        query_params: dict[str, str],
        payload: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """POST /api/reminders"""
        if not payload or not payload.get("opportunity_id") or not payload.get("due_at"):
            return error_response(
                "validation_error",
                status_code=400,
                details="Fields 'opportunity_id' and 'due_at' are required.",
            )

        reminder = self.service.create_reminder(payload)
        return success_response(reminder.to_dict(), status_code=201)

    def update_reminder(
        self,
        path_params: dict[str, str],
        query_params: dict[str, str],
        payload: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """PUT /api/reminders/:id"""
        try:
            reminder_id = int(path_params["id"])
        except ValueError:
            return error_response("invalid_reminder_id", status_code=400)

        updated = self.service.update_reminder(reminder_id, payload or {})
        if updated is None:
            return error_response("reminder_not_found", status_code=404)
        return success_response(updated.to_dict())

    def delete_reminder(
        self,
        path_params: dict[str, str],
        query_params: dict[str, str],
        payload: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """DELETE /api/reminders/:id"""
        try:
            reminder_id = int(path_params["id"])
        except ValueError:
            return error_response("invalid_reminder_id", status_code=400)

        deleted = self.service.delete_reminder(reminder_id)
        if not deleted:
            return error_response("reminder_not_found", status_code=404)
        return success_response(None, status_code=204)
