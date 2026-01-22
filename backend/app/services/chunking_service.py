"""Text chunking service."""

from typing import List
from app.core.config import settings
from app.core.logging_config import get_logger


logger = get_logger(__name__)


class ChunkingService:
    """
    Provides text chunking functionality.
    
    Implements character-based chunking with overlap.
    """
    
    def __init__(
        self,
        chunk_size: int = None,
        chunk_overlap: int = None,
    ):
        self.chunk_size = chunk_size or settings.chunk_size
        self.chunk_overlap = chunk_overlap or settings.chunk_overlap
    
    def chunk_text(self, text: str) -> List[str]:
        """
        Split text into overlapping chunks.
        
        Simple character-based chunking with overlap.
        TODO: Consider more sophisticated chunking:
        - Sentence-aware chunking
        - Semantic chunking
        - Language-specific tokenization
        """
        if not text or not text.strip():
            return []
        
        chunks = []
        start = 0
        text_length = len(text)
        
        while start < text_length:
            # Get chunk
            end = start + self.chunk_size
            chunk = text[start:end]
            
            # Skip empty chunks
            if chunk.strip():
                chunks.append(chunk.strip())
            
            # Move start position (with overlap)
            start += self.chunk_size - self.chunk_overlap
            
            # Avoid infinite loop
            if start <= 0:
                break
        
        logger.debug(f"Chunked text into {len(chunks)} chunks")
        return chunks
