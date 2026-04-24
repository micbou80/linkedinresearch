#!/usr/bin/env python3
"""Daily LinkedIn engagement metrics scraper via Apify."""

import os
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


def apify_request(method: str, path: str, data: dict = None, token: str = "") -> dict:
    url = f"{APIFY_BASE}{path}?token={token}"
    body = json.dumps(data).encode() if data else None
    headers = {"Content-Type": "application/json"} if body else {}
    req = urllib.request.Request(url, data=body, headers=headers, method=method)
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read())


def run_actor(actor_id: str, input_data: dict, token: str) -> list:
    result = apify_request(
        "POST",
        f"/acts/{urllib.parse.quote(actor_id, safe='')}/runs",
        input_data,
        token
    )
    run_id = result["data"]["id"]
    print(f"Actor run started: {run_id}")

    while True:
        status = apify_request("GET", f"/actor-runs/{run_id}", token=token)
        run_status = status["data"]["status"]
        print(f"Status: {run_status}")
        if run_status == "SUCCEEDED":
            dataset_id = status["data"]["defaultDatasetId"]
            break
        if run_status in ("FAILED", "ABORTED", "TIMED-OUT"):
            raise RuntimeError(f"Actor run {run_status}")
        time.sleep(10)

    items = apify_request("GET", f"/datasets/{dataset_id}/items", token=token)
    return items.get("items", [])


def parse_metrics(raw: list) -> list:
    posts = []
    for item in raw:
        text = item.get("text") or item.get("content") or item.get("description", "")
        published = item.get("publishedAt") or item.get("postedAt") or item.get("date", "")
        likes = item.get("likes") or item.get("numLikes") or 0
        comments = item.get("comments") or item.get("numComments") or 0
        shares = item.get("shares") or item.get("numShares") or 0
        impressions = item.get("impressions") or item.get("views") or 0

        if isinstance(likes, dict):
            likes = likes.get("count", 0)
        if isinstance(comments, dict):
            comments = comments.get("count", 0)

        engagement_rate = 0.0
        if impressions > 0:
            engagement_rate = round((likes + comments + shares) / impressions * 100, 4)

        post_date = str(published)[:10] if published else ""

        posts.append({
            "date": post_date,
            "url": item.get("url") or item.get("postUrl", ""),
            "text_preview": text[:200] if text else "",
            "likes": int(likes),
            "comments": int(comments),
            "shares": int(shares),
            "impressions": int(impressions),
            "engagement_rate": engagement_rate,
            "scraped_at": TODAY
        })
    return posts


def update_engagement_json(new_posts: list):
    data_path = VAULT_ROOT / "data" / "engagement.json"
    data_path.parent.mkdir(exist_ok=True)
    existing = {"posts": [], "last_scraped": ""}
    if data_path.exists():
        with open(data_path) as f:
            existing = json.load(f)
    by_date = {p["date"]: p for p in existing["posts"] if p["date"]}
    for post in new_posts:
        if post["date"]:
            by_date[post["date"]] = post
    existing["posts"] = sorted(by_date.values(), key=lambda x: x["date"], reverse=True)
    existing["last_scraped"] = TODAY
    with open(data_path, "w") as f:
        json.dump(existing, f, indent=2)
    print(f"engagement.json: {len(existing['posts'])} posts")


def update_engagement_log(posts: list):
    log_path = VAULT_ROOT / "Analytics" / "engagement_log.md"
    log_path.parent.mkdir(exist_ok=True)
    if not log_path.exists():
        log_path.write_text(
            "# Engagement Log\n\n*Updated daily by scrape.py*\n\n"
            "| Date | Likes | Comments | Shares | Impressions | Engagement Rate |\n"
            "|------|-------|----------|--------|-------------|----------------|\n",
            encoding="utf-8"
        )
    log = log_path.read_text(encoding="utf-8")
    for post in sorted(posts, key=lambda x: x["date"]):
        d = post["date"]
        if not d:
            continue
        row = f"| {d} | {post['likes']} | {post['comments']} | {post['shares']} | {post['impressions']} | {post['engagement_rate']}% |"
        if d in log:
            log = re.sub(rf"\| {d} \|.*\n", row + "\n", log)
        else:
            log += row + "\n"
    log_path.write_text(log, encoding="utf-8")


def update_post_frontmatter(post: dict):
    d = post.get("date", "")
    if not d:
        return
    post_file = VAULT_ROOT / "Posts" / f"{d}.md"
    if not post_file.exists():
        return
    content = post_file.read_text(encoding="utf-8")
    for field in ("likes", "comments", "shares", "impressions", "engagement_rate"):
        content = re.sub(
            rf"(  {field}: )[\d.]+",
            rf"\g<1>{post[field]}",
            content
        )
    post_file.write_text(content, encoding="utf-8")
    print(f"Updated frontmatter: Posts/{d}.md")


def main():
    token = os.environ["APIFY_API_KEY"]
    actor_id = os.environ.get("APIFY_ACTOR_ID", "curious_coder/linkedin-profile-posts-scraper")
    profile_url = os.environ["LINKEDIN_PROFILE_URL"]

    print(f"Scraping: {profile_url}")
    raw = run_actor(actor_id, {"profileUrls": [profile_url], "maxPosts": 30}, token)
    print(f"Got {len(raw)} raw items")

    posts = parse_metrics(raw)
    update_engagement_json(posts)
    update_engagement_log(posts)
    for post in posts:
        update_post_frontmatter(post)

    print("Scrape complete.")


if __name__ == "__main__":
    main()
