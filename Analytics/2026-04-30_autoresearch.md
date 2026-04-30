---
date: 2026-04-30
week: 2026-W18
posts_analyzed: 65
avg_engagement_score: 6529.2
avg_comment_ratio: 0.0648
avg_insight_ratio: 0.0247
---

# Autoresearch — 2026-04-30

No new posts added since last run (still n=65); analysis deepened with salience-tier framework and H10/H11/H12 hypotheses formalized from qualitative top-5/bottom-5 pattern review. Key updates: 00:00 UTC flagged as outlier-inflated, first-person hook rule added as directional Rule 6, and tier classification framework introduced to explain why format optimization has diminishing returns without content salience.

## Variable Findings

| Variable | Finding |
|----------|---------|
| hook_type | Insufficient data — hook_type field unpopulated across all 65 posts. Qualitative inspection of top-5 vs. bottom-5 hooks suggests named-entity/announcement hooks (e.g., 'Today I am honored to step into the role of CEO', 'Announcing Copilot Cowork') outperform abstract-benefit hooks ('AI and quantum are transforming...', 'Agents will keep joining...'), but this cannot be quantified without tagging. |
| has_numbers | Posts with numbers avg 8,188 (n=24) vs. posts without avg 5,558 (n=41) — a +47% lift. Confirmed signal with meaningful sample sizes on both sides. However, numbers alone do not guarantee top performance: the bottom-5 includes 4 posts with numbers, suggesting numbers are necessary but not sufficient. |
| has_question_cta | Insufficient data — zero posts in the 65-post corpus use a question CTA. No comparison possible. Remains highest-priority untested variable. |
| has_image | Posts with images avg 7,236 (n=50) vs. without avg 4,174 (n=15) — a +73% lift. Strong signal with large sample. One bottom-5 post lacks an image (score 1,389); another bottom-5 also lacks an image (score 667). The single top-5 post without an image does not exist — all top-5 posts have images. Rule is near-confirmed. |
| word_count | Clear inverse trend: ≤38 words avg 7,004; 38–59 words avg 6,671; >59 words avg 5,866. Shorter is directionally better. Exception: the #3 post (score 22,045) is 296 words, driven by a major CEO announcement event — suggesting content salience can override length penalties. Default recommendation remains ≤50 words unless content is a major announcement. |
| line_count | U-shaped pattern: single-line posts avg 7,777; 2–3 line posts avg 5,209 (worst); >3 line posts avg 7,266. The 2–3 line 'formless middle' underperforms both extremes. Top-5 posts split between single-line (2 posts) and multi-line structured (3 posts). Bottom-5 posts cluster in single-line and 3-line formats — suggesting line count alone is not determinative; content type matters. Avoid 2-line posts as a structural default. |
| content_theme | Insufficient data — content_theme field unpopulated across all 65 posts. Qualitative read: top-5 are all high-salience announcements (PM meeting, CEO appointment, major product launch, AI chip launch, partnership news). Bottom-5 are product feature releases and abstract tech trend commentary. Tagging required for quantification. |
| angle | Insufficient data — angle field unpopulated across all 65 posts. Qualitative observation: first-person announcement angles ('Today I am honored...', 'Thank you, PM Modi...') appear in top-3. Third-person product-push angles appear in bottom-5. Cannot quantify without tagging. |
| lead_magnet_type | Insufficient data — lead_magnet_type field unpopulated across all 65 posts. No analysis possible. |
| posted_time | 14:00 UTC is the clear best slot: avg 14,974 (n=4). Next best are 16:00 UTC avg 8,173 (n=6), 19:00 UTC avg 8,120 (n=3), and 18:00 UTC avg 6,955 (n=11). The 00:00 UTC slot shows avg 7,133 (n=8) — elevated by the CEO announcement post (score 22,045) which posted at midnight; without that outlier this slot likely underperforms. Worst slot is 01:00 UTC avg 1,880 (n=5) — 71% below corpus average. The 14:00–19:00 UTC window dominates. |


## Confirmed
- H2: Specific numbers outperform vague claims — +47% lift (8,188 vs. 5,558), n=65
- H4: Posts under ~60 words outperform longer posts directionally — confirmed with structured exceptions for major announcement content
- H7: Zero hashtags outperform tagged posts — 0 tags avg 6,842 (n=61); every post with hashtags is in the bottom tier; bottom-5 includes posts with 3 and 5 hashtags
- H5: Images are mandatory for top performance — +73% lift (7,236 vs. 4,174), n=65, all top-5 posts have images

## Rejected
- H1: Insufficient data — hook_type field never populated; untestable with current dataset

## New Hypotheses
- H10: First-person voice in the hook ('Today I...', 'Thank you...') drives higher engagement than third-person product-push hooks ('Live in Foundry today:', 'At Microsoft, we believe...') — top-3 posts use first-person; bottom-5 use third-person or abstract openings. Needs hook_type tagging to test formally.
- H11: Post salience tier (tier 1 = CEO/head-of-state/major partnership; tier 2 = product launch; tier 3 = feature release/abstract commentary) is the dominant predictor of score, overriding all format variables. Top-5 are all tier-1 events; bottom-5 are all tier-2/3. Format optimization may have diminishing returns without salience.
- H12: The 00:00 UTC hour avg (7,133, n=8) is inflated by the CEO-appointment outlier (score 22,045). Excluding that post, the true 00:00 UTC avg is likely below the corpus mean. Do not treat midnight as a viable posting window.
- H9: Named entities (companies, people, products) in hook drive reposts via news value — directionally supported: top-5 by repost count all name specific entities; bottom-5 use generic category language. Still active, needs angle-field tagging to confirm.

