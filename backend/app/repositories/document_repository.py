"""Repository for Document operations."""

from typing import Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.document import Document
from app.core.exceptions import NotFoundError


class DocumentRepository:
    """Handles database operations for Document."""
    
    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def create(self, document: Document) -> Document:
        """Create a new document."""
        self.session.add(document)
        await self.session.commit()
        await self.session.refresh(document)
        return document
    
    async def get_by_id(self, document_id: int) -> Document:
        """Get document by ID or raise NotFoundError."""
        result = await self.session.execute(
            select(Document).where(Document.id == document_id)
        )
        document = result.scalar_one_or_none()
        
        if not document:
            raise NotFoundError(f"Document with id {document_id} not found")
        
        return document
    
    async def get_by_id_optional(self, document_id: int) -> Optional[Document]:
        """Get document by ID, return None if not found."""
        result = await self.session.execute(
            select(Document).where(Document.id == document_id)
        )
        return result.scalar_one_or_none()
    
    async def list_by_chatbox(self, chatbox_id: int, limit: int = 100) -> list[Document]:
        """List documents for a chatbox."""
        result = await self.session.execute(
            select(Document)
            .where(Document.chatbox_id == chatbox_id)
            .limit(limit)
        )
        return list(result.scalars().all())
