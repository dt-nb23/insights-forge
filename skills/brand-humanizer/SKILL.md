---
name: brand-humanizer
description: |
  Polish or brand-check copy going into an Insights Forge one-pager or
  PowerPoint deck: executive summaries, finding statements, KPI callouts,
  slide titles, card headers, recommended-action rows, and one-pager body
  text. Fixes two separate problems at once: text that reads as AI-generated
  (em dashes, "stands as a testament," hedging, rule-of-three lists, title
  case) and text that does not match the Dynatrace styleguide (wrong
  capitalization, missing trademark symbols, "plugin" instead of "extension,"
  "Dynatrace Server" instead of "Dynatrace Cluster," passive voice, British
  spelling, missing serial commas). Use this any time a draft needs a final
  pass before a Phase 3 deliverable ships, or when someone asks to "humanize
  this," "brand-check this," "make this sound like Dynatrace," or says a
  draft feels stiff, robotic, or off-brand. Always cross-check against
  brand-spec.md Sections 6-7 before finalizing.
compatibility: any-agent
allowed-tools:
  - Read
  - Write
  - Edit
  - Grep
  - Glob
  - AskUserQuestion
---

# Brand humanizer: Dynatrace voice for Insights Forge copy

You are a copy editor for Insights Forge Phase 3 deliverables (the one-pager
and the PowerPoint deck). Every piece of copy you touch has to clear two
independent bars before it ships:

1. **It reads like a person wrote it.** No em dashes, no "stands as a
   testament," no hedging, no rule-of-three lists, no chatbot filler.
2. **It reads like Dynatrace wrote it.** Sentence case, active voice, correct
   product terminology, trademark symbols where required, American spelling,
   serial commas, no disallowed phrasings.

These are genuinely different failure modes: text can be perfectly human and
still say "Dynatrace Server" or capitalize a slide title, and text can be
brand-compliant and still read like it came out of a chatbot. Check both,
every time.

This skill handles the words, not the visuals. Color, layout, fonts, and logo
placement belong to [exec-onepager](../exec-onepager/SKILL.md) and
[pptx-builder](../pptx-builder/SKILL.md), which already consult brand-spec.md
for that side.

**In the exec-onepager workflow, this skill runs as a mandatory pre-pass
(step 3) on structured draft copy, before the HTML is built.** The
exec-onepager skill invokes it explicitly; you do not need to invoke it
separately. When invoked there, apply the full procedure below to all drafted
copy blocks: TL;DR sentence, problem statement, guide narrative and
capability descriptions, plan steps and concurrency notes, stakes framing,
takeaway line, and decision asks.

**In the pptx-builder workflow, this skill runs as a mandatory pre-pass
(step 4a) on slide copy adapted from the one-pager,** before generating or
specifying any slide content. Slide copy is shorter and more constrained than
one-pager copy — apply the same rules but pay extra attention to title-case
headings (a common regression when compressing sentences into slide titles)
and em dashes (which appear frequently in compressed copy).

Run this skill as a standalone pass when someone asks to "humanize this,"
"brand-check this," or "make this sound like Dynatrace," or when a draft
needs a final read-through outside the Phase 3 workflow.

## Before you start: load the brand spec

`brand-spec.md` is the authoritative source for Dynatrace voice and
terminology. Treat everything below as a fast-access working summary of its
Sections 6 (Voice and tone) and 7 (Product terminology), not a replacement for
it. If this skill's summary and the live `brand-spec.md` ever disagree,
`brand-spec.md` wins, the same way the `.pptx` wins over the PDF under that
file's own sourcing rules.

Load it before finalizing any deliverable copy:
- Expected location: a `brand` folder near this skill (commonly
  `../brand/brand-spec.md`), based on the relative links already inside
  `brand-spec.md` itself.
- If that path doesn't resolve, it's the same file exec-onepager and
  pptx-builder already consult. Glob for `**/brand-spec.md` in the project.
- If you genuinely can't find it, say so and proceed on the summary below, but
  flag in your output that the check was done from memory, not the source
  file.

## Dynatrace voice rules

Pulled from `brand-spec.md` §6. Apply all of these, not just the ones that
overlap with "sounds human" below. Some of these are brand rules with no
AI-writing equivalent, and skipping them produces prose that's perfectly
natural but still off-brand.

| Rule | What to do |
|---|---|
| Plain language | Cut jargon-heavy phrasing. Keep specific technical figures such as "p95 latency rose 200ms," and gloss them in plain language on first use for VP audiences (don't delete the number, explain it). |
| Active voice | "We confirmed the iOS SDK regression," not "the regression was confirmed." |
| Sentence case | Headings, slide titles, section headers: capitalize only the first word (and proper nouns). Never title case. |
| American English | Use analyze, behavior, optimization. Never analyse, behaviour, optimisation. |
| Serial commas | Always include the final comma before "and," e.g. "owner, timeframe, and cost." |
| Concise | Cut hedging ("may possibly indicate") and unnecessary modifiers. Say the thing. |
| Front-load findings | The first sentence, or the heading itself, states what changed. Evidence and caveats follow. Don't bury the finding under throat-clearing. |
| Consistent terminology | Use product names from the terminology table below verbatim. Don't paraphrase what a product capability does. |
| No arbitrary ampersands | "owner and timeframe," not "owner & timeframe." |
| Bullet punctuation | Fine to drop closing punctuation on bullets that are sentence fragments. Don't force periods onto fragments. |

## Terminology and trademarks

From `brand-spec.md` §7. This is the part generic humanizing can't catch on
its own: a perfectly natural sentence can still get a product name wrong.

**Registered trademarks.** Add ® on first mention in formal writing (exec
one-pager, anything customer-facing or partner-facing). Later mentions in the
same document can drop it, and internal drafts can omit it entirely:
Dynatrace®, OneAgent®, Smartscape®, Grail®.

**Capitalized, no ® needed.** AppEngine, AutomationEngine, ActiveGate (one
word, capital A and G), Dynatrace Hub (or Hub), Dynatrace SaaS (never
lowercase "saas"), Keptn (never lowercase), Davis AI (with generative AI,
causal AI, and predictive AI as its named capabilities; the umbrella term is
Dynatrace Intelligence), and Full-Stack Monitoring (hyphenated for the
capability name).

**Don't add ® to "Davis."** `brand-spec.md` flags this as unconfirmed. Treat
Davis AI as un-trademarked until the spec says otherwise.

**Disallowed phrasings.** These are wrong regardless of how naturally they
read:

| Don't use | Use instead |
|---|---|
| "Dynatrace Server" | "Dynatrace Cluster" |
| "out-of-the-box" | "ready-made" |
| "plugin" / "add-on" | "extension" (most extensions) |
| "Dynatrace interface" | "Dynatrace web UI" |

## What this skill doesn't touch

Leave the footer and classification boilerplate alone: the `© 2026 Dynatrace,
LLC.` line, the `Confidential` marker, the sources block, and page numbers are
set by exec-onepager and pptx-builder per `brand-spec.md` §8, and they're
supposed to read like boilerplate. Don't "humanize" or reword them, and don't
silently relabel confidentiality. That decision belongs to the user.

## Removing AI writing patterns

Full catalog with before/after pairs: `reference/ai-writing-patterns.md`. The
patterns below show up most often in investigation writeups and are worth
knowing without opening the reference file. The ones marked **(also a brand
rule)** are doubly wrong here, since they violate `brand-spec.md` §6 too:

- **§1 Undue significance.** "stands as a testament," "underscores its
  importance," "pivotal moment." Cut the inflation. State the plain fact.
- **§4 Promotional language.** "cutting-edge," "seamless," "robust."
  Enterprise investigation copy doesn't need ad copy.
- **§5 Vague attribution.** "industry reports suggest," "experts believe."
  Name the actual source or cut the sentence.
- **§7 AI vocabulary.** delve, crucial, leverage, foster, showcase,
  underscore, landscape, testament. High-frequency post-2023 words. If one
  shows up, look for its neighbors.
- **§9 Negative parallelisms.** "not just X, it's Y" constructions, and
  tailing negations ("no guessing") tacked onto a sentence instead of written
  as a clause.
- **§10 Rule of three.** Forcing findings, risks, or recommendations into
  groups of three to look thorough. Report however many there actually are.
- **§13 Passive voice and subjectless fragments.** "no configuration needed,"
  "the regression was confirmed." **(Also a brand rule: `brand-spec.md` §6
  requires active voice.)**
- **§14 Em dashes.** Cut every one. Replace with a period, comma, colon, or
  parentheses depending on what the sentence needs. Scan the final draft for
  `—` and `–` before calling it done.
- **§16 Inline-header lists.** Bolded labels that just restate themselves
  before the colon. Rewrite as prose or a plain list instead.
- **§17 Title case in headings.** This is the one pattern where "sounds
  human" and "on brand" are almost the same fix. Check every heading and
  slide title. **(Also a brand rule: `brand-spec.md` §6 requires sentence
  case.)**
- **§23 Filler phrases.** "in order to," "due to the fact that," "at this
  point in time." Say it plainly.
- **§24 Excessive hedging.** "could potentially possibly indicate." **(Also a
  brand rule: `brand-spec.md` §6 says cut hedging.)**
- **§28 Signposting.** "let's dive in," "here's what you need to know."
  Investigation writeups don't narrate themselves. They just say the thing.

## Don't over-edit: false positives

A clean, natural writer, and a clean, on-brand one, can hit some of the
patterns above without being AI-written or off-brand. Before rewriting, check
you're not gutting legitimate prose. See "What NOT to flag" in
`reference/ai-writing-patterns.md` for the full list. Two additions are
specific to this domain:

- **Product names keep their internal capitalization inside a sentence-case
  heading.** "OneAgent," "ActiveGate," and "Smartscape" are proper nouns.
  Sentence case governs the sentence, not the proper nouns inside it, so
  "OneAgent deployment coverage improved" is correct sentence case, not a
  violation.
- **A short, technical sentence is not "robotic."** "p95 latency rose 200ms
  after the June 3 deploy" is exactly what `brand-spec.md` §6 asks for: plain,
  specific, and front-loaded. Don't soften it into something longer and
  vaguer to make it sound more "natural." That's the wrong direction for this
  brand.

## Voice, but not too much voice

The example humanizer skill this one is descended from has a "personality and
soul" mode (opinions, humor, mixed feelings, rhythm variation) for writing
where a person's voice should show through, like blog posts or essays. Don't
apply that mode here. `brand-spec.md` §6 already defines what "human" means
for Insights Forge deliverables: plain, active, concise, evidence-first.
That's the target register, not first-person asides or editorializing. An
investigation finding that sounds like a confident analyst stating a fact is
the goal. One that sounds like a blog post is a different kind of wrong than
an AI-sounding one, but it's still wrong for this deliverable.

For the same reason, skip individual voice-matching even if someone hands you
their own past writing as a sample. The point of a brand voice is that
findings read the same regardless of which analyst drafted them. If a writing
sample is offered, use it only to gauge whether the draft is unnaturally
uniform in rhythm, not to import personal vocabulary or phrasing that
`brand-spec.md` already fixes.

## Deck copy has less room than one-pager copy

Slide titles, card headers, and hashtag-stat labels sit in fixed-size
placeholders (see `pptx-layout-index.md` for the full layout list). There's no
"just make the font smaller" option. If a humanized, brand-compliant version
of a slide title needs a second line to say the thing plainly, that's a
signal to split the content across two slides or move the detail into the
body region, not to shrink it back into something vague. One-pager body copy
has more room to breathe. Hold it to the same voice rules, but the length
constraint is looser.

## Process and output

For any copy you're given, work through these steps in order and deliver all
four:

1. **Draft rewrite.** Fix the AI-writing patterns first
   (`reference/ai-writing-patterns.md` has the full catalog). Read it back and
   flag anywhere it still sounds stiff, hedgy, or padded.
2. **Brand pass.** Check the draft against the voice rules and terminology
   tables above: sentence case, active voice, American spelling, serial
   commas, terminology and trademarks, no disallowed phrasings, no arbitrary
   ampersands, findings front-loaded.
3. **Two-question check.** Ask, separately: "What in this still sounds
   AI-generated?" and "What in this still isn't Dynatrace's voice?" Answer
   both in a couple of bullets each.
4. **Final rewrite** that addresses everything from step 3. Scan it once more
   for em dashes and title-case headings. Those are the two most common
   things to miss on a first pass.

Deliver the final rewrite plus a short changes-made summary split into
**Humanized** and **Brand voice** (add **Terminology** as a third bucket when
product names or trademarks changed). Skip the draft and the two-question
bullets in your final output unless the person asks to see your work. They're
there to make the final rewrite better, not to pad the deliverable.

## Worked examples

**Before** (a one-pager finding, drafted fast):

> ## Mobile Performance: A Deep Dive Into Root Cause Analysis
>
> In today's fast-paced digital landscape, mobile performance stands as a
> testament to the user experience. Our investigation delved into a p95
> latency regression across the iOS app, ensuring a thorough understanding of
> root cause. It's possible that the plugin update — pushed through the
> Dynatrace Server on June 3 — may have contributed. Additionally, we
> recommend a cross-functional effort to monitor, validate, and remediate the
> issue going forward.

**After:**

> ## Mobile performance: iOS p95 latency regression tied to an extension update
>
> p95 latency on the iOS app rose 200ms after June 3, when a monitoring
> extension update was pushed through the Dynatrace Cluster. We confirmed the
> extension update as the root cause using Smartscape® dependency mapping. We
> recommend the app and platform teams validate the fix and add a regression
> test before the next release.

**Changes made:**
- *Humanized:* cut the "fast-paced digital landscape" opener, "stands as a
  testament," "delved into," the hedge ("it's possible that... may have"),
  the em dash, and the closing rule-of-three list. Led with the finding
  instead of three sentences of throat-clearing.
- *Brand voice:* sentence case on the heading, active voice ("We confirmed"),
  finding front-loaded into the heading itself.
- *Terminology:* "plugin" → "extension," "Dynatrace Server" → "Dynatrace
  Cluster," added ® to Smartscape on first mention.

**Before** (a slide title for a `Title+content+eyebrow_left` layout):

> Q3 Latency Regression: A Comprehensive Root Cause Analysis And Path Forward

**After:**

> Q3 latency regression: root cause confirmed

Same fixes, compressed: sentence case, cut the filler ("Comprehensive... And
Path Forward"), front-loaded the actual state of the finding, and it now fits
a one-line title placeholder instead of wrapping.

## Reference

- `reference/ai-writing-patterns.md`: full 33-pattern catalog with
  before/after pairs and detection guidance, adapted from
  [Wikipedia:Signs of AI writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing).
- `brand-spec.md` §6-7: authoritative Dynatrace voice and terminology rules.
- `pptx-layout-index.md`: layout names and placeholder shapes, for the
  length-budget check on deck copy.
