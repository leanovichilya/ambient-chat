from __future__ import annotations

import json
from typing import Any, Dict, Generator, List, Optional, Union

import httpx

from .errors import AmbientError
from .sse_iter_data_lines import iter_sse_data_lines
from .types import ChatMessage
from .utils_format_http_error import format_http_error
from .utils_set_if_not_none import set_if_not_none


def chat_stream(
        client: httpx.Client,
        *,
        model: str,
        messages: List[ChatMessage],
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        top_p: Optional[float] = None,
        stop: Optional[Union[str, List[str]]] = None,
        presence_penalty: Optional[float] = None,
        frequency_penalty: Optional[float] = None,
        seed: Optional[int] = None,
        user: Optional[str] = None,
        extra: Optional[Dict[str, Any]] = None,
) -> Generator[Dict[str, Any], None, None]:
    payload: Dict[str, Any] = {
        "model": model,
        "messages": [m.__dict__ for m in messages],
        "stream": True,
    }

    set_if_not_none(payload, "temperature", temperature)
    set_if_not_none(payload, "max_tokens", max_tokens)
    set_if_not_none(payload, "top_p", top_p)
    set_if_not_none(payload, "stop", stop)
    set_if_not_none(payload, "presence_penalty", presence_penalty)
    set_if_not_none(payload, "frequency_penalty", frequency_penalty)
    set_if_not_none(payload, "seed", seed)
    set_if_not_none(payload, "user", user)

    if extra:
        payload.update(extra)

    with client.stream("POST", "/chat/completions", json=payload) as r:
        if r.status_code >= 400:
            body = r.read().decode("utf-8", errors="replace")
            raise AmbientError(format_http_error(r, body_override=body))

        for event in iter_sse_data_lines(r.iter_lines()):
            if event == "[DONE]":
                return
            try:
                yield json.loads(event)
            except json.JSONDecodeError:
                continue
