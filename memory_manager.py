"""
Memory management module for NayePankh AI Assistant.
Handles ChromaDB operations with proper error handling and cleanup.
"""

import chromadb
from chromadb.config import Settings
from typing import Optional, List, Dict, Any
from datetime import datetime, timedelta
from config import Config
from logger import get_logger

logger = get_logger(__name__)


class MemoryManager:
    """Manages ChromaDB memory operations with error handling."""
    
    def __init__(self):
        """Initialize the memory manager with ChromaDB client."""
        self.client = None
        self.collection = None
        self._initialize_client()
    
    def _initialize_client(self) -> None:
        """Initialize ChromaDB client with error handling."""
        try:
            self.client = chromadb.PersistentClient(
                path=str(Config.MEMORY_DIR),
                settings=Settings(
                    anonymized_telemetry=False,
                    allow_reset=True
                )
            )
            self.collection = self.client.get_or_create_collection(
                name=Config.MEMORY_COLLECTION_NAME,
                metadata={"hnsw:space": "cosine"}
            )
            logger.info(f"Memory system initialized: {Config.MEMORY_COLLECTION_NAME}")
            
        except Exception as e:
            logger.error(f"Failed to initialize memory system: {e}")
            raise
    
    def add_memory(self, document: str, metadata: Optional[Dict[str, Any]] = None) -> str:
        """
        Add a document to memory with duplicate prevention.
        
        Args:
            document: Document text to add
            metadata: Optional metadata dictionary
        
        Returns:
            ID of the added document
        """
        try:
            # Check for duplicates
            existing = self.collection.get(
                where={"document": document}
            )
            
            if existing and existing.get('ids'):
                logger.debug(f"Duplicate document detected, skipping: {document[:50]}...")
                return existing['ids'][0]
            
            # Generate unique ID
            import uuid
            doc_id = str(uuid.uuid4())
            
            # Add metadata if not provided
            if metadata is None:
                metadata = {}
            
            metadata.update({
                "document": document,
                "timestamp": datetime.now().isoformat()
            })
            
            self.collection.add(
                documents=[document],
                metadatas=[metadata],
                ids=[doc_id]
            )
            
            logger.debug(f"Memory added: {doc_id}")
            return doc_id
            
        except Exception as e:
            logger.error(f"Error adding memory: {e}")
            raise
    
    def query_memory(self, query_text: str, n_results: int = 3) -> List[Dict[str, Any]]:
        """
        Query memory for similar documents.
        
        Args:
            query_text: Query text
            n_results: Number of results to return
        
        Returns:
            List of matching documents with metadata
        """
        try:
            results = self.collection.query(
                query_texts=[query_text],
                n_results=min(n_results, Config.MEMORY_MAX_RESULTS)
            )
            
            if not results or not results.get('documents'):
                logger.debug(f"No memories found for query: {query_text[:50]}...")
                return []
            
            memories = []
            for i, doc in enumerate(results['documents'][0]):
                memory = {
                    'document': doc,
                    'metadata': results['metadatas'][0][i] if results.get('metadatas') else {},
                    'distance': results['distances'][0][i] if results.get('distances') else 0
                }
                memories.append(memory)
            
            logger.debug(f"Retrieved {len(memories)} memories")
            return memories
            
        except Exception as e:
            logger.error(f"Error querying memory: {e}")
            return []
    
    def cleanup_old_memories(self, days: int = Config.MEMORY_RETENTION_DAYS) -> int:
        """
        Remove memories older than specified days.
        
        Args:
            days: Number of days to retain memories
        
        Returns:
            Number of memories removed
        """
        try:
            cutoff_date = datetime.now() - timedelta(days=days)
            
            # Get all memories
            all_memories = self.collection.get()
            
            if not all_memories or not all_memories.get('ids'):
                logger.debug("No memories to clean up")
                return 0
            
            # Find old memories
            ids_to_remove = []
            for i, metadata in enumerate(all_memories.get('metadatas', [])):
                if metadata:
                    timestamp_str = metadata.get('timestamp')
                    if timestamp_str:
                        try:
                            timestamp = datetime.fromisoformat(timestamp_str)
                            if timestamp < cutoff_date:
                                ids_to_remove.append(all_memories['ids'][i])
                        except ValueError:
                            continue
            
            # Remove old memories
            if ids_to_remove:
                self.collection.delete(ids=ids_to_remove)
                logger.info(f"Cleaned up {len(ids_to_remove)} old memories")
                return len(ids_to_remove)
            
            logger.debug("No old memories to clean up")
            return 0
            
        except Exception as e:
            logger.error(f"Error cleaning up memories: {e}")
            return 0
    
    def get_memory_count(self) -> int:
        """
        Get the total number of memories in the collection.
        
        Returns:
            Number of memories
        """
        try:
            count = self.collection.count()
            logger.debug(f"Memory count: {count}")
            return count
        except Exception as e:
            logger.error(f"Error getting memory count: {e}")
            return 0
    
    def clear_all_memories(self) -> None:
        """Clear all memories from the collection."""
        try:
            self.client.delete_collection(Config.MEMORY_COLLECTION_NAME)
            self.collection = self.client.get_or_create_collection(
                name=Config.MEMORY_COLLECTION_NAME
            )
            logger.warning("All memories cleared")
        except Exception as e:
            logger.error(f"Error clearing memories: {e}")
            raise


# Global memory manager instance
memory_manager = MemoryManager()

# Backward compatibility - expose collection directly
collection = memory_manager.collection