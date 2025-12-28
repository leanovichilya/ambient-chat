import os
import sys
from typing import Optional, Dict, Tuple

import requests
from dotenv import load_dotenv


def env(name: str, default: Optional[str] = None) -> Optional[str]:
    value = os.getenv(name)
    return value if value not in (None, "") else default


def parse_timeout() -> Tuple[float, float]:
    # requests timeout can be (connect_timeout, read_timeout)
    connect_timeout = float(env("AMBIENT_CONNECT_TIMEOUT", "10"))
    read_timeout = float(env("AMBIENT_READ_TIMEOUT", "180"))
    return connect_timeout, read_timeout


def main() -> None:
    load_dotenv()

    api_key = env("AMBIENT_API_KEY")
    if not api_key:
        raise RuntimeError("AMBIENT_API_KEY not found in .env")

    base_url = env("AMBIENT_BASE_URL", "https://api.ambient.xyz/v1").rstrip("/")
    model = env("AMBIENT_MODEL", "zai-org/GLM-4.6")

    prompt = " ".join(sys.argv[1:]).strip() or "Hello"

    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": "Reply in English."},
            {"role": "user", "content": prompt},
        ],
        "stream": False,
    }

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "Accept": "application/json",
    }

    # By default, ignore system/env proxy settings for predictability.
    session = requests.Session()
    session.trust_env = False

    # Enable proxy only if explicitly requested
    use_proxy = env("USE_PROXY", "0").lower() in ("1", "true", "yes", "y", "on")
    proxies: Optional[Dict[str, str]] = None
    if use_proxy:
        http_proxy = env("HTTP_PROXY") or env("http_proxy")
        https_proxy = env("HTTPS_PROXY") or env("https_proxy")
        if http_proxy or https_proxy:
            proxies = {}
            if http_proxy:
                proxies["http"] = http_proxy
            if https_proxy:
                proxies["https"] = https_proxy

    timeout = parse_timeout()

    r = session.post(
        f"{base_url}/chat/completions",
        json=payload,
        headers=headers,
        timeout=timeout,
        proxies=proxies,
    )

    if r.status_code >= 400:
        raise RuntimeError(f"HTTP {r.status_code} {r.reason}. Body: {r.text[:2000]}")

    data = r.json()
    print(data["choices"][0]["message"]["content"])

    usage = data.get("usage")
    if usage:
        print("\n---\nusage:", usage)


if __name__ == "__main__":
    main()
