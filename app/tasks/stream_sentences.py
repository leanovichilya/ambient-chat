from __future__ import annotations

from typing import Tuple

from ambient import AmbientClient, ChatMessage
from app.prompts import SYSTEM_EN_NO_COMMENTARY, USER_3_SHORT_SENTENCES


def run_stream_sentences(
        c: AmbientClient,
        model: str,
        collect_reasoning: bool,
) -> Tuple[str, str]:
    final_parts: list[str] = []
    reasoning_parts: list[str] = []

    for chunk in c.chat_stream(
            model=model,
            messages=[
                ChatMessage(role="system", content=SYSTEM_EN_NO_COMMENTARY),
                ChatMessage(role="user", content=USER_3_SHORT_SENTENCES),
            ],
    ):
        delta = chunk.get("choices", [{}])[0].get("delta", {})

        if collect_reasoning:
            rc = delta.get("reasoning_content")
            if rc:
                reasoning_parts.append(rc)

        content = delta.get("content")
        if content:
            final_parts.append(content)

    return "".join(final_parts), "".join(reasoning_parts)
