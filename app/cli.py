from __future__ import annotations

from ambient import AmbientClient
from ambient.errors import AmbientError

from app.config import load_settings
from app.tasks.chat_hello import run_chat_hello
from app.tasks.stream_sentences import run_stream_sentences, run_stream_sentences_live


def run() -> None:
    s = load_settings()

    try:
        with AmbientClient(s.api_key, timeout=s.timeout, proxies=s.proxy) as c:
            text = run_chat_hello(c, s.model)
            print(text)
            print()

            if s.stream_mode == "live":
                final_text, reasoning_text = run_stream_sentences_live(
                    c,
                    s.model,
                    collect_reasoning=s.show_reasoning,
                    print_reasoning=False,  # set True if you want reasoning printed live
                )
                print()  # extra spacing after live output
            else:
                final_text, reasoning_text = run_stream_sentences(
                    c,
                    s.model,
                    collect_reasoning=s.show_reasoning,
                )
                print(final_text)
                print()

            if s.show_reasoning and reasoning_text:
                print("----- REASONING -----")
                print(reasoning_text)

    except AmbientError as e:
        print("AmbientError:", e)
