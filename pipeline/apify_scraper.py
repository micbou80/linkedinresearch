#!/usr/bin/env python3
"""Metrics agent — scrapes LinkedIn via Apify, appends to results.tsv."""

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
FIELDS = ["date", "post_url", "topic", "hook_type", "likes", "comments", "shares", "impressions", "engagement_rate", "scraped_at"]


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
    posts_dir = VAULT_ROOT / "Posts"
    meta = {}
    if not posts_dir.exists():
        return meta
    for f in posts_dir.glob("*.md"):
        c = f.read_text(encoding="utf-8")
        topic = re.search(r'^topic: "(.*?)"', c, re.MULTILINE)
        hook = re.search(r'^hook_type: (\S+)', c, re.MULTILINE)
        meta[f.stem] = {
            "topic": topic.group(1) if topic else "",
            "hook_type": hook.group(1) if hook else ""
        }
    return meta


def load_existing() -> dict:
    if not RESULTS.exists():
        return {}
    with open(RESULTS, newline="", encoding="utf-8") as f:
        return {r["date"]: r for r in csv.DictReader(f, delimiter="\t")}


def write_results(rows: dict):
    sorted_rows = sorted(rows.values(), key=lambda x: x["date"], reverse=True)
    with open(RESULTS, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS, delimiter="\t")
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
        rate = round((likes + comments + shares) / impressions * 100, 4) if impressions > 0 else 0.0
        posts.append({
            "date": str(published)[:10] if published else "",
            "url": item.get("url") or item.get("postUrl", ""),
            "likes": likes, "comments": comments, "shares": shares,
            "impressions": impressions, "engagement_rate": rate
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
            "post_url": post["url"],
            "topic": m.get("topic", ""),
            "hook_type": m.get("hook_type", ""),
            "likes": post["likes"],
            "comments": post["comments"],
            "shares": post["shares"],
            "impressions": post["impressions"],
            "engagement_rate": post["engagement_rate"],
            "scraped_at": TODAY
        }

    write_results(existing)
    print("Done.")


if __name__ == "__main__":
    main()
