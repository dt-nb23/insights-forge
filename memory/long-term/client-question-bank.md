# Client-Facing Question Bank (Phase 0)

A companion to [skills/context-framing/SKILL.md](../../skills/context-framing/SKILL.md). The 9 clarifying questions in the parent skill are **consultant-facing** — they prompt the consultant to recall or look up what they already know about the customer. This file inverts them: **what a consultant could ask the customer directly** during discovery to gather the same context consultatively.

## How to use this bank

- **Pick, don't recite.** Not every question gets asked in every call. Choose 4–6 based on what you already know.
- **Sequence matters.** Open with relationship/context questions, move to specifics, end with intent and format. Asking "what does success look like for you?" cold feels transactional; asking it after they've described their year feels collaborative.
- **Listen for adjacent answers.** A single open-ended question often resolves two or three rubric fields at once. Cross them off as they're answered organically.
- **Translate, don't quote.** These are starting drafts; reshape them in your own voice for the relationship you're in.

The questions are grouped by the rubric classification in [skills/context-framing/SKILL.md:163-181](../../skills/context-framing/SKILL.md#L163-L181).

---

## MUST-HAVE — questions you should be able to answer leaving the call

### Customer + business description
*(Usually known going in. Client question is forward-looking, not introductory.)*

- "What's changed for your business in the last 6–12 months that's most affecting how the engineering and platform teams are spending their time?"
- "If you had to describe what your team is being measured on this year in one sentence, what would it be?"

### Vertical
*(Always known going in — no client question needed.)*

### Engagement Framing — **Context (C)**
*Goal: relationship history, mood, tone heading in.*

- "Before we dig in, walk me through how your team has been using Dynatrace so far — what's worked, where it's plateaued, and what you wish were different."
- "How is the relationship between your team and the Dynatrace platform feeling right now — energized, fatigued, neutral?"
- "Has anything changed in your org recently — leadership, priorities, headcount — that's reshaping how observability gets resourced?"

### Engagement Framing — **Specific Information (S)**
*Goal: known pain points, constraints, environment realities.*

- "What are the two or three things in your environment today that you'd most want to be different a quarter from now?"
- "Are there any constraints I should know about up front — data access, regulated workloads, vendor commitments, frozen architectures — that shape what we can realistically explore?"
- "What have prior reviews or QBRs surfaced that's still open or unresolved?"

### Engagement Framing — **Intent (I)**
*Goal: what the customer expects to walk away with.*

Two variants — match to the relationship dynamic before asking. A healthy/expansion customer can talk aspirationally; an at-risk/renewal customer needs a narrower frame that gives them linguistic cover to be honest about doubt.

- *Healthy/expansion variant:* "Where are you trying to take this practice next, and where would Dynatrace need to be stronger to help you get there?"
- *At-risk/renewal variant:* "If this engagement does one thing for you between now and renewal, what would have the most impact on your decision?"

### Engagement Framing — **Response Format (R)**
*Goal: deliverable format, primary audience, length/tone constraints.*

- "When we wrap this up, who on your side most needs to see the output — and what format do they actually absorb best? A deck, a written brief, a live walkthrough, something else?"
- "Is there a forum this is feeding into — a QBR, a board update, an internal review — that we should write toward?"
- "How long do you typically have to make a case to [name the audience]? Are we talking a 15-minute readout or a 45-minute working session?"

### Active capabilities (Q5)
*Goal: which capabilities are actually in active use.*

*(Most of this you confirm in-tenant or with the SE — but one client-facing question is high-value:)*

- "Of the capabilities you have licensed, which ones do your engineers actually open every week, and which ones are turned on but rarely touched?"

### RUM status on the application in question
*(Conditional MUST-HAVE — required if Intent is UX-focused.)*

- "For [application X] specifically, is Real User Monitoring running today? And when's the last time someone on your team actually reviewed session data or replays for it?"

### Stakeholder role archetype (+ named overlay)
*Goal: identify the eventual reader of the Phase 3 deliverable.*

- "Who specifically will this end up in front of — and what do they care most about right now? KPIs, board narratives, cost pressure, reliability targets — what's top of mind for them this quarter?"
- "If [that person] read one paragraph of our findings, what would make them say 'yes, this is what I needed'?"

### Consulting objective (reframed)
*(Derived by the agent — no client question.)*

---

## SHOULD-HAVE — ask if the moment is right; not blocking

### Tenant type (SaaS vs Managed)
*(Usually known from the account record — no client question typically needed. If unknown, ask the SE first.)*

### Leadership priorities (named KPIs)
*Goal: the 2–3 numbers leadership is watching.*

- "When [leader] is asked at the next board cycle what their org is doing well, what answer are they hoping to give?"

*Why this framing:* surfaces priorities through the leader's aspirations rather than asking the client to enumerate KPIs to a vendor. The aspirational frame elicits more candid, narrative-shaped answers than a direct KPI question, and it positions Dynatrace as a supporting cast member for an outcome the leader already wants.

### Technical team priorities
*Goal: day-to-day pain points and what the technical team is grinding on.*

- "What's the thing your platform/SRE team would throw a party for if it got fixed this quarter?"

*Why this framing:* a positive frame makes the team the hero rather than the victim and surfaces real pain without forcing the client to admit to a "problem." The quarter-bound time horizon keeps the answer concrete and operational rather than abstract or aspirational.

### Engagement trigger
*Goal: QBR / renewal / expansion / scheduled touchpoint.*

- "What made now the right moment to have this conversation — was there a specific event, milestone, or trigger that prompted it?"
- *(Often already implicit from context — only ask if it's genuinely unclear.)*

---

## NICE-TO-HAVE — record if it surfaces, but don't probe

### Prior engagement reference

- *(Not a client question — the agent checks this client's own `memory/clients/<client-name>/README.md` history and `engagements/` folders directly.)*
- If a client mentions prior work organically — "we did something like this last year with [team]" — capture it.

---

## Sequencing patterns

A few opener → follow-up patterns that tend to flow well:

**Pattern A — Relationship-first** (recommended for renewals and established accounts)
1. Context (C) — relationship and mood
2. Specific Information (S) — pain points and constraints
3. Intent (I) — what success looks like
4. Response Format (R) — who and how
5. Stakeholder priorities — the eventual reader

**Pattern B — Outcome-first** (recommended for new logos and expansions)
1. Intent (I) — what they're trying to accomplish
2. Specific Information (S) — what's in the way
3. Context (C) — relationship and history (filled in lighter)
4. Response Format (R) — who and how
5. Stakeholder priorities — the eventual reader

**Pattern C — Triage** (recommended when something is on fire)
1. Engagement trigger — what happened
2. Specific Information (S) — what's known so far
3. Intent (I) — what "good" looks like in 2 weeks
4. Stakeholder priorities — who needs to see what
5. Response Format (R) — how and when

---

## Notes for the consultant

- **Don't lead with capability questions.** Asking "do you use Davis AI?" before establishing relationship context positions the conversation as a product audit, not a value conversation.
- **Resist the urge to ask all nine.** A discovery call where 4 great questions get fully answered beats one where 9 partial answers leave everything thin.
- **Write down their exact phrasing.** When a customer says "we want to stop chasing alerts" — that exact phrase becomes the headline of the Phase 3 one-pager. The consultant's paraphrase loses the signal.
