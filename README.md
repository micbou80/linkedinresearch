# LinkedIn Lead Magnet Research System

Autonomous LinkedIn content engine that creates daily lead magnets and posts, tracks engagement, and self-improves via weekly analysis — modeled on the autoresearch optimization loop.

## How It Works

```
[prompts.md] → generate.py → Post + Lead Magnet
                                       ↓
                               [You publish to LinkedIn]
                                       ↓
                               scrape.py (Apify) → engagement.json
                                       ↓
                               analyze.py → updated prompts.md
                                       ↑
                                   [repeat]
```

Like autoresearch:
- **`prompts.md`** = `train.py` (the thing the agent improves)
- **`research_brief.md`** = `program.md` (fixed objective)
- **`engagement_rate`** = `val_bpb` (the metric to optimize)
- **`analyze.py`** = the agent that rewrites the config

## Setup

### 1. GitHub Secrets

Go to **Settings → Secrets → Actions** and add:

| Secret | Description |
|--------|-------------|
| `ANTHROPIC_API_KEY` | Claude API key |
| `APIFY_API_KEY` | Apify API key |
| `APIFY_ACTOR_ID` | LinkedIn scraper actor ID (e.g. `curious_coder/linkedin-profile-posts-scraper`) |
| `LINKEDIN_PROFILE_URL` | Your LinkedIn profile URL |

### 2. Obsidian Sync

Install the [Obsidian Git plugin](https://github.com/denolehov/obsidian-git) in your LinkedIn vault. Point it to this repo. Set auto-pull to every 5 minutes — GitHub Actions will push new content daily and Obsidian will pick it up automatically.

## Schedule

| Time (UTC) | Action |
|------------|--------|
| 8:00 daily | Generate post + lead magnet |
| 20:00 daily | Scrape engagement metrics |
| 9:00 Monday | Run analysis, update prompts |

## Vault Structure

```
Posts/               ← Daily LinkedIn posts (generated)
Lead Magnets/        ← Daily lead magnets (generated)
Analytics/           ← Engagement log + weekly analyses
Agent/
  prompts.md         ← Evolving generation prompts (auto-updated)
  research_brief.md  ← Fixed optimization objective (edit manually)
data/
  engagement.json    ← Raw metrics store
scripts/             ← Python automation
Dashboard.md         ← Obsidian overview
```
