"""Repository for Chatbox operations."""

from typing import Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.chatbox import Chatbox
from app.core.exceptions import NotFoundError


class ChatboxRepository:
    """Handles database operations for Chatbox."""
    
    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def create(self, chatbox: Chatbox) -> Chatbox:
        """Create a new chatbox."""
        self.session.add(chatbox)
        await self.session.commit()
        await self.session.refresh(chatbox)
        return chatbox
    
    async def get_by_id(self, chatbox_id: int) -> Chatbox:
        """Get chatbox by ID or raise NotFoundError."""
        result = await self.session.execute(
            select(Chatbox).where(Chatbox.id == chatbox_id)
        )
        chatbox = result.scalar_one_or_none()
        
        if not chatbox:
            raise NotFoundError(f"Chatbox with id {chatbox_id} not found")
        
        return chatbox
    
    async def get_by_id_optional(self, chatbox_id: int) -> Optional[Chatbox]:
        """Get chatbox by ID, return None if not found."""
        result = await self.session.execute(
            select(Chatbox).where(Chatbox.id == chatbox_id)
        )
        return result.scalar_one_or_none()
    
    async def list_by_organization(self, org_id: int, limit: int = 100, offset: int = 0) -> list[Chatbox]:
        """List chatboxes for an organization."""
        result = await self.session.execute(
            select(Chatbox)
            .where(Chatbox.organization_id == org_id)
            .limit(limit)
            .offset(offset)
        )
        return list(result.scalars().all())
    
    async def count_by_organization(self, org_id: int) -> int:
        """Count chatboxes for an organization."""
        from sqlalchemy import func
        result = await self.session.execute(
            select(func.count(Chatbox.id)).where(Chatbox.organization_id == org_id)
        )
        return result.scalar() or 0
    
    async def update(self, chatbox: Chatbox) -> Chatbox:
        """Update a chatbox."""
        await self.session.commit()
        await self.session.refresh(chatbox)
        return chatbox
    
    async def delete(self, chatbox: Chatbox) -> None:
        """Delete a chatbox."""
        await self.session.delete(chatbox)
        await self.session.commit()
