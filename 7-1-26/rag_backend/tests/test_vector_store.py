"""
Vector Store Tests
Tests for ChromaDB storage, retrieval, and vector operations
"""
import pytest
from database.chroma import collection
from services.embeddings import generate_embedding


@pytest.fixture(autouse=True)
def cleanup_before_and_after():
    """Clean up test data before and after each test"""
    test_ids = [
        "store-test-1", "store-test-2", "store-test-3",
        "embedding-test-1", "query-test-1"
    ]
    
    # Cleanup before
    for doc_id in test_ids:
        try:
            collection.delete(ids=[doc_id])
        except:
            pass
    
    yield
    
    # Cleanup after
    for doc_id in test_ids:
        try:
            collection.delete(ids=[doc_id])
        except:
            pass


class TestChromaDBOperations:
    """Test basic ChromaDB CRUD operations"""
    
    def test_add_document_to_collection(self):
        """Test adding a document to ChromaDB"""
        text = "This is a test document for ChromaDB"
        doc_id = "store-test-1"
        
        collection.add(
            documents=[text],
            ids=[doc_id],
            metadatas=[{"source": "test"}]
        )
        
        result = collection.get(ids=[doc_id])
        assert result is not None
        assert len(result["documents"]) == 1
        assert result["documents"][0] == text
    
    def test_add_multiple_documents(self):
        """Test adding multiple documents at once"""
        texts = [
            "First test document",
            "Second test document",
            "Third test document"
        ]
        ids = ["store-test-1", "store-test-2", "store-test-3"]
        
        collection.add(
            documents=texts,
            ids=ids,
            metadatas=[{"source": "test"} for _ in texts]
        )
        
        result = collection.get(ids=ids)
        assert len(result["documents"]) == 3
        assert result["documents"] == texts
    
    def test_retrieve_document_by_id(self):
        """Test retrieving a document by ID"""
        text = "Retrieve this document"
        doc_id = "store-test-1"
        
        collection.add(documents=[text], ids=[doc_id])
        result = collection.get(ids=[doc_id])
        
        assert result["documents"][0] == text
    
    def test_update_document(self):
        """Test updating an existing document"""
        original_text = "Original content"
        updated_text = "Updated content"
        doc_id = "store-test-1"
        
        # Add original
        collection.add(documents=[original_text], ids=[doc_id])
        
        # Update using upsert
        collection.upsert(
            documents=[updated_text],
            ids=[doc_id]
        )
        
        result = collection.get(ids=[doc_id])
        assert result["documents"][0] == updated_text
    
    def test_delete_document(self):
        """Test deleting a document"""
        text = "Document to delete"
        doc_id = "store-test-1"
        
        # Add document
        collection.add(documents=[text], ids=[doc_id])
        
        # Verify it exists
        result = collection.get(ids=[doc_id])
        assert len(result["documents"]) == 1
        
        # Delete document
        collection.delete(ids=[doc_id])
        
        # Verify it's deleted
        result = collection.get(ids=[doc_id])
        assert len(result["documents"]) == 0
    
    def test_count_documents(self):
        """Test counting documents in collection"""
        initial_count = collection.count()
        
        collection.add(
            documents=["Doc 1", "Doc 2"],
            ids=["store-test-1", "store-test-2"]
        )
        
        new_count = collection.count()
        assert new_count == initial_count + 2


class TestVectorEmbeddings:
    """Test embedding generation and storage"""
    
    def test_add_with_embeddings(self):
        """Test adding documents with embeddings"""
        text = "Document with embedding"
        doc_id = "embedding-test-1"
        
        # Generate embedding
        embedding = generate_embedding(text)
        
        # Verify embedding is generated
        assert embedding is not None
        assert isinstance(embedding, list)
        assert len(embedding) > 0
        
        # Add to collection with embedding
        collection.add(
            documents=[text],
            embeddings=[embedding],
            ids=[doc_id]
        )
        
        result = collection.get(ids=[doc_id])
        assert result["documents"][0] == text
    
    def test_embedding_consistency(self):
        """Test that embedding same text produces same result"""
        text = "Consistent embedding test"
        
        embedding1 = generate_embedding(text)
        embedding2 = generate_embedding(text)
        
        # Embeddings should be identical for same text
        assert embedding1 == embedding2
    
    def test_different_texts_different_embeddings(self):
        """Test that different texts produce different embeddings"""
        text1 = "First unique text"
        text2 = "Second unique text"
        
        embedding1 = generate_embedding(text1)
        embedding2 = generate_embedding(text2)
        
        # Embeddings should be different
        assert embedding1 != embedding2


class TestVectorSimilaritySearch:
    """Test similarity search functionality"""
    
    def test_query_by_embedding(self):
        """Test querying by embedding vector"""
        # Add test documents
        texts = [
            "Machine learning is a subset of artificial intelligence",
            "Deep learning uses neural networks",
            "Python is a programming language"
        ]
        ids = ["query-test-1", "query-test-2", "query-test-3"]
        
        collection.add(
            documents=texts,
            ids=ids,
            metadatas=[{"source": "test"} for _ in texts]
        )
        
        # Query with embedding
        query_text = "artificial intelligence and machine learning"
        query_embedding = generate_embedding(query_text)
        
        results = collection.query(
            query_embeddings=[query_embedding],
            n_results=2
        )
        
        assert results is not None
        assert len(results["documents"]) > 0
        assert len(results["documents"][0]) <= 2  # Should return at most 2
    
    def test_query_returns_distances(self):
        """Test that query results include distance scores"""
        text = "Query distance test"
        doc_id = "query-test-1"
        
        collection.add(documents=[text], ids=[doc_id])
        
        query_embedding = generate_embedding(text)
        results = collection.query(
            query_embeddings=[query_embedding],
            n_results=1
        )
        
        assert "distances" in results
        assert len(results["distances"]) > 0
    
    def test_query_with_metadata_filtering(self):
        """Test querying with metadata"""
        texts = ["Doc 1", "Doc 2"]
        ids = ["query-test-1", "query-test-2"]
        metadatas = [
            {"source": "file1", "type": "test"},
            {"source": "file2", "type": "test"}
        ]
        
        collection.add(
            documents=texts,
            ids=ids,
            metadatas=metadatas
        )
        
        query_embedding = generate_embedding("test query")
        results = collection.query(
            query_embeddings=[query_embedding],
            n_results=2
        )
        
        assert results is not None
        assert "metadatas" in results


class TestCollectionMetadata:
    """Test metadata storage and retrieval"""
    
    def test_store_document_metadata(self):
        """Test storing metadata with documents"""
        text = "Document with metadata"
        doc_id = "store-test-1"
        metadata = {
            "source": "test_file.txt",
            "type": "test",
            "version": "1.0"
        }
        
        collection.add(
            documents=[text],
            ids=[doc_id],
            metadatas=[metadata]
        )
        
        result = collection.get(ids=[doc_id])
        assert result["metadatas"][0]["source"] == "test_file.txt"
        assert result["metadatas"][0]["type"] == "test"
    
    def test_retrieve_metadata(self):
        """Test retrieving stored metadata"""
        collection.add(
            documents=["Test"],
            ids=["store-test-1"],
            metadatas=[{"key": "value"}]
        )
        
        result = collection.get(ids=["store-test-1"])
        assert "metadatas" in result
        assert result["metadatas"][0]["key"] == "value"
    
    def test_metadata_with_multiple_documents(self):
        """Test metadata with multiple documents"""
        texts = ["Doc 1", "Doc 2", "Doc 3"]
        ids = ["store-test-1", "store-test-2", "store-test-3"]
        metadatas = [
            {"doc_num": 1},
            {"doc_num": 2},
            {"doc_num": 3}
        ]
        
        collection.add(
            documents=texts,
            ids=ids,
            metadatas=metadatas
        )
        
        result = collection.get(ids=ids)
        for i, metadata in enumerate(result["metadatas"]):
            assert metadata["doc_num"] == i + 1  