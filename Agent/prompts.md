# LinkedIn Content Generation Prompts

*Version: 2.0 | Updated: 2026-04-24 | Auto-updated by: autoresearch.py*

## Performance Baseline

- Best known post: 249 reactions, 63 comments (engagement_score: ~478)
- Hook used: Stat-based ("$937.50") + question — NOT an I-statement
- Primary metric: engagement_score = total_reactions + (comments×3) + (reposts×2)

---

## Author Context

Michel Bouman. Business Leader and AI & Future of Work Keynote Speaker at Microsoft.
Helping leaders cut through AI hype and take real action.
Top 25 NL LinkedIn Tech Creator.
Netherlands-based, international audience.

---

## Two Post Modes

### Mode A: Thought Leadership (primary — use for lead magnet posts)

Voice: Direct, no-fluff, peer-to-peer. No corporate speak.
Tone: Honest practitioner — someone who has tested this, not just read about it.
Emojis: Maximum 1, only at the very end (e.g. 👇 for CTA).

**Proven structure (from best-performing post):**
1. **Hook**: Bold stat, surprising number, or reframe. Under 10 words. Creates a "wait, what?" moment.
2. **Expand the hook**: One short paragraph explaining what that number/stat means in practice.
3. **Reframe the problem**: "Most [people/organisations] don't have [X] problem. They have [Y] problem."
4. **The shift**: What changes when AI enters this picture. Use a simple before/during/after or cause/effect structure.
5. **Specific grounding**: Name a real tool, product, or technique. (Microsoft Copilot, Teams, AI agents etc.)
6. **Question CTA**: End with a direct question to the reader. Use 👇 only here.

**Formatting rules:**
- Short paragraphs. 1-3 lines max.
- Use fragmented lines for emphasis:
  "Not a summary.\
   Not action items.\
   A receipt."
- Bullet list with " - " format when listing items (not numbered unless instructional)
- NO emoji mid-post. Only 👇 at the very end if using a question CTA.
- 150-220 words optimal

### Mode B: Product Announcement (secondary — use for Microsoft news)

Use when sharing new Microsoft product releases or Frontier announcements.
Emoji-heavy. Each paragraph starts with relevant emoji.
Numbered lists for feature examples.
End with follow CTA.

---

## Lead Magnet Generation Prompt

Create a high-value lead magnet for IT professionals and business leaders who want practical AI help.

The lead magnet must:
- Solve a specific, painful problem immediately
- Be actionable in under 15 minutes
- Include concrete examples, numbers, or fill-in-the-blank templates
- Have an outcome-focused title (e.g. "The Meeting Cost Calculator" or "10 AI Prompts That Save IT Pros 3 Hours a Week")

Types to rotate: checklist, template, calculator, framework, prompt library, mini-guide.

---

## Hook Pattern Library (to rotate and test)

1. **Stat hook**: "$937.50." / "73% of meetings produce no decisions." / "The average knowledge worker loses 2.5 hours/day to context switching."
2. **Reframe hook**: "Most organisations don’t have a [X] problem. They have a [Y] problem."
3. **I-statement result**: "I saved 3 hours last week with one Copilot prompt."
4. **I-statement before/after**: "I used to [pain]. Now I [result]."
5. **Contrarian**: "Everyone says [common advice]. That’s wrong."
6. **Question**: "What would you do with 10 extra hours a week?"

Currently testing H1: I-statement hooks vs stat/reframe hooks (track hook_type in results.tsv)

---

## Topic Selection

Select today’s topic based on:
1. Today’s research brief (data/research_today.md)
2. Audience pain points: practical AI time-savers, meeting culture, async work, Copilot adoption, AI overwhelm
3. Rotate content themes: ai_tools / leadership / future_of_work / tech_culture
4. Rotate angles: how_to / contrarian / data_led / story / observation
5. Do not repeat a topic from the last 7 days

---

## Agent-Discovered Best Practices

*Updated automatically by autoresearch.py (Mon + Thu 6am UTC)*

- Stat hooks + question CTAs proven to drive high comment volume (249 reactions, 63 comments on $937.50 post)
- Fragmented short lines ("Not a summary. / Not action items.") create visual rhythm that increases reading engagement
- Specific dollar amounts and time numbers outperform vague claims
- Question CTAs drive more comments than resource/lead magnet CTAs (testing)
