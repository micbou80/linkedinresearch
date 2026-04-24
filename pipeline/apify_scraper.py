#!/usr/bin/env python3
"""Metrics agent — scrapes LinkedIn via Apify, updates results.tsv with full signal set."""

import os
import csv
import json
import re
import time
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


def apify(method, path, data=None, token=""):
    url = f"{APIFY_BASE}{path}?token={token}"
    body = json.dumps(data).encode() if data else None
    req = urllib.request.Request(url, data=body, headers={"Content-Type": "application/json"} if body else {}, method=method)
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.loads(r.read())


def run_actor(actor_id, input_data, token):
    res = apify("POST", f"/acts/{urllib.parse.quote(actor_id, safe='')}/runs", input_data, token)
    run_id = res["data"]["id"]
    print(f"Run: {run_id}")
    while True:
        s = apify("GET", f"/actor-runs/{run_id}", token=token)["data"]
        print(f"Status: {s['status']}")
        if s["status"] == "SUCCEEDED":
            return s["defaultDatasetId"]
        if s["status"] in ("FAILED", "ABORTED", "TIMED-OUT"):
            raise RuntimeError(f"Actor {s['status']}")
        time.sleep(10)


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
            pattern = rf'^{field}: "?(.*?)"?$'
            m = re.search(pattern, c, re.MULTILINE)
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


def parse(raw: list) -> list:
    posts = []
    for item in raw:
        published = item.get("publishedAt") or item.get("postedAt") or item.get("date", "")
        likes = item.get("likes") or item.get("numLikes") or 0
        comments = item.get("comments") or item.get("numComments") or 0
        shares = item.get("shares") or item.get("numShares") or 0
        impressions = item.get("impressions") or item.get("views") or 0
        if isinstance(likes, dict): likes = likes.get("count", 0)
        if isinstance(comments, dict): comments = comments.get("count", 0)
        likes, comments, shares, impressions = int(likes), int(comments), int(shares), int(impressions)
        eng_rate = round((likes + comments + shares) / impressions * 100, 4) if impressions > 0 else 0.0
        comment_rate = round(comments / impressions * 100, 4) if impressions > 0 else 0.0
        # Try to extract publish time (HH:MM)
        posted_time = ""
        if published and "T" in str(published):
            try:
                posted_time = str(published)[11:16]  # e.g. "09:30"
            except Exception:
                pass
        posts.append({
            "date": str(published)[:10] if published else "",
            "posted_time": posted_time,
            "url": item.get("url") or item.get("postUrl", ""),
            "likes": likes, "comments": comments, "shares": shares,
            "impressions": impressions, "engagement_rate": eng_rate,
            "comment_rate": comment_rate
        })
    return posts


def main():
    token = os.environ["APIFY_API_KEY"]
    actor_id = os.environ.get("APIFY_ACTOR_ID", "curious_coder/linkedin-profile-posts-scraper")
    profile_url = os.environ["LINKEDIN_PROFILE_URL"]

    print(f"Scraping: {profile_url}")
    dataset_id = run_actor(actor_id, {"profileUrls": [profile_url], "maxPosts": 30}, token)
    items = apify("GET", f"/datasets/{dataset_id}/items", token=token).get("items", [])
    print(f"Got {len(items)} items")

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
            "scraped_at": TODAY
        }

    write_results(existing)
    print("Done.")


if __name__ == "__main__":
    main()
