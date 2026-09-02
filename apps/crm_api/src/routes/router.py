from __future__ import annotations

import re
from typing import Any, Callable
from urllib.parse import parse_qs, urlparse

from src.utils.logger import log_error, log_info
from src.utils.response import error_response, success_response


class Router:
    """Lightweight pattern-matching HTTP router for Python Worker without external framework dependencies."""

    def __init__(self) -> None:
        """Initialize route registry mapping (HTTP method, regex_pattern) -> handler."""
        self.routes: list[tuple[str, re.Pattern[str], Callable[..., dict[str, Any]]]] = []

    def add_route(
        self,
        method: str,
        path_template: str,
        handler: Callable[..., dict[str, Any]],
    ) -> None:
        """Register a path handler template.

        Args:
            method: HTTP method string (GET, POST, PUT, DELETE).
            path_template: Route template with `:param` markers (e.g. `/api/companies/:id`).
            handler: Callable returning response dict.
        """
        # Convert path_template like /api/companies/:id into regex
        pattern_str = "^" + re.sub(r":([a-zA-Z_]+)", r"(?P<\1>[^/]+)", path_template) + "$"
        regex = re.compile(pattern_str)
        self.routes.append((method.upper(), regex, handler))

    def dispatch(
        self,
        method: str,
        url_or_path: str,
        payload: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Dispatch HTTP request to matching handler.

        Args:
            method: HTTP method (GET, POST, etc.)
            url_or_path: Request URL or path string.
            payload: Request JSON body payload dictionary.

        Returns:
            Formatted response dict with `status` and `body`.
        """
        parsed_url = urlparse(url_or_path)
        path = parsed_url.path or "/"

        # Parse query parameters from query string
        query_dict: dict[str, str] = {}
        if parsed_url.query:
            qs = parse_qs(parsed_url.query)
            for k, v in qs.items():
                if v:
                    query_dict[k] = v[-1]

        method_upper = method.upper()

        for route_method, regex, handler in self.routes:
            if route_method == method_upper:
                match = regex.match(path)
                if match:
                    path_params = match.groupdict()
                    try:
                        return handler(path_params=path_params, query_params=query_dict, payload=payload)
                    except Exception as exc:
                        log_error(f"Internal Route Error on {method} {path}: {exc}")
                        return error_response(message="internal_server_error", status_code=500, details=str(exc))

        return error_response(message="not_found", status_code=404)
