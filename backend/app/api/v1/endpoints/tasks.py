import uuid

from fastapi import APIRouter, Query, status

from app.api.v1.dependencies import CurrentUserDep, SessionDep
from app.schemas.task import TaskCreate, TaskRead, TaskUpdate
from app.services.task_service import TaskService

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.get("", response_model=list[TaskRead])
async def list_tasks(
    session: SessionDep,
    current_user: CurrentUserDep,
    board_id: uuid.UUID | None = Query(default=None),
) -> list[TaskRead]:
    service = TaskService(session)
    return await service.list_tasks(current_user.id, board_id)


@router.post("", response_model=TaskRead, status_code=status.HTTP_201_CREATED)
async def create_task(
    data: TaskCreate, session: SessionDep, current_user: CurrentUserDep
) -> TaskRead:
    service = TaskService(session)
    return await service.create_task(current_user.id, data)


@router.get("/{task_id}", response_model=TaskRead)
async def get_task(
    task_id: uuid.UUID, session: SessionDep, current_user: CurrentUserDep
) -> TaskRead:
    service = TaskService(session)
    return await service.get_task(task_id, current_user.id)


@router.patch("/{task_id}", response_model=TaskRead)
async def update_task(
    task_id: uuid.UUID,
    data: TaskUpdate,
    session: SessionDep,
    current_user: CurrentUserDep,
) -> TaskRead:
    service = TaskService(session)
    return await service.update_task(task_id, current_user.id, data)


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(
    task_id: uuid.UUID, session: SessionDep, current_user: CurrentUserDep
) -> None:
    service = TaskService(session)
    await service.delete_task(task_id, current_user.id)
