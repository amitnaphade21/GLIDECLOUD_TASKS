"""
Text Chunking Utility Tests
Tests for document reading and text chunking functionality
"""
import pytest
import os
from utils.chunking import read_docs_file, split_text
from config.settings import DOCS_PATH


class TestReadDocsFile:
    """Test document file reading functionality"""
    
    def test_read_docs_file_returns_string(self):
        """Test that read_docs_file returns a string"""
        content = read_docs_file()
        
        assert content is not None
        assert isinstance(content, str)
    
    def test_read_docs_file_not_empty(self):
        """Test that docs.txt file is not empty"""
        content = read_docs_file()
        
        assert len(content) > 0
    
    def test_read_docs_file_content_type(self):
        """Test that docs file contains valid text content"""
        content = read_docs_file()
        
        # Should be readable text
        assert isinstance(content, str)
        assert all(ord(c) < 128 or ord(c) > 31 for c in content if c != '\n')
    
    def test_docs_file_path_configured(self):
        """Test that DOCS_PATH is properly configured"""
        assert DOCS_PATH is not None
        assert isinstance(DOCS_PATH, str)
        assert DOCS_PATH.endswith('.txt')
    
    def test_read_docs_file_handles_encoding(self):
        """Test that file is read with proper encoding"""
        try:
            content = read_docs_file()
            # If it reads successfully, encoding is handled
            assert content is not None
        except Exception as e:
            pytest.fail(f"Failed to read docs file with proper encoding: {str(e)}")


class TestTextSplitting:
    """Test text chunking functionality"""
    
    def test_split_text_returns_list(self):
        """Test that split_text returns a list"""
        text = "This is a sample text for chunking with multiple words"
        chunks = split_text(text)
        
        assert chunks is not None
        assert isinstance(chunks, list)
    
    def test_split_text_creates_chunks(self):
        """Test that text is split into chunks"""
        text = " ".join(["word"] * 100)
        chunks = split_text(text, chunk_size=10)
        
        assert len(chunks) > 1
    
    def test_split_text_chunk_structure(self):
        """Test that chunks are properly structured strings"""
        text = "One two three four five six seven eight nine ten"
        chunks = split_text(text, chunk_size=3)
        
        for chunk in chunks:
            assert isinstance(chunk, str)
            assert len(chunk) > 0
    
    def test_split_text_with_custom_chunk_size(self):
        """Test splitting with custom chunk size"""
        text = " ".join(["word"] * 50)
        chunks_small = split_text(text, chunk_size=5)
        chunks_large = split_text(text, chunk_size=20)
        
        # More chunks with smaller size
        assert len(chunks_small) >= len(chunks_large)
    
    def test_split_text_preserves_content(self):
        """Test that splitting preserves all content"""
        text = "The quick brown fox jumps over the lazy dog"
        chunks = split_text(text)
        
        # Rejoin chunks and verify content
        rejoined = " ".join(chunks)
        
        # All original words should be present
        for word in text.split():
            assert word in rejoined
    
    def test_split_text_short_content(self):
        """Test splitting text shorter than chunk size"""
        text = "Short text"
        chunks = split_text(text, chunk_size=10)
        
        assert len(chunks) >= 1
        assert all(isinstance(chunk, str) for chunk in chunks)
    
    def test_split_text_exact_chunk_size(self):
        """Test splitting text that's exactly chunk size"""
        words = ["word"] * 10
        text = " ".join(words)
        chunks = split_text(text, chunk_size=10)
        
        assert len(chunks) >= 1
    
    def test_split_text_single_word(self):
        """Test splitting text with single word"""
        text = "SingleWord"
        chunks = split_text(text)
        
        assert len(chunks) >= 1
        assert chunks[0] == "SingleWord"
    
    def test_split_text_empty_string(self):
        """Test splitting empty string"""
        text = ""
        chunks = split_text(text)
        
        # Should handle gracefully
        assert isinstance(chunks, list)
    
    def test_split_text_with_special_characters(self):
        """Test splitting text with special characters"""
        text = "Hello! @How #are $you% ^doing& *today?"
        chunks = split_text(text, chunk_size=2)
        
        assert len(chunks) > 0
        # Verify special characters preserved
        all_content = " ".join(chunks)
        assert "!" in all_content
        assert "@" in all_content
    
    def test_split_text_with_punctuation(self):
        """Test splitting text with punctuation"""
        text = "First sentence. Second sentence! Third question? Fourth statement."
        chunks = split_text(text, chunk_size=3)
        
        assert len(chunks) > 0
        assert all(isinstance(chunk, str) for chunk in chunks)
    
    def test_split_text_chunk_no_empty_chunks(self):
        """Test that no empty chunks are created"""
        text = " ".join(["word"] * 50)
        chunks = split_text(text, chunk_size=10)
        
        # All chunks should have content
        for chunk in chunks:
            assert len(chunk.strip()) > 0
    
    def test_split_text_document(self):
        """Test splitting actual document content"""
        content = read_docs_file()
        chunks = split_text(content)
        
        assert len(chunks) > 0
        assert all(isinstance(chunk, str) for chunk in chunks)
        assert all(len(chunk) > 0 for chunk in chunks)


class TestChunkingWithDocuments:
    """Integration tests for chunking with actual documents"""
    
    def test_chunk_real_document(self):
        """Test chunking the actual docs.txt file"""
        content = read_docs_file()
        chunks = split_text(content)
        
        assert len(chunks) > 0
        
        # Verify chunks are meaningful
        for chunk in chunks:
            words = chunk.split()
            assert len(words) > 0
    
    def test_chunks_maintain_word_order(self):
        """Test that word order is maintained in chunks"""
        text = "The quick brown fox jumps over the lazy dog"
        chunks = split_text(text, chunk_size=3)
        
        # First chunk should start with "The quick brown"
        assert "The" in chunks[0]
    
    def test_all_words_in_chunks(self):
        """Test that all words from original text are in chunks"""
        original_words = set("The quick brown fox jumps over the lazy dog".split())
        text = "The quick brown fox jumps over the lazy dog"
        chunks = split_text(text)
        
        chunk_words = set(" ".join(chunks).split())
        
        # All original words should be in chunks
        assert original_words.issubset(chunk_words)
    
    def test_chunking_consistency(self):
        """Test that chunking the same text produces consistent results"""
        text = " ".join(["word"] * 100)
        
        chunks1 = split_text(text, chunk_size=10)
        chunks2 = split_text(text, chunk_size=10)
        
        assert chunks1 == chunks2
    
    def test_large_document_chunking(self):
        """Test chunking large documents"""
        large_text = " ".join(["document"] * 1000)
        chunks = split_text(large_text, chunk_size=50)
        
        assert len(chunks) > 0
        assert all(len(chunk) > 0 for chunk in chunks)
