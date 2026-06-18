"""
Tests for memory management system.
"""

import pytest
from memory_manager import memory_manager


class TestMemoryManager:
    """Test cases for memory management."""
    
    def test_add_memory(self):
        """Test adding memory."""
        doc_id = memory_manager.add_memory("Test memory entry")
        assert doc_id is not None
    
    def test_add_duplicate_memory(self):
        """Test adding duplicate memory (should return existing ID)."""
        text = "Test duplicate memory"
        doc_id1 = memory_manager.add_memory(text)
        doc_id2 = memory_manager.add_memory(text)
        assert doc_id1 == doc_id2
    
    def test_query_memory(self):
        """Test querying memory."""
        memory_manager.add_memory("Python programming tutorial")
        results = memory_manager.query_memory("Python")
        assert isinstance(results, list)
    
    def test_query_memory_empty(self):
        """Test querying memory with no results."""
        results = memory_manager.query_memory("NonExistentQuery12345")
        assert results == []
    
    def test_get_memory_count(self):
        """Test getting memory count."""
        count = memory_manager.get_memory_count()
        assert count >= 0
    
    def test_cleanup_old_memories(self):
        """Test cleaning up old memories."""
        removed = memory_manager.cleanup_old_memories(days=0)
        assert removed >= 0
