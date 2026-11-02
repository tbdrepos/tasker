import uuid
from datetime import UTC, datetime
from enum import Enum

from sqlmodel import Field, SQLModel


class TaskStatus(str, Enum):
    TODO = "todo"
    DOING = "doing"
    DONE = "done"


class TaskPriority(str, Enum):
    IMPORTANT = "important"
    NORMAL = "normal"
    TRIVIAL = "trivial"


class Task(SQLModel, table=True):
    __tablename__ = "tasks"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    user_id: uuid.UUID = Field(foreign_key="users.id", index=True)
    board_id: uuid.UUID | None = Field(default=None, foreign_key="boards.id", index=True)
    title: str = Field(max_length=200)
    description: str = Field(default="", max_length=2000)
    priority: TaskPriority = Field(default=TaskPriority.NORMAL)
    status: TaskStatus = Field(default=TaskStatus.TODO)
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
