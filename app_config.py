from __future__ import annotations

import os
from dataclasses import dataclass

from dotenv import load_dotenv


@dataclass(frozen=True)
class Settings:
    api_key: str
    show_reasoning: bool
    model: str
    timeout: float


def load_settings() -> Settings:
    load_dotenv()  # читает .env из текущей директории/родителей

    api_key = os.getenv("AMBIENT_API_KEY")
    if not api_key:
        raise RuntimeError("AMBIENT_API_KEY not found in env/.env")

    show_reasoning = os.getenv("SHOW_REASONING", "0").lower() in ("1", "true", "yes", "y", "on")

    # можно тоже вынести в .env при желании
    model = os.getenv("AMBIENT_MODEL", "zai-org/GLM-4.6")
    timeout = float(os.getenv("AMBIENT_TIMEOUT", "60"))

    return Settings(
        api_key=api_key,
        show_reasoning=show_reasoning,
        model=model,
        timeout=timeout,
    )
