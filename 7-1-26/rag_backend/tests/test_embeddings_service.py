"""
Embeddings Service Tests
Tests for embedding generation and validation
"""
import pytest
from services.embeddings import generate_embedding


class TestEmbeddingGeneration:
    """Test embedding generation functionality"""
    
    def test_generate_embedding_returns_list(self):
        """Test that embeddings are returned as lists"""
        text = "Test embedding generation"
        embedding = generate_embedding(text)
        
        assert embedding is not None
        assert isinstance(embedding, list)
        assert len(embedding) > 0
    
    def test_embedding_contains_floats(self):
        """Test that embeddings contain numerical values"""
        text = "Numerical embedding test"
        embedding = generate_embedding(text)
        
        for value in embedding:
            assert isinstance(value, (int, float))
    
    def test_embedding_dimension_consistent(self):
        """Test that embeddings have consistent dimensions"""
        text1 = "First test sentence"
        text2 = "Second test sentence with more words"
        
        embedding1 = generate_embedding(text1)
        embedding2 = generate_embedding(text2)
        
        # Embeddings should have same dimension regardless of input length
        assert len(embedding1) == len(embedding2)
    
    def test_short_text_embedding(self):
        """Test embedding of short text"""
        short_text = "Hi"
        embedding = generate_embedding(short_text)
        
        assert embedding is not None
        assert len(embedding) > 0
    
    def test_long_text_embedding(self):
        """Test embedding of long text"""
        long_text = " ".join(["word"] * 1000)
        embedding = generate_embedding(long_text)
        
        assert embedding is not None
        assert len(embedding) > 0
    
    def test_special_characters_embedding(self):
        """Test embedding with special characters"""
        special_text = "Special: @#$%^&*() and numbers: 123456"
        embedding = generate_embedding(special_text)
        
        assert embedding is not None
        assert len(embedding) > 0
    
    def test_unicode_text_embedding(self):
        """Test embedding with unicode characters"""
        unicode_text = "Unicode test: 你好世界 مرحبا بالعالم"
        embedding = generate_embedding(unicode_text)
        
        assert embedding is not None
        assert len(embedding) > 0
    
    def test_empty_string_embedding(self):
        """Test embedding of empty string"""
        embedding = generate_embedding("")
        
        # Should either return valid embedding or raise exception
        if embedding is not None:
            assert isinstance(embedding, list)
    
    def test_whitespace_embedding(self):
        """Test embedding of whitespace"""
        whitespace_text = "   \t\n   "
        embedding = generate_embedding(whitespace_text)
        
        assert embedding is not None
        assert isinstance(embedding, list)


class TestEmbeddingSimilarity:
    """Test semantic similarity of embeddings"""
    
    def test_similar_texts_similar_embeddings(self):
        """Test that similar texts produce similar embeddings"""
        text1 = "The cat sat on the mat"
        text2 = "A cat sitting on a mat"
        
        embedding1 = generate_embedding(text1)
        embedding2 = generate_embedding(text2)
        
        # Calculate cosine similarity
        similarity = calculate_similarity(embedding1, embedding2)
        
        # Similar texts should have higher similarity
        assert similarity > 0
    
    def test_different_texts_different_embeddings(self):
        """Test that different texts produce different embeddings"""
        text1 = "Machine learning is a subset of AI"
        text2 = "Cooking recipes for beginners"
        
        embedding1 = generate_embedding(text1)
        embedding2 = generate_embedding(text2)
        
        similarity = calculate_similarity(embedding1, embedding2)
        
        # Different topics should have lower similarity
        assert similarity < 1.0
    
    def test_identical_texts_identical_embeddings(self):
        """Test that identical texts produce identical embeddings"""
        text = "This is the same text"
        
        embedding1 = generate_embedding(text)
        embedding2 = generate_embedding(text)
        
        assert embedding1 == embedding2


class TestEmbeddingNormalization:
    """Test embedding normalization properties"""
    
    def test_embedding_magnitude(self):
        """Test that embeddings have reasonable magnitude"""
        text = "Magnitude test"
        embedding = generate_embedding(text)
        
        # Calculate magnitude
        magnitude = sum(x**2 for x in embedding) ** 0.5
        
        # Should be a reasonable value
        assert magnitude > 0
        assert magnitude < float('inf')
    
    def test_embedding_range(self):
        """Test that embedding values are in reasonable range"""
        text = "Range test"
        embedding = generate_embedding(text)
        
        for value in embedding:
            # Most embeddings should be in reasonable range
            assert -100 < value < 100


def calculate_similarity(vec1, vec2):
    """Calculate cosine similarity between two vectors"""
    dot_product = sum(a * b for a, b in zip(vec1, vec2))
    magnitude1 = sum(a**2 for a in vec1) ** 0.5
    magnitude2 = sum(b**2 for b in vec2) ** 0.5
    
    if magnitude1 == 0 or magnitude2 == 0:
        return 0
    
    return dot_product / (magnitude1 * magnitude2)
