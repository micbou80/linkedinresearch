# LinkedIn Lead Magnet System — Dashboard

> Updated by scrape.py daily.

## Quick Stats

| Metric | Value |
|--------|-------|
| Total Posts | 0 |
| Avg Engagement Rate | — |
| Best Performing Post | — |
| Lead Magnets Created | 0 |
| Last Scraped | — |

## Navigation

- [[Analytics/engagement_log|Engagement Log]]
- [[Agent/prompts|Prompts (evolving)]]
- [[Agent/research_brief|Research Brief]]

## How It Works

1. **Daily 8am UTC** — `generate.py` creates today's post + lead magnet using current `prompts.md`
2. **Daily 8pm UTC** — `scrape.py` pulls engagement metrics from LinkedIn via Apify
3. **Every Monday 9am UTC** — `analyze.py` reads performance data, rewrites `prompts.md` to improve future content

The system learns what works and updates its own prompts automatically.
