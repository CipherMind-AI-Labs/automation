from __future__ import annotations

import sqlite3
from typing import Any

import httpx

from src.utils.logger import log_error, log_info

_D1_QUERY_URL = (
    "https://api.cloudflare.com/client/v4"
    "/accounts/{account_id}/d1/database/{database_id}/query"
)


class D1HttpConnection:
    """Cloudflare D1 REST API connection — no Workers runtime required.

    Exposes a single ``execute()`` method so that ``DatabaseAdapter``'s
    duck-typing fallback picks it up automatically without any changes to
    the adapter or repository layers.
    """

    def __init__(
        self,
        account_id: str,
        database_id: str,
        api_token: str,
    ) -> None:
        """Initialise connection parameters.

        Args:
            account_id:  Cloudflare account ID (CF_ACCOUNT_ID).
            database_id: D1 database ID (CF_D1_DATABASE_ID).
            api_token:   Cloudflare API token with D1:Edit permission (CF_API_TOKEN).
        """
        account_id = account_id.strip().strip("'").strip('"')
        database_id = database_id.strip().strip("'").strip('"')
        api_token = api_token.strip().strip("'").strip('"')

        self._url = _D1_QUERY_URL.format(
            account_id=account_id,
            database_id=database_id,
        )
        self._headers = {
            "Authorization": f"Bearer {api_token}",
            "Content-Type": "application/json",
        }

    def execute(self, query: str, params: list[Any]) -> list[dict[str, Any]]:
        """Send a parameterised SQL query to D1 and return rows as dicts.

        Mirrors the interface used by ``DatabaseAdapter``'s duck-typing
        fallback so no repository code needs modification.

        Args:
            query:  Parameterised SQL using ``?`` placeholders.
            params: Positional bind values.

        Returns:
            List of row dictionaries for SELECT queries.
            ``[{"id": <last_row_id>}]`` for INSERT queries that produce a row ID.
            Empty list for UPDATE / DELETE or INSERT without a row ID.

        Raises:
            httpx.HTTPStatusError: On HTTP 4xx / 5xx responses.
            RuntimeError: If the D1 API reports a logical query failure.
        """
        response = httpx.post(
            self._url,
            json={"sql": query, "params": params},
            headers=self._headers,
            timeout=30.0,
        )
        response.raise_for_status()
        data: dict[str, Any] = response.json()

        if not data.get("success"):
            errors = data.get("errors", [])
            raise RuntimeError(f"D1 query failed: {errors}")

        query_result: dict[str, Any] = data["result"][0]
        results: list[dict[str, Any]] = query_result.get("results") or []

        if not results:
            # INSERT statements surface the new row ID via meta.last_row_id
            last_row_id: int | None = query_result.get("meta", {}).get("last_row_id")
            if last_row_id:
                return [{"id": last_row_id}]

        return results


class DatabaseAdapter:
    """Thin abstraction over Cloudflare D1 bindings and SQLite connections for repository usage.

    Repositories execute raw SQL via this adapter exclusively.
    """

    def __init__(self, connection: Any | None = None) -> None:
        """Initialize database adapter.

        Args:
            connection: D1 binding object (`env.DB`), `sqlite3.Connection`, or None.
        """
        self.connection = connection

    def execute(self, query: str, params: list[Any] | None = None) -> list[dict[str, Any]]:
        """Execute a SQL query with parameters and return result rows as dictionaries.

        Args:
            query: Parameterized SQL string using `?` positional placeholders.
            params: Values to bind to SQL query parameters.

        Returns:
            List of row dictionaries.
        """
        params = params or []

        if self.connection is None:
            log_error("Database connection is not initialized.")
            return []

        # Handle Cloudflare D1 Binding (`env.DB`)
        if hasattr(self.connection, "prepare"):
            try:
                stmt = self.connection.prepare(query)
                if params:
                    stmt = stmt.bind(*params)

                res = stmt.all()
                results = getattr(res, "results", res)
                if hasattr(results, "to_py"):
                    results = results.to_py()

                if isinstance(results, list):
                    return [dict(row) for row in results]
                return []
            except Exception as exc:
                log_error(f"D1 Query Execution Failure: {exc}", {"query": query, "params": params})
                raise exc

        # Handle standard SQLite connection
        if isinstance(self.connection, sqlite3.Connection):
            try:
                cursor = self.connection.cursor()
                cursor.execute(query, params)
                if query.strip().upper().startswith(("INSERT", "UPDATE", "DELETE")):
                    self.connection.commit()
                    if query.strip().upper().startswith("INSERT"):
                        last_id = cursor.lastrowid
                        if last_id is not None:
                            return [{"id": last_id}]
                    return []
                rows = cursor.fetchall()
                return [dict(row) for row in rows]
            except Exception as exc:
                log_error(f"SQLite Query Execution Failure: {exc}", {"query": query, "params": params})
                raise exc

        # Fallback for mock/duck-typed connection objects
        if hasattr(self.connection, "execute"):
            res = self.connection.execute(query, params)
            if isinstance(res, list):
                return res

        return []
