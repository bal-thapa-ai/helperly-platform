"""Repository for Chunk operations with vector search."""

from typing import Optional
from sqlalchemy import select, text
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.chunk import Chunk
from app.core.logging_config import get_logger


logger = get_logger(__name__)


class ChunkRepository:
    """Handles database operations for Chunk including vector similarity search."""
    
    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def create_many(self, chunks: list[Chunk]) -> list[Chunk]:
        """Bulk create chunks."""
        self.session.add_all(chunks)
        await self.session.commit()
        for chunk in chunks:
            await self.session.refresh(chunk)
        return chunks
    
    async def delete_by_document(self, document_id: int) -> None:
        """Delete all chunks for a document."""
        result = await self.session.execute(
            select(Chunk).where(Chunk.document_id == document_id)
        )
        chunks = result.scalars().all()
        for chunk in chunks:
            await self.session.delete(chunk)
        await self.session.commit()
    
    async def similarity_search(
        self,
        chatbox_id: int,
        query_embedding: list[float],
        top_k: int = 5,
        min_score: float = 0.7,
        document_id: Optional[int] = None,
    ) -> list[tuple[Chunk, float]]:
        """
        Perform vector similarity search using pgvector.
        
        Returns list of (Chunk, similarity_score) tuples.
        
        TODO: This implementation requires pgvector extension enabled:
        CREATE EXTENSION IF NOT EXISTS vector;
        
        TODO: For better performance, create HNSW index:
        CREATE INDEX ON chunks USING hnsw (embedding vector_cosine_ops);
        """
        try:
            # Convert embedding to pgvector format
            embedding_str = f"[{','.join(map(str, query_embedding))}]"
            
            # Build query with vector similarity
            # Using cosine similarity: 1 - (embedding <=> query_embedding)
            query = """
                SELECT id, document_id, chatbox_id, content, chunk_index, embedding,
                       1 - (embedding <=> :embedding::vector) AS similarity
                FROM chunks
                WHERE chatbox_id = :chatbox_id
            """
            
            params = {
                "embedding": embedding_str,
                "chatbox_id": chatbox_id,
            }
            
            # Add document filter if specified
            if document_id is not None:
                query += " AND document_id = :document_id"
                params["document_id"] = document_id
            
            # Filter by minimum score and limit
            query += """
                AND (1 - (embedding <=> :embedding::vector)) >= :min_score
                ORDER BY embedding <=> :embedding::vector
                LIMIT :top_k
            """
            params["min_score"] = min_score
            params["top_k"] = top_k
            
            result = await self.session.execute(text(query), params)
            rows = result.fetchall()
            
            # Convert rows to Chunk objects with scores
            chunks_with_scores = []
            for row in rows:
                chunk = Chunk(
                    id=row.id,
                    document_id=row.document_id,
                    chatbox_id=row.chatbox_id,
                    content=row.content,
                    chunk_index=row.chunk_index,
                )
                score = float(row.similarity)
                chunks_with_scores.append((chunk, score))
            
            return chunks_with_scores
            
        except Exception as e:
            logger.warning(
                f"Vector search failed (pgvector may not be enabled): {e}. "
                "Falling back to stub implementation."
            )
            # Fallback: return empty results in dev mode
            # TODO: Implement alternative search or ensure pgvector is enabled
            return []
