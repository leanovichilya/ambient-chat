from typing import Optional

import httpx


def format_http_error(r: httpx.Response, body_override: Optional[str] = None) -> str:
    body = body_override if body_override is not None else (r.text or "")
    return f"HTTP {r.status_code} {r.reason_phrase}. Body: {body[:2000]}"
