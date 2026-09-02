from src.app import create_app
from src.database.sqlite_adapter import get_test_database_adapter


class FakeRequest:
    def __init__(self, method, url, body=None, authorization="Bearer dev_access_token_123"):
        self.method = method
        self.url = url
        self._body = body or {}
        self.authorization = authorization

    def json(self):
        return self._body


def test_opportunities_flow():
    db = get_test_database_adapter()
    app = create_app(database=db)

    comp_res = app.handle_request(FakeRequest("POST", "/api/companies", {"name": "Nexus Dynamics"}))
    company_id = comp_res["body"]["id"]

    # 1. Create Opportunity
    opp_payload = {
        "company_id": company_id,
        "primary_opportunity": "E-Commerce Catalog Modernization",
        "opportunity_score": 9,
        "lead_status": "Qualified",
        "priority": "High",
    }
    res = app.handle_request(FakeRequest("POST", "/api/opportunities", opp_payload))
    assert res["status"] == 201
    opp_id = res["body"]["id"]
    assert res["body"]["lead_status"] == "Qualified"

    # 2. Filter opportunities
    list_res = app.handle_request(
        FakeRequest("GET", f"/api/opportunities?company_id={company_id}&priority=High")
    )
    assert list_res["status"] == 200
    assert len(list_res["body"]) == 1

    # 3. Update Opportunity status
    update_res = app.handle_request(
        FakeRequest("PUT", f"/api/opportunities/{opp_id}", {"lead_status": "Proposal Sent"})
    )
    assert update_res["status"] == 200
    assert update_res["body"]["lead_status"] == "Proposal Sent"

    # 4. Delete Opportunity
    del_res = app.handle_request(FakeRequest("DELETE", f"/api/opportunities/{opp_id}"))
    assert del_res["status"] == 204
