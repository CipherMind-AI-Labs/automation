from __future__ import annotations

import json
import os
from contextlib import asynccontextmanager
from pathlib import Path
from typing import Any

from dotenv import load_dotenv

# Load .env from apps/crm_api/ regardless of the working directory.
load_dotenv(Path(__file__).resolve().parent.parent / ".env", override=True)

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from src.database.base import D1HttpConnection, DatabaseAdapter
from src.repositories.communication_repository import CommunicationRepository
from src.repositories.company_repository import CompanyRepository
from src.repositories.contact_repository import ContactRepository
from src.repositories.digital_assessment_repository import DigitalAssessmentRepository
from src.repositories.follow_up_reminder_repository import FollowUpReminderRepository
from src.repositories.opportunity_repository import OpportunityRepository
from src.repositories.product_assessment_repository import ProductAssessmentRepository
from src.repositories.research_profile_repository import ResearchProfileRepository
from src.repositories.research_source_repository import ResearchSourceRepository
from src.routes.communication_routes import CommunicationRoutes
from src.routes.company_routes import CompanyRoutes
from src.routes.contact_routes import ContactRoutes
from src.routes.follow_up_reminder_routes import FollowUpReminderRoutes
from src.routes.opportunity_routes import OpportunityRoutes
from src.routes.research_profile_routes import ResearchProfileRoutes
from src.routes.router import Router
from src.services.communication_service import CommunicationService
from src.services.company_service import CompanyService
from src.services.contact_service import ContactService
from src.services.follow_up_reminder_service import FollowUpReminderService
from src.services.opportunity_service import OpportunityService
from src.services.research_profile_service import ResearchProfileService
from src.utils.logger import log_info
from src.utils.response import success_response


class CRMApp:
    """Main application container for the CRM API Worker."""

    def __init__(self, database: DatabaseAdapter | None = None) -> None:
        """Initialize CRM application, dependencies, repositories, services, and routes.

        Args:
            database: Optional DatabaseAdapter instance.
        """
        self.database = database or DatabaseAdapter(connection=None)

        # Repositories
        self.company_repo = CompanyRepository(self.database)
        self.research_profile_repo = ResearchProfileRepository(self.database)
        self.digital_repo = DigitalAssessmentRepository(self.database)
        self.product_repo = ProductAssessmentRepository(self.database)
        self.source_repo = ResearchSourceRepository(self.database)
        self.opportunity_repo = OpportunityRepository(self.database)
        self.contact_repo = ContactRepository(self.database)
        self.communication_repo = CommunicationRepository(self.database)
        self.reminder_repo = FollowUpReminderRepository(self.database)

        # Services
        self.company_service = CompanyService(self.company_repo)
        self.research_profile_service = ResearchProfileService(
            self.research_profile_repo,
            self.digital_repo,
            self.product_repo,
            self.source_repo,
        )
        self.opportunity_service = OpportunityService(self.opportunity_repo)
        self.contact_service = ContactService(self.contact_repo)
        self.communication_service = CommunicationService(self.communication_repo)
        self.reminder_service = FollowUpReminderService(self.reminder_repo)

        # Router & Routes
        self.router = Router()
        CompanyRoutes(self.company_service).register(self.router)
        ResearchProfileRoutes(self.research_profile_service).register(self.router)
        OpportunityRoutes(self.opportunity_service).register(self.router)
        ContactRoutes(self.contact_service).register(self.router)
        CommunicationRoutes(self.communication_service).register(self.router)
        FollowUpReminderRoutes(self.reminder_service).register(self.router)

    def health(self) -> dict[str, Any]:
        """Health check endpoint response dictionary."""
        return success_response({"status": "ok", "service": "crm-api"})

    def handle_request(self, request: Any) -> dict[str, Any]:
        """Process incoming HTTP request object.

        Args:
            request: Worker Request or MockRequest object.

        Returns:
            Dictionary containing `status`, `body`, and `headers`.
        """
        url = getattr(request, "url", "") or ""
        path = getattr(request, "path", url)
        method = getattr(request, "method", "GET")

        if method == "GET" and (url.endswith("/health") or path == "/health"):
            return self.health()

        payload: dict[str, Any] | None = None
        if hasattr(request, "json"):
            try:
                body = request.json()
                if callable(body):
                    body = body()
                if isinstance(body, dict):
                    payload = body
                elif isinstance(body, str) and body.strip():
                    payload = json.loads(body)
            except Exception:
                payload = None

        return self.router.dispatch(method=method, url_or_path=url or path, payload=payload)


def create_app(database: DatabaseAdapter | None = None) -> CRMApp:
    """Factory method for creating a CRMApp instance.

    Args:
        database: Optional DatabaseAdapter.

    Returns:
        CRMApp application instance.
    """
    return CRMApp(database=database)


# ---------------------------------------------------------------------------
# HTTP adapter — bridges FastAPI Request → CRMApp.handle_request()
# ---------------------------------------------------------------------------

class _RequestAdapter:
    """Thin adapter that makes a FastAPI request look like a Worker Request.

    ``CRMApp.handle_request()`` reads ``.url``, ``.method``, and calls
    ``.json()`` — this class satisfies that interface.
    """

    def __init__(self, url: str, method: str, body: dict[str, Any] | None) -> None:
        self.url = url
        self.method = method
        self._body = body

    def json(self) -> dict[str, Any] | None:  # noqa: D102
        """Return the pre-parsed request body (or None for bodyless requests)."""
        return self._body


# ---------------------------------------------------------------------------
# D1 database adapter factory
# ---------------------------------------------------------------------------

_REQUIRED_ENV: tuple[str, ...] = ("CF_ACCOUNT_ID", "CF_D1_DATABASE_ID", "CF_API_TOKEN")


def _build_db_adapter() -> DatabaseAdapter:
    """Construct a DatabaseAdapter backed by the Cloudflare D1 REST API.

    Reads credentials from environment variables (populated via .env).

    Returns:
        Configured DatabaseAdapter using D1HttpConnection.

    Raises:
        KeyError: If any required environment variable is missing.
    """
    conn = D1HttpConnection(
        account_id=os.environ["CF_ACCOUNT_ID"],
        database_id=os.environ["CF_D1_DATABASE_ID"],
        api_token=os.environ["CF_API_TOKEN"],
    )
    return DatabaseAdapter(connection=conn)


# ---------------------------------------------------------------------------
# FastAPI application
# ---------------------------------------------------------------------------

@asynccontextmanager
async def _lifespan(application: FastAPI):  # type: ignore[type-arg]
    """Validate required credentials before accepting any traffic."""
    missing = [v for v in _REQUIRED_ENV if not os.environ.get(v)]
    if missing:
        raise RuntimeError(
            f"Missing environment variables: {', '.join(missing)}. "
            "Copy apps/crm_api/.env.example → apps/crm_api/.env and fill in the values."
        )
    log_info("CRM API started", {"transport": "Cloudflare D1 REST API"})
    yield


app = FastAPI(title="CRM API", version="1.0.0", lifespan=_lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health", tags=["meta"])
async def health() -> dict[str, str]:
    """Liveness probe — does not require D1 credentials."""
    return {"status": "ok", "service": "crm-api"}


@app.api_route(
    "/api/{path:path}",
    methods=["GET", "POST", "PUT", "DELETE", "PATCH"],
    tags=["crm"],
)
async def handle_all(request: Request, path: str) -> JSONResponse:  # noqa: ARG001
    """Catch-all route that proxies every /api/* request through CRMApp.

    Args:
        request: Incoming FastAPI request.
        path: Remainder of the URL path after /api/.

    Returns:
        JSONResponse with status code and body from the CRM router.
    """
    body: dict[str, Any] | None = None
    if request.method in ("POST", "PUT", "PATCH"):
        try:
            body = await request.json()
        except Exception:
            body = None

    mock_req = _RequestAdapter(
        url=str(request.url),
        method=request.method,
        body=body,
    )
    crm = create_app(database=_build_db_adapter())
    res = crm.handle_request(mock_req)

    return JSONResponse(
        content=res.get("body", {}),
        status_code=res.get("status", 200),
    )
