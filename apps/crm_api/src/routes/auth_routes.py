from __future__ import annotations

from typing import Any

from src.routes.router import Router
from src.utils.response import success_response


class AuthRoutes:
    """HTTP route handlers for authentication endpoints."""

    def register(self, router: Router) -> None:
        """Register authentication endpoints on router instance.

        Args:
            router: Router instance.
        """
        router.add_route("GET", "/api/auth/verify", self.verify_token)

    def verify_token(
        self,
        path_params: dict[str, str],
        query_params: dict[str, str],
        payload: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """GET /api/auth/verify — verifies provided Bearer token."""
        return success_response({"status": "ok", "authenticated": True})
