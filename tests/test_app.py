"""Tests for the FastAPI backend using the Arrange-Act-Assert pattern."""


def test_root_redirect(client):
    # Arrange: no additional setup needed
    # Act
    resp = client.get("/", follow_redirects=False)
    # Assert
    assert resp.status_code in (301, 302, 303, 307)


def test_get_activities(client):
    # Arrange: no additional setup needed
    # Act
    resp = client.get("/activities")
    # Assert
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data


def test_signup_and_unregister(client):
    # Arrange
    activity = "Chess Club"
    email = "tester@example.com"

    # Act - signup
    resp = client.post(f"/activities/{activity}/signup", params={"email": email})
    # Assert signup succeeded
    assert resp.status_code == 200
    assert "Signed up" in resp.json().get("message", "")

    # Act - verify participant present
    resp = client.get("/activities")
    assert email in resp.json().get(activity, {}).get("participants", [])

    # Act - unregister
    resp = client.delete(f"/activities/{activity}/participants", params={"email": email})
    # Assert unregister succeeded and participant removed
    assert resp.status_code == 200
    assert "Unregistered" in resp.json().get("message", "")
    resp = client.get("/activities")
    assert email not in resp.json().get(activity, {}).get("participants", [])


def test_signup_already_signed_up(client):
    # Arrange
    activity = "Programming Class"
    email = "duplicate@example.com"

    # Act - first signup
    resp = client.post(f"/activities/{activity}/signup", params={"email": email})
    assert resp.status_code == 200

    # Act - second signup (should fail)
    resp = client.post(f"/activities/{activity}/signup", params={"email": email})
    # Assert
    assert resp.status_code == 400
