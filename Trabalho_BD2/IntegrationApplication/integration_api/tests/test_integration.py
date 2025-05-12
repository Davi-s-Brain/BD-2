from fastapi.testclient import TestClient
from integration_api.integration_application import app

client = TestClient(app)

def test_post_item():
    response = client.post("/integration/", json={"name": "PostItem", "description": "desc"})
    assert response.status_code == 200

def test_get_items():
    response = client.get("/integration/", headers={"Authorization": "Bearer secreta"})
    assert response.status_code == 200

def test_put_item():
    post_resp = client.post("/integration/", json={"name": "ToUpdate", "description": "before"})
    assert post_resp.status_code == 200

    put_resp = client.put("/integration/1", json={"name": "Updated", "description": "after"})
    assert put_resp.status_code == 200

def test_unauthorized_request():
    resp = client.get("/integration/")
    assert resp.status_code == 401

def test_invalid_token():
    resp = client.get("/integration/", headers={"Authorization": "Bearer wrong"})
    assert resp.status_code == 403

def test_valid_token():
    resp = client.get("/integration/", headers={"Authorization": "Bearer secreta"})
    assert resp.status_code == 200
