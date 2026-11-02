import uuid

from fastapi import APIRouter, status

from app.api.v1.dependencies import CurrentUserDep, SessionDep
from app.schemas.board import BoardCreate, BoardRead, BoardUpdate
from app.services.board_service import BoardService

router = APIRouter(prefix="/boards", tags=["boards"])


@router.get("", response_model=list[BoardRead])
async def list_boards(session: SessionDep, current_user: CurrentUserDep):
    service = BoardService(session)
    return await service.list_boards(current_user.id)


@router.post("", response_model=BoardRead, status_code=status.HTTP_201_CREATED)
async def create_board(
    data: BoardCreate, session: SessionDep, current_user: CurrentUserDep
):
    service = BoardService(session)
    return await service.create_board(current_user.id, data)


@router.get("/{board_id}", response_model=BoardRead)
async def get_board(
    board_id: uuid.UUID, session: SessionDep, current_user: CurrentUserDep
):
    service = BoardService(session)
    return await service.get_board(board_id, current_user.id)


@router.patch("/{board_id}", response_model=BoardRead)
async def update_board(
    board_id: uuid.UUID,
    data: BoardUpdate,
    session: SessionDep,
    current_user: CurrentUserDep,
):
    service = BoardService(session)
    return await service.update_board(board_id, current_user.id, data)


@router.delete("/{board_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_board(
    board_id: uuid.UUID, session: SessionDep, current_user: CurrentUserDep
):
    service = BoardService(session)
    await service.delete_board(board_id, current_user.id)
