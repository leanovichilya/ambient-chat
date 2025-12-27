from __future__ import annotations

from typing import List, Tuple

from ambient import AmbientClient, ChatMessage


def stream_chat_collected(
        c: AmbientClient,
        model: str,
        messages: List[ChatMessage],
        collect_reasoning: bool,
) -> Tuple[str, str]:
    """Stream response, collect and return (final_text, reasoning_text)."""
    final_parts: list[str] = []
    reasoning_parts: list[str] = []

    for chunk in c.chat_stream(model=model, messages=messages):
        delta = chunk.get("choices", [{}])[0].get("delta", {})

        if collect_reasoning:
            rc = delta.get("reasoning_content")
            if rc:
                reasoning_parts.append(rc)

        content = delta.get("content")
        if content:
            final_parts.append(content)

    return "".join(final_parts), "".join(reasoning_parts)


def stream_chat_live(
        c: AmbientClient,
        model: str,
        messages: List[ChatMessage],
        collect_reasoning: bool,
        print_reasoning: bool = False,
) -> Tuple[str, str]:
    """Print final answer as it streams in and return (final_text, reasoning_text)."""
    final_parts: list[str] = []
    reasoning_parts: list[str] = []

    for chunk in c.chat_stream(model=model, messages=messages):
        delta = chunk.get("choices", [{}])[0].get("delta", {})

        rc = delta.get("reasoning_content")
        if rc:
            if collect_reasoning:
                reasoning_parts.append(rc)
            if print_reasoning:
                print(rc, end="", flush=True)

        content = delta.get("content")
        if content:
            final_parts.append(content)
            print(content, end="", flush=True)

    print()
    return "".join(final_parts), "".join(reasoning_parts)
