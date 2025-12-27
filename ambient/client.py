from __future__ import annotations

from typing import Any, Dict, Generator, List, Optional, Union

from .endpoints.chat import chat as chat_fn
from .endpoints.chat_stream import chat_stream as chat_stream_fn
from .http.create_client import create_httpx_client
from .types import ChatMessage


class AmbientClient:
    def __init__(
            self,
            api_key: str,
            base_url: str = "https://api.ambient.xyz/v1",
            timeout: float = 60.0,
            proxies: Optional[Union[str, Dict[str, str]]] = None,
            verify: bool = True,
            http2: bool = True,
    ) -> None:
        self.base_url = base_url.rstrip("/")

        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        }

        self._client = create_httpx_client(
            base_url=self.base_url,
            timeout=timeout,
            proxies=proxies,
            verify=verify,
            http2=http2,
            headers=headers,
        )

    def close(self) -> None:
        self._client.close()

    def __enter__(self) -> "AmbientClient":
        return self

    def __exit__(self, exc_type, exc, tb) -> None:
        self.close()

    def chat(
            self,
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
        return chat_fn(
            self._client,
            model=model,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
            top_p=top_p,
            stop=stop,
            presence_penalty=presence_penalty,
            frequency_penalty=frequency_penalty,
            seed=seed,
            user=user,
            extra=extra,
        )

    def chat_stream(
            self,
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
        return chat_stream_fn(
            self._client,
            model=model,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
            top_p=top_p,
            stop=stop,
            presence_penalty=presence_penalty,
            frequency_penalty=frequency_penalty,
            seed=seed,
            user=user,
            extra=extra,
        )
