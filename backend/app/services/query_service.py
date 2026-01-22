"""Query service for RAG (Retrieval-Augmented Generation)."""

from typing import Optional

from app.models.chatbox import Chatbox
from app.repositories.chunk_repository import ChunkRepository
from app.repositories.document_repository import DocumentRepository
from app.services.embedding_service import EmbeddingService
from app.services.llm_service import LLMService
from app.core.config import settings
from app.core.exceptions import ForbiddenError, OriginNotAllowedError
from app.core.logging_config import get_logger
from app.schemas.query import SourceChunk


logger = get_logger(__name__)


class QueryService:
    """
    Handles query processing with RAG:
    1. Validate origin (if required)
    2. Embed query
    3. Retrieve relevant chunks
    4. Generate answer with LLM
    """
    
    def __init__(
        self,
        chunk_repo: ChunkRepository,
        document_repo: DocumentRepository,
        embedding_service: EmbeddingService,
        llm_service: LLMService,
    ):
        self.chunk_repo = chunk_repo
        self.document_repo = document_repo
        self.embedding_service = embedding_service
        self.llm_service = llm_service
    
    def validate_origin(self, chatbox: Chatbox, origin: Optional[str]) -> None:
        """
        Validate request origin against chatbox's allowed domains.
        
        Enforcement rules:
        - If enforce_allowed_domains is True: origin is required and must match
        - If enforce_allowed_domains is False: origin check is optional
        """
        if not chatbox.enforce_allowed_domains:
            # Optional validation - no enforcement
            return
        
        # Origin is required for enforced chatboxes
        if not origin:
            raise ForbiddenError("Origin header is required for this chatbox")
        
        # Check if origin is in allowed list
        if not chatbox.allowed_domains:
            raise ForbiddenError("No allowed domains configured for this chatbox")
        
        # Normalize origin and allowed domains
        origin_normalized = origin.lower().rstrip("/")
        allowed_normalized = [d.lower().rstrip("/") for d in chatbox.allowed_domains]
        
        if origin_normalized not in allowed_normalized:
            raise OriginNotAllowedError(origin)
        
        logger.debug(f"Origin {origin} validated for chatbox {chatbox.id}")
    
    async def query(
        self,
        chatbox: Chatbox,
        question: str,
        origin: Optional[str] = None,
        document_id: Optional[int] = None,
        top_k: Optional[int] = None,
        min_score: Optional[float] = None,
    ) -> tuple[str, list[SourceChunk]]:
        """
        Process a query with RAG.
        
        Returns: (answer, source_chunks)
        """
        logger.info(f"Processing query for chatbox {chatbox.id}: {question[:50]}...")
        
        # Validate origin
        self.validate_origin(chatbox, origin)
        
        # Set defaults
        top_k = top_k or settings.vector_top_k_default
        min_score = min_score or settings.vector_min_score_default
        
        # Embed query
        query_embedding = await self.embedding_service.embed_text(question)
        
        # Retrieve relevant chunks
        chunks_with_scores = await self.chunk_repo.similarity_search(
            chatbox_id=chatbox.id,
            query_embedding=query_embedding,
            top_k=top_k,
            min_score=min_score,
            document_id=document_id,
        )
        
        if not chunks_with_scores:
            logger.info("No relevant chunks found")
            answer = "I couldn't find any relevant information to answer your question."
            return answer, []
        
        # Extract chunks and build context
        chunks = [chunk for chunk, score in chunks_with_scores]
        scores = [score for chunk, score in chunks_with_scores]
        context_texts = [chunk.content for chunk in chunks]
        
        # Generate answer with LLM
        answer = await self.llm_service.generate_answer(
            question=question,
            context_chunks=context_texts,
        )
        
        # Build source chunks response
        # Get document metadata for sources
        doc_ids = list(set(chunk.document_id for chunk in chunks))
        documents = {}
        for doc_id in doc_ids:
            doc = await self.document_repo.get_by_id_optional(doc_id)
            if doc:
                documents[doc_id] = doc
        
        source_chunks = []
        for chunk, score in zip(chunks, scores):
            doc = documents.get(chunk.document_id)
            source_chunks.append(
                SourceChunk(
                    document_id=chunk.document_id,
                    chunk_id=chunk.id,
                    content=chunk.content,
                    score=score,
                    source_name=doc.source_name if doc else None,
                )
            )
        
        logger.info(f"Generated answer with {len(source_chunks)} sources")
        return answer, source_chunks
