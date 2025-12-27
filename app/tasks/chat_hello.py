from __future__ import annotations

from ambient import AmbientClient, ChatMessage
from app.prompts import SYSTEM_EN, USER_HELLO


def run_chat_hello(c: AmbientClient, model: str) -> str:
    resp = c.chat(
        model=model,
        messages=[
            ChatMessage(role="system", content=SYSTEM_EN),
            ChatMessage(role="user", content=USER_HELLO),
        ],
    )
    return resp["choices"][0]["message"]["content"]
