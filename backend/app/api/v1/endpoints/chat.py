from fastapi import APIRouter

from app.api.v1.dependencies import CurrentUserDep, SessionDep
from app.schemas.chat import ChatRequest, ChatResponse, ChatSessionRead
from app.services.ai.agent import ChatAgent

router = APIRouter(prefix="/chat", tags=["chat"])


@router.get("/sessions", response_model=list[ChatSessionRead])
async def list_sessions(session: SessionDep, current_user: CurrentUserDep) -> list[ChatSessionRead]:
    from sqlmodel import select

    from app.models.chat import ChatSession

    result = await session.execute(
        select(ChatSession)
        .where(ChatSession.user_id == current_user.id)
        .order_by(ChatSession.updated_at.desc())
    )
    return list(result.scalars().all())


@router.post("", response_model=ChatResponse)
async def send_message(
    data: ChatRequest, session: SessionDep, current_user: CurrentUserDep
) -> ChatResponse:
    agent = ChatAgent(session, current_user.id)
    chat_session, user_msg, reply = await agent.run(data.message, data.session_id)
    return ChatResponse(session_id=chat_session.id, message=user_msg, reply=reply)
