#!/usr/bin/env python3
"""Analysis agent — reads results.tsv, tests hypotheses, rewrites strategy.md. Runs Mon + Thu."""

import os
import csv
import json
import re
import statistics
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
            for num_field in ("engagement_rate", "comment_rate", "likes", "comments", "shares", "impressions", "word_count", "line_count", "hashtag_count"):
                try:
                    row[num_field] = float(row[num_field]) if row.get(num_field) else 0.0
                except (ValueError, KeyError):
                    row[num_field] = 0.0
            for bool_field in ("has_numbers", "has_question_cta"):
                row[bool_field] = str(row.get(bool_field, "")).lower() == "true"
            rows.append(row)
    return rows


def group_avg(rows: list, key: str, metric: str = "engagement_rate") -> dict:
    """Average metric grouped by a categorical field."""
    groups: dict = {}
    for r in rows:
        v = r.get(key, "")
        if v:
            groups.setdefault(v, []).append(r.get(metric, 0))
    return {k: round(sum(v) / len(v), 4) for k, v in groups.items() if len(v) >= 2}


def bool_split_avg(rows: list, key: str, metric: str = "engagement_rate") -> dict:
    true_vals = [r.get(metric, 0) for r in rows if r.get(key) is True]
    false_vals = [r.get(metric, 0) for r in rows if r.get(key) is False]
    return {
        f"{key}=true": round(sum(true_vals) / len(true_vals), 4) if true_vals else None,
        f"{key}=false": round(sum(false_vals) / len(false_vals), 4) if false_vals else None,
        "true_n": len(true_vals),
        "false_n": len(false_vals)
    }


def correlation_buckets(rows: list, field: str, metric: str = "engagement_rate") -> dict:
    """Bin a numeric field into terciles and show avg metric per bucket."""
    vals = [r.get(field, 0) for r in rows if r.get(field, 0) > 0]
    if len(vals) < 6:
        return {}
    vals.sort()
    n = len(vals)
    low_thresh = vals[n // 3]
    high_thresh = vals[2 * n // 3]
    buckets = {"low": [], "mid": [], "high": []}
    for r in rows:
        v = r.get(field, 0)
        if v <= low_thresh:
            buckets["low"].append(r.get(metric, 0))
        elif v <= high_thresh:
            buckets["mid"].append(r.get(metric, 0))
        else:
            buckets["high"].append(r.get(metric, 0))
    return {
        f"{field}_low_avg_{metric}": round(sum(buckets['low']) / len(buckets['low']), 4) if buckets['low'] else None,
        f"{field}_mid_avg_{metric}": round(sum(buckets['mid']) / len(buckets['mid']), 4) if buckets['mid'] else None,
        f"{field}_high_avg_{metric}": round(sum(buckets['high']) / len(buckets['high']), 4) if buckets['high'] else None,
        "low_range": f"<= {low_thresh:.0f}",
        "mid_range": f"{low_thresh:.0f} - {high_thresh:.0f}",
        "high_range": f"> {high_thresh:.0f}"
    }


def build_analysis_data(results: list) -> dict:
    """Compile all hypothesis-testable signals into a structured dict."""
    by_rate = sorted(results, key=lambda x: x.get("engagement_rate", 0), reverse=True)
    avg_eng = sum(r.get("engagement_rate", 0) for r in results) / len(results)
    avg_comment = sum(r.get("comment_rate", 0) for r in results) / len(results)

    return {
        "summary": {
            "total_posts": len(results),
            "avg_engagement_rate": round(avg_eng, 4),
            "avg_comment_rate": round(avg_comment, 4),
        },
        "top_5_posts": by_rate[:5],
        "bottom_5_posts": by_rate[-5:] if len(by_rate) >= 5 else [],
        # H1: I-statement hooks
        "by_hook_type": group_avg(results, "hook_type"),
        # H2: Specific numbers
        "has_numbers_split": bool_split_avg(results, "has_numbers"),
        # H3: Question CTA
        "has_question_cta_split": bool_split_avg(results, "has_question_cta"),
        # H4: Post length (word count)
        "word_count_buckets": correlation_buckets(results, "word_count"),
        # Line count
        "line_count_buckets": correlation_buckets(results, "line_count"),
        # Hashtag count
        "by_hashtag_count": group_avg(results, "hashtag_count"),
        # Content theme
        "by_content_theme": group_avg(results, "content_theme"),
        # Post angle
        "by_angle": group_avg(results, "angle"),
        # Lead magnet type
        "by_lead_magnet_type": group_avg(results, "lead_magnet_type"),
        # Posting time (hour)
        "by_posted_hour": group_avg(
            [{**r, "hour": r.get("posted_time", "")[:2]} for r in results if r.get("posted_time")],
            "hour"
        ),
    }


def run_analysis(client: anthropic.Anthropic, analysis_data: dict, strategy: str) -> dict:
    resp = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=6000,
        system="""You are a LinkedIn growth strategist running an autoresearch loop.
You receive structured performance data with engagement signals broken down by every tracked variable.
Your job: draw conclusions from the numbers, update the hypotheses, and rewrite the strategy playbook.
Be specific — cite the actual numbers when you make a claim.""",
        messages=[{"role": "user", "content": f"""Analyze this data and rewrite strategy.md.

PERFORMANCE DATA:
{json.dumps(analysis_data, indent=2)}

CURRENT STRATEGY:
{strategy}

For each tracked variable, state what the data shows (or "insufficient data").
Then rewrite strategy.md to encode what's been learned.

Return ONLY valid JSON:
{{
  "variable_findings": {{
    "hook_type": "...",
    "has_numbers": "...",
    "has_question_cta": "...",
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
        print(f"Only {len(results)} posts with data. Need at least 3. Skipping.")
        return

    analysis_data = build_analysis_data(results)
    strategy = (VAULT_ROOT / "strategy.md").read_text(encoding="utf-8") if (VAULT_ROOT / "strategy.md").exists() else ""

    print(f"Analyzing {len(results)} posts...")
    result = run_analysis(client, analysis_data, strategy)

    (VAULT_ROOT / "strategy.md").write_text(result["updated_strategy_md"], encoding="utf-8")
    print("Updated strategy.md")

    analytics_dir = VAULT_ROOT / "Analytics"
    analytics_dir.mkdir(exist_ok=True)
    findings = result.get("variable_findings", {})
    report = f"""---
date: {TODAY}
week: {WEEK}
posts_analyzed: {analysis_data['summary']['total_posts']}
avg_engagement_rate: {analysis_data['summary']['avg_engagement_rate']}
avg_comment_rate: {analysis_data['summary']['avg_comment_rate']}
---

# Autoresearch — {TODAY}

{result.get('summary', '')}

## Variable Findings

| Variable | Finding |
|----------|---------|
{''.join(f"| {k} | {v} |{chr(10)}" for k, v in findings.items())}

## Confirmed Hypotheses
{''.join('- ' + h + chr(10) for h in result.get('confirmed_hypotheses', []))}
## Rejected Hypotheses
{''.join('- ' + h + chr(10) for h in result.get('rejected_hypotheses', []))}
## New Hypotheses
{''.join('- ' + h + chr(10) for h in result.get('new_hypotheses', []))}

## Raw Analysis Data
```json
{json.dumps(analysis_data['summary'], indent=2)}
```
"""
    (analytics_dir / f"{TODAY}_autoresearch.md").write_text(report, encoding="utf-8")
    print(f"Saved: Analytics/{TODAY}_autoresearch.md")
    print("Done.")


if __name__ == "__main__":
    main()
