import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from app.models.chat import ChatRole


class ChatMessageCreate(BaseModel):
    content: str = Field(min_length=1, max_length=10000)


class ChatRequest(BaseModel):
    message: str = Field(min_length=1, max_length=10000)
    session_id: uuid.UUID | None = None


class ChatMessageRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    session_id: uuid.UUID
    role: ChatRole
    content: str
    created_at: datetime


class ChatSessionRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    user_id: uuid.UUID
    title: str
    created_at: datetime
    updated_at: datetime


class ChatResponse(BaseModel):
    session_id: uuid.UUID
    message: ChatMessageRead
    reply: ChatMessageRead
