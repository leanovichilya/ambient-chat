from __future__ import annotations

from typing import Tuple

from ambient import AmbientClient
from app.tasks.presets import PRESET_3_SHORT_SENTENCES, preset_messages
from app.tasks.stream_chat import stream_chat_collected, stream_chat_live


def run_stream_sentences(
        c: AmbientClient,
        model: str,
        collect_reasoning: bool,
) -> Tuple[str, str]:
    return stream_chat_collected(
        c,
        model,
        preset_messages(PRESET_3_SHORT_SENTENCES),
        collect_reasoning,
    )


def run_stream_sentences_live(
        c: AmbientClient,
        model: str,
        collect_reasoning: bool,
        print_reasoning: bool = False,
) -> Tuple[str, str]:
    return stream_chat_live(
        c,
        model,
        preset_messages(PRESET_3_SHORT_SENTENCES),
        collect_reasoning=collect_reasoning,
        print_reasoning=print_reasoning,
    )
