import os
import pytest
from fastapi.testclient import TestClient

# Ensure .env is not required for tests
os.environ.setdefault("JWT_SECRET", "test-secret")
os.environ.setdefault("FERNET_KEY", "vJHk7r8xCw4rj5rKf1l5m4pQw1kRkYg9c0oXc3Hc1a0=")  # valid format

from app.main import app  # noqa: E402

client = TestClient(app)


def test_register_login_and_notes_flow():
    r = client.post("/auth/register", json={"username": "alice", "password": "LongEnoughPassword1!"})
    assert r.status_code == 200
    token = r.json()["access_token"]

    r = client.post(
        "/notes",
        headers={"Authorization": f"Bearer {token}"},
        json={"title": "t1", "body": "secret body"},
    )
    assert r.status_code == 200
    note_id = r.json()["id"]

    r = client.get("/notes", headers={"Authorization": f"Bearer {token}"})
    assert r.status_code == 200
    assert any(n["id"] == note_id and n["body"] == "secret body" for n in r.json())

    r = client.delete(f"/notes/{note_id}", headers={"Authorization": f"Bearer {token}"})
    assert r.status_code == 204