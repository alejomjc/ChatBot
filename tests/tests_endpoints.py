import pytest
from fastapi.testclient import TestClient
from sqlmodel import create_engine, Session
from app.main import app
from app import models, database

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})

models.SQLModel.metadata.create_all(bind=engine)


def override_get_session():
    db = Session(bind=engine)
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[database.get_session] = override_get_session


@pytest.fixture(scope="module")
def client():
    with TestClient(app) as client:
        yield client
    models.SQLModel.metadata.drop_all(bind=engine)


@pytest.fixture
def create_user(client):
    """Fixture to create users for testing."""

    def _create_user(username, role):
        response = client.post("/init_user", json={"username": username, "role": role})
        assert response.status_code == 200
        return response.json()["user"]

    return _create_user


def test_init_user(client):
    user_data = {"username": "test_init_user", "role": "admin"}
    response = client.post("/init_user", json=user_data)
    assert response.status_code == 200
    response_data = response.json()
    assert response_data["message"] == "User created"
    assert "id" in response_data["user"]
    assert response_data["user"]["username"] == "test_init_user"
    assert response_data["user"]["role"] == "admin"


def test_ask(client, create_user):
    user = create_user("test_ask_user", "expert in risk assessment")

    params = {"username": user["username"], "question": "What are common workplace risks?"}
    response = client.post("/ask", json=params)

    assert response.status_code == 200, f"Expected 200, got {response.status_code}"
    response_data = response.json()
    assert "response" in response_data, "Expected 'response' key in response"
    assert response_data["response"], "Expected a non-empty response"


def test_history(client, create_user):
    user = create_user("test_history_user", "expert in risk assessment")

    params = {"username": user["username"], "question": "What are common workplace risks?"}
    response = client.post("/ask", json=params)
    assert response.status_code == 200

    response = client.get(f"/history/{user['username']}")
    assert response.status_code == 200, f"Expected 200, got {response.status_code}"
    history = response.json().get("history", [])

    assert len(history) > 0, "History should not be empty"
    assert history[0]["question"] == "What are common workplace risks?", "First question in history doesn't match"
    assert "response" in history[0], "Expected response in history"


def test_health(client):
    response = client.get("/health")
    assert response.status_code == 200, f"Expected 200, got {response.status_code}"

    health_data = response.json()
    assert health_data["service"] == "ok", "Expected service status 'ok'"
    assert health_data["database"] == "ok", "Expected database status 'ok'"
    assert health_data["gpt"] == "ok", "Expected GPT status 'ok'"
