#!/usr/bin/env python3
"""Metrics agent — scrapes LinkedIn via Apify sync endpoint, updates results.tsv."""

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
RESULTS = VAULT_ROOT / "results.tsv"
FIELDS = [
    "date", "posted_time", "topic", "content_theme", "angle",
    "hook_type", "hook_text", "word_count", "line_count",
    "has_numbers", "has_question_cta", "hashtag_count", "lead_magnet_type",
    "likes", "comments", "shares", "impressions",
    "engagement_rate", "comment_rate", "scraped_at"
]


def run_actor_sync(actor_id: str, input_data: dict, token: str) -> list:
    """
    POST /acts/{actorId}/run-sync-get-dataset-items
    Blocks until the run finishes (up to 300s) and returns dataset items directly.
    """
    url = (
        f"{APIFY_BASE}/acts/{urllib.parse.quote(actor_id, safe='')}"
        f"/run-sync-get-dataset-items?token={token}&format=json&clean=true"
    )
    body = json.dumps(input_data).encode()
    req = urllib.request.Request(
        url,
        data=body,
        headers={"Content-Type": "application/json"},
        method="POST"
    )
    # LinkedIn scrapers can take a while — use 290s to stay under the 300s API limit
    with urllib.request.urlopen(req, timeout=290) as resp:
        items = json.loads(resp.read())
    print(f"Got {len(items)} items from Apify")
    return items


def load_post_meta() -> dict:
    """Read all tracked signals from post frontmatter."""
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


def parse(items: list) -> list:
    """
    Normalize Apify output to our schema.
    Field names vary by actor — we try common variants.
    """
    posts = []
    for item in items:
        published = (
            item.get("publishedAt") or item.get("postedAt")
            or item.get("date") or item.get("createdAt", "")
        )
        likes = item.get("likes") or item.get("numLikes") or item.get("likeCount") or 0
        comments = item.get("comments") or item.get("numComments") or item.get("commentCount") or 0
        shares = item.get("shares") or item.get("numShares") or item.get("shareCount") or 0
        impressions = (
            item.get("impressions") or item.get("views")
            or item.get("impressionCount") or 0
        )

        # Some actors return reaction objects instead of counts
        if isinstance(likes, dict):
            likes = likes.get("count", 0)
        if isinstance(comments, dict):
            comments = comments.get("count", 0)

        likes, comments, shares, impressions = (
            int(likes), int(comments), int(shares), int(impressions)
        )

        eng_rate = (
            round((likes + comments + shares) / impressions * 100, 4)
            if impressions > 0 else 0.0
        )
        comment_rate = (
            round(comments / impressions * 100, 4)
            if impressions > 0 else 0.0
        )

        # Extract date and time from published timestamp
        post_date = str(published)[:10] if published else ""
        posted_time = ""
        if published and "T" in str(published):
            try:
                posted_time = str(published)[11:16]  # HH:MM
            except Exception:
                pass

        posts.append({
            "date": post_date,
            "posted_time": posted_time,
            "url": item.get("url") or item.get("postUrl") or item.get("link", ""),
            "likes": likes,
            "comments": comments,
            "shares": shares,
            "impressions": impressions,
            "engagement_rate": eng_rate,
            "comment_rate": comment_rate,
        })
    return posts


def main():
    token = os.environ["APIFY_API_KEY"]
    actor_id = os.environ["APIFY_ACTOR_ID"]  # e.g. "username~actor-name"
    profile_url = os.environ["LINKEDIN_PROFILE_URL"]

    # Actor input — adjust field names to match your actor's input schema
    actor_input = {
        "profileUrls": [profile_url],
        "maxPosts": 30,
    }

    print(f"Running actor: {actor_id}")
    print(f"Profile: {profile_url}")

    items = run_actor_sync(actor_id, actor_input, token)
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
            "hook_text": m.get("hook_text", ""),
            "word_count": m.get("word_count", ""),
            "line_count": m.get("line_count", ""),
            "has_numbers": m.get("has_numbers", ""),
            "has_question_cta": m.get("has_question_cta", ""),
            "hashtag_count": m.get("hashtag_count", ""),
            "lead_magnet_type": m.get("lead_magnet_type", ""),
            "likes": post["likes"],
            "comments": post["comments"],
            "shares": post["shares"],
            "impressions": post["impressions"],
            "engagement_rate": post["engagement_rate"],
            "comment_rate": post["comment_rate"],
            "scraped_at": TODAY,
        }

    write_results(existing)
    print("Done.")


if __name__ == "__main__":
    main()
