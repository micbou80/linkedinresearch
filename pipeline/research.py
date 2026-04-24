#!/usr/bin/env python3
"""Research agent — scrapes Reddit + Microsoft blogs + AI news, synthesizes topic ideas."""

import os
import json
import re
import urllib.request
from datetime import date
from pathlib import Path
import anthropic

VAULT_ROOT = Path(__file__).parent.parent
TODAY = date.today().isoformat()

MICROSOFT_BLOG_FEEDS = [
    "https://techcommunity.microsoft.com/t5/Microsoft-Teams-Blog/bg-p/MicrosoftTeamsBlog.rss",
    "https://techcommunity.microsoft.com/t5/microsoft-365-blog/bg-p/Microsoft365Blog.rss",
]

AI_NEWS_FEEDS = [
    "https://feeds.feedburner.com/venturebeat/SZYF",  # VentureBeat AI
    "https://www.technologyreview.com/feed/",
]


def fetch_url(url: str, timeout: int = 10) -> str:
    try:
        req = urllib.request.Request(
            url,
            headers={"User-Agent": "Mozilla/5.0 (compatible; linkedin-research-bot/1.0)"}
        )
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return resp.read().decode("utf-8", errors="ignore")[:8000]
    except Exception as e:
        print(f"Fetch error {url}: {e}")
        return ""


def fetch_reddit(subreddits_config: dict) -> list:
    """Fetch hot posts via Reddit JSON API (no auth required)."""
    posts = []
    for category, subs in subreddits_config.items():
        for subreddit in subs[:3]:  # max 3 per category to stay within rate limits
            try:
                url = f"https://www.reddit.com/r/{subreddit}/hot.json?limit=5"
                raw = fetch_url(url)
                if not raw:
                    continue
                data = json.loads(raw)
                for child in data.get("data", {}).get("children", []):
                    p = child["data"]
                    if p.get("score", 0) > 50 and not p.get("stickied"):
                        posts.append({
                            "title": p["title"],
                            "url": f"https://reddit.com{p['permalink']}",
                            "subreddit": subreddit,
                            "category": category,
                            "score": p["score"],
                            "comments": p.get("num_comments", 0),
                            "preview": p.get("selftext", "")[:200]
                        })
            except Exception as e:
                print(f"Reddit error r/{subreddit}: {e}")
    return sorted(posts, key=lambda x: x["score"], reverse=True)


def fetch_rss_titles(feeds: list) -> list:
    """Extract article titles from RSS feeds."""
    titles = []
    for feed_url in feeds:
        raw = fetch_url(feed_url)
        if raw:
            found = re.findall(r"<title><!\[CDATA\[(.*?)\]\]></title>|<title>(.*?)</title>", raw)
            for match in found[:5]:
                title = (match[0] or match[1]).strip()
                if title and len(title) > 10:
                    titles.append({"title": title, "source": feed_url})
    return titles


def synthesize(client: anthropic.Anthropic, reddit_posts: list, blog_titles: list, strategy: str) -> str:
    reddit_str = json.dumps(reddit_posts[:15], indent=2)
    blogs_str = json.dumps(blog_titles[:10], indent=2)

    resp = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=2500,
        system=f"""You are a LinkedIn content research analyst. Scan today's signal and identify the 5 strongest topic ideas.

Audience: IT professionals and enthusiasts who need practical AI help and are into Future of Work.
Niche: AI | Leadership | Future of Work | Tech Culture

Current strategy:
{strategy}

Key constraint: every topic idea must have a compelling first-person hook — start with "I" and a specific personal result.""",
        messages=[{"role": "user", "content": f"""Today's signal:

REDDIT HOT POSTS:
{reddit_str}

MICROSOFT + TECH BLOG HEADLINES:
{blogs_str}

Generate 5 topic ideas. For each:
1. Topic angle (specific, not generic)
2. Draft "I" statement hook (personal experience + concrete result)
3. Lead magnet idea that pairs with it
4. Why this is timely today

Format as markdown with ## headings."""}]
    )
    return resp.content[0].text


def main():
    api_key = os.environ["ANTHROPIC_API_KEY"]
    client = anthropic.Anthropic(api_key=api_key)

    subreddits_path = VAULT_ROOT / "data" / "subreddits.json"
    with open(subreddits_path) as f:
        subreddits = json.load(f)

    strategy_path = VAULT_ROOT / "strategy.md"
    strategy = strategy_path.read_text(encoding="utf-8") if strategy_path.exists() else ""

    print("Fetching Reddit...")
    reddit_posts = fetch_reddit(subreddits)
    print(f"Got {len(reddit_posts)} Reddit posts")

    print("Fetching blog feeds...")
    blog_titles = fetch_rss_titles(MICROSOFT_BLOG_FEEDS + AI_NEWS_FEEDS)
    print(f"Got {len(blog_titles)} blog headlines")

    print("Synthesizing topics...")
    topics_md = synthesize(client, reddit_posts, blog_titles, strategy)

    (VAULT_ROOT / "data").mkdir(exist_ok=True)
    content = f"# Daily Research — {TODAY}\n\n## Top Reddit Signal\n\n"
    content += "\n".join(f"- **{p['title'][:80]}** — r/{p['subreddit']} ({p['score']} pts)" for p in reddit_posts[:10])
    content += f"\n\n## Microsoft & AI Blog Headlines\n\n"
    content += "\n".join(f"- {t['title']}" for t in blog_titles[:8])
    content += f"\n\n---\n\n## Synthesized Topic Ideas\n\n{topics_md}\n"

    (VAULT_ROOT / "data" / "research_today.md").write_text(content, encoding="utf-8")
    print("Saved: data/research_today.md")


if __name__ == "__main__":
    main()
