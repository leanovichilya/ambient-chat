from __future__ import annotations

from typing import Dict, List, Tuple

from ambient import ChatMessage
from app.prompts import (
    SYSTEM_EN,
    SYSTEM_EN_NO_COMMENTARY,
    USER_HELLO,
    USER_3_SHORT_SENTENCES,
)
from app.tasks.message_builders import build_messages

PRESET_HELLO = "hello"
PRESET_3_SHORT_SENTENCES = "3_short_sentences"

_PRESETS: Dict[str, Tuple[str, str]] = {
    PRESET_HELLO: (SYSTEM_EN, USER_HELLO),
    PRESET_3_SHORT_SENTENCES: (SYSTEM_EN_NO_COMMENTARY, USER_3_SHORT_SENTENCES),
}


def preset_messages(name: str) -> List[ChatMessage]:
    """Return a fresh messages list for a named preset."""
    system_prompt, user_prompt = _PRESETS[name]
    return build_messages(system=system_prompt, user=user_prompt)
