from __future__ import annotations

from ambient import AmbientClient
from app.tasks.presets import messages_hello


def run_chat_hello(c: AmbientClient, model: str) -> str:
    resp = c.chat(model=model, messages=messages_hello())
    return resp["choices"][0]["message"]["content"]
