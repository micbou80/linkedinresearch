#!/usr/bin/env python3
"""Analysis agent — reads results.tsv, tests hypotheses, rewrites strategy.md. Runs Mon + Thu."""

import os
import csv
import json
import re
from datetime import datetime, date
from pathlib import Path
import anthropic

VAULT_ROOT = Path(__file__).parent.parent
TODAY = date.today().isoformat()
WEEK = datetime.now().strftime("%Y-W%V")


def load_results() -> list:
    path = VAULT_ROOT / "results.tsv"
    if not path.exists():
        return []
    rows = []
    with open(path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f, delimiter="\t"):
            try:
                row["engagement_rate"] = float(row["engagement_rate"])
                row["likes"] = int(row["likes"])
                row["comments"] = int(row["comments"])
                row["impressions"] = int(row["impressions"])
            except (ValueError, KeyError):
                pass
            rows.append(row)
    return rows


def enrich_with_bodies(results: list) -> list:
    posts_dir = VAULT_ROOT / "Posts"
    enriched = []
    for row in results:
        body = ""
        f = posts_dir / f"{row['date']}.md"
        if f.exists():
            c = f.read_text(encoding="utf-8")
            m = re.match(r"^---\n.*?\n---\n(.*)", c, re.DOTALL)
            if m:
                body = m.group(1).strip()[:400]
        enriched.append({**row, "body_preview": body})
    return enriched


def run_analysis(client: anthropic.Anthropic, results: list, strategy: str) -> dict:
    by_rate = sorted(results, key=lambda x: x.get("engagement_rate", 0), reverse=True)
    top5 = by_rate[:5]
    bottom5 = by_rate[-5:] if len(by_rate) >= 5 else []
    avg = sum(r.get("engagement_rate", 0) for r in results) / len(results)

    # Test H1: I-statement hypothesis
    i_posts = [r for r in results if str(r.get("hook_type", "")).startswith("i_statement")]
    other_posts = [r for r in results if r.get("hook_type") and not str(r.get("hook_type", "")).startswith("i_statement")]
    i_avg = sum(r.get("engagement_rate", 0) for r in i_posts) / len(i_posts) if i_posts else None
    other_avg = sum(r.get("engagement_rate", 0) for r in other_posts) / len(other_posts) if other_posts else None

    hypothesis_data = {
        "H1_i_statement_posts": len(i_posts),
        "H1_i_statement_avg_engagement": round(i_avg, 4) if i_avg is not None else None,
        "H1_other_hook_posts": len(other_posts),
        "H1_other_hook_avg_engagement": round(other_avg, 4) if other_avg is not None else None,
        "H1_verdict": "insufficient_data" if len(i_posts) < 3 or len(other_posts) < 3 else ("confirmed" if (i_avg or 0) > (other_avg or 0) else "rejected")
    }

    resp = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=6000,
        system="""You are a LinkedIn growth strategist running an autoresearch optimization loop.
Analyze engagement data, test hypotheses with real numbers, identify patterns, and rewrite the strategy playbook to reflect what the data says.
Think like a scientist: update beliefs based on evidence, not intuition.""",
        messages=[{"role": "user", "content": f"""Analyze this LinkedIn performance data and rewrite strategy.md.

STATS:
- Total posts: {len(results)}
- Average engagement rate: {avg:.4f}%

TOP 5 POSTS:
{json.dumps(top5, indent=2)}

BOTTOM 5 POSTS:
{json.dumps(bottom5, indent=2)}

HYPOTHESIS TEST DATA:
{json.dumps(hypothesis_data, indent=2)}

CURRENT STRATEGY:
{strategy}

Return ONLY valid JSON:
{{
  "what_works": ["..."],
  "what_doesnt": ["..."],
  "hypothesis_notes": "...(plain English verdict on H1 and any others)",
  "new_hypotheses": ["..."],
  "updated_strategy_md": "...(complete replacement — keep same structure, update based on data)",
  "summary": "...(1-2 sentences for commit message)"
}}"""}]
    )

    raw = resp.content[0].text
    m = re.search(r"\{.*\}", raw, re.DOTALL)
    if m:
        return json.loads(m.group())
    raise ValueError(f"No JSON: {raw[:300]}")


def main():
    client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])

    results = load_results()
    if len(results) < 3:
        print(f"Only {len(results)} posts. Need at least 3. Skipping.")
        return

    results = enrich_with_bodies(results)
    strategy = (VAULT_ROOT / "strategy.md").read_text(encoding="utf-8") if (VAULT_ROOT / "strategy.md").exists() else ""
    avg = sum(r.get("engagement_rate", 0) for r in results) / len(results)

    print(f"Analyzing {len(results)} posts (avg: {avg:.3f}%)...")
    result = run_analysis(client, results, strategy)

    (VAULT_ROOT / "strategy.md").write_text(result["updated_strategy_md"], encoding="utf-8")
    print("Updated strategy.md")

    analytics_dir = VAULT_ROOT / "Analytics"
    analytics_dir.mkdir(exist_ok=True)
    report = f"""---
date: {TODAY}
week: {WEEK}
avg_engagement_rate: {avg:.4f}
posts_analyzed: {len(results)}
---

# Autoresearch — {TODAY}

{result.get('summary', '')}

## Hypothesis Notes
{result.get('hypothesis_notes', '')}

## What Works
{''.join('- ' + w + chr(10) for w in result.get('what_works', []))}
## What Doesn't
{''.join('- ' + w + chr(10) for w in result.get('what_doesnt', []))}
## New Hypotheses
{''.join('- ' + h + chr(10) for h in result.get('new_hypotheses', []))}
"""
    (analytics_dir / f"{TODAY}_autoresearch.md").write_text(report, encoding="utf-8")
    print(f"Saved: Analytics/{TODAY}_autoresearch.md")
    print("Done.")


if __name__ == "__main__":
    main()
