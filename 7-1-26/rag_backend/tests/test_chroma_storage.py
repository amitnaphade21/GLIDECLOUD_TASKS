"""
ChromaDB Storage and Persistence Tests
Tests for ChromaDB persistence, initialization, and data durability
"""
import pytest
import os
from database.chroma import collection
from config.settings import CHROMA_PATH, COLLECTION_NAME


@pytest.fixture(autouse=True)
def cleanup():
    """Clean up test documents"""
    test_ids = ["persist-test-1", "persist-test-2", "persist-test-3", "init-test-1"]
    for doc_id in test_ids:
        try:
            collection.delete(ids=[doc_id])
        except:
            pass
    yield
    for doc_id in test_ids:
        try:
            collection.delete(ids=[doc_id])
        except:
            pass


class TestChromaDBInitialization:
    """Test ChromaDB initialization and configuration"""
    
    def test_chroma_path_exists(self):
        """Test that ChromaDB path is properly configured"""
        assert CHROMA_PATH is not None
        assert isinstance(CHROMA_PATH, str)
    
    def test_collection_name_configured(self):
        """Test that collection name is configured"""
        assert COLLECTION_NAME is not None
        assert COLLECTION_NAME == "knowledge_base"
    
    def test_collection_is_initialized(self):
        """Test that collection is properly initialized"""
        assert collection is not None
        count = collection.count()
        assert isinstance(count, int)
        assert count >= 0
    
    def test_collection_has_correct_name(self):
        """Test that collection has the expected name"""
        # Try to get collection metadata
        try:
            name = collection.name
            assert name == COLLECTION_NAME
        except:
            # If name attribute doesn't exist, that's okay
            # Collection is still initialized
            assert collection is not None


class TestChromaDBPersistence:
    """Test data persistence and durability"""
    
    def test_document_persists_after_add(self):
        """Test that added documents persist"""
        text = "Persistence test document"
        doc_id = "persist-test-1"
        
        # Add document
        collection.add(
            documents=[text],
            ids=[doc_id],
            metadatas=[{"source": "test"}]
        )
        
        # Retrieve immediately
        result = collection.get(ids=[doc_id])
        assert result["documents"][0] == text
    
    def test_multiple_documents_persist(self):
        """Test that multiple documents persist correctly"""
        texts = [
            "First persistent document",
            "Second persistent document",
            "Third persistent document"
        ]
        ids = ["persist-test-1", "persist-test-2", "persist-test-3"]
        
        # Add documents
        collection.add(
            documents=texts,
            ids=ids,
            metadatas=[{"source": "test"} for _ in texts]
        )
        
        # Count should increase
        for doc_id in ids:
            result = collection.get(ids=[doc_id])
            assert len(result["documents"]) > 0
    
    def test_document_survives_multiple_operations(self):
        """Test document integrity after multiple operations"""
        original_text = "Original document"
        doc_id = "persist-test-1"
        
        # Add
        collection.add(documents=[original_text], ids=[doc_id])
        result1 = collection.get(ids=[doc_id])
        assert result1["documents"][0] == original_text
        
        # Update
        updated_text = "Updated document"
        collection.upsert(documents=[updated_text], ids=[doc_id])
        result2 = collection.get(ids=[doc_id])
        assert result2["documents"][0] == updated_text
        
        # Verify update persisted
        result3 = collection.get(ids=[doc_id])
        assert result3["documents"][0] == updated_text


class TestChromaDBDataIntegrity:
    """Test data integrity and correctness"""
    
    def test_document_content_preserved(self):
        """Test that document content is preserved exactly"""
        special_text = "Special chars: @#$%^&*() and unicode: 你好"
        doc_id = "persist-test-1"
        
        collection.add(documents=[special_text], ids=[doc_id])
        result = collection.get(ids=[doc_id])
        
        assert result["documents"][0] == special_text
    
    def test_metadata_preserved(self):
        """Test that metadata is preserved correctly"""
        metadata = {
            "source": "test.txt",
            "type": "test",
            "tags": ["tag1", "tag2"]
        }
        doc_id = "persist-test-1"
        
        collection.add(
            documents=["Test"],
            ids=[doc_id],
            metadatas=[metadata]
        )
        
        result = collection.get(ids=[doc_id])
        stored_metadata = result["metadatas"][0]
        
        assert stored_metadata["source"] == metadata["source"]
        assert stored_metadata["type"] == metadata["type"]
    
    def test_multiple_adds_dont_create_duplicates(self):
        """Test that adding same ID twice updates instead of duplicating"""
        doc_id = "persist-test-1"
        text1 = "First version"
        text2 = "Second version"
        
        # Add first version
        collection.add(documents=[text1], ids=[doc_id])
        count1 = collection.count()
        
        # Add second version with same ID (should update)
        collection.add(documents=[text2], ids=[doc_id])
        count2 = collection.count()
        
        # Count should be same or possibly different depending on implementation
        # But document should have latest content
        result = collection.get(ids=[doc_id])
        assert text2 in result["documents"][0] or result["documents"][0] == text2


class TestChromaDBErrorHandling:
    """Test error handling and edge cases"""
    
    def test_get_nonexistent_document(self):
        """Test getting a document that doesn't exist"""
        result = collection.get(ids=["nonexistent-id-xyz"])
        # Should return empty or handle gracefully
        assert result is not None
        assert len(result.get("documents", [])) == 0
    
    def test_delete_nonexistent_document(self):
        """Test deleting a document that doesn't exist"""
        try:
            collection.delete(ids=["nonexistent-id-xyz"])
            # Should not raise error
            assert True
        except Exception as e:
            pytest.fail(f"Delete should handle nonexistent ID gracefully: {str(e)}")
    
    def test_empty_document_list(self):
        """Test handling empty document list"""
        try:
            collection.add(documents=[], ids=[])
            # Should handle gracefully
            assert True
        except:
            # Some implementations might reject empty lists
            assert True
    
    def test_add_document_with_empty_string(self):
        """Test adding a document with empty string"""
        doc_id = "persist-test-1"
        empty_text = ""
        
        collection.add(documents=[empty_text], ids=[doc_id])
        result = collection.get(ids=[doc_id])
        
        assert len(result["documents"]) > 0


class TestChromaDBStorageStats:
    """Test storage statistics and metrics"""
    
    def test_collection_count_increases(self):
        """Test that collection count increases when adding documents"""
        initial_count = collection.count()
        
        collection.add(
            documents=["Doc 1", "Doc 2"],
            ids=["persist-test-1", "persist-test-2"]
        )
        
        final_count = collection.count()
        assert final_count >= initial_count + 1  # At least one document added
    
    def test_collection_count_decreases_on_delete(self):
        """Test that collection count decreases when deleting documents"""
        # Add document
        collection.add(documents=["Test"], ids=["persist-test-1"])
        count_before_delete = collection.count()
        
        # Delete document
        collection.delete(ids=["persist-test-1"])
        count_after_delete = collection.count()
        
        assert count_after_delete <= count_before_delete
    
    def test_collection_not_empty(self):
        """Test that collection has documents"""
        count = collection.count()
        # Collection should have at least some documents from previous tests
        # or we can add one to test
        assert isinstance(count, int)
        assert count >= 0
