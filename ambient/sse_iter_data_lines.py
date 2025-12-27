from typing import Generator, Iterable, Union


def iter_sse_data_lines(lines: Iterable[Union[str, bytes]]) -> Generator[str, None, None]:
    """
    Extracts 'data: ...' payloads from SSE stream.
    Ignores event:, id:, retry: and blank lines.
    """
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
