# LinkedIn Autoresearch

Autonomous LinkedIn content engine. Creates daily posts + lead magnets, tracks engagement, and self-improves its own strategy via an autoresearch loop.

## How It Works

```
[strategy.md + research] → generate_content.py → Post + Lead Magnet
                                                           ↓
                                                  [Michel publishes manually]
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
| `val_bpb` metric | `engagement_score` in `results.tsv` |
| Agent modifies code | `autoresearch.py` rewrites strategy |

## Agents

| Script | Role | Schedule |
|--------|------|----------|
| `pipeline/research.py` | Reddit + blogs → topic ideas | Daily 6am UTC |
| `pipeline/generate_content.py` | Research + strategy → post + lead magnet | Daily 6am UTC |
| `pipeline/apify_scraper.py` | LinkedIn → results.tsv | Daily 8pm UTC |
| `pipeline/autoresearch.py` | results.tsv → strategy.md rewrite | Mon + Thu 6am UTC |

## GitHub Secrets Required

Only **2 secrets** needed:

| Secret | Description |
|--------|-------------|
| `ANTHROPIC_API_KEY` | Claude API key |
| `APIFY_API_KEY` | Apify API key |

Everything else (actor ID, LinkedIn username) is hardcoded as public information.

## Tracking Schema (`results.tsv`)

| Field | Source | Tests |
|-------|--------|-------|
| `hook_type` | frontmatter | H1: I-statement vs stat vs reframe |
| `hook_text` | frontmatter / scraped | Pattern analysis |
| `angle` | frontmatter | how_to vs contrarian vs data_led |
| `word_count` | auto-computed | H4: optimal post length |
| `line_count` | auto-computed | Formatting density |
| `has_numbers` | auto-computed | H2: specific numbers |
| `has_question_cta` | auto-computed | H3: question vs resource CTA |
| `has_image` | scraped | Image vs text-only |
| `hashtag_count` | auto-computed | Tag volume |
| `total_reactions` | scraped | Volume signal |
| `insight_reactions` | scraped | B2B quality signal |
| `comments` | scraped | Depth signal |
| `engagement_score` | computed | Primary metric: reactions+(comments×3)+(reposts×2) |
| `comment_ratio` | computed | comments/reactions |
| `insight_ratio` | computed | insight/reactions |

## Obsidian Sync
Install [Obsidian Git plugin](https://github.com/denolehov/obsidian-git), point to this repo, auto-pull every 5 min.
