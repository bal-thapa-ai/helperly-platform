"""Ingestion service for processing and storing documents."""

from typing import Optional
import requests
from bs4 import BeautifulSoup

from app.models.document import Document, DocumentType
from app.models.chunk import Chunk
from app.repositories.document_repository import DocumentRepository
from app.repositories.chunk_repository import ChunkRepository
from app.services.chunking_service import ChunkingService
from app.services.embedding_service import EmbeddingService
from app.core.logging_config import get_logger
from app.core.exceptions import ValidationError, ExternalServiceError


logger = get_logger(__name__)


class IngestionService:
    """
    Handles document ingestion: chunking, embedding, and storage.
    """
    
    def __init__(
        self,
        document_repo: DocumentRepository,
        chunk_repo: ChunkRepository,
        chunking_service: ChunkingService,
        embedding_service: EmbeddingService,
    ):
        self.document_repo = document_repo
        self.chunk_repo = chunk_repo
        self.chunking_service = chunking_service
        self.embedding_service = embedding_service
    
    async def ingest_text(
        self,
        chatbox_id: int,
        text: str,
        source_name: Optional[str] = None,
    ) -> tuple[Document, int]:
        """
        Ingest raw text: chunk, embed, and store.
        
        Returns: (Document, number of chunks created)
        """
        logger.info(f"Ingesting text for chatbox {chatbox_id}")
        
        # Create document
        document = Document(
            chatbox_id=chatbox_id,
            source_type=DocumentType.TEXT,
            source_name=source_name or "Raw Text",
            raw_content=text,
        )
        document = await self.document_repo.create(document)
        
        # Chunk text
        chunks_text = self.chunking_service.chunk_text(text)
        
        if not chunks_text:
            logger.warning("No chunks created from text")
            return document, 0
        
        # Generate embeddings
        embeddings = await self.embedding_service.embed_texts(chunks_text)
        
        # Create chunk objects
        chunks = []
        for i, (chunk_text, embedding) in enumerate(zip(chunks_text, embeddings)):
            chunk = Chunk(
                document_id=document.id,
                chatbox_id=chatbox_id,
                content=chunk_text,
                chunk_index=i,
                embedding=embedding,
            )
            chunks.append(chunk)
        
        # Store chunks
        await self.chunk_repo.create_many(chunks)
        
        logger.info(f"Created document {document.id} with {len(chunks)} chunks")
        return document, len(chunks)
    
    async def ingest_url(
        self,
        chatbox_id: int,
        url: str,
        depth: int = 1,
    ) -> tuple[Document, int]:
        """
        Ingest content from URL: fetch, extract text, chunk, embed, and store.
        
        TODO: Implement robust crawler with:
        - Respect robots.txt
        - Handle JavaScript-rendered pages
        - Follow links to specified depth
        - Rate limiting
        
        For now: simple single-page fetch.
        """
        logger.info(f"Ingesting URL {url} for chatbox {chatbox_id}")
        
        try:
            # Fetch URL content
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            
            # Extract text from HTML
            soup = BeautifulSoup(response.content, "html.parser")
            
            # Remove script and style elements
            for script in soup(["script", "style"]):
                script.decompose()
            
            # Get text
            text = soup.get_text(separator="\n", strip=True)
            
            if not text or len(text.strip()) < 10:
                raise ValidationError("URL contains no extractable text")
            
        except requests.RequestException as e:
            logger.error(f"Failed to fetch URL {url}: {e}")
            raise ExternalServiceError(f"Failed to fetch URL: {str(e)}", service="url_fetch")
        except Exception as e:
            logger.error(f"Failed to process URL {url}: {e}")
            raise ValidationError(f"Failed to process URL: {str(e)}")
        
        # Create document
        document = Document(
            chatbox_id=chatbox_id,
            source_type=DocumentType.URL,
            source_name=url,
            source_url=url,
            raw_content=text,
        )
        document = await self.document_repo.create(document)
        
        # Chunk and embed (reuse logic from ingest_text)
        chunks_text = self.chunking_service.chunk_text(text)
        
        if not chunks_text:
            logger.warning("No chunks created from URL content")
            return document, 0
        
        embeddings = await self.embedding_service.embed_texts(chunks_text)
        
        chunks = []
        for i, (chunk_text, embedding) in enumerate(zip(chunks_text, embeddings)):
            chunk = Chunk(
                document_id=document.id,
                chatbox_id=chatbox_id,
                content=chunk_text,
                chunk_index=i,
                embedding=embedding,
            )
            chunks.append(chunk)
        
        await self.chunk_repo.create_many(chunks)
        
        logger.info(f"Created document {document.id} from URL with {len(chunks)} chunks")
        return document, len(chunks)
    
    async def ingest_file(
        self,
        chatbox_id: int,
        filename: str,
        content: bytes,
        mime_type: Optional[str] = None,
    ) -> tuple[Document, int]:
        """
        Ingest uploaded file: extract text, chunk, embed, and store.
        
        TODO: Add support for more file types:
        - PDF: PyPDF2 or pdfplumber
        - DOCX: python-docx
        - XLSX: openpyxl
        
        For now: support plain text and basic PDF.
        """
        logger.info(f"Ingesting file {filename} for chatbox {chatbox_id}")
        
        # Extract text based on file type
        text = ""
        
        if mime_type == "text/plain" or filename.endswith(".txt"):
            text = content.decode("utf-8", errors="ignore")
        
        elif mime_type == "application/pdf" or filename.endswith(".pdf"):
            # TODO: Implement PDF extraction using PyPDF2 or pdfplumber
            # For now, placeholder
            text = "[PDF content - TODO: implement PDF extraction]"
            logger.warning("PDF extraction not yet implemented. Using placeholder.")
        
        else:
            raise ValidationError(f"Unsupported file type: {mime_type or 'unknown'}")
        
        if not text or len(text.strip()) < 10:
            raise ValidationError("File contains no extractable text")
        
        # Create document
        document = Document(
            chatbox_id=chatbox_id,
            source_type=DocumentType.FILE,
            source_name=filename,
            raw_content=text,
            file_size_bytes=len(content),
            mime_type=mime_type,
        )
        document = await self.document_repo.create(document)
        
        # Chunk and embed
        chunks_text = self.chunking_service.chunk_text(text)
        
        if not chunks_text:
            logger.warning("No chunks created from file")
            return document, 0
        
        embeddings = await self.embedding_service.embed_texts(chunks_text)
        
        chunks = []
        for i, (chunk_text, embedding) in enumerate(zip(chunks_text, embeddings)):
            chunk = Chunk(
                document_id=document.id,
                chatbox_id=chatbox_id,
                content=chunk_text,
                chunk_index=i,
                embedding=embedding,
            )
            chunks.append(chunk)
        
        await self.chunk_repo.create_many(chunks)
        
        logger.info(f"Created document {document.id} from file with {len(chunks)} chunks")
        return document, len(chunks)
