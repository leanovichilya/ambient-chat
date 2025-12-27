from __future__ import annotations

from typing import List

from ambient import ChatMessage
from app.prompts import (
    SYSTEM_EN,
    SYSTEM_EN_NO_COMMENTARY,
    USER_HELLO,
    USER_3_SHORT_SENTENCES,
)


def messages_hello() -> List[ChatMessage]:
    return [
        ChatMessage(role="system", content=SYSTEM_EN),
        ChatMessage(role="user", content=USER_HELLO),
    ]


def messages_3_short_sentences() -> List[ChatMessage]:
    return [
        ChatMessage(role="system", content=SYSTEM_EN_NO_COMMENTARY),
        ChatMessage(role="user", content=USER_3_SHORT_SENTENCES),
    ]
