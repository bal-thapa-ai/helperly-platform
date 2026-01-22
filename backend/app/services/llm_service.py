"""LLM service with OpenAI integration and stub for dev mode."""

from typing import Optional

from app.core.config import settings
from app.core.exceptions import ExternalServiceError
from app.core.logging_config import get_logger


logger = get_logger(__name__)


class LLMService:
    """
    Provides LLM (Language Model) functionality for generating answers.
    
    Uses OpenAI chat completions if API key is configured.
    Falls back to stub answers in dev mode.
    """
    
    def __init__(self):
        self.openai_client: Optional[any] = None
        
        # Initialize OpenAI client if key is available
        if settings.openai_api_key:
            try:
                from openai import AsyncOpenAI
                self.openai_client = AsyncOpenAI(api_key=settings.openai_api_key)
                logger.info("OpenAI LLM initialized")
            except ImportError:
                logger.warning("openai package not installed. Using stub LLM responses.")
            except Exception as e:
                logger.warning(f"Failed to initialize OpenAI client: {e}. Using stub LLM responses.")
        else:
            logger.info("OpenAI API key not configured. Using stub LLM responses in dev mode.")
    
    async def generate_answer(
        self,
        question: str,
        context_chunks: list[str],
        max_tokens: int = 500,
    ) -> str:
        """
        Generate an answer to a question based on retrieved context chunks.
        
        Uses OpenAI if configured, otherwise returns stub answer.
        """
        # Use OpenAI if available
        if self.openai_client:
            try:
                # Build context from chunks
                context = "\n\n".join([f"[{i+1}] {chunk}" for i, chunk in enumerate(context_chunks)])
                
                # Create prompt
                system_prompt = (
                    "You are a helpful assistant that answers questions based on the provided context. "
                    "If the answer is not in the context, say so. "
                    "Always cite your sources by reference number [1], [2], etc."
                )
                
                user_prompt = f"Context:\n{context}\n\nQuestion: {question}\n\nAnswer:"
                
                # Call OpenAI
                response = await self.openai_client.chat.completions.create(
                    model=settings.openai_chat_model,
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt},
                    ],
                    max_tokens=max_tokens,
                    temperature=0.7,
                )
                
                answer = response.choices[0].message.content.strip()
                return answer
                
            except Exception as e:
                logger.error(f"OpenAI LLM failed: {e}")
                raise ExternalServiceError(
                    f"Failed to generate answer: {str(e)}",
                    service="openai"
                )
        
        # Fallback: Generate stub answer (for dev mode)
        logger.debug("Using stub LLM response (dev mode)")
        return self._generate_stub_answer(question, context_chunks)
    
    def _generate_stub_answer(self, question: str, context_chunks: list[str]) -> str:
        """Generate a stub answer for dev mode."""
        if not context_chunks:
            return (
                f"[DEV MODE - Stub Answer] I don't have enough information to answer: '{question}'. "
                "No relevant content was found."
            )
        
        return (
            f"[DEV MODE - Stub Answer] Based on the retrieved context, here's a response to: '{question}'. "
            f"Found {len(context_chunks)} relevant chunks. "
            "In production, OpenAI would generate a detailed answer here."
        )
