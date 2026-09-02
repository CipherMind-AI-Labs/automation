from src.app import create_app
from src.database.sqlite_adapter import get_test_database_adapter


class FakeRequest:
    def __init__(self, method, url, body=None):
        self.method = method
        self.url = url
        self._body = body or {}

    def json(self):
        return self._body


def test_communications_flow():
    db = get_test_database_adapter()
    app = create_app(database=db)

    comp_res = app.handle_request(FakeRequest("POST", "/api/companies", {"name": "Starlight Corp"}))
    company_id = comp_res["body"]["id"]

    # 1. Create Thread
    thread_payload = {
        "company_id": company_id,
        "subject": "Introductory Partnership Inquiry",
        "channel": "email",
    }
    thread_res = app.handle_request(FakeRequest("POST", "/api/communication-threads", thread_payload))
    assert thread_res["status"] == 201
    thread_id = thread_res["body"]["id"]

    # 2. Create Communication Message in Thread
    msg_payload = {
        "thread_id": thread_id,
        "direction": "outbound",
        "subject": "Introductory Partnership Inquiry",
        "body_text": "Hello, we would love to connect.",
        "message_status": "sent",
    }
    msg_res = app.handle_request(FakeRequest("POST", "/api/communications", msg_payload))
    assert msg_res["status"] == 201
    msg_id = msg_res["body"]["id"]

    # 3. Add Webhook Event to Message
    event_payload = {
        "event_type": "delivered",
        "occurred_at": "2026-08-08T00:00:00Z",
    }
    event_res = app.handle_request(
        FakeRequest("POST", f"/api/communications/{msg_id}/events", event_payload)
    )
    assert event_res["status"] == 201

    # 4. Retrieve Thread with messages
    get_thread_res = app.handle_request(FakeRequest("GET", f"/api/communication-threads/{thread_id}"))
    assert get_thread_res["status"] == 200
    assert len(get_thread_res["body"]["messages"]) == 1

    # 5. Retrieve Communication with events
    get_comm_res = app.handle_request(FakeRequest("GET", f"/api/communications/{msg_id}"))
    assert get_comm_res["status"] == 200
    assert len(get_comm_res["body"]["events"]) == 1
