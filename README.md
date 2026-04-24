# LinkedIn Autoresearch

Autonomous LinkedIn content engine. Creates daily posts + lead magnets, tracks engagement, and self-improves its own strategy via an autoresearch loop.

## How It Works

```
[strategy.md + research] → generate_content.py → Post + Lead Magnet
                                                           ↓
                                                  [You publish manually]
                                                           ↓
                                          apify_scraper.py → results.tsv
                                                           ↓
                                          autoresearch.py → updated strategy.md
                                                           ↑
                                                       [repeat]
```

| autoresearch analogy | this system |
|---------------------|-------------|
| `train.py` | `strategy.md` |
| `program.md` | `Agent/research_brief.md` |
| `val_bpb` metric | `engagement_rate` in `results.tsv` |
| Agent modifies code | `autoresearch.py` rewrites strategy |

## Agents

| Script | Role | Schedule |
|--------|------|----------|
| `pipeline/research.py` | Reddit + blogs → topic ideas | Daily 6am UTC |
| `pipeline/generate_content.py` | Research + strategy → post + lead magnet | Daily 6am UTC |
| `pipeline/apify_scraper.py` | LinkedIn → results.tsv | Daily 8pm UTC |
| `pipeline/autoresearch.py` | results.tsv → strategy.md rewrite | Mon + Thu 6am UTC |

## Setup

### GitHub Secrets

| Secret | Description |
|--------|-------------|
| `ANTHROPIC_API_KEY` | Claude API key |
| `APIFY_API_KEY` | Apify API key |
| `APIFY_ACTOR_ID` | LinkedIn Profile Post Scraper actor ID |
| `LINKEDIN_PROFILE_URL` | Your LinkedIn profile URL |
| `BLOTATO_API_KEY` | (Optional) BloTato key for auto-publish |

### Obsidian Sync
Install [Obsidian Git plugin](https://github.com/denolehov/obsidian-git), point to this repo, auto-pull every 5 min.

## File Structure

```
pipeline/           ← Agent scripts
data/
  subreddits.json   ← Reddit communities to monitor
  research_today.md ← Daily synthesized topics (overwritten daily)
Posts/              ← Generated daily posts
Lead Magnets/       ← Generated lead magnets
Analytics/          ← Autoresearch reports
strategy.md         ← Evolving content playbook (auto-updated)
results.tsv         ← Post performance log
examples/           ← Your best posts (add these for voice matching)
```

## Adding Your Example Posts

Paste your best-performing LinkedIn posts into `examples/example1.md` etc.
The content agent reads these for voice and style matching.
