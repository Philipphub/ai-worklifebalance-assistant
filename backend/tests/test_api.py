from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_read_root():
    """Test the health check endpoint."""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_analyze_schedule_placeholder():
    """Test the placeholder analyze-schedule endpoint."""
    response = client.post(
        "/api/v1/analyze-schedule", json={"tasks": ["test task 1", "test task 2"]}
    )
    assert response.status_code == 200

    # Check if the response contains the expected keys for the placeholder
    data = response.json()
    assert "categorized_tasks" in data
    assert "analysis_report" in data
    assert "suggestions" in data
