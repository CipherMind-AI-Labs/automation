from src.app import create_app
from src.database.sqlite_adapter import get_test_database_adapter


class FakeRequest:
    def __init__(self, method, url, body=None):
        self.method = method
        self.url = url
        self._body = body or {}

    def json(self):
        return self._body


def test_reminders_flow():
    db = get_test_database_adapter()
    app = create_app(database=db)

    comp_res = app.handle_request(FakeRequest("POST", "/api/companies", {"name": "Vanguard Tech"}))
    company_id = comp_res["body"]["id"]

    opp_res = app.handle_request(
        FakeRequest("POST", "/api/opportunities", {"company_id": company_id, "primary_opportunity": "Lead Followup"})
    )
    opp_id = opp_res["body"]["id"]

    # 1. Create Reminder
    reminder_payload = {
        "opportunity_id": opp_id,
        "due_at": "2026-08-15T09:00:00Z",
        "notes": "Follow up on proposal feedback",
    }
    res = app.handle_request(FakeRequest("POST", "/api/reminders", reminder_payload))
    assert res["status"] == 201
    reminder_id = res["body"]["id"]
    assert res["body"]["status"] == "pending"

    # 2. Filter Reminders
    list_res = app.handle_request(FakeRequest("GET", f"/api/reminders?opportunity_id={opp_id}&status=pending"))
    assert list_res["status"] == 200
    assert len(list_res["body"]) == 1

    # 3. Update Reminder status
    update_res = app.handle_request(
        FakeRequest("PUT", f"/api/reminders/{reminder_id}", {"status": "completed"})
    )
    assert update_res["status"] == 200
    assert update_res["body"]["status"] == "completed"

    # 4. Delete Reminder
    del_res = app.handle_request(FakeRequest("DELETE", f"/api/reminders/{reminder_id}"))
    assert del_res["status"] == 204
