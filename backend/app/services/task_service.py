import uuid

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from app.models.task import Task
from app.schemas.task import TaskCreate, TaskUpdate


class TaskService:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def list_tasks(self, user_id: uuid.UUID, board_id: uuid.UUID | None = None) -> list[Task]:
        query = select(Task).where(Task.user_id == user_id)
        if board_id is not None:
            query = query.where(Task.board_id == board_id)
        query = query.order_by(Task.created_at)
        result = await self.session.execute(query)
        return list(result.scalars().all())

    async def get_task(self, task_id: uuid.UUID, user_id: uuid.UUID) -> Task:
        task = await self.session.get(Task, task_id)
        if task is None or task.user_id != user_id:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
        return task

    async def create_task(self, user_id: uuid.UUID, data: TaskCreate) -> Task:
        task = Task(user_id=user_id, **data.model_dump())
        self.session.add(task)
        await self.session.commit()
        await self.session.refresh(task)
        return task

    async def update_task(
        self, task_id: uuid.UUID, user_id: uuid.UUID, data: TaskUpdate
    ) -> Task:
        task = await self.get_task(task_id, user_id)
        update_data = data.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(task, key, value)
        self.session.add(task)
        await self.session.commit()
        await self.session.refresh(task)
        return task

    async def delete_task(self, task_id: uuid.UUID, user_id: uuid.UUID) -> None:
        task = await self.get_task(task_id, user_id)
        await self.session.delete(task)
        await self.session.commit()
