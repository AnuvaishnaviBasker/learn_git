from __future__ import annotations

from typing import Any

from pydantic import BaseModel


class ChatHistoryItem(BaseModel):
    role: str
    content: str


class ChatRequest(BaseModel):
    question: str
    chat_history: list[ChatHistoryItem] = []


class ChatResponse(BaseModel):
    answer: str
    details: dict[str, Any] = {}
