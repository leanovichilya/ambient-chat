from __future__ import annotations

from typing import Generator, Iterable, Union


def iter_sse_data_lines(lines: Iterable[Union[str, bytes]]) -> Generator[str, None, None]:
    for raw in lines:
        if not raw:
            continue

        if isinstance(raw, bytes):
            raw = raw.decode("utf-8", errors="replace")

        raw = raw.strip()
        if raw.startswith("data:"):
            data = raw[len("data:"):].strip()
            if data:
                yield data
