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
            for num_field in (
                "engagement_score", "comment_ratio", "insight_ratio",
                "total_reactions", "likes", "insight_reactions",
                "comments", "reposts", "word_count", "line_count", "hashtag_count"
            ):
                try:
                    row[num_field] = float(row.get(num_field) or 0)
                except ValueError:
                    row[num_field] = 0.0
            for bool_field in ("has_numbers", "has_question_cta", "has_image"):
                row[bool_field] = str(row.get(bool_field, "")).lower() == "true"
            rows.append(row)
    return rows


def group_avg(rows: list, key: str, metric: str = "engagement_score") -> dict:
    groups: dict = {}
    for r in rows:
        v = str(r.get(key, "")).strip()
        if v:
            groups.setdefault(v, []).append(r.get(metric, 0))
    return {
        k: {"avg": round(sum(v) / len(v), 2), "n": len(v)}
        for k, v in groups.items() if len(v) >= 2
    }


def bool_split_avg(rows: list, key: str, metric: str = "engagement_score") -> dict:
    true_vals = [r.get(metric, 0) for r in rows if r.get(key) is True]
    false_vals = [r.get(metric, 0) for r in rows if r.get(key) is False]
    return {
        "true": {"avg": round(sum(true_vals) / len(true_vals), 2), "n": len(true_vals)} if true_vals else None,
        "false": {"avg": round(sum(false_vals) / len(false_vals), 2), "n": len(false_vals)} if false_vals else None,
    }


def tercile_buckets(rows: list, field: str, metric: str = "engagement_score") -> dict:
    vals = sorted([r.get(field, 0) for r in rows if r.get(field, 0) > 0])
    if len(vals) < 6:
        return {"note": "insufficient data"}
    n = len(vals)
    lo, hi = vals[n // 3], vals[2 * n // 3]
    buckets = {"low": [], "mid": [], "high": []}
    for r in rows:
        v = r.get(field, 0)
        b = "low" if v <= lo else ("mid" if v <= hi else "high")
        buckets[b].append(r.get(metric, 0))
    return {
        "low": {"range": f"<={lo:.0f}", "avg": round(sum(buckets['low']) / len(buckets['low']), 2)} if buckets['low'] else None,
        "mid": {"range": f"{lo:.0f}-{hi:.0f}", "avg": round(sum(buckets['mid']) / len(buckets['mid']), 2)} if buckets['mid'] else None,
        "high": {"range": f">{hi:.0f}", "avg": round(sum(buckets['high']) / len(buckets['high']), 2)} if buckets['high'] else None,
    }


def build_analysis(results: list) -> dict:
    by_score = sorted(results, key=lambda x: x.get("engagement_score", 0), reverse=True)
    avg_score = sum(r.get("engagement_score", 0) for r in results) / len(results)
    avg_comment_ratio = sum(r.get("comment_ratio", 0) for r in results) / len(results)
    avg_insight_ratio = sum(r.get("insight_ratio", 0) for r in results) / len(results)

    return {
        "summary": {
            "total_posts": len(results),
            "avg_engagement_score": round(avg_score, 1),
            "avg_comment_ratio": round(avg_comment_ratio, 4),
            "avg_insight_ratio": round(avg_insight_ratio, 4),
            "metric_note": "engagement_score = total_reactions + (comments*3) + (reposts*2). No impressions available."
        },
        "top_5": by_score[:5],
        "bottom_5": by_score[-5:] if len(by_score) >= 5 else [],
        # H1: I-statement vs other hooks
        "by_hook_type": group_avg(results, "hook_type"),
        # H2: specific numbers in post
        "has_numbers": bool_split_avg(results, "has_numbers"),
        # H3: question CTA
        "has_question_cta": bool_split_avg(results, "has_question_cta"),
        # Image posts vs text-only
        "has_image": bool_split_avg(results, "has_image"),
        # H4: word count
        "word_count_buckets": tercile_buckets(results, "word_count"),
        # Line count
        "line_count_buckets": tercile_buckets(results, "line_count"),
        # Hashtag count
        "by_hashtag_count": group_avg(results, "hashtag_count"),
        # Content dimensions
        "by_content_theme": group_avg(results, "content_theme"),
        "by_angle": group_avg(results, "angle"),
        "by_lead_magnet_type": group_avg(results, "lead_magnet_type"),
        # Posting hour
        "by_posted_hour": group_avg(
            [{**r, "hour": r.get("posted_time", "")[:2]} for r in results if r.get("posted_time")],
            "hour"
        ),
    }


def run_analysis(client: anthropic.Anthropic, data: dict, strategy: str) -> dict:
    resp = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=6000,
        system="""You are a LinkedIn growth strategist running an autoresearch optimization loop.
Analyze the structured performance data, draw data-driven conclusions about each tracked variable, and rewrite strategy.md.
Be specific — cite actual numbers. State "insufficient data" where sample size is too small.
Primary metric: engagement_score = total_reactions + (comments×3) + (reposts×2).
Secondary quality signals: comment_ratio and insight_ratio.""",
        messages=[{"role": "user", "content": f"""Analyze this data and rewrite strategy.md.

DATA:
{json.dumps(data, indent=2)}

CURRENT STRATEGY:
{strategy}

For each tracked variable, state what the data shows.
Then rewrite strategy.md to encode what's been learned.

Return ONLY valid JSON:
{{
  "variable_findings": {{
    "hook_type": "...",
    "has_numbers": "...",
    "has_question_cta": "...",
    "has_image": "...",
    "word_count": "...",
    "line_count": "...",
    "content_theme": "...",
    "angle": "...",
    "lead_magnet_type": "...",
    "posted_time": "..."
  }},
  "confirmed_hypotheses": ["..."],
  "rejected_hypotheses": ["..."],
  "new_hypotheses": ["..."],
  "updated_strategy_md": "...(complete replacement for strategy.md)...",
  "summary": "...(2 sentences for commit message)"
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

    data = build_analysis(results)
    strategy = (VAULT_ROOT / "strategy.md").read_text(encoding="utf-8") if (VAULT_ROOT / "strategy.md").exists() else ""
    avg = data["summary"]["avg_engagement_score"]

    print(f"Analyzing {len(results)} posts (avg score: {avg})...")
    result = run_analysis(client, data, strategy)

    (VAULT_ROOT / "strategy.md").write_text(result["updated_strategy_md"], encoding="utf-8")
    print("Updated strategy.md")

    analytics_dir = VAULT_ROOT / "Analytics"
    analytics_dir.mkdir(exist_ok=True)
    findings = result.get("variable_findings", {})
    report = f"""---
date: {TODAY}
week: {WEEK}
posts_analyzed: {data['summary']['total_posts']}
avg_engagement_score: {avg}
avg_comment_ratio: {data['summary']['avg_comment_ratio']}
avg_insight_ratio: {data['summary']['avg_insight_ratio']}
---

# Autoresearch — {TODAY}

{result.get('summary', '')}

## Variable Findings

| Variable | Finding |
|----------|---------|
{''.join(f"| {k} | {v} |{chr(10)}" for k, v in findings.items())}

## Confirmed
{''.join('- ' + h + chr(10) for h in result.get('confirmed_hypotheses', []))}
## Rejected
{''.join('- ' + h + chr(10) for h in result.get('rejected_hypotheses', []))}
## New Hypotheses
{''.join('- ' + h + chr(10) for h in result.get('new_hypotheses', []))}
"""
    (analytics_dir / f"{TODAY}_autoresearch.md").write_text(report, encoding="utf-8")
    print(f"Saved: Analytics/{TODAY}_autoresearch.md")
    print("Done.")


if __name__ == "__main__":
    main()
