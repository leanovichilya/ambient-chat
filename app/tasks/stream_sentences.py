from __future__ import annotations

from typing import Tuple

from ambient import AmbientClient, ChatMessage
from app.prompts import SYSTEM_EN_NO_COMMENTARY, USER_3_SHORT_SENTENCES
from app.tasks.stream_chat import stream_chat_collected, stream_chat_live


def run_stream_sentences(
        c: AmbientClient,
        model: str,
        collect_reasoning: bool,
) -> Tuple[str, str]:
    messages = [
        ChatMessage(role="system", content=SYSTEM_EN_NO_COMMENTARY),
        ChatMessage(role="user", content=USER_3_SHORT_SENTENCES),
    ]
    return stream_chat_collected(c, model, messages, collect_reasoning)


def run_stream_sentences_live(
        c: AmbientClient,
        model: str,
        collect_reasoning: bool,
        print_reasoning: bool = False,
) -> Tuple[str, str]:
    messages = [
        ChatMessage(role="system", content=SYSTEM_EN_NO_COMMENTARY),
        ChatMessage(role="user", content=USER_3_SHORT_SENTENCES),
    ]
    return stream_chat_live(
        c,
        model,
        messages,
        collect_reasoning=collect_reasoning,
        print_reasoning=print_reasoning,
    )
