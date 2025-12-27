from __future__ import annotations

from typing import Any, Dict


def set_if_not_none(d: Dict[str, Any], k: str, v: Any) -> None:
    if v is not None:
        d[k] = v
