from src.app import create_app
from src.database.sqlite_adapter import get_test_database_adapter


class FakeRequest:
    def __init__(self, method, url, body=None):
        self.method = method
        self.url = url
        self._body = body or {}

    def json(self):
        return self._body


def test_company_crud_flow():
    db = get_test_database_adapter()
    app = create_app(database=db)

    # 1. Create company
    create_response = app.handle_request(
        FakeRequest("POST", "/api/companies", {"name": "Contoso Labs", "industry": "Technology"})
    )
    assert create_response["status"] == 201
    created = create_response["body"]
    assert created["name"] == "Contoso Labs"
    assert created["industry"] == "Technology"
    assert created["id"] == 1

    # 2. List companies
    list_response = app.handle_request(FakeRequest("GET", "/api/companies"))
    assert list_response["status"] == 200
    assert len(list_response["body"]) == 1

    # 3. Search company by query filter
    search_response = app.handle_request(FakeRequest("GET", "/api/companies?q=Contoso"))
    assert search_response["status"] == 200
    assert len(search_response["body"]) == 1

    # 4. Get company by ID
    get_response = app.handle_request(FakeRequest("GET", f"/api/companies/{created['id']}"))
    assert get_response["status"] == 200
    assert get_response["body"]["name"] == "Contoso Labs"

    # 5. Update company
    update_response = app.handle_request(
        FakeRequest("PUT", f"/api/companies/{created['id']}", {"name": "Contoso Corp"})
    )
    assert update_response["status"] == 200
    assert update_response["body"]["name"] == "Contoso Corp"

    # 6. Delete company
    delete_response = app.handle_request(FakeRequest("DELETE", f"/api/companies/{created['id']}"))
    assert delete_response["status"] == 204

    # Verify deleted
    get_after_del = app.handle_request(FakeRequest("GET", f"/api/companies/{created['id']}"))
    assert get_after_del["status"] == 404
