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
- **+73% lift. No exceptions. Every post ships with an image.**

### Rule 2: Use specific numbers in the post
- Posts **with** numbers: avg **8,188** (n=24)
- Posts **without** numbers: avg **5,558** (n=41)
- **+47% lift. Include at least one concrete figure (%, $, count, time, speed) per post.**
- Note: numbers are necessary but not sufficient — 4 of the bottom-5 posts also contain numbers. Numbers without salience or specificity don't rescue weak content.

### Rule 3: Zero hashtags
- 0 hashtags: avg **6,842** (n=61)
- 1 hashtag: avg **2,554** (n=2 — small sample, directional)
- Posts with 3 hashtags: score 1,274 (bottom-5). Posts with 5 hashtags: score 667 (bottom-5).
- **Default to 0 hashtags. Do not add hashtags to improve reach — the data shows the opposite effect.**

### Rule 4: Post in the 14:00–19:00 UTC window; anchor on 14:00
- 14:00 UTC: avg **14,974** (n=4) ← best slot
- 16:00 UTC: avg **8,173** (n=6)
- 19:00 UTC: avg **8,120** (n=3)
- 18:00 UTC: avg **6,955** (n=11)
- 17:00 UTC: avg **7,098** (n=3)
- 01:00 UTC: avg **1,880** (n=5) ← worst slot — 71% below corpus average
- 00:00 UTC: avg **7,133** (n=8) — **inflated by one CEO-announcement outlier (score 22,045); do not treat as a reliable window**
- **Primary target: 14:00 UTC. Acceptable range: 16:00–19:00 UTC. Hard avoid: 01:00–03:00 UTC.**

### Rule 5: Short or structured long; never the formless middle
- ≤38 words: avg **7,004**
- 38–59 words: avg **6,671**
- >59 words: avg **5,866**
- Single-line posts: avg **7,777** | 2–3 line posts: avg **5,209** (worst) | >3 line structured posts: avg **7,266**
- Exception: a 296-word CEO announcement posted at midnight scored 22,045 — salience overrides length for tier-1 events
- **Default: ≤50 words in a single punchy block. If writing long (tier-1 announcement only), use >3 clear paragraph breaks. Never write 2–3 unstructured lines — this is the weakest format in the corpus.**

### Rule 6: First-person hook outperforms product-push hook (directional — needs tagging confirmation)
- Top-3 posts open with first-person voice: "Thank you, PM Modi...", "Today I am honored...", "10 PRINT..."
- Bottom-5 posts open with third-person or abstract category statements: "At Microsoft, we believe...", "AI and quantum are transforming...", "Agents will keep joining..."
- **Until hook_type is tagged and this is quantified, default to first-person or named-entity hooks. Avoid category-level abstractions as openers.**

---

## Active Hypotheses

| ID | Hypothesis | Status | Evidence |
|----|-----------|--------|----------|
| H6 | 14:00–16:00 UTC is optimal posting window | **NEAR-CONFIRMED** | 14:00 avg 14,974 (n=4); 16:00 avg 8,173 (n=6); consistent across multiple slots |
| H9 | Named entities in hook drive reposts via news value | **ACTIVE** | All top-5 repost leaders name specific entities; bottom-5 use generic language; needs angle tagging |
| H10 | First-person hook outperforms third-person product-push hook | **ACTIVE** | Top-3 use first-person; bottom-5 use third-person/abstract; needs hook_type tagging |
| H11 | Post salience tier is the dominant predictor of score, overriding format variables | **ACTIVE** | Top-5 all tier-1 events (CEO/PM/major launch); bottom-5 all tier-2/3 feature/abstract posts |
| H12 | 00:00 UTC avg (7,133) is inflated by one outlier; true midnight performance is below average | **ACTIVE** | One post (score 22,045) distorts n=8 average; exclude midnight from default schedule |
| H3 | Question CTAs drive more comments than no CTA | **UNTESTABLE — 0 question-CTA posts in corpus** | Must introduce question CTAs to test |

---

## Retired Hypotheses

| ID | Hypothesis | Outcome |
|----|-----------|--------|
| H1 | "I" statement hooks outperform generic hooks | **INSUFFICIENT DATA** — hook_type never populated; replaced by H10 (qualitative) |
| H2 | Specific numbers outperform vague claims | **CONFIRMED** — +47% lift (8,188 vs. 5,558) |
| H4 | Posts under 200 words outperform posts over 200 words | **DIRECTIONALLY CONFIRMED** — shorter buckets lead; tier-1 salience overrides for long-form |
| H5 | Images are mandatory for top performance | **CONFIRMED** — +73% lift (7,236 vs. 4,174), n=65 |
| H7 | Zero hashtags outperform tagged posts | **CONFIRMED** — 0 tags avg 6,842; all hashtagged posts underperform; bottom-5 includes posts with 3 and 5 hashtags |

---

## Post Formula (Evidence-Revised)

1. **Hook** (line 1): First-person voice OR name a specific entity/product/person — give the reader a news hook or personal stake, not a category observation. Bad: "AI is transforming...". Good: "Today we launched X" or "Thank you [Name] for..."
2. **Body**: Either (a) ≤38 words total in a single punchy block, or (b) for tier-1 announcements only: structured narrative >3 lines with clear paragraph breaks. Never write 2–3 unstructured lines.
3. **Numbers**: At least one concrete figure per post (%, $, time, count, speed benchmark).
4. **Image**: Always. No exceptions.
5. **Hashtags**: None. Do not add hashtags.
6. **CTA**: Introduce question-based CTAs — zero exist in the current dataset, so this is the highest-priority format experiment.

---

## Salience Tier Framework

All top-5 posts are tier-1 events. Format optimization matters most at tier-2 and tier-3. Tier-1 posts can survive format imperfections (e.g., midnight posting, 296 words) because content salience dominates.

| Tier | Definition | Realistic score range | Format priority |
|------|-----------|----------------------|----------------|
| 1 | CEO/head-of-state interaction, major executive appointment, flagship product launch, landmark partnership | 15,000–30,000+ | Format still matters but salience drives most of the variance |
| 2 | Named product launch, significant partnership, AI infrastructure announcement | 5,000–18,000 | Format rules apply fully; follow all confirmed rules |
| 3 | Feature release, abstract trend commentary, enterprise product update | 1,000–6,000 | Maximum format discipline required; even then ceiling is low |

**Implication**: Increase tier-1 event post frequency. Reduce standalone tier-3 feature-release posts unless paired with a tier-1 hook.

---

## Posting Schedule

- **Primary window**: 14:00 UTC (avg 14,974 — 2.3× corpus average)
- **Acceptable secondary**: 16:00–19:00 UTC (avg scores 6,955–8,173)
- **Avoid**: 01:00–03:00 UTC (avg 1,880–4,250 — 35–71% below corpus average)
- **Do not schedule for 00:00 UTC** — the avg of 7,133 is an outlier artifact from one CEO announcement; the underlying slot is unreliable

---

## Voice & Tone

- Direct — no fluff, no corporate-speak
- First-person or named-entity opening — personal stake or specific news, not category claims
- Peer-to-peer: colleague sharing a discovery or milestone, not a brand broadcasting a feature
- News-aware: posts referencing real events (appointments, partnerships, head-of-state meetings) generate significantly more reposts
- Concrete always beats abstract: name the product, the person, the number
- Honest about failures, not just wins

---

## Content Mix (Target)

| Theme | % | Example angle |
|-------|---|---------------|
| AI product / major launch announcements (tier-1/2) | 35% | Named product + specific capability + concrete number, first-person if possible |
| Leadership / milestone / personal (tier-1) | 25% | First-person voice + named context + one data point or outcome |
| Tech culture / honest takes | 20% | Contrarian or counterintuitive claim backed by a number, short format |
| Partnership / ecosystem news (tier-1/2) | 20% | Named companies + what it means in one punchy line + number |

---

## Data Gaps — Fields That Must Be Populated

The following fields are empty across all 65 posts. Analysis is blocked until tagging is applied:

- `hook_type` — **highest priority**; required to confirm H10 and build hook taxonomy
- `content_theme` — required to measure theme performance and validate content mix targets
- `angle` — required to confirm H9 and H10; identify winning framing patterns
- `lead_magnet_type` — required to measure lead magnet impact
- `topic` — required for niche-level breakdown

**Action required**: Backfill these fields for the most recent 20 posts before the next strategy update. Without hook_type, the two most actionable hypotheses (H9, H10) remain unquantified.

---

## Experiments Queue (Next 30 Days)

1. **Introduce question CTAs** on 5 posts — measure comment_ratio vs. 0.065 baseline (tests H3). This is the only major format variable with zero data points.
2. **Tag hook_type on last 20 posts** — backfill to confirm H10 (first-person vs. third-person hook lift) and unblock H9 analysis.
3. **Anchor 5 consecutive posts to 14:00 UTC exactly** — build confidence interval around best time slot (currently n=4).
4. **Pair tier-3 feature posts with a tier-1 angle** — e.g., instead of "MAI-Image-2-Efficient is now live" (score 1,389), frame as a first-person milestone with a named context. Test whether hook reframing lifts tier-3 content into tier-2 range.
5. **A/B format test**: 5 posts at ≤38 words vs. 5 posts at >3 structured lines — same topic, same hour — to formally test the line-count U-curve.

---

## What's Not Working

- **Mid-length unstructured posts (2–3 lines)**: avg 5,209 — worst line-count bucket in the corpus
- **Hashtag use**: every hashtagged post underperforms; bottom-5 includes the only posts with 3+ hashtags
- **Late-night posting (01:00 UTC)**: avg 1,880 — 71% below corpus average
- **Abstract benefit-led hooks**: "AI and quantum are transforming...", "Agents will keep joining...", "At Microsoft, we believe..." — all appear in bottom-5; category abstractions do not hook readers
- **Posts without images**: avg 4,174 — 36% below corpus average
- **Tier-3 standalone feature announcements**: short hook + no named person + no broader context = bottom-5 territory regardless of format execution (see: MAI-Image-2-Efficient post, score 1,389)

---

*Strategy auto-updated from 65-post performance dataset. Next review triggers at 75 posts or 30 days, whichever comes first.*