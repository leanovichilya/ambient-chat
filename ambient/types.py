from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Union

MessageContent = Union[str, List[Dict[str, Any]]]


@dataclass(frozen=True)
class ChatMessage:
    role: str
    content: MessageContent
