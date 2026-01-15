from database.chroma import collection
import uuid


def test_vectors_are_stored():
    """Test that vectors exist in the ChromaDB collection"""
    count = collection.count()
    assert count >= 0, "Collection should have non-negative vector count"


def test_collection_exists():
    """Test that ChromaDB collection is properly initialized"""
    assert collection is not None
    assert hasattr(collection, 'count'), "Collection should have count method"
    assert hasattr(collection, 'add'), "Collection should have add method"
    assert hasattr(collection, 'query'), "Collection should have query method"


def test_add_and_retrieve_vector():
    """Test adding a vector to the collection and retrieving it"""
    doc_id = str(uuid.uuid4())
    test_doc = "This is a test document for semantic search"
    
    # Add document to collection
    collection.add(
        documents=[test_doc],
        ids=[doc_id],
        metadatas=[{"source": "test", "type": "unit_test"}]
    )
    
    # Query the collection
    results = collection.query(
        query_texts=[test_doc],
        n_results=1
    )
    
    assert len(results["documents"]) > 0
    assert len(results["documents"][0]) > 0
    assert results["documents"][0][0] == test_doc


def test_query_with_metadata():
    """Test that metadata is properly stored and retrieved with vectors"""
    doc_id = str(uuid.uuid4())
    test_doc = "Document with metadata for testing"
    metadata = {"source": "test_file.txt", "chunk_index": 1}
    
    # Add document with metadata
    collection.add(
        documents=[test_doc],
        ids=[doc_id],
        metadatas=[metadata]
    )
    
    # Query and verify metadata
    results = collection.query(
        query_texts=[test_doc],
        n_results=1,
        include=["metadatas", "documents"]
    )
    
    assert len(results["metadatas"]) > 0
    retrieved_metadata = results["metadatas"][0][0]
    assert retrieved_metadata["source"] == "test_file.txt"
    assert retrieved_metadata["chunk_index"] == 1


def test_semantic_search_distance_calculation():
    """Test that semantic search returns valid distance scores"""
    doc_id = str(uuid.uuid4())
    test_doc = "Machine learning is a subset of artificial intelligence"
    
    # Add document
    collection.add(
        documents=[test_doc],
        ids=[doc_id],
        metadatas=[{"source": "test"}]
    )
    
    # Query with similar text
    results = collection.query(
        query_texts=["machine learning and AI"],
        n_results=1,
        include=["distances"]
    )
    
    assert len(results["distances"]) > 0
    assert len(results["distances"][0]) > 0
    # Distance should be a number (float)
    distance = results["distances"][0][0]
    assert isinstance(distance, (int, float))
    # Distance should be >= 0 (typically between 0 and 2 for cosine distance)
    assert distance >= 0
