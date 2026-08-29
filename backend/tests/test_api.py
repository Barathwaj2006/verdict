import pytest
from fastapi.testclient import TestClient
from unittest.mock import MagicMock
from main import app
from app.api.dependencies import get_firestore_repository, get_investigation_controller
from app.services.firestore_repository import FirestoreRepository
from app.orchestration.investigation_controller import InvestigationController

client = TestClient(app)

@pytest.fixture
def mock_repo():
    repo = MagicMock(spec=FirestoreRepository)
    app.dependency_overrides[get_firestore_repository] = lambda: repo
    yield repo
    app.dependency_overrides.pop(get_firestore_repository, None)

@pytest.fixture
def mock_controller(mock_repo):
    # Pass api_key to avoid ValueError
    controller = MagicMock(spec=InvestigationController)
    controller.repository = mock_repo
    app.dependency_overrides[get_investigation_controller] = lambda: controller
    yield controller
    app.dependency_overrides.pop(get_investigation_controller, None)

def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok", "service": "verdict-api"}

def test_start_investigation(mock_controller, mock_repo):
    response = client.post("/api/investigations", json={"objective": "Find out who made C++", "constraints": []})
    assert response.status_code == 200
    data = response.json()
    assert "investigation_id" in data
    assert data["status"] == "STARTED"

def test_get_investigation_status(mock_repo):
    mock_repo.get_investigation_metadata.return_value = {"status": "IN_PROGRESS"}
    response = client.get("/api/investigations/inv_123")
    assert response.status_code == 200
    assert response.json() == {"status": "IN_PROGRESS"}

def test_get_investigation_status_not_found(mock_repo):
    mock_repo.get_investigation_metadata.return_value = None
    response = client.get("/api/investigations/inv_123")
    assert response.status_code == 404

def test_resume_investigation(mock_controller, mock_repo):
    mock_repo.get_investigation_metadata.return_value = {"status": "IN_PROGRESS"}
    mock_controller.repository = mock_repo
    response = client.post("/api/investigations/inv_123/resume")
    assert response.status_code == 200
    assert response.json()["status"] == "RESUMED"

def test_resume_finished_investigation(mock_controller, mock_repo):
    mock_repo.get_investigation_metadata.return_value = {"status": "COMPLETED"}
    mock_controller.repository = mock_repo
    response = client.post("/api/investigations/inv_123/resume")
    assert response.status_code == 400

def test_get_verdict(mock_repo):
    mock_repo.get_investigation_metadata.return_value = {"status": "COMPLETED", "final_verdict": {"conclusion": "Bjarne Stroustrup"}}
    response = client.get("/api/investigations/inv_123/verdict")
    assert response.status_code == 200
    assert response.json() == {"conclusion": "Bjarne Stroustrup"}
