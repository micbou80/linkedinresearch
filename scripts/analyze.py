#!/usr/bin/env python3
"""Weekly analysis agent — reads engagement data, rewrites prompts.md."""

import os
import json
import re
from datetime import datetime, date
from pathlib import Path
import anthropic

VAULT_ROOT = Path(__file__).parent.parent
TODAY = date.today().isoformat()
WEEK = datetime.now().strftime("%Y-W%V")


def load_posts() -> list:
    posts_dir = VAULT_ROOT / "Posts"
    if not posts_dir.exists():
        return []
    posts = []
    for f in sorted(posts_dir.glob("*.md")):
        content = f.read_text(encoding="utf-8")
        fm_match = re.match(r"^---\n(.*?)\n---\n(.*)", content, re.DOTALL)
        if not fm_match:
            continue
        fm_text, body = fm_match.groups()
        eng = {}
        eng_block = re.search(r"engagement:\n((?:  \w+:.*\n)*)", fm_text)
        if eng_block:
            for line in eng_block.group(1).split("\n"):
                if ":" in line:
                    k, _, v = line.strip().partition(":")
                    try:
                        eng[k.strip()] = float(v.strip())
                    except ValueError:
                        pass
        posts.append({"date": f.stem, "engagement": eng, "body": body.strip()[:600]})
    return posts


def main():
    api_key = os.environ["ANTHROPIC_API_KEY"]
    client = anthropic.Anthropic(api_key=api_key)

    data_path = VAULT_ROOT / "data" / "engagement.json"
    if not data_path.exists():
        print("No engagement data yet. Skipping.")
        return

    with open(data_path) as f:
        engagement_data = json.load(f)

    all_posts = engagement_data.get("posts", [])
    if len(all_posts) < 3:
        print(f"Only {len(all_posts)} posts with data. Need at least 3. Skipping.")
        return

    post_bodies = load_posts()
    bodies_by_date = {p["date"]: p["body"] for p in post_bodies}

    sorted_posts = sorted(all_posts, key=lambda x: x.get("engagement_rate", 0), reverse=True)
    top_5 = [{**p, "body_preview": bodies_by_date.get(p["date"], "")} for p in sorted_posts[:5]]
    bottom_5 = sorted_posts[-5:] if len(sorted_posts) >= 5 else []
    avg_rate = sum(p.get("engagement_rate", 0) for p in all_posts) / len(all_posts)

    current_prompts = (VAULT_ROOT / "Agent" / "prompts.md").read_text(encoding="utf-8")
    brief = (VAULT_ROOT / "Agent" / "research_brief.md").read_text(encoding="utf-8")

    print(f"Analyzing {len(all_posts)} posts (avg engagement: {avg_rate:.3f}%)...")

    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=8000,
        system=f"""You are an expert LinkedIn content strategist running an autoresearch-style optimization loop.
Your job: analyze engagement data, extract what works, and rewrite the generation prompts to perform better next week.

Research Brief:
{brief}""",
        messages=[{"role": "user", "content": f"""Analyze this data and improve the prompts.

TOP 5 POSTS (by engagement rate):
{json.dumps(top_5, indent=2)}

BOTTOM 5 POSTS:
{json.dumps(bottom_5, indent=2)}

TOTAL POSTS: {len(all_posts)}
AVERAGE ENGAGEMENT RATE: {avg_rate:.4f}%

CURRENT PROMPTS.MD:
{current_prompts}

Return ONLY a valid JSON object:
{{
  "insights": {{
    "what_works": ["..."],
    "what_doesnt": ["..."],
    "top_hook_patterns": ["..."],
    "top_topics": ["..."],
    "optimal_length": "...",
    "best_cta_patterns": ["..."],
    "trend": "improving|declining|stable"
  }},
  "updated_prompts_md": "...(complete replacement for prompts.md)...",
  "analysis_report": "...(markdown report with headers and bullets)"
}}"""}]
    )

    content = response.content[0].text
    json_match = re.search(r"\{.*\}", content, re.DOTALL)
    if not json_match:
        raise ValueError(f"No JSON in response: {content[:300]}")

    result = json.loads(json_match.group())
    insights = result["insights"]

    prompts_path = VAULT_ROOT / "Agent" / "prompts.md"
    prompts_path.write_text(
        f"<!-- Updated by analyze.py on {TODAY} -->\n{result['updated_prompts_md']}",
        encoding="utf-8"
    )
    print("Updated Agent/prompts.md")

    analytics_dir = VAULT_ROOT / "Analytics"
    analytics_dir.mkdir(exist_ok=True)
    report = f"""---
date: {TODAY}
week: {WEEK}
trend: {insights.get('trend', 'unknown')}
avg_engagement_rate: {avg_rate:.4f}
---

# Weekly Analysis — {WEEK}

{result['analysis_report']}

---

## What Works
{''.join('- ' + w + chr(10) for w in insights.get('what_works', []))}
## What Doesn't
{''.join('- ' + w + chr(10) for w in insights.get('what_doesnt', []))}
## Top Hook Patterns
{''.join('- ' + h + chr(10) for h in insights.get('top_hook_patterns', []))}
## Top Topics
{''.join('- ' + t + chr(10) for t in insights.get('top_topics', []))}
## Optimal Length
{insights.get('optimal_length', 'N/A')}
## Best CTA Patterns
{''.join('- ' + c + chr(10) for c in insights.get('best_cta_patterns', []))}
"""
    (analytics_dir / f"{WEEK}_analysis.md").write_text(report, encoding="utf-8")
    print(f"Saved Analytics/{WEEK}_analysis.md")
    print("Analysis complete.")


if __name__ == "__main__":
    main()
