from __future__ import annotations

from ambient import AmbientClient, ChatMessage
from prompts import SYSTEM_EN_NO_COMMENTARY, USER_3_SHORT_SENTENCES


def run_stream_sentences(c: AmbientClient, model: str, show_reasoning: bool) -> None:
    for chunk in c.chat_stream(
            model=model,
            messages=[
                ChatMessage(role="system", content=SYSTEM_EN_NO_COMMENTARY),
                ChatMessage(role="user", content=USER_3_SHORT_SENTENCES),
            ],
    ):
        delta = chunk.get("choices", [{}])[0].get("delta", {})

        if show_reasoning and "reasoning_content" in delta:
            print(delta["reasoning_content"], end="", flush=True)

        if "content" in delta:
            print(delta["content"], end="", flush=True)

    print()
