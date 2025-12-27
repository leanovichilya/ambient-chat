import os
from dotenv import load_dotenv

from ambient import AmbientClient, ChatMessage
from ambient.errors import AmbientError
from ambient.stream_text import stream_text

load_dotenv()  # читает .env из текущей директории/родителей

API_KEY = os.getenv("AMBIENT_API_KEY")
if not API_KEY:
    raise RuntimeError("AMBIENT_API_KEY not found in env/.env")

SHOW_REASONING = os.getenv("SHOW_REASONING", "0") in ("1", "true", "True", "yes", "YES")

with AmbientClient(API_KEY, timeout=60.0) as c:
    try:
        resp = c.chat(
            model="zai-org/GLM-4.6",
            messages=[
                ChatMessage(role="system", content="Reply in English."),
                ChatMessage(role="user", content="Hello"),
            ],
        )
        print(resp["choices"][0]["message"]["content"])

        reasoning_parts = []

        for chunk in c.chat_stream(
                model="zai-org/GLM-4.6",
                messages=[
                    ChatMessage(role="system", content="Reply in English. No extra commentary."),
                    ChatMessage(role="user", content="Say 3 short sentences."),
                ],
        ):
            delta = chunk.get("choices", [{}])[0].get("delta", {})

            if SHOW_REASONING and "reasoning_content" in delta:
                print(delta["reasoning_content"], end="", flush=True)

            if "content" in delta:
                print(delta["content"], end="", flush=True)

        print()


    except AmbientError as e:
        print("AmbientError:", e)
