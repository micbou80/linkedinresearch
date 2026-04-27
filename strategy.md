# Content Strategy

*Initialized: 2026-04-24 | Auto-updated: Mon + Thu 6am UTC by autoresearch.py*

---

## Data Baseline (65 posts)

| Metric | Value |
|--------|-------|
| Avg engagement score | 6,529 |
| Avg comment ratio | 0.065 |
| Avg insight ratio | 0.025 |
| Formula | reactions + (comments×3) + (reposts×2) |

---

## Confirmed Rules (Data-Backed)

### Rule 1: Always include an image
- Posts **with** images: avg **7,236** (n=50)
- Posts **without** images: avg **4,174** (n=15)
- **+73% lift. Non-negotiable.**

### Rule 2: Use specific numbers in the post
- Posts **with** numbers: avg **8,188** (n=24)
- Posts **without** numbers: avg **5,558** (n=41)
- **+47% lift. Every post should contain at least one concrete figure.**

### Rule 3: Zero hashtags
- 0 hashtags: avg **6,842** (n=61)
- 1 hashtag: avg **2,554** (n=2 — small sample, treat as directional)
- Bottom-5 posts include the only posts with 3 and 5 hashtags (scores 1,274 and 667)
- **Previous recommendation of 3–5 hashtags is REVERSED. Default to 0.**

### Rule 4: Post between 14:00–16:00 UTC
- 14:00 UTC: avg **14,974** (n=4) ← best slot
- 16:00 UTC: avg **8,173** (n=6)
- 19:00 UTC: avg **8,120** (n=3)
- 01:00 UTC: avg **1,880** (n=5) ← worst slot
- **Target 14:00–16:00 UTC. Avoid 01:00–03:00 UTC.**

### Rule 5: Favor short posts, but structured long posts can work
- ≤38 words: avg **7,004**
- 38–59 words: avg **6,671**
- >59 words: avg **5,866**
- Exception: single-line posts avg **7,777**; structured posts >3 lines avg **7,266**; the 2–3 line mid-format is the weakest at **5,209**
- **Default to ≤50 words. If going long, use clear structure with line breaks (>3 lines). Avoid the formless middle.** 

---

## Active Hypotheses

| ID | Hypothesis | Status | Evidence |
|----|-----------|--------|----------|
| H5 | Images are mandatory for top performance | **TESTING → near-confirmed** | +73% lift, n=65 |
| H6 | 14:00–16:00 UTC is optimal posting window | **TESTING** | 14:00 avg 14,974 (n=4); needs more reps |
| H7 | Zero hashtags outperform tagged posts | **TESTING → near-confirmed** | 0 tags avg 6,842; tagged posts in bottom-5 |
| H8 | Organic posts realistically target 5,000–15,000 score range; top-5 are outlier authority events | **TESTING** | Top 5 all involve CEO/PM/major launch news |
| H9 | Named entities (companies, people, products) in hook drive reposts via news value | **TESTING** | Top repost posts all name specific entities |
| H3 | Question CTAs drive more comments than resource CTAs | **UNTESTABLE** | 0 question-CTA posts in dataset — must introduce |

---

## Retired Hypotheses

| ID | Hypothesis | Outcome |
|----|-----------|--------|
| H1 | "I" statement hooks outperform generic hooks | **INSUFFICIENT DATA** — hook_type field unpopulated across all 65 posts |
| H2 | Specific numbers outperform vague claims | **CONFIRMED** — +47% lift (8,188 vs. 5,558) |
| H4 | Posts under 200 words outperform posts over 200 words | **DIRECTIONALLY CONFIRMED** — shorter buckets consistently lead, with structured exceptions |

---

## Post Formula (Evidence-Revised)

1. **Hook** (line 1): Name a specific entity, product, number, or event — give the reader a news hook, not a generic observation
2. **Body**: Either (a) ≤38 words total in a single punchy block, or (b) structured narrative >3 lines with clear paragraph breaks — avoid the 2–3 line formless middle
3. **Numbers**: Include at least one concrete figure (%, $, time, count)
4. **Image**: Always. No exceptions.
5. **Hashtags**: None (default). Do not add hashtags.
6. **CTA**: Test question-based CTAs — currently zero exist in the dataset, so this is the highest-priority experiment to run

---

## Posting Schedule

- **Primary window**: 14:00–16:00 UTC (avg scores 8,173–14,974)
- **Acceptable secondary**: 17:00–19:00 UTC (avg scores 7,098–8,120)
- **Avoid**: 01:00–03:00 UTC (avg scores 1,880–4,250)

---

## Voice & Tone

- Direct — no fluff, no corporate-speak
- Name specific things: products, people, companies, numbers
- Peer-to-peer: colleague sharing a discovery, not expert lecturing
- News-aware: posts that reference real events generate significantly more reposts (H9)
- Honest about failures, not just wins

---

## Content Mix (Target)

| Theme | % | Example angle |
|-------|---|---------------|
| AI product / launch announcements | 35% | Named product + specific capability + concrete number |
| Leadership / Future of Work | 30% | Pattern observed + named context + one data point |
| Tech culture / honest takes | 20% | Contrarian or counterintuitive claim backed by a number |
| Partnership / ecosystem news | 15% | Named companies + what it means in one line |

---

## Data Gaps — Fields That Must Be Populated

The following fields are empty across all 65 posts. Analysis is blocked until tagging is applied:

- `hook_type` — required to test H1 and develop hook taxonomy
- `content_theme` — required to measure theme performance
- `angle` — required to identify winning framing patterns
- `lead_magnet_type` — required to measure lead magnet impact
- `topic` — required for niche-level breakdown

**Action required**: Backfill these fields for the most recent 20 posts before the next strategy update.

---

## Experiments Queue (Next 30 Days)

1. **Introduce question CTAs** on 5 posts — measure comment_ratio vs. 0.065 baseline (tests H3)
2. **Name a specific person or company in every hook** for 10 posts — measure repost lift (tests H9)
3. **Backfill hook_type tags** on last 20 posts to unblock H1 analysis
4. **A/B format test**: 5 posts at ≤38 words vs. 5 posts at >3 structured lines — same topic, same hour, measure score difference (tests line-count U-curve hypothesis)

---

## What's Not Working

- **Mid-length unstructured posts (2–3 lines)**: avg 5,209 — worst line-count bucket
- **Hashtag use**: correlated with bottom-5 performance; remove entirely
- **Late-night posting (01:00 UTC)**: avg 1,880 — 71% below corpus average
- **Abstract benefit-led hooks** ("AI and quantum are transforming...", "Agents will keep joining..."): both appear in bottom-5; specificity beats abstraction
- **Posts without images**: avg 4,174 — 36% below corpus average

---

*Strategy auto-updated from 65-post performance dataset. Next review triggers at 75 posts or 30 days, whichever comes first.*
