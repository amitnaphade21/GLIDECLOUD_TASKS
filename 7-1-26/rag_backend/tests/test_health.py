"""
Health Check Tests
Tests for application startup and basic endpoints
"""
import pytest
from fastapi.testclient import TestClient
from main import app


@pytest.fixture
def client():
    """Create a test client for the FastAPI app"""
    return TestClient(app)


class TestHealthEndpoints:
    """Test suite for health and root endpoints"""
    
    def test_app_root_endpoint(self, client):
        """Test root endpoint returns success"""
        response = client.get("/")
        assert response.status_code == 200
        assert "status" in response.json()
        assert response.json()["status"] == "RAG API running"
    
    def test_app_starts_successfully(self, client):
        """Test that the app initializes without errors"""
        assert client is not None
        assert client.base_url == "http://testserver"
    
    def test_swagger_ui_available(self, client):
        """Test that Swagger UI documentation is accessible"""
        response = client.get("/docs")
        assert response.status_code == 200
        assert "swagger" in response.text.lower() or "openapi" in response.text.lower()
    
    def test_redoc_available(self, client):
        """Test that ReDoc documentation is accessible"""
        response = client.get("/redoc")
        assert response.status_code == 200
    
    def test_openapi_schema_available(self, client):
        """Test that OpenAPI schema is available"""
        response = client.get("/openapi.json")
        assert response.status_code == 200
        assert "openapi" in response.json()
        assert "paths" in response.json()
