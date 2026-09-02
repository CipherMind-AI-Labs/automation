from src.app import create_app
from src.database.sqlite_adapter import get_test_database_adapter


class FakeRequest:
    def __init__(self, method, url, body=None, authorization=None):
        self.method = method
        self.url = url
        self._body = body or {}
        self.authorization = authorization

    def json(self):
        return self._body


def test_auth_flows():
    db = get_test_database_adapter()
    app = create_app(database=db)

    # 1. /health works unauthenticated
    health_res = app.handle_request(FakeRequest("GET", "/health"))
    assert health_res["status"] == 200
    assert health_res["body"]["status"] == "ok"

    # 2. Missing authorization header -> 401
    unauth_res = app.handle_request(FakeRequest("GET", "/api/companies"))
    assert unauth_res["status"] == 401
    assert unauth_res["body"]["error"] == "unauthorized"

    # 3. Invalid token format -> 401
    bad_format_res = app.handle_request(FakeRequest("GET", "/api/companies", authorization="Basic 12345"))
    assert bad_format_res["status"] == 401

    # 4. Wrong access token -> 401
    wrong_token_res = app.handle_request(FakeRequest("GET", "/api/companies", authorization="Bearer wrong_token_xyz"))
    assert wrong_token_res["status"] == 401

    # 5. Valid access token -> 200
    valid_res = app.handle_request(FakeRequest("GET", "/api/companies", authorization="Bearer dev_access_token_123"))
    assert valid_res["status"] == 200

    # 6. Verify token endpoint with valid token -> 200
    verify_valid = app.handle_request(FakeRequest("GET", "/api/auth/verify", authorization="Bearer dev_access_token_123"))
    assert verify_valid["status"] == 200
    assert verify_valid["body"]["authenticated"] is True

    # 7. Verify token endpoint with invalid token -> 401
    verify_invalid = app.handle_request(FakeRequest("GET", "/api/auth/verify", authorization="Bearer invalid_token"))
    assert verify_invalid["status"] == 401
