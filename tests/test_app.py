import pytest
from fastapi.testclient import TestClient

from src.app import app, activities


@pytest.fixture(autouse=True)
def reset_activities():
    # Ensure participant lists are empty before each test
    for a in activities.values():
        a["participants"] = []
    yield


@pytest.fixture
def client():
    with TestClient(app) as c:
        yield c


def test_get_activities(client):
    resp = client.get("/activities")
    assert resp.status_code == 200
    data = resp.json()
    assert "soccer" in data
    assert isinstance(data["soccer"]["participants"], list)
    assert data["soccer"]["participants"] == []


def test_signup_and_duplicate(client):
    resp = client.post("/activities/soccer/signup?email=student@example.com")
    assert resp.status_code == 200
    assert resp.json()["message"] == "Signed up student@example.com for soccer"

    # Duplicate signup returns 400
    resp2 = client.post("/activities/soccer/signup?email=student@example.com")
    assert resp2.status_code == 400
    assert resp2.json()["detail"] == "Student is already signed up"


def test_delete_participant(client):
    # Sign up first
    resp = client.post("/activities/soccer/signup?email=student2@example.com")
    assert resp.status_code == 200

    # Then remove
    resp = client.delete("/activities/soccer/participants?email=student2@example.com")
    assert resp.status_code == 200
    assert resp.json()["message"] == "Removed student2@example.com from soccer"

    # Removing again should return 404
    resp2 = client.delete("/activities/soccer/participants?email=student2@example.com")
    assert resp2.status_code == 404
    assert resp2.json()["detail"] == "Participant not found"


def test_activity_not_found(client):
    resp = client.post("/activities/nonexistent/signup?email=a@b.com")
    assert resp.status_code == 404
    assert resp.json()["detail"] == "Activity not found"
