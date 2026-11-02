import uuid
from datetime import UTC, datetime

from sqlmodel import Field, SQLModel


class Board(SQLModel, table=True):
    __tablename__ = "boards"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    user_id: uuid.UUID = Field(foreign_key="users.id", index=True)
    title: str = Field(max_length=200)
    description: str = Field(default="", max_length=2000)
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
