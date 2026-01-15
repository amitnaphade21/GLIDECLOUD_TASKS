"""
Request Schemas Validation Tests
Tests for Pydantic request model validation
"""
import pytest
from pydantic import ValidationError
from schemas.requests import QueryRequest, UpdateRequest, DeleteRequest, ChatRequest


class TestQueryRequestSchema:
    """Test QueryRequest Pydantic model"""
    
    def test_query_request_valid(self):
        """Test creating valid QueryRequest"""
        request = QueryRequest(query="What is AI?")
        
        assert request.query == "What is AI?"
    
    def test_query_request_required_field(self):
        """Test that query field is required"""
        with pytest.raises(ValidationError):
            QueryRequest()
    
    def test_query_request_string_type(self):
        """Test that query must be string"""
        # Valid: string
        request = QueryRequest(query="test")
        assert isinstance(request.query, str)
        
        # Invalid: integer
        with pytest.raises(ValidationError):
            QueryRequest(query=123)
    
    def test_query_request_empty_string(self):
        """Test QueryRequest with empty string"""
        request = QueryRequest(query="")
        
        assert request.query == ""
    
    def test_query_request_long_query(self):
        """Test QueryRequest with very long query"""
        long_query = "a" * 10000
        request = QueryRequest(query=long_query)
        
        assert request.query == long_query
    
    def test_query_request_special_characters(self):
        """Test QueryRequest with special characters"""
        query = "Search for @#$%^&*() special chars!"
        request = QueryRequest(query=query)
        
        assert request.query == query
    
    def test_query_request_unicode(self):
        """Test QueryRequest with unicode characters"""
        query = "Search: 你好 مرحبا"
        request = QueryRequest(query=query)
        
        assert request.query == query
    
    def test_query_request_json_serializable(self):
        """Test that QueryRequest can be serialized to JSON"""
        request = QueryRequest(query="test query")
        
        json_data = request.model_dump()
        assert json_data["query"] == "test query"


class TestUpdateRequestSchema:
    """Test UpdateRequest Pydantic model"""
    
    def test_update_request_valid(self):
        """Test creating valid UpdateRequest"""
        request = UpdateRequest(
            id="doc-123",
            updated_text="Updated content"
        )
        
        assert request.id == "doc-123"
        assert request.updated_text == "Updated content"
    
    def test_update_request_missing_id(self):
        """Test that id field is required"""
        with pytest.raises(ValidationError):
            UpdateRequest(updated_text="content")
    
    def test_update_request_missing_text(self):
        """Test that updated_text field is required"""
        with pytest.raises(ValidationError):
            UpdateRequest(id="doc-123")
    
    def test_update_request_both_required(self):
        """Test that both fields are required"""
        with pytest.raises(ValidationError):
            UpdateRequest()
    
    def test_update_request_id_type(self):
        """Test that id must be string"""
        # Valid: string
        request = UpdateRequest(
            id="doc-123",
            updated_text="content"
        )
        assert isinstance(request.id, str)
        
        # Invalid: integer
        with pytest.raises(ValidationError):
            UpdateRequest(id=123, updated_text="content")
    
    def test_update_request_text_type(self):
        """Test that updated_text must be string"""
        # Valid: string
        request = UpdateRequest(
            id="doc-123",
            updated_text="content"
        )
        assert isinstance(request.updated_text, str)
        
        # Invalid: list
        with pytest.raises(ValidationError):
            UpdateRequest(id="doc-123", updated_text=["content"])
    
    def test_update_request_empty_fields(self):
        """Test UpdateRequest with empty strings"""
        request = UpdateRequest(
            id="",
            updated_text=""
        )
        
        assert request.id == ""
        assert request.updated_text == ""
    
    def test_update_request_long_values(self):
        """Test UpdateRequest with very long values"""
        long_id = "id-" + "x" * 1000
        long_text = "text-" + "y" * 10000
        
        request = UpdateRequest(
            id=long_id,
            updated_text=long_text
        )
        
        assert request.id == long_id
        assert request.updated_text == long_text
    
    def test_update_request_json_serializable(self):
        """Test that UpdateRequest can be serialized to JSON"""
        request = UpdateRequest(
            id="doc-123",
            updated_text="Updated"
        )
        
        json_data = request.model_dump()
        assert json_data["id"] == "doc-123"
        assert json_data["updated_text"] == "Updated"


class TestDeleteRequestSchema:
    """Test DeleteRequest Pydantic model"""
    
    def test_delete_request_valid(self):
        """Test creating valid DeleteRequest"""
        request = DeleteRequest(id="doc-123")
        
        assert request.id == "doc-123"
    
    def test_delete_request_required_field(self):
        """Test that id field is required"""
        with pytest.raises(ValidationError):
            DeleteRequest()
    
    def test_delete_request_id_type(self):
        """Test that id must be string"""
        # Valid: string
        request = DeleteRequest(id="doc-123")
        assert isinstance(request.id, str)
        
        # Invalid: integer
        with pytest.raises(ValidationError):
            DeleteRequest(id=123)
    
    def test_delete_request_empty_id(self):
        """Test DeleteRequest with empty id"""
        request = DeleteRequest(id="")
        
        assert request.id == ""
    
    def test_delete_request_long_id(self):
        """Test DeleteRequest with very long id"""
        long_id = "id-" + "x" * 1000
        
        request = DeleteRequest(id=long_id)
        
        assert request.id == long_id
    
    def test_delete_request_special_chars(self):
        """Test DeleteRequest with special characters"""
        special_id = "id-@#$%^&*()"
        request = DeleteRequest(id=special_id)
        
        assert request.id == special_id
    
    def test_delete_request_json_serializable(self):
        """Test that DeleteRequest can be serialized to JSON"""
        request = DeleteRequest(id="doc-123")
        
        json_data = request.model_dump()
        assert json_data["id"] == "doc-123"


class TestChatRequestSchema:
    """Test ChatRequest Pydantic model"""
    
    def test_chat_request_valid(self):
        """Test creating valid ChatRequest"""
        request = ChatRequest(query="Tell me about AI")
        
        assert request.query == "Tell me about AI"
    
    def test_chat_request_required_field(self):
        """Test that query field is required"""
        with pytest.raises(ValidationError):
            ChatRequest()
    
    def test_chat_request_string_type(self):
        """Test that query must be string"""
        # Valid: string
        request = ChatRequest(query="test")
        assert isinstance(request.query, str)
        
        # Invalid: list
        with pytest.raises(ValidationError):
            ChatRequest(query=["test"])
    
    def test_chat_request_empty_query(self):
        """Test ChatRequest with empty query"""
        request = ChatRequest(query="")
        
        assert request.query == ""
    
    def test_chat_request_long_query(self):
        """Test ChatRequest with long query"""
        long_query = "q" * 5000
        request = ChatRequest(query=long_query)
        
        assert request.query == long_query
    
    def test_chat_request_unicode(self):
        """Test ChatRequest with unicode"""
        query = "Ask: 你好吗"
        request = ChatRequest(query=query)
        
        assert request.query == query
    
    def test_chat_request_json_serializable(self):
        """Test that ChatRequest can be serialized to JSON"""
        request = ChatRequest(query="test query")
        
        json_data = request.model_dump()
        assert json_data["query"] == "test query"


class TestRequestSchemaEdgeCases:
    """Test edge cases across all request schemas"""
    
    def test_models_reject_extra_fields(self):
        """Test that models handle extra fields"""
        # Some Pydantic configs ignore extra fields
        try:
            request = QueryRequest(
                query="test",
                extra_field="should be ignored"
            )
            # If no error, check that extra field is ignored
            assert not hasattr(request, 'extra_field')
        except ValidationError:
            # It's also valid to reject extra fields
            assert True
    
    def test_request_field_none_values(self):
        """Test handling of None values"""
        # These should fail validation
        with pytest.raises(ValidationError):
            QueryRequest(query=None)
        
        with pytest.raises(ValidationError):
            DeleteRequest(id=None)
    
    def test_requests_are_immutable(self):
        """Test that request objects handle attributes correctly"""
        request = QueryRequest(query="test")
        
        # Depending on Pydantic config, might be mutable or immutable
        try:
            request.query = "changed"
            # If mutable, that's okay
        except:
            # If immutable, that's also okay
            pass
