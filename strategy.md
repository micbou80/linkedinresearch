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
- **+73% lift. This is the strongest confirmed format variable. No exceptions. Every post ships with an image.**

### Rule 2: Use specific numbers in the post
- Posts **with** numbers: avg **8,188** (n=24)
- Posts **without** numbers: avg **5,558** (n=41)
- **+47% lift. Include at least one concrete figure (%, $, count, time, speed) per post.**
- Critical caveat: 4 of the bottom-5 posts also contain numbers. Numbers amplify strong content but do not rescue weak salience or abstract hooks. Numbers are necessary, not sufficient.

### Rule 3: Zero hashtags
- 0 hashtags: avg **6,842** (n=61)
- 1 hashtag: avg **2,554** (n=2 — directional only)
- Posts with 3 hashtags: score 1,274 (bottom-5). Posts with 5 hashtags: score 667 (bottom-5).
- **Default to 0 hashtags. The data shows hashtags are negatively correlated with performance at every count level observed. Do not add hashtags to improve reach.**

### Rule 4: Post at 14:00 UTC; acceptable range 16:00–19:00 UTC
- 14:00 UTC: avg **14,974** (n=4) ← best slot, 2.3× corpus average
- 16:00 UTC: avg **8,173** (n=6)
- 19:00 UTC: avg **8,120** (n=3)
- 18:00 UTC: avg **6,955** (n=11) ← highest-confidence secondary slot
- 17:00 UTC: avg **7,098** (n=3)
- 01:00 UTC: avg **1,880** (n=5) ← worst confirmed slot, 71% below corpus average
- 00:00 UTC: avg **7,133** (n=8) — **inflated by one CEO-announcement outlier (score 22,045); do not treat as a reliable window**
- 02:00 UTC: avg **4,250** (n=3) — below average
- **Primary target: 14:00 UTC. Note: n=4 still has a wide confidence interval — H13 suggests some of this lift may be salience-driven. Acceptable range: 16:00–19:00 UTC. Hard avoid: 01:00–03:00 UTC.**

### Rule 5: Short or structured long; never the formless middle
- ≤38 words: avg **7,004**
- 38–59 words: avg **6,671**
- >59 words: avg **5,866**
- Single-line posts: avg **7,777** | 2–3 line posts: avg **5,209** (worst) | >3 line structured posts: avg **7,266**
- Tier-1 exception: a 296-word CEO announcement at midnight scored 22,045 — salience overrides format at tier-1
- **Default: ≤50 words in a single punchy block. If writing long (tier-1 announcement only), use >3 clear paragraph breaks. Never write 2–3 unstructured lines — this is the weakest format in the corpus, 33% below single-line.**

### Rule 6: First-person or named-entity hook; never abstract-benefit opener
- Top-3 posts open with first-person or named-entity hooks: "Thank you, PM Narendra Modi ji...", "Today I am honored to step into the role of CEO...", "10 PRINT \"ANTHROPIC + MICROSOFT + NVIDIA...\""
- Bottom-5 posts open with abstract category statements: "At Microsoft, we believe agentic business applications...", "AI and quantum are transforming how we tackle...", "Agents will keep joining and adapting at work..."
- 3 of the 5 bottom posts use abstract-benefit framing (H15). This pattern is consistent enough to treat as a rule until hook_type tagging quantifies the lift.
- **Default to first-person voice or named-entity/product hooks. Hard avoid: category-level abstractions, corporate-we benefit statements, and vague future-tense trend claims as openers.**

---

## Salience Tier Framework

All top-5 posts are tier-1 events. Format optimization matters most at tier-2 and tier-3. Tier-1 posts can survive format imperfections because content salience dominates all format variables.

| Tier | Definition | Observed score range | Format priority |
|------|-----------|---------------------|-----------------|
| 1 | CEO/head-of-state interaction, major executive appointment, flagship product launch, landmark named partnership | 15,000–30,000+ | Format still matters but salience drives most variance |
| 2 | Named product launch, significant named partnership, AI infrastructure announcement | 5,000–18,000 | All confirmed rules apply fully |
| 3 | Feature release, abstract trend commentary, enterprise product update without named hook | 452–6,000 | Maximum format discipline required; ceiling is structurally low regardless of execution |

**Key implication**: Tier-1 event frequency is the highest-leverage growth lever. Reduce standalone tier-3 posts unless reframed with a tier-1 angle. The MAI-Image-2-Efficient post (score 1,389) is the archetype of what to avoid: no image, product-push hook, no named person, no broader context.

---

## Active Hypotheses

| ID | Hypothesis | Status | Evidence |
|----|-----------|--------|----------|
| H9 | Named entities in hook drive reposts via news value | **ACTIVE** | All top-5 repost leaders name specific entities; bottom-5 use generic language; requires angle tagging to quantify |
| H10 | First-person hook outperforms third-person product-push hook | **ACTIVE** | Top-3 use first-person/named-entity; bottom-5 use third-person/abstract; requires hook_type tagging to quantify |
| H13 | 14:00 UTC advantage is partially salience-driven, not purely timing | **ACTIVE** | 2 of 4 posts at 14:00 are tier-1 events; true time lift may be smaller than avg 14,974 implies; test with tier-2 posts at 14:00 |
| H14 | Named multi-company partnerships drive significantly higher repost counts than single-company announcements | **ACTIVE** | MSFT+Anthropic+NVIDIA: 1,687 reposts; Copilot Cowork: 1,706 reposts; requires angle tagging to confirm |
| H15 | Abstract-benefit hooks systematically underperform concrete-event hooks regardless of other format variables | **ACTIVE** | 3 of bottom-5 use abstract-benefit framing; requires hook_type tagging to quantify |
| H3 | Question CTAs drive more comments than no CTA | **UNTESTABLE — 0 question-CTA posts in corpus** | Must introduce question CTAs to generate any data |

---

## Retired Hypotheses

| ID | Hypothesis | Outcome |
|----|-----------|--------|
| H1 | "I" statement hooks outperform generic hooks | **INSUFFICIENT DATA** — hook_type never populated; replaced by H10/H15 (qualitative pattern) |
| H2 | Specific numbers outperform vague claims | **CONFIRMED** — +47% lift (8,188 vs. 5,558, n=65) |
| H4 | Posts under 200 words outperform posts over 200 words | **DIRECTIONALLY CONFIRMED** — shorter buckets lead across word-count and line-count buckets; tier-1 salience overrides |
| H5 | Images are mandatory for top performance | **CONFIRMED** — +73% lift (7,236 vs. 4,174, n=65) |
| H6 | 14:00–16:00 UTC is optimal posting window | **NEAR-CONFIRMED** — 14:00 avg 14,974 (n=4); 16:00 avg 8,173 (n=6); promoted to Rule 4; H13 adds salience-confound caveat |
| H7 | Zero hashtags outperform tagged posts | **CONFIRMED** — 0 tags avg 6,842; all hashtagged posts underperform; bottom-5 includes posts with 3 and 5 hashtags |
| H11 | Post salience tier is the dominant predictor of score | **CONFIRMED** — top-5 all tier-1 (15,000–30,000+); bottom-5 all tier-2/3 (452–1,389) |
| H12 | 00:00 UTC average is inflated by one outlier | **CONFIRMED** — single post (22,045) distorts n=8 mean to 7,133 |

---

## Post Formula (Evidence-Revised)

1. **Hook** (line 1): First-person voice OR name a specific entity/product/person/company. Give the reader a concrete news hook or personal stake. Hard avoid: category abstractions, corporate-we benefit statements, vague trend claims.
 - Bad: "AI and quantum are transforming how we tackle scientific challenges."
 - Bad: "At Microsoft, we believe agentic applications are the future."
 - Good: "Today I am honored to step into the role of CEO of Microsoft Gaming."
 - Good: "10 PRINT 'ANTHROPIC + MICROSOFT + NVIDIA = MORE COMPUTE, COGNITION, AND CHOICE.'"
2. **Body**: Either (a) ≤38 words total in a single punchy block, or (b) for tier-1 announcements only: structured narrative >3 lines with clear paragraph breaks. Never write 2–3 unstructured lines — avg 5,209 vs. 7,777 for single-line.
3. **Numbers**: At least one concrete figure per post (%, $, time, count, speed benchmark). Remember: numbers amplify strong content; they do not rescue weak hooks.
4. **Image**: Always. +73% lift. No exceptions.
5. **Hashtags**: None.
6. **CTA**: Introduce question-based CTAs — zero exist in current dataset; highest-priority format experiment.

---

## Posting Schedule

- **Primary window**: 14:00 UTC (avg 14,974 — 2.3× corpus average; n=4, confidence interval still wide — see H13)
- **Acceptable secondary**: 16:00–19:00 UTC (avg scores 6,955–8,173; 18:00 UTC has highest confidence at n=11)
- **Avoid**: 01:00–03:00 UTC (avg 1,880–4,250 — 35–71% below corpus average)
- **Do not schedule for 00:00 UTC** — avg of 7,133 is an outlier artifact; underlying slot is unreliable

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
| Partnership / ecosystem news (tier-1/2) | 20% | Named companies + what it means in one punchy line + number |
| Tech culture / honest takes | 20% | Contrarian or counterintuitive claim backed by a number, short format |

---

## Data Gaps — Fields That Must Be Populated

The following fields are empty across all 65 posts. Analysis is blocked until tagging is applied:

- `hook_type` — **highest priority**; required to confirm H10 and H15 and build a quantified hook taxonomy
- `content_theme` — required to measure theme performance and validate content mix targets
- `angle` — required to confirm H9 and H14; identify winning framing patterns
- `lead_magnet_type` — required to measure lead magnet impact
- `topic` — required for niche-level breakdown

**Action required**: Backfill these fields for the most recent 20 posts before the next strategy update. Without hook_type, the three most actionable hypotheses (H10, H14, H15) remain unquantified.

---

## Experiments Queue (Next 30 Days)

1. **Introduce question CTAs** on 5 posts — measure comment_ratio vs. 0.065 baseline (tests H3). This is the only major format variable with zero data points. Priority: immediate.
2. **Tag hook_type on last 20 posts** — backfill to confirm H10 and H15 (first-person/named-entity vs. abstract-benefit hook lift) and unblock H9/H14 analysis.
3. **Anchor 5 consecutive tier-2 posts to 14:00 UTC exactly** — isolate time-of-day effect from salience (tests H13); current n=4 at 14:00 includes 2 tier-1 posts.
4. **Reframe the next tier-3 feature release with a tier-1 angle** — e.g., instead of "MAI-Image-2-Efficient is now live" (score 1,389), open with first-person milestone framing and a named context. Test whether hook reframing lifts tier-3 content into tier-2 range (5,000+).
5. **A/B format test**: 5 posts at ≤38 words vs. 5 posts at >3 structured lines — same topic tier, same hour — to formally test the line-count U-curve and build confidence in the structured-long exception.

---

## What's Not Working

- **Mid-length unstructured posts (2–3 lines)**: avg 5,209 — worst line-count format in the corpus, 33% below single-line
- **Hashtag use**: every hashtagged post underperforms; bottom-5 includes the only posts with 3+ hashtags; avg 2,554 with even 1 hashtag
- **Late-night posting (01:00 UTC)**: avg 1,880 — 71% below corpus average
- **Abstract-benefit hooks**: "AI and quantum are transforming...", "Agents will keep joining...", "At Microsoft, we believe..." — all appear in bottom-5; 3 of 5 bottom posts use this framing
- **Posts without images**: avg 4,174 — 36% below corpus average
- **Tier-3 standalone feature announcements**: short hook + no named person + no broader context = bottom-5 territory regardless of format execution
- **Numbers without salience**: 4 of bottom-5 posts contain numbers yet still scored below 1,400 — numbers do not compensate for weak hooks or low-salience topics

---

*Strategy auto-updated from 65-post performance dataset. Next review triggers at 75 posts or 30 days, whichever comes first.*