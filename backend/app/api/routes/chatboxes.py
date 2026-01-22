"""Chatbox CRUD endpoints."""

from fastapi import APIRouter, Depends, status

from app.core.exceptions import ValidationError
from app.schemas.chatbox import (
    ChatboxCreate,
    ChatboxUpdate,
    ChatboxResponse,
    ChatboxListResponse,
)
from app.models.chatbox import Chatbox
from app.repositories.chatbox_repository import ChatboxRepository
from app.api.dependencies import (
    get_chatbox_repo,
    verify_api_key,
    get_current_org_id,
)


router = APIRouter(prefix="/v1/chatboxes", tags=["chatboxes"])


@router.post(
    "",
    response_model=ChatboxResponse,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(verify_api_key)],
)
async def create_chatbox(
    data: ChatboxCreate,
    org_id: int = Depends(get_current_org_id),
    repo: ChatboxRepository = Depends(get_chatbox_repo),
) -> ChatboxResponse:
    """
    Create a new chatbox.
    
    Pro/Enterprise plans should set enforce_allowed_domains=True
    and provide allowed_domains.
    """
    # Validate allowed domains requirement
    if data.enforce_allowed_domains and not data.allowed_domains:
        raise ValidationError(
            "allowed_domains is required when enforce_allowed_domains is True"
        )
    
    chatbox = Chatbox(
        organization_id=org_id,
        name=data.name,
        description=data.description,
        allowed_domains=data.allowed_domains,
        enforce_allowed_domains=data.enforce_allowed_domains,
    )
    
    chatbox = await repo.create(chatbox)
    return ChatboxResponse.from_orm(chatbox)


@router.get(
    "",
    response_model=ChatboxListResponse,
    dependencies=[Depends(verify_api_key)],
)
async def list_chatboxes(
    org_id: int = Depends(get_current_org_id),
    repo: ChatboxRepository = Depends(get_chatbox_repo),
    limit: int = 100,
    offset: int = 0,
) -> ChatboxListResponse:
    """List all chatboxes for the organization."""
    chatboxes = await repo.list_by_organization(org_id, limit=limit, offset=offset)
    total = await repo.count_by_organization(org_id)
    
    return ChatboxListResponse(
        chatboxes=[ChatboxResponse.from_orm(cb) for cb in chatboxes],
        total=total,
    )


@router.get(
    "/{chatbox_id}",
    response_model=ChatboxResponse,
    dependencies=[Depends(verify_api_key)],
)
async def get_chatbox(
    chatbox_id: int,
    repo: ChatboxRepository = Depends(get_chatbox_repo),
) -> ChatboxResponse:
    """Get a specific chatbox by ID."""
    chatbox = await repo.get_by_id(chatbox_id)
    return ChatboxResponse.from_orm(chatbox)


@router.patch(
    "/{chatbox_id}",
    response_model=ChatboxResponse,
    dependencies=[Depends(verify_api_key)],
)
async def update_chatbox(
    chatbox_id: int,
    data: ChatboxUpdate,
    repo: ChatboxRepository = Depends(get_chatbox_repo),
) -> ChatboxResponse:
    """Update a chatbox."""
    chatbox = await repo.get_by_id(chatbox_id)
    
    # Update fields if provided
    if data.name is not None:
        chatbox.name = data.name
    if data.description is not None:
        chatbox.description = data.description
    if data.allowed_domains is not None:
        chatbox.allowed_domains = data.allowed_domains
    if data.enforce_allowed_domains is not None:
        chatbox.enforce_allowed_domains = data.enforce_allowed_domains
    
    # Validate
    if chatbox.enforce_allowed_domains and not chatbox.allowed_domains:
        raise ValidationError(
            "allowed_domains is required when enforce_allowed_domains is True"
        )
    
    chatbox = await repo.update(chatbox)
    return ChatboxResponse.from_orm(chatbox)
