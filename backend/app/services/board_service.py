import uuid

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from app.models.board import Board
from app.schemas.board import BoardCreate, BoardUpdate


class BoardService:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def list_boards(self, user_id: uuid.UUID) -> list[Board]:
        result = await self.session.execute(
            select(Board).where(Board.user_id == user_id).order_by(Board.created_at)
        )
        return list(result.scalars().all())

    async def get_board(self, board_id: uuid.UUID, user_id: uuid.UUID) -> Board:
        board = await self.session.get(Board, board_id)
        if board is None or board.user_id != user_id:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Board not found")
        return board

    async def create_board(self, user_id: uuid.UUID, data: BoardCreate) -> Board:
        board = Board(user_id=user_id, title=data.title, description=data.description)
        self.session.add(board)
        await self.session.commit()
        await self.session.refresh(board)
        return board

    async def update_board(
        self, board_id: uuid.UUID, user_id: uuid.UUID, data: BoardUpdate
    ) -> Board:
        board = await self.get_board(board_id, user_id)
        update_data = data.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(board, key, value)
        self.session.add(board)
        await self.session.commit()
        await self.session.refresh(board)
        return board

    async def delete_board(self, board_id: uuid.UUID, user_id: uuid.UUID) -> None:
        board = await self.get_board(board_id, user_id)
        await self.session.delete(board)
        await self.session.commit()
