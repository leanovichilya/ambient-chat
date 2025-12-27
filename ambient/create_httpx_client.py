from __future__ import annotations

import inspect
from typing import Dict, Optional, Union

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
    """
    Совместимо с разными версиями httpx:
    - httpx>=0.28: использует proxy=... или mounts=...
    - httpx<0.28: может поддерживать proxies=...
    """
    kwargs = dict(
        base_url=base_url,
        timeout=httpx.Timeout(timeout),
        verify=verify,
        http2=http2,
        headers=headers,
    )

    sig = inspect.signature(httpx.Client.__init__)
    params = sig.parameters

    if proxies is None:
        return httpx.Client(**kwargs)

    # 1) Один прокси строкой
    if isinstance(proxies, str):
        if "proxy" in params:  # httpx>=0.28
            kwargs["proxy"] = proxies
        elif "proxies" in params:  # старые версии
            kwargs["proxies"] = proxies
        else:
            # fallback: можно оставить только env vars HTTP(S)_PROXY
            pass
        return httpx.Client(**kwargs)

    # 2) Прокси словарём
    # Разрешаем форматы: {"http": "...", "https": "..."} или {"http://": "...", "https://": "..."}
    http_proxy = proxies.get("http") or proxies.get("http://")
    https_proxy = proxies.get("https") or proxies.get("https://")

    # httpx>=0.28 рекомендует mounts для разных прокси :contentReference[oaicite:1]{index=1}
    if "mounts" in params:
        proxy_mounts = {}
        if http_proxy:
            proxy_mounts["http://"] = httpx.HTTPTransport(proxy=http_proxy)
        if https_proxy:
            proxy_mounts["https://"] = httpx.HTTPTransport(proxy=https_proxy)
        kwargs["mounts"] = proxy_mounts
        return httpx.Client(**kwargs)

    # старые версии могли принимать proxies=dict
    if "proxies" in params:
        # нормализуем ключи под requests/httpx-старый стиль
        normalized = {}
        if http_proxy:
            normalized["http://"] = http_proxy
        if https_proxy:
            normalized["https://"] = https_proxy
        kwargs["proxies"] = normalized
        return httpx.Client(**kwargs)

    return httpx.Client(**kwargs)
