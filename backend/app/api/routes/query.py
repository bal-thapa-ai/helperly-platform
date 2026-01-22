"""Query endpoint for RAG."""

from fastapi import APIRouter, Depends

from app.schemas.query import QueryRequest, QueryResponse
from app.services.query_service import QueryService
from app.repositories.chatbox_repository import ChatboxRepository
from app.api.dependencies import (
    get_query_service,
    get_chatbox_repo,
    verify_api_key,
)


router = APIRouter(prefix="/v1", tags=["query"])


@router.post(
    "/query",
    response_model=QueryResponse,
    dependencies=[Depends(verify_api_key)],
)
async def query_chatbox(
    data: QueryRequest,
    chatbox_repo: ChatboxRepository = Depends(get_chatbox_repo),
    query_service: QueryService = Depends(get_query_service),
) -> QueryResponse:
    """
    Query a chatbox with a question.
    
    This endpoint:
    1. Validates the request origin (if required by chatbox plan)
    2. Retrieves relevant document chunks using vector similarity
    3. Generates an answer using LLM with the retrieved context
    4. Returns the answer with source citations
    
    Origin validation:
    - Free/Starter plans: origin check is optional
    - Pro/Enterprise plans: origin must be in allowed_domains
    """
    # Get chatbox
    chatbox = await chatbox_repo.get_by_id(data.chatbox_id)
    
    # Process query
    answer, sources = await query_service.query(
        chatbox=chatbox,
        question=data.question,
        origin=data.origin,
        document_id=data.document_id,
        top_k=data.top_k,
    )
    
    return QueryResponse(
        answer=answer,
        sources=sources,
        chatbox_id=data.chatbox_id,
    )
