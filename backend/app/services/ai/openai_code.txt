import json
import uuid
from datetime import UTC, datetime
from typing import Any

from fastapi import HTTPException, status
from openai import AsyncOpenAI
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from app.core.config import get_settings
from app.models.chat import ChatMessage, ChatRole, ChatSession
from app.services.ai.prompts import SYSTEM_PROMPT, TOOL_INSTRUCTIONS
from app.services.ai.tools import TOOL_DEFINITIONS, AgentTools

settings = get_settings()


class ChatAgent:
    def __init__(self, session: AsyncSession, user_id: uuid.UUID) -> None:
        self.session = session
        self.user_id = user_id
        self.tools = AgentTools(session, user_id)
        self.client = (
            AsyncOpenAI(api_key=settings.openai_api_key) if settings.openai_api_key else None
        )

    async def get_or_create_session(self, session_id: uuid.UUID | None) -> ChatSession:
        if session_id is not None:
            chat_session = await self.session.get(ChatSession, session_id)
            if chat_session is None or chat_session.user_id != self.user_id:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, detail="Chat session not found"
                )
            return chat_session

        chat_session = ChatSession(user_id=self.user_id)
        self.session.add(chat_session)
        await self.session.commit()
        await self.session.refresh(chat_session)
        return chat_session

    async def list_messages(self, session_id: uuid.UUID) -> list[ChatMessage]:
        result = await self.session.execute(
            select(ChatMessage)
            .where(ChatMessage.session_id == session_id)
            .order_by(ChatMessage.created_at)
        )
        return list(result.scalars().all())

    async def save_message(
        self, session_id: uuid.UUID, role: ChatRole, content: str
    ) -> ChatMessage:
        message = ChatMessage(session_id=session_id, role=role, content=content)
        self.session.add(message)

        chat_session = await self.session.get(ChatSession, session_id)
        if chat_session is not None:
            chat_session.updated_at = datetime.now(UTC)
            self.session.add(chat_session)

        await self.session.commit()
        await self.session.refresh(message)
        return message

    async def run(self, user_message: str, session_id: uuid.UUID | None = None) -> tuple[ChatSession, ChatMessage, ChatMessage]:
        chat_session = await self.get_or_create_session(session_id)
        user_msg = await self.save_message(chat_session.id, ChatRole.USER, user_message)

        if self.client is None:
            reply_content = (
                "AI is not configured. Set OPENAI_API_KEY in your environment to enable chat."
            )
            reply = await self.save_message(chat_session.id, ChatRole.ASSISTANT, reply_content)
            return chat_session, user_msg, reply

        history = await self.list_messages(chat_session.id)
        messages: list[dict[str, Any]] = [
            {"role": "system", "content": f"{SYSTEM_PROMPT}\n\n{TOOL_INSTRUCTIONS}"},
            *[{"role": msg.role.value, "content": msg.content} for msg in history],
        ]

        for _ in range(5):
            response = await self.client.chat.completions.create(
                model=settings.openai_model,
                messages=messages,
                tools=TOOL_DEFINITIONS,
            )
            choice = response.choices[0].message

            if choice.tool_calls:
                messages.append(
                    {
                        "role": "assistant",
                        "content": choice.content or "",
                        "tool_calls": [
                            {
                                "id": call.id,
                                "type": "function",
                                "function": {
                                    "name": call.function.name,
                                    "arguments": call.function.arguments,
                                },
                            }
                            for call in choice.tool_calls
                        ],
                    }
                )
                for call in choice.tool_calls:
                    args = json.loads(call.function.arguments or "{}")
                    result = await self.tools.execute(call.function.name, args)
                    messages.append(
                        {
                            "role": "tool",
                            "tool_call_id": call.id,
                            "content": result,
                        }
                    )
                continue

            reply_content = choice.content or "I couldn't generate a response."
            reply = await self.save_message(chat_session.id, ChatRole.ASSISTANT, reply_content)
            return chat_session, user_msg, reply

        fallback = "I hit the tool-call limit. Please try a simpler request."
        reply = await self.save_message(chat_session.id, ChatRole.ASSISTANT, fallback)
        return chat_session, user_msg, reply
