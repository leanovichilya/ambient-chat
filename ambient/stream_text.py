from __future__ import annotations

from typing import Any, Dict, Generator, Optional


def stream_text(
        chunk: Dict[str, Any],
        *,
        include_reasoning: bool = False,
) -> Generator[str, None, None]:
    """
    Из одного OpenAI-style stream chunk вытаскивает кусочки текста.
    По умолчанию отдаёт только финальный content.
    """
    choice = (chunk.get("choices") or [{}])[0]
    delta: Dict[str, Any] = choice.get("delta") or {}

    if include_reasoning:
        rc: Optional[str] = delta.get("reasoning_content")
        if rc:
            yield rc

    c: Optional[str] = delta.get("content")
    if c:
        yield c
