"""Ingestion endpoints."""

from fastapi import APIRouter, Depends, UploadFile, File, Form, status

from app.core.config import settings
from app.core.exceptions import ValidationError
from app.schemas.ingest import (
    IngestTextRequest,
    IngestTextResponse,
    IngestURLRequest,
    IngestURLResponse,
    UploadResponse,
)
from app.services.ingestion_service import IngestionService
from app.repositories.chatbox_repository import ChatboxRepository
from app.api.dependencies import (
    get_ingestion_service,
    get_chatbox_repo,
    verify_api_key,
)


router = APIRouter(prefix="/v1/ingest", tags=["ingestion"])


@router.post(
    "/text",
    response_model=IngestTextResponse,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(verify_api_key)],
)
async def ingest_text(
    data: IngestTextRequest,
    chatbox_repo: ChatboxRepository = Depends(get_chatbox_repo),
    ingestion_service: IngestionService = Depends(get_ingestion_service),
) -> IngestTextResponse:
    """
    Ingest raw text into a chatbox.
    
    The text will be chunked, embedded, and stored for later retrieval.
    """
    # Verify chatbox exists
    await chatbox_repo.get_by_id(data.chatbox_id)
    
    # Ingest text
    document, chunks_created = await ingestion_service.ingest_text(
        chatbox_id=data.chatbox_id,
        text=data.text,
        source_name=data.source_name,
    )
    
    return IngestTextResponse(
        document_id=document.id,
        chunks_created=chunks_created,
        message=f"Successfully ingested text with {chunks_created} chunks",
    )


@router.post(
    "/url",
    response_model=IngestURLResponse,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(verify_api_key)],
)
async def ingest_url(
    data: IngestURLRequest,
    chatbox_repo: ChatboxRepository = Depends(get_chatbox_repo),
    ingestion_service: IngestionService = Depends(get_ingestion_service),
) -> IngestURLResponse:
    """
    Ingest content from a URL into a chatbox.
    
    TODO: Implement robust crawler with depth support.
    Currently fetches single page only.
    """
    # Verify chatbox exists
    await chatbox_repo.get_by_id(data.chatbox_id)
    
    # Ingest URL
    document, chunks_created = await ingestion_service.ingest_url(
        chatbox_id=data.chatbox_id,
        url=str(data.url),
        depth=data.depth,
    )
    
    return IngestURLResponse(
        document_id=document.id,
        chunks_created=chunks_created,
        url=str(data.url),
        message=f"Successfully ingested URL with {chunks_created} chunks",
    )


@router.post(
    "/upload",
    response_model=UploadResponse,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(verify_api_key)],
)
async def upload_file(
    chatbox_id: int = Form(...),
    file: UploadFile = File(...),
    chatbox_repo: ChatboxRepository = Depends(get_chatbox_repo),
    ingestion_service: IngestionService = Depends(get_ingestion_service),
) -> UploadResponse:
    """
    Upload and ingest a file into a chatbox.
    
    Supported formats: .txt, .pdf (TODO: add .docx, .xlsx)
    
    File size limit is configurable (default 7MB).
    """
    # Verify chatbox exists
    await chatbox_repo.get_by_id(chatbox_id)
    
    # Read file content
    content = await file.read()
    file_size_mb = len(content) / (1024 * 1024)
    
    # Check size limit
    if file_size_mb > settings.upload_max_mb:
        raise ValidationError(
            f"File size ({file_size_mb:.2f}MB) exceeds limit ({settings.upload_max_mb}MB)"
        )
    
    # Ingest file
    document, chunks_created = await ingestion_service.ingest_file(
        chatbox_id=chatbox_id,
        filename=file.filename or "untitled",
        content=content,
        mime_type=file.content_type,
    )
    
    return UploadResponse(
        document_id=document.id,
        chunks_created=chunks_created,
        filename=file.filename or "untitled",
        file_size_bytes=len(content),
        message=f"Successfully uploaded and ingested file with {chunks_created} chunks",
    )
