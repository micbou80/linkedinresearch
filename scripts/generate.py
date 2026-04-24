#!/usr/bin/env python3
"""Daily lead magnet and LinkedIn post generator."""

import os
import json
import re
from datetime import date
from pathlib import Path
import anthropic

VAULT_ROOT = Path(__file__).parent.parent
TODAY = date.today().isoformat()


def load_file(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def load_engagement_data() -> dict:
    data_path = VAULT_ROOT / "data" / "engagement.json"
    if data_path.exists():
        with open(data_path) as f:
            return json.load(f)
    return {"posts": []}


def generate_content(client: anthropic.Anthropic, prompts: str, brief: str, engagement_data: dict) -> dict:
    posts = engagement_data.get("posts", [])
    top_posts = sorted(posts, key=lambda x: x.get("engagement_rate", 0), reverse=True)[:3]
    top_context = json.dumps(top_posts, indent=2) if top_posts else "No performance data yet."

    system_prompt = f"""You are a LinkedIn content expert.

{prompts}

Research Brief:
{brief}

Top Performing Posts So Far:
{top_context}
"""

    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=4000,
        system=system_prompt,
        messages=[{
            "role": "user",
            "content": f"""Generate today's ({TODAY}) LinkedIn lead magnet and post.

Return ONLY a valid JSON object with this exact structure:
{{
  "topic": "...",
  "lead_magnet": {{
    "title": "...",
    "type": "checklist|template|guide|calculator|framework",
    "content": "...(full markdown content)..."
  }},
  "post": {{
    "hook": "...(first line only)...",
    "full_text": "...(complete post ready to copy-paste, no hashtags)...",
    "hashtags": ["tag1", "tag2", "tag3"],
    "cta": "...(the call to action line)..."
  }}
}}"""
        }]
    )

    content = response.content[0].text
    json_match = re.search(r"\{.*\}", content, re.DOTALL)
    if json_match:
        return json.loads(json_match.group())
    raise ValueError(f"Could not parse JSON from response:\n{content[:400]}")


def save_post(data: dict):
    posts_dir = VAULT_ROOT / "Posts"
    posts_dir.mkdir(exist_ok=True)
    post = data["post"]
    hashtags = " ".join(f"#{h.lstrip('#')}" for h in post["hashtags"])
    content = f"""---
date: {TODAY}
topic: "{data['topic']}"
lead_magnet: "[[Lead Magnets/{TODAY}|{data['lead_magnet']['title']}]]"
status: draft
posted_at:
engagement:
  likes: 0
  comments: 0
  shares: 0
  impressions: 0
  engagement_rate: 0.0
tags: []
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
    print(f"Saved post: Posts/{TODAY}.md")


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
    print(f"Saved lead magnet: Lead Magnets/{TODAY}.md")


def main():
    api_key = os.environ["ANTHROPIC_API_KEY"]
    client = anthropic.Anthropic(api_key=api_key)

    prompts = load_file(VAULT_ROOT / "Agent" / "prompts.md")
    brief = load_file(VAULT_ROOT / "Agent" / "research_brief.md")
    engagement_data = load_engagement_data()

    print(f"Generating content for {TODAY}...")
    data = generate_content(client, prompts, brief, engagement_data)

    save_post(data)
    save_lead_magnet(data)
    print("Done.")


if __name__ == "__main__":
    main()
