from fastapi.testclient import TestClient
from main import app
import json

client = TestClient(app)


def test_app_starts():
    """Test that the API server starts and root endpoint responds"""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"status": "RAG API running"}


def test_api_documentation_swagger():
    """Test that Swagger UI documentation is accessible"""
    response = client.get("/docs")
    assert response.status_code == 200
    assert "swagger" in response.text.lower()


def test_api_documentation_redoc():
    """Test that ReDoc documentation is accessible"""
    response = client.get("/redoc")
    assert response.status_code == 200
    assert "redoc" in response.text.lower()


def test_invalid_endpoint_returns_404():
    """Test that invalid endpoints return 404 error"""
    response = client.get("/invalid-endpoint")
    assert response.status_code == 404


def test_root_returns_json():
    """Test that root endpoint returns valid JSON with correct structure"""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "status" in data
    assert isinstance(data["status"], str)
