from __future__ import annotations

from ambient import AmbientClient
from ambient.errors import AmbientError

from app_config import load_settings
from run_chat_hello import run_chat_hello
from run_stream_sentences import run_stream_sentences


def main() -> None:
    s = load_settings()

    try:
        with AmbientClient(s.api_key, timeout=s.timeout) as c:
            # 1) обычный чат
            text = run_chat_hello(c, s.model)
            print(text)
            print()

            # 2) streaming
            run_stream_sentences(c, s.model, s.show_reasoning)

    except AmbientError as e:
        print("AmbientError:", e)


if __name__ == "__main__":
    main()
