import json
import uuid
from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from app.models.board import Board
from app.models.task import Task
from app.schemas.task import TaskCreate, TaskUpdate
from app.services.task_service import TaskService

TOOL_DEFINITIONS: list[dict[str, Any]] = [
    {
        "type": "function",
        "function": {
            "name": "list_tasks",
            "description": "List all tasks for the current user, optionally filtered by board.",
            "parameters": {
                "type": "object",
                "properties": {
                    "board_id": {
                        "type": "string",
                        "description": "Optional board UUID to filter tasks.",
                    }
                },
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "create_task",
            "description": "Create a new task for the current user.",
            "parameters": {
                "type": "object",
                "properties": {
                    "title": {"type": "string"},
                    "description": {"type": "string"},
                    "priority": {
                        "type": "string",
                        "enum": ["important", "normal", "trivial"],
                    },
                    "status": {
                        "type": "string",
                        "enum": ["todo", "doing", "done"],
                    },
                    "board_id": {"type": "string"},
                },
                "required": ["title"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "update_task",
            "description": "Update an existing task by ID.",
            "parameters": {
                "type": "object",
                "properties": {
                    "task_id": {"type": "string"},
                    "title": {"type": "string"},
                    "description": {"type": "string"},
                    "priority": {
                        "type": "string",
                        "enum": ["important", "normal", "trivial"],
                    },
                    "status": {
                        "type": "string",
                        "enum": ["todo", "doing", "done"],
                    },
                },
                "required": ["task_id"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "list_boards",
            "description": "List all boards for the current user.",
            "parameters": {"type": "object", "properties": {}},
        },
    },
]


class AgentTools:
    def __init__(self, session: AsyncSession, user_id: uuid.UUID) -> None:
        self.session = session
        self.user_id = user_id
        self.task_service = TaskService(session)

    async def execute(self, name: str, arguments: dict[str, Any]) -> str:
        handler = getattr(self, f"_tool_{name}", None)
        if handler is None:
            return json.dumps({"error": f"Unknown tool: {name}"})
        return await handler(arguments)

    async def _tool_list_tasks(self, arguments: dict[str, Any]) -> str:
        board_id = arguments.get("board_id")
        parsed_board_id = uuid.UUID(board_id) if board_id else None
        tasks = await self.task_service.list_tasks(self.user_id, parsed_board_id)
        payload = [
            {
                "id": str(task.id),
                "title": task.title,
                "status": task.status.value,
                "priority": task.priority.value,
            }
            for task in tasks
        ]
        return json.dumps(payload)

    async def _tool_create_task(self, arguments: dict[str, Any]) -> str:
        data = TaskCreate(
            title=arguments["title"],
            description=arguments.get("description", ""),
            priority=arguments.get("priority", "normal"),
            status=arguments.get("status", "todo"),
            board_id=uuid.UUID(arguments["board_id"]) if arguments.get("board_id") else None,
        )
        task = await self.task_service.create_task(self.user_id, data)
        return json.dumps({"id": str(task.id), "title": task.title})

    async def _tool_update_task(self, arguments: dict[str, Any]) -> str:
        task_id = uuid.UUID(arguments["task_id"])
        data = TaskUpdate(**{k: v for k, v in arguments.items() if k != "task_id" and v is not None})
        task = await self.task_service.update_task(task_id, self.user_id, data)
        return json.dumps({"id": str(task.id), "status": task.status.value})

    async def _tool_list_boards(self, _arguments: dict[str, Any]) -> str:
        result = await self.session.execute(
            select(Board).where(Board.user_id == self.user_id).order_by(Board.created_at)
        )
        boards = result.scalars().all()
        payload = [{"id": str(board.id), "title": board.title} for board in boards]
        return json.dumps(payload)
