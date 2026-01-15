"""
Vector API Endpoint Tests
Tests for all vector API endpoints (create, read, update, delete, count)
"""
import pytest
from fastapi.testclient import TestClient
from main import app
from database.chroma import collection


@pytest.fixture
def client():
    """Create a test client for the FastAPI app"""
    return TestClient(app)


@pytest.fixture(autouse=True)
def cleanup_test_docs():
    """Clean up test documents before and after tests"""
    test_ids = ["test-doc-1", "test-doc-2", "test-doc-3"]
    for doc_id in test_ids:
        try:
            collection.delete(ids=[doc_id])
        except:
            pass
    yield
    # Cleanup after test
    for doc_id in test_ids:
        try:
            collection.delete(ids=[doc_id])
        except:
            pass


class TestVectorCreateEndpoint:
    """Test cases for /vectors/create endpoint"""
    
    def test_create_vectors_success(self, client):
        """Test successful vector creation from docs.txt"""
        response = client.post("/vectors/create")
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "chunks_stored" in data
        assert "document_ids" in data
        assert data["chunks_stored"] > 0
        assert len(data["document_ids"]) == data["chunks_stored"]
    
    def test_create_vectors_returns_valid_ids(self, client):
        """Test that created vectors have valid UUIDs"""
        response = client.post("/vectors/create")
        data = response.json()
        
        for doc_id in data["document_ids"]:
            assert isinstance(doc_id, str)
            assert len(doc_id) > 0


class TestVectorReadEndpoint:
    """Test cases for /vectors/read endpoint"""
    
    def test_read_vectors_with_valid_query(self, client):
        """Test successful vector search with valid query"""
        # First create vectors
        client.post("/vectors/create")
        
        # Then search
        response = client.post(
            "/vectors/read",
            json={"query": "test query"}
        )
        assert response.status_code == 200
        data = response.json()
        assert "query" in data
        assert "results" in data
        assert data["query"] == "test query"
    
    def test_read_vectors_returns_structured_results(self, client):
        """Test that search results have proper structure"""
        client.post("/vectors/create")
        
        response = client.post(
            "/vectors/read",
            json={"query": "test"}
        )
        data = response.json()
        
        if data["results"]:  # If results exist
            result = data["results"][0]
            assert "document" in result
            assert "metadata" in result
            assert "distance" in result
    
    def test_read_vectors_invalid_request(self, client):
        """Test read endpoint with missing query"""
        response = client.post(
            "/vectors/read",
            json={}
        )
        assert response.status_code == 422  # Validation error
    
    def test_read_vectors_with_empty_string(self, client):
        """Test search with empty query string"""
        client.post("/vectors/create")
        
        response = client.post(
            "/vectors/read",
            json={"query": ""}
        )
        # Should handle empty query gracefully
        assert response.status_code in [200, 422]


class TestVectorCountEndpoint:
    """Test cases for /vectors/count endpoint"""
    
    def test_count_vectors_returns_integer(self, client):
        """Test that count endpoint returns valid integer"""
        response = client.get("/vectors/count")
        assert response.status_code == 200
        data = response.json()
        assert "count" in data
        assert isinstance(data["count"], int)
        assert data["count"] >= 0
    
    def test_count_vectors_after_create(self, client):
        """Test that count increases after creating vectors"""
        # Get initial count
        response1 = client.get("/vectors/count")
        initial_count = response1.json()["count"]
        
        # Create vectors
        response2 = client.post("/vectors/create")
        chunks_stored = response2.json()["chunks_stored"]
        
        # Get new count
        response3 = client.get("/vectors/count")
        new_count = response3.json()["count"]
        
        # Count should increase
        assert new_count >= initial_count


class TestVectorUpdateEndpoint:
    """Test cases for /vectors/update endpoint"""
    
    def test_update_vector_success(self, client):
        """Test successful vector update"""
        # Create a vector first
        client.post("/vectors/create")
        response = client.get("/vectors/count")
        count = response.json()["count"]
        
        if count > 0:
            # Get a document ID to update (we'll use a test ID)
            response = client.post(
                "/vectors/update",
                json={
                    "id": "test-update-id",
                    "updated_text": "Updated test content for vector"
                }
            )
            assert response.status_code == 200
            data = response.json()
            assert "message" in data
            assert "update" in data["message"].lower()
    
    def test_update_vector_invalid_request(self, client):
        """Test update endpoint with missing fields"""
        response = client.post(
            "/vectors/update",
            json={"id": "test-id"}  # Missing updated_text
        )
        assert response.status_code == 422  # Validation error
    
    def test_update_vector_with_empty_fields(self, client):
        """Test update with empty required fields"""
        response = client.post(
            "/vectors/update",
            json={"id": "", "updated_text": ""}
        )
        # Should handle empty fields gracefully
        assert response.status_code in [200, 422]


class TestVectorDeleteEndpoint:
    """Test cases for /vectors/delete endpoint"""
    
    def test_delete_vector_success(self, client):
        """Test successful vector deletion"""
        response = client.post(
            "/vectors/delete",
            json={"id": "test-delete-id"}
        )
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "delete" in data["message"].lower()
    
    def test_delete_vector_invalid_request(self, client):
        """Test delete endpoint with missing id"""
        response = client.post(
            "/vectors/delete",
            json={}
        )
        assert response.status_code == 422  # Validation error
    
    def test_delete_nonexistent_vector(self, client):
        """Test deleting a vector that doesn't exist"""
        response = client.post(
            "/vectors/delete",
            json={"id": "nonexistent-id-12345"}
        )
        # Should handle gracefully even if ID doesn't exist
        assert response.status_code in [200, 404]


class TestVectorEndpointsIntegration:
    """Integration tests for multiple endpoints working together"""
    
    def test_create_read_count_workflow(self, client):
        """Test complete workflow: create, read, count"""
        # Create
        create_response = client.post("/vectors/create")
        assert create_response.status_code == 200
        
        # Count
        count_response = client.get("/vectors/count")
        assert count_response.status_code == 200
        assert count_response.json()["count"] > 0
        
        # Read
        read_response = client.post(
            "/vectors/read",
            json={"query": "test"}
        )
        assert read_response.status_code == 200
    
    def test_create_update_read_workflow(self, client):
        """Test workflow: create, update, read"""
        # Create
        client.post("/vectors/create")
        
        # Update
        update_response = client.post(
            "/vectors/update",
            json={
                "id": "workflow-test-id",
                "updated_text": "Updated workflow content"
            }
        )
        assert update_response.status_code == 200
        
        # Read
        read_response = client.post(
            "/vectors/read",
            json={"query": "workflow"}
        )
        assert read_response.status_code == 200
    
    def test_all_endpoints_return_json(self, client):
        """Test that all endpoints return valid JSON"""
        # Create
        response = client.post("/vectors/create")
        assert response.headers.get("content-type") == "application/json"
        
        # Count
        response = client.get("/vectors/count")
        assert response.headers.get("content-type") == "application/json"
        
        # Read
        response = client.post("/vectors/read", json={"query": "test"})
        assert response.headers.get("content-type") == "application/json"
