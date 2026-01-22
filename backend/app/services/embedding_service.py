"""Embedding service with OpenAI integration and stub for dev mode."""

from typing import Optional
import numpy as np

from app.core.config import settings
from app.core.exceptions import ExternalServiceError
from app.core.logging_config import get_logger


logger = get_logger(__name__)


class EmbeddingService:
    """
    Provides text embedding functionality.
    
    Uses OpenAI embeddings if API key is configured.
    Falls back to stub embeddings in dev mode.
    """
    
    def __init__(self):
        self.openai_client: Optional[any] = None
        self.embedding_dim = 1536  # OpenAI text-embedding-3-small dimension
        
        # Initialize OpenAI client if key is available
        if settings.openai_api_key:
            try:
                from openai import AsyncOpenAI
                self.openai_client = AsyncOpenAI(api_key=settings.openai_api_key)
                logger.info("OpenAI embeddings initialized")
            except ImportError:
                logger.warning("openai package not installed. Using stub embeddings.")
            except Exception as e:
                logger.warning(f"Failed to initialize OpenAI client: {e}. Using stub embeddings.")
        else:
            logger.info("OpenAI API key not configured. Using stub embeddings in dev mode.")
    
    async def embed_text(self, text: str) -> list[float]:
        """Generate embedding for a single text."""
        return await self.embed_texts([text])[0]
    
    async def embed_texts(self, texts: list[str]) -> list[list[float]]:
        """
        Generate embeddings for multiple texts.
        
        Uses OpenAI if configured, otherwise returns stub embeddings.
        """
        if not texts:
            return []
        
        # Use OpenAI if available
        if self.openai_client:
            try:
                response = await self.openai_client.embeddings.create(
                    model=settings.openai_embedding_model,
                    input=texts,
                )
                return [item.embedding for item in response.data]
            except Exception as e:
                logger.error(f"OpenAI embedding failed: {e}")
                raise ExternalServiceError(
                    f"Failed to generate embeddings: {str(e)}",
                    service="openai"
                )
        
        # Fallback: Generate stub embeddings (for dev mode)
        logger.debug("Using stub embeddings (dev mode)")
        return [self._generate_stub_embedding(text) for text in texts]
    
    def _generate_stub_embedding(self, text: str) -> list[float]:
        """
        Generate a deterministic stub embedding for dev mode.
        
        Uses text hash to create consistent embeddings.
        """
        # Create a pseudo-random but deterministic embedding based on text hash
        np.random.seed(hash(text) % (2**32))
        embedding = np.random.randn(self.embedding_dim).tolist()
        
        # Normalize to unit vector (common practice)
        norm = np.linalg.norm(embedding)
        if norm > 0:
            embedding = (np.array(embedding) / norm).tolist()
        
        return embedding
