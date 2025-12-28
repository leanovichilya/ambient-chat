from __future__ import annotations

from typing import Any, Dict, Optional, Union

import httpx


def create_httpx_client(
        *,
        base_url: str,
        timeout: float,
        proxies: Optional[Union[str, Dict[str, str]]],
        verify: bool,
        http2: bool,
        headers: Dict[str, str],
) -> httpx.Client:
    client_kwargs: Dict[str, Any] = {
        "base_url": base_url,
        "timeout": httpx.Timeout(timeout),
        "verify": verify,
        "http2": http2,
        "headers": headers,
        "trust_env": False,
    }

    if proxies:
        if isinstance(proxies, str):
            client_kwargs["proxy"] = proxies
        else:
            http_proxy = proxies.get("http") or proxies.get("http://")
            https_proxy = proxies.get("https") or proxies.get("https://")

            mounts: Dict[str, httpx.BaseTransport] = {}
            if http_proxy:
                mounts["http://"] = httpx.HTTPTransport(proxy=http_proxy)
            if https_proxy:
                mounts["https://"] = httpx.HTTPTransport(proxy=https_proxy)

            if mounts:
                client_kwargs["mounts"] = mounts

    return httpx.Client(**client_kwargs)
