from __future__ import annotations

from typing import Any, Dict, List, Optional, Union

import httpx

from .errors import AmbientError
from .types import ChatMessage
from .utils_format_http_error import format_http_error
from .utils_set_if_not_none import set_if_not_none


def chat(
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
) -> Dict[str, Any]:
    payload: Dict[str, Any] = {
        "model": model,
        "messages": [m.__dict__ for m in messages],
        "stream": False,
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

    r = client.post("/chat/completions", json=payload)
    if r.status_code >= 400:
        raise AmbientError(format_http_error(r))

    return r.json()
