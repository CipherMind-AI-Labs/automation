from __future__ import annotations

from typing import Any


def json_response(
    status_code: int,
    data: Any = None,
    error: str | None = None,
    details: Any = None,
) -> dict[str, Any]:
    """Format a standard JSON response dictionary for the API worker.

    Args:
        status_code: HTTP status code.
        data: Payload data for successful responses.
        error: High-level error string or code.
        details: Additional error context or validation details.

    Returns:
        Structured response dictionary containing status and body.
    """
    body: dict[str, Any] = {}
    if error is not None:
        body["error"] = error
        if details is not None:
            body["details"] = details
    elif data is not None:
        body = data

    return {
        "status": status_code,
        "body": body,
        "headers": {"Content-Type": "application/json"},
    }


def success_response(data: Any, status_code: int = 200) -> dict[str, Any]:
    """Helper for successful responses.

    Args:
        data: Serialized data object or list.
        status_code: HTTP status code, defaults to 200 OK.

    Returns:
        Standard JSON response dict.
    """
    return json_response(status_code=status_code, data=data)


def error_response(
    message: str,
    status_code: int = 400,
    details: Any = None,
) -> dict[str, Any]:
    """Helper for error responses.

    Args:
        message: Error description or code.
        status_code: HTTP status code (e.g., 400, 404, 500).
        details: Detailed validation error context.

    Returns:
        Standard JSON error response dict.
    """
    return json_response(status_code=status_code, error=message, details=details)
