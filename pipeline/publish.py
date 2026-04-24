#!/usr/bin/env python3
"""Publisher stub — configure with BloTato or your preferred LinkedIn scheduling tool."""

import os
import re
import json
import urllib.request
from datetime import date
from pathlib import Path

VAULT_ROOT = Path(__file__).parent.parent
TODAY = date.today().isoformat()

# BloTato API: https://blotato.com
BLOTATO_API = "https://api.blotato.com/v1"


def load_today_post() -> str:
    post_file = VAULT_ROOT / "Posts" / f"{TODAY}.md"
    if not post_file.exists():
        raise FileNotFoundError(f"No post found: {post_file}")
    content = post_file.read_text(encoding="utf-8")
    # Extract full post + hashtags
    full_text = re.search(r"## Full Post\n(.*?)\n\n#", content, re.DOTALL)
    hashtags = re.search(r"\n(#\w[\w ]*(?:#\w[\w ]*)*)\n", content)
    text = (full_text.group(1).strip() if full_text else "") + "\n\n" + (hashtags.group(1).strip() if hashtags else "")
    return text.strip()


def publish(text: str, api_key: str):
    payload = {"platform": "linkedin", "content": text, "schedule": "immediate"}
    req = urllib.request.Request(
        f"{BLOTATO_API}/posts",
        data=json.dumps(payload).encode(),
        headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
    )
    with urllib.request.urlopen(req) as resp:
        print(f"Published: {json.loads(resp.read())}")


def main():
    api_key = os.environ.get("BLOTATO_API_KEY")
    if not api_key:
        print("BLOTATO_API_KEY not set — skipping auto-publish.")
        print(f"Post ready to copy from: Posts/{TODAY}.md")
        return
    text = load_today_post()
    publish(text, api_key)


if __name__ == "__main__":
    main()
