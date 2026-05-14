---
date: 2026-05-14
week: 2026-W20
posts_analyzed: 65
avg_engagement_score: 6529.2
avg_comment_ratio: 0.0648
avg_insight_ratio: 0.0247
---

# Autoresearch — 2026-05-14

No new variable data has been added since the last update (65 posts, all tagged fields still empty); strategy has been refined to promote H11/H12 to confirmed, add three new hypotheses (H13/H14/H15) based on closer reading of top/bottom post patterns, and harden Rule 6 with explicit bad/good hook examples. Experiments queue updated to prioritize H13 isolation test (tier-2 posts at 14:00 UTC) and hook_type backfill to unblock H10/H14/H15.

## Variable Findings

| Variable | Finding |
|----------|---------|
| hook_type | Insufficient data — hook_type field is unpopulated across all 65 posts. Qualitative inspection of top-5 vs. bottom-5 hooks remains the only evidence: top-3 posts open with first-person or named-entity hooks ('Thank you, PM Modi...', 'Today I am honored...', '10 PRINT...'); bottom-5 open with abstract category statements ('At Microsoft, we believe...', 'AI and quantum are transforming...'). H10 cannot be quantified until tagging is applied. |
| has_numbers | Posts with numbers: avg 8,188 (n=24). Posts without numbers: avg 5,558 (n=41). +47% lift is statistically meaningful at n=65. However, 4 of the bottom-5 posts also contain numbers (scores 1,389; 1,347; 1,274; 667), confirming that numbers are necessary but not sufficient — they amplify strong content but do not rescue weak salience or bad hooks. |
| has_question_cta | Zero question-CTA posts exist in the 65-post corpus. The variable is entirely untested. No comparison is possible. This remains the highest-priority format experiment with no baseline. |
| has_image | Posts with images: avg 7,236 (n=50). Posts without images: avg 4,174 (n=15). +73% lift on 65 posts. This is the strongest confirmed format variable in the dataset. One no-image post in the bottom-5 (score 667) and one in the bottom-5 (score 452) reinforce the signal. Rule is confirmed: always include an image. |
| word_count | Low bucket (≤38 words): avg 7,004. Mid bucket (38–59 words): avg 6,671. High bucket (>59 words): avg 5,866. Shorter is consistently better, but the gap is moderate (~20% from low to high). The 296-word CEO announcement (score 22,045) is a tier-1 outlier that does not invalidate the rule — salience overrides format at tier-1. Default: ≤50 words. |
| line_count | Single-line posts: avg 7,777 (best). 2–3 line posts: avg 5,209 (worst, -33% vs. single-line). >3 line structured posts: avg 7,266. The U-curve pattern is consistent: either a single punchy block or a structured multi-paragraph piece. The 2–3 line mid-format is the weakest structural choice in the corpus. |
| content_theme | Insufficient data — content_theme field is unpopulated across all 65 posts. Cannot quantify performance by theme. Qualitative pattern: top-5 are all major announcements or partnerships; bottom-5 are feature releases and abstract trend commentary. |
| angle | Insufficient data — angle field is unpopulated across all 65 posts. H9 (named entities in hook drive reposts via news value) and H10 remain unquantifiable until this field is backfilled. |
| lead_magnet_type | Insufficient data — lead_magnet_type field is unpopulated across all 65 posts. No analysis possible. |
| posted_time | 14:00 UTC is the clear best slot: avg 14,974 (n=4), 2.3× corpus average of 6,529. 16:00 UTC: avg 8,173 (n=6). 19:00 UTC: avg 8,120 (n=3). 18:00 UTC: avg 6,955 (n=11) — highest-confidence secondary slot at n=11. 17:00 UTC: avg 7,098 (n=3). 01:00 UTC: avg 1,880 (n=5) — worst confirmed slot, 71% below average. 00:00 UTC: avg 7,133 (n=8) — inflated by the CEO-announcement outlier (22,045); not a reliable slot. 02:00 UTC: avg 4,250 (n=3) — below average. 14:00 UTC remains the primary target; n=4 is still small and confidence interval is wide — needs deliberate anchoring. |


## Confirmed
- H2: Specific numbers outperform vague claims — +47% lift (8,188 vs. 5,558, n=65). CONFIRMED.
- H5: Images are mandatory for top performance — +73% lift (7,236 vs. 4,174, n=65). CONFIRMED.
- H6: 14:00–16:00 UTC is optimal posting window — 14:00 avg 14,974 (n=4); 16:00 avg 8,173 (n=6). NEAR-CONFIRMED, needs more n=14:00 data.
- H7: Zero hashtags outperform tagged posts — 0 hashtags avg 6,842 (n=61); all hashtagged posts underperform; bottom-5 includes posts with 3 and 5 hashtags. CONFIRMED.
- H11: Post salience tier is the dominant predictor of score — all top-5 are tier-1 events (15,000–30,000+); all bottom-5 are tier-2/3 (452–1,389). CONFIRMED directionally.
- H12: 00:00 UTC average is inflated by one outlier — one post (22,045) distorts n=8 mean to 7,133; the slot is not reliably above average. CONFIRMED.

## Rejected
- No previously active hypotheses have been rejected in this update cycle. H3 (question CTAs) remains untestable. H9 and H10 remain active pending tagging.

## New Hypotheses
- H13: The 14:00 UTC slot advantage is partly driven by post salience (2 of the 4 posts at 14:00 are tier-1 events scoring 30,378 and 18,004); the true time-of-day lift may be smaller than the raw avg of 14,974 implies. Test by scheduling 5 tier-2 posts at 14:00 UTC and comparing against tier-2 posts in other slots.
- H14: Named partnerships between major companies (Microsoft + Anthropic + NVIDIA, Copilot Cowork in M365) drive significantly higher repost counts than single-company product announcements — the Anthropic/NVIDIA post generated 1,687 reposts and the Copilot Cowork post generated 1,706 reposts vs. corpus repost average. Requires angle tagging to confirm.
- H15: Abstract-benefit hooks ('AI and quantum are transforming...', 'Agents will keep joining...') systematically underperform concrete-event hooks regardless of image, numbers, or timing — 3 of the bottom-5 hooks are abstract-benefit framing. Requires hook_type tagging to quantify.

