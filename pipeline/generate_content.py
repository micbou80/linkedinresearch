#!/usr/bin/env python3
"""Content agent — reads research + strategy + examples, generates post + lead magnet."""

import os
import json
import re
from datetime import date
from pathlib import Path
import anthropic

VAULT_ROOT = Path(__file__).parent.parent
TODAY = date.today().isoformat()


def load_examples() -> str:
    examples_dir = VAULT_ROOT / "examples"
    if not examples_dir.exists():
        return ""
    parts = []
    for f in sorted(examples_dir.glob("*.md")):
        content = f.read_text(encoding="utf-8").strip()
        if content:
            parts.append(f"--- {f.name} ---\n{content}")
    return "\n\n".join(parts[:3])  # use top 3 examples


def load_text(path: Path, fallback: str = "") -> str:
    return path.read_text(encoding="utf-8") if path.exists() else fallback


def generate(client: anthropic.Anthropic) -> dict:
    strategy = load_text(VAULT_ROOT / "strategy.md")
    research = load_text(VAULT_ROOT / "data" / "research_today.md", "No research available.")
    prompts = load_text(VAULT_ROOT / "Agent" / "prompts.md")
    examples = load_examples()

    examples_block = f"\n\nEXAMPLE POSTS (match this voice exactly):\n{examples}" if examples else ""

    resp = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=4000,
        system=f"""You are a LinkedIn ghostwriter writing in the author's exact voice.

{prompts}

CONTENT STRATEGY:
{strategy}{examples_block}""",
        messages=[{"role": "user", "content": f"""TODAY'S RESEARCH:\n{research}\n\nPick the single strongest topic and generate today's content.\n\nCRITICAL: The post MUST open with an \"I\" statement — a specific personal experience or result.\nGood: \"I saved 3 hours last week with one prompt.\"\nGood: \"I used to dread Monday mornings. Then I changed one thing.\"\nBad: \"AI is transforming the way we work.\"\n\nReturn ONLY valid JSON:\n{{\n  \"topic\": \"...\",\n  \"hook_type\": \"i_statement_result|i_statement_before_after|i_statement_observation\",\n  \"lead_magnet\": {{\n    \"title\": \"...\",\n    \"type\": \"checklist|template|guide|framework\",\n    \"content\": \"...(full markdown)...\"\n  }},\n  \"post\": {{\n    \"hook\": \"...(first line — must be I statement)...\",\n    \"full_text\": \"...(complete post, no hashtags, 150-250 words)...\",\n    \"hashtags\": [\"AI\", \"Leadership\", \"FutureOfWork\"],\n    \"cta\": \"...\"\n  }}\n}}"""}]
    )

    raw = resp.content[0].text
    match = re.search(r"\{.*\}", raw, re.DOTALL)
    if match:
        return json.loads(match.group())
    raise ValueError(f"No JSON in response:\n{raw[:400]}")


def save_post(data: dict):
    posts_dir = VAULT_ROOT / "Posts"
    posts_dir.mkdir(exist_ok=True)
    post = data["post"]
    hashtags = " ".join(f"#{h.lstrip('#')}" for h in post["hashtags"])
    content = f"""---
date: {TODAY}
topic: "{data['topic']}"
hook_type: {data.get('hook_type', 'unknown')}
lead_magnet: "[[Lead Magnets/{TODAY}|{data['lead_magnet']['title']}]]"
status: draft
posted_at:
engagement:
  likes: 0
  comments: 0
  shares: 0
  impressions: 0
  engagement_rate: 0.0
---

# {data['topic']}

## Hook
{post['hook']}

## Full Post
{post['full_text']}

{hashtags}

## Lead Magnet
[[Lead Magnets/{TODAY}|{data['lead_magnet']['title']}]]
"""
    (posts_dir / f"{TODAY}.md").write_text(content, encoding="utf-8")
    print(f"Saved: Posts/{TODAY}.md")


def save_lead_magnet(data: dict):
    lm_dir = VAULT_ROOT / "Lead Magnets"
    lm_dir.mkdir(exist_ok=True)
    lm = data["lead_magnet"]
    content = f"""---
date: {TODAY}
title: "{lm['title']}"
type: {lm['type']}
topic: "{data['topic']}"
post: "[[Posts/{TODAY}]]"
---

# {lm['title']}

{lm['content']}
"""
    (lm_dir / f"{TODAY}.md").write_text(content, encoding="utf-8")
    print(f"Saved: Lead Magnets/{TODAY}.md")


def main():
    client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
    print(f"Generating content for {TODAY}...")
    data = generate(client)
    save_post(data)
    save_lead_magnet(data)
    print("Done.")


if __name__ == "__main__":
    main()
