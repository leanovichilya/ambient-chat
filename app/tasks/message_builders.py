from __future__ import annotations

from typing import List, Optional

from ambient import ChatMessage


def build_messages(*, system: Optional[str], user: str) -> List[ChatMessage]:
    """Build a minimal OpenAI-style messages list from system + user prompts."""
    messages: List[ChatMessage] = []
    if system:
        messages.append(ChatMessage(role="system", content=system))
    messages.append(ChatMessage(role="user", content=user))
    return messages
