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


def test_research_profile_flow():
    db = get_test_database_adapter()
    app = create_app(database=db)

    # First create a parent company
    comp_res = app.handle_request(FakeRequest("POST", "/api/companies", {"name": "Acme Industrial"}))
    company_id = comp_res["body"]["id"]

    # 1. Create Research Profile with digital & product assessment
    profile_payload = {
        "company_id": company_id,
        "company_overview": "Leading industrial tooling manufacturer.",
        "digital_assessment": {
            "website_quality_score": 8,
            "mobile_friendly": "Yes",
            "cms": "WordPress",
        },
        "product_assessment": {
            "estimated_catalog_size": "5000+",
            "product_information_quality_score": 7,
        },
    }
    res = app.handle_request(FakeRequest("POST", "/api/research-profiles", profile_payload))
    assert res["status"] == 201
    profile = res["body"]
    profile_id = profile["id"]
    assert profile["company_id"] == company_id
    assert profile["digital_assessment"]["website_quality_score"] == 8
    assert profile["product_assessment"]["estimated_catalog_size"] == "5000+"

    # 2. Add Research Source citation
    source_payload = {"source_name": "Official Website", "source_url": "https://acme.test"}
    source_res = app.handle_request(
        FakeRequest("POST", f"/api/research-profiles/{profile_id}/sources", source_payload)
    )
    assert source_res["status"] == 201
    assert source_res["body"]["source_name"] == "Official Website"

    # 3. Get profile by ID
    get_res = app.handle_request(FakeRequest("GET", f"/api/research-profiles/{profile_id}"))
    assert get_res["status"] == 200
    assert len(get_res["body"]["sources"]) == 1

    # 4. List profiles
    list_res = app.handle_request(FakeRequest("GET", f"/api/research-profiles?company_id={company_id}"))
    assert list_res["status"] == 200
    assert len(list_res["body"]) == 1

    # 5. Delete profile
    del_res = app.handle_request(FakeRequest("DELETE", f"/api/research-profiles/{profile_id}"))
    assert del_res["status"] == 204
