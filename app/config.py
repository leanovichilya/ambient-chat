from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Optional

from dotenv import load_dotenv


@dataclass(frozen=True)
class Settings:
    api_key: str
    show_reasoning: bool
    model: str
    timeout: float
    stream_mode: str
    proxy: Optional[str]  # None means no proxy


def load_settings() -> Settings:
    load_dotenv()

    api_key = os.getenv("AMBIENT_API_KEY")
    if not api_key:
        raise RuntimeError("AMBIENT_API_KEY not found in env/.env")

    show_reasoning = os.getenv("SHOW_REASONING", "0").lower() in ("1", "true", "yes", "y", "on")
    model = os.getenv("AMBIENT_MODEL", "zai-org/GLM-4.6")
    timeout = float(os.getenv("AMBIENT_TIMEOUT", "60"))

    stream_mode = os.getenv("STREAM_MODE", "collected").strip().lower()
    if stream_mode not in ("live", "collected"):
        stream_mode = "collected"

    use_proxy = os.getenv("USE_PROXY", "0").lower() in ("1", "true", "yes", "y", "on")
    proxy = os.getenv("AMBIENT_PROXY") if use_proxy else None

    return Settings(
        api_key=api_key,
        show_reasoning=show_reasoning,
        model=model,
        timeout=timeout,
        stream_mode=stream_mode,
        proxy=proxy,
    )
