from __future__ import annotations

from ambient import AmbientClient
from app.tasks.presets import PRESET_HELLO, preset_messages


def run_chat_hello(c: AmbientClient, model: str) -> str:
    resp = c.chat(model=model, messages=preset_messages(PRESET_HELLO))
    return resp["choices"][0]["message"]["content"]
