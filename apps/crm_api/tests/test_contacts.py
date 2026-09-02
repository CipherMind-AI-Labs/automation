from src.app import create_app
from src.database.sqlite_adapter import get_test_database_adapter


class FakeRequest:
    def __init__(self, method, url, body=None):
        self.method = method
        self.url = url
        self._body = body or {}

    def json(self):
        return self._body


def test_contacts_flow():
    db = get_test_database_adapter()
    app = create_app(database=db)

    comp_res = app.handle_request(FakeRequest("POST", "/api/companies", {"name": "Apex Group"}))
    company_id = comp_res["body"]["id"]

    # 1. Create Contact
    contact_payload = {
        "company_id": company_id,
        "first_name": "Jane",
        "last_name": "Doe",
        "job_title": "VP of Operations",
        "email": "jane.doe@apex.test",
        "is_decision_maker": 1,
    }
    res = app.handle_request(FakeRequest("POST", "/api/contacts", contact_payload))
    assert res["status"] == 201
    contact_id = res["body"]["id"]
    assert res["body"]["full_name"] == "Jane Doe"
    assert res["body"]["is_decision_maker"] == 1

    # 2. Filter contacts by search query & decision maker status
    search_res = app.handle_request(
        FakeRequest("GET", f"/api/contacts?q=Jane&is_decision_maker=1&company_id={company_id}")
    )
    assert search_res["status"] == 200
    assert len(search_res["body"]) == 1

    # 3. Update Contact
    update_res = app.handle_request(
        FakeRequest("PUT", f"/api/contacts/{contact_id}", {"job_title": "Chief Operating Officer"})
    )
    assert update_res["status"] == 200
    assert update_res["body"]["job_title"] == "Chief Operating Officer"

    # 4. Delete Contact
    del_res = app.handle_request(FakeRequest("DELETE", f"/api/contacts/{contact_id}"))
    assert del_res["status"] == 204
