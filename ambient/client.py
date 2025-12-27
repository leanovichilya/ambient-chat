from __future__ import annotations

from typing import Any, Dict, Generator, List, Optional, Union

import httpx

from .chat import chat as chat_fn
from .chat_stream import chat_stream as chat_stream_fn
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

        client_kwargs: Dict[str, Any] = {
            "base_url": self.base_url,
            "timeout": httpx.Timeout(timeout),
            "verify": verify,
            "http2": http2,
            "headers": {
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
                "Accept": "text/event-stream",
            },
        }

        # httpx>=0.28: proxies= удалён, используем proxy= или mounts=
        # proxy=  -> один прокси на всё
        # mounts= -> разные прокси для http:// и https://
        if proxies:
            if isinstance(proxies, str):
                client_kwargs["proxy"] = proxies  # httpx docs: proxy=... :contentReference[oaicite:1]{index=1}
            elif isinstance(proxies, dict):
                http_proxy = proxies.get("http") or proxies.get("http://")
                https_proxy = proxies.get("https") or proxies.get("https://")

                mounts: Dict[str, httpx.BaseTransport] = {}
                if http_proxy:
                    mounts["http://"] = httpx.HTTPTransport(proxy=http_proxy)
                if https_proxy:
                    mounts["https://"] = httpx.HTTPTransport(proxy=https_proxy)

                # если пользователь передал dict, но он пустой/без ключей — просто не задаём mounts
                if mounts:
                    client_kwargs[
                        "mounts"] = mounts  # httpx: mounts={"http://": ...} :contentReference[oaicite:2]{index=2}

        self._client = httpx.Client(**client_kwargs)

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
