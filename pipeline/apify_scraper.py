#!/usr/bin/env python3
"""Metrics agent — scrapes LinkedIn via Apify sync endpoint, updates results.tsv.

Actor: apimaestro/linkedin-profile-posts
API:   POST /acts/apimaestro~linkedin-profile-posts/run-sync-get-dataset-items
Input: { "profileUsername": "michelbouman", "resultLimit": 30 }

Apify response schema (key fields used):
  posted_at.date         -> "2026-04-21 09:33:07"
  text                   -> full post text
  url                    -> LinkedIn post URL
  stats.total_reactions  -> all reactions combined
  stats.like / .insight / .comments / .reposts
  media.type             -> "image", "video", None

NOTE: No impressions field in this actor's output.
Primary metric: engagement_score = total_reactions + (comments*3) + (reposts*2)
"""

import os
import csv
import json
import re
import urllib.request
import urllib.parse
from datetime import date
from pathlib import Path

VAULT_ROOT = Path(__file__).parent.parent
TODAY = date.today().isoformat()
APIFY_BASE = "https://api.apify.com/v2"
ACTOR_ID = "apimaestro~linkedin-profile-posts"
LINKEDIN_USERNAME = "michelbouman"  # public profile, not a secret
RESULTS = VAULT_ROOT / "results.tsv"
FIELDS = [
    "date", "posted_time", "topic", "content_theme", "angle",
    "hook_type", "hook_text", "word_count", "line_count",
    "has_numbers", "has_question_cta", "has_image", "hashtag_count", "lead_magnet_type",
    "total_reactions", "likes", "insight_reactions", "comments", "reposts",
    "engagement_score", "comment_ratio", "insight_ratio",
    "scraped_at"
]


def run_actor_sync(token: str) -> list:
    url = (
        f"{APIFY_BASE}/acts/{urllib.parse.quote(ACTOR_ID, safe='')}"
        f"/run-sync-get-dataset-items?token={token}&format=json&clean=true"
    )
    body = json.dumps({
        "profileUsername": LINKEDIN_USERNAME,
        "resultLimit": 30,
    }).encode()
    req = urllib.request.Request(
        url, data=body,
        headers={"Content-Type": "application/json"},
        method="POST"
    )
    with urllib.request.urlopen(req, timeout=290) as resp:
        items = json.loads(resp.read())
    print(f"Got {len(items)} items from Apify")
    return items


def extract_hook(text: str) -> str:
    for line in text.split("\n"):
        line = line.strip()
        if line:
            return line[:120]
    return ""


def count_words(text: str) -> int:
    return len(re.findall(r"\b\w+\b", text))


def count_lines(text: str) -> int:
    return len([l for l in text.split("\n") if l.strip()])


def parse(items: list) -> list:
    posts = []
    for item in items:
        # Date and time
        posted_at = item.get("posted_at", {}) or {}
        dt = posted_at.get("date", "") if isinstance(posted_at, dict) else ""
        date_str = dt[:10] if dt else ""
        posted_time = dt[11:16] if len(dt) >= 16 else ""

        # Stats
        stats = item.get("stats", {}) or {}
        total_reactions = int(stats.get("total_reactions", 0) or 0)
        likes = int(stats.get("like", 0) or 0)
        insight = int(stats.get("insight", 0) or 0)
        comments = int(stats.get("comments", 0) or 0)
        reposts = int(stats.get("reposts", 0) or 0)

        engagement_score = total_reactions + (comments * 3) + (reposts * 2)
        comment_ratio = round(comments / total_reactions, 4) if total_reactions > 0 else 0.0
        insight_ratio = round(insight / total_reactions, 4) if total_reactions > 0 else 0.0

        # Content signals (derived from post text)
        text = item.get("text", "") or ""
        hook_text = extract_hook(text)
        word_count = count_words(text)
        line_count = count_lines(text)
        has_numbers = bool(re.search(r"\b\d+[%hxmk$€£]?\b", text))
        has_question_cta = bool(re.search(r"\?\s*[👇]?\s*$", text.strip()))
        hashtag_count = len(re.findall(r"#\w+", text))

        # Media
        media = item.get("media") or {}
        has_image = isinstance(media, dict) and media.get("type") in ("image", "video")

        posts.append({
            "date": date_str,
            "posted_time": posted_time,
            "url": item.get("url", ""),
            "text": text,
            "hook_text_scraped": hook_text,
            "word_count": word_count,
            "line_count": line_count,
            "has_numbers": has_numbers,
            "has_question_cta": has_question_cta,
            "has_image": has_image,
            "hashtag_count": hashtag_count,
            "total_reactions": total_reactions,
            "likes": likes,
            "insight_reactions": insight,
            "comments": comments,
            "reposts": reposts,
            "engagement_score": engagement_score,
            "comment_ratio": comment_ratio,
            "insight_ratio": insight_ratio,
        })
    return posts


def load_post_meta() -> dict:
    posts_dir = VAULT_ROOT / "Posts"
    meta = {}
    if not posts_dir.exists():
        return meta
    fm_fields = [
        "topic", "content_theme", "angle", "hook_type", "hook_text",
        "word_count", "line_count", "has_numbers", "has_question_cta",
        "hashtag_count", "lead_magnet_type", "posted_time"
    ]
    for f in posts_dir.glob("*.md"):
        c = f.read_text(encoding="utf-8")
        record = {}
        for field in fm_fields:
            m = re.search(rf'^{field}: "?(.*?)"?$', c, re.MULTILINE)
            record[field] = m.group(1).strip() if m else ""
        meta[f.stem] = record
    return meta


def load_existing() -> dict:
    if not RESULTS.exists():
        return {}
    with open(RESULTS, newline="", encoding="utf-8") as f:
        return {r["date"]: r for r in csv.DictReader(f, delimiter="\t")}


def write_results(rows: dict):
    sorted_rows = sorted(rows.values(), key=lambda x: x["date"], reverse=True)
    with open(RESULTS, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS, delimiter="\t", extrasaction="ignore")
        w.writeheader()
        w.writerows(sorted_rows)
    print(f"results.tsv: {len(sorted_rows)} rows")


def main():
    token = os.environ["APIFY_API_KEY"]
    print(f"Scraping @{LINKEDIN_USERNAME} via {ACTOR_ID}")

    items = run_actor_sync(token)
    posts = parse(items)

    meta = load_post_meta()
    existing = load_existing()

    for post in posts:
        d = post["date"]
        if not d:
            continue
        m = meta.get(d, {})
        existing[d] = {
            "date": d,
            "posted_time": m.get("posted_time") or post["posted_time"],
            "topic": m.get("topic", ""),
            "content_theme": m.get("content_theme", ""),
            "angle": m.get("angle", ""),
            "hook_type": m.get("hook_type", ""),
            "hook_text": m.get("hook_text") or post["hook_text_scraped"],
            "word_count": m.get("word_count") or post["word_count"],
            "line_count": m.get("line_count") or post["line_count"],
            "has_numbers": m.get("has_numbers") or str(post["has_numbers"]).lower(),
            "has_question_cta": m.get("has_question_cta") or str(post["has_question_cta"]).lower(),
            "has_image": str(post["has_image"]).lower(),
            "hashtag_count": m.get("hashtag_count") or post["hashtag_count"],
            "lead_magnet_type": m.get("lead_magnet_type", ""),
            "total_reactions": post["total_reactions"],
            "likes": post["likes"],
            "insight_reactions": post["insight_reactions"],
            "comments": post["comments"],
            "reposts": post["reposts"],
            "engagement_score": post["engagement_score"],
            "comment_ratio": post["comment_ratio"],
            "insight_ratio": post["insight_ratio"],
            "scraped_at": TODAY,
        }

    write_results(existing)
    print("Done.")


if __name__ == "__main__":
    main()
