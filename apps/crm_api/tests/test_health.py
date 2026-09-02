from src.app import create_app
from src.database.sqlite_adapter import get_test_database_adapter


def test_health_route_returns_ok():
    db = get_test_database_adapter()
    app = create_app(database=db)
    request = type("Request", (), {"method": "GET", "url": "https://example.test/health"})()

    response = app.handle_request(request)

    assert response["status"] == 200
    assert response["body"]["service"] == "crm-api"
    assert response["body"]["status"] == "ok"
