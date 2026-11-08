import uuid
from datetime import UTC, datetime
from typing import Any

from fastapi import HTTPException, status
from ollama import AsyncClient, Message, ResponseError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import col, select

from app.core.config import get_settings
from app.models.chat import ChatMessage, ChatRole, ChatSession
from app.services.ai.prompts import SYSTEM_PROMPT, TOOL_INSTRUCTIONS
from app.services.ai.tools import TOOL_DEFINITIONS, AgentTools

settings = get_settings()

OLLAMA_TIMEOUT_SECONDS = 120.0
OLLAMA_THINK = False
MAX_TOOL_ROUNDS = 5


class ChatAgent:
    def __init__(self, db_session: AsyncSession, user_id: uuid.UUID) -> None:
        self.db_session = db_session
        self.user_id = user_id
        self.tools = AgentTools(db_session, user_id)
        self.client = AsyncClient(
            host=settings.ollama_host,
            timeout=OLLAMA_TIMEOUT_SECONDS,
        )

    async def get_or_create_session(
        self, chat_session_id: uuid.UUID | None
    ) -> ChatSession:
        """
        Retrieve an existing chat session or create a new one if not found.

        Args:
            chat_session_id: Optional UUID of the chat session to retrieve.
                             If None, a new session will be created.

        Returns:
            The retrieved or newly created ChatSession object.

        Raises:
            HTTPException: If the specified session is not found or belongs
                          to a different user (404 error).
        """
        if chat_session_id is not None:
            chat_session = await self.db_session.get(ChatSession, chat_session_id)
            if chat_session is None or chat_session.user_id != self.user_id:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Chat session not found",
                )
            return chat_session

        chat_session = ChatSession(user_id=self.user_id)
        self.db_session.add(chat_session)
        await self.db_session.commit()
        await self.db_session.refresh(chat_session)
        return chat_session

    async def list_messages(self, chat_session_id: uuid.UUID) -> list[ChatMessage]:
        """List the chat messages of the provided session"""
        result = await self.db_session.execute(
            select(ChatMessage)
            .where(ChatMessage.session_id == chat_session_id)
            .order_by(col(ChatMessage.created_at))
        )
        return list(result.scalars().all())

    async def save_message(
        self, chat_session_id: uuid.UUID, role: ChatRole, content: str
    ) -> ChatMessage:
        """
        Save a chat message to the database and update the session's timestamp.

        Args:
            chat_session_id: The UUID of the chat session.
            role: The role of the message sender (e.g., USER, ASSISTANT).
            content: The text content of the message.

        Returns:
            The created ChatMessage object.
        """
        message = ChatMessage(session_id=chat_session_id, role=role, content=content)
        self.db_session.add(message)

        chat_session = await self.db_session.get(ChatSession, chat_session_id)
        if chat_session is not None:
            chat_session.updated_at = datetime.now(UTC)
            self.db_session.add(chat_session)

        await self.db_session.commit()
        await self.db_session.refresh(message)
        return message

    async def _chat(self, messages: list[dict[str, Any] | Message]) -> Message:
        """Call Ollama and translate common failures into HTTP errors.

        Args: a list of messages to send to the model.

        Returns: the model response message.
        """
        try:
            response = await self.client.chat(
                model=settings.ollama_model,
                messages=messages,
                tools=TOOL_DEFINITIONS,
                think=OLLAMA_THINK,
            )
        except ConnectionError as exc:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail=f"Cannot reach Ollama at {settings.ollama_host}. Is it running?",
            ) from exc
        except ResponseError as exc:
            if exc.status_code == status.HTTP_404_NOT_FOUND:
                detail = (
                    f"Model '{settings.ollama_model}' not found. "
                    f"Run: ollama pull {settings.ollama_model}"
                )
            else:
                detail = f"Ollama error: {exc.error}"
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY, detail=detail
            ) from exc

        return response.message

    async def run(
        self, user_message: str, chat_session_id: uuid.UUID | None = None
    ) -> tuple[ChatSession, ChatMessage, ChatMessage]:
        """Execute a chat conversation flow with the LLM and tools.

        Args:
            user_message: The user's input message to process.
            chat_session_id: Optional session ID to use or create a new one.

        Returns:
            A tuple containing (chat_session, user_msg, reply) where:
            - chat_session: The current chat session object
            - user_msg: The saved user message for this conversation
            - reply: The assistant's response message

        """
        chat_session = await self.get_or_create_session(chat_session_id)
        user_msg = await self.save_message(chat_session.id, ChatRole.USER, user_message)

        history = await self.list_messages(chat_session.id)
        messages: list[dict[str, Any] | Message] = [
            {"role": "system", "content": f"{SYSTEM_PROMPT}\n\n{TOOL_INSTRUCTIONS}"},
            # the * unpacks the list comprehension
            *[{"role": msg.role.value, "content": msg.content} for msg in history],
        ]

        for _ in range(MAX_TOOL_ROUNDS):
            message = await self._chat(messages)

            if message.tool_calls:
                # Ollama returns tool-call arguments as a dict, not a JSON string,
                # and the assistant message can be passed straight back in.
                messages.append(message)
                for call in message.tool_calls:
                    result = await self.tools.execute(
                        call.function.name, dict(call.function.arguments)
                    )
                    # Ollama matches tool results by tool_name rather than tool_call_id.
                    messages.append(
                        {
                            "role": "tool",
                            "tool_name": call.function.name,
                            "content": result,
                        }
                    )
                continue

            reply_content = message.content or "I couldn't generate a response."
            reply = await self.save_message(
                chat_session.id, ChatRole.ASSISTANT, reply_content
            )
            return chat_session, user_msg, reply

        fallback = "I hit the tool-call limit. Please try a simpler request."
        reply = await self.save_message(chat_session.id, ChatRole.ASSISTANT, fallback)
        return chat_session, user_msg, reply
