---
name: exec-onepager
description: Procedure for producing the Phase 3 exec-ready one-page written deliverable. Use after the action plan has been approved.
---

# Exec One-Pager

## When to use

The **Phase 3 written deliverable**. Use after the Phase 2 action plan has been approved by the user and the team is ready to package the findings for a named senior technical leader (VP of Engineering, Director of Reliability, Head of Data Analytics, or similar).

Use this skill when:

- The action plan is approved and the deliverable is destined for a specific named leader.
- The team has been asked for a written brief ahead of a leadership review.
- A previous one-pager needs revision after new evidence or a redirected scope.

## Inputs

**Resolve the engagement path first (before reading any files):**

1. Use the `ENGAGEMENT_PATH` already established for this session. The agent fixes it once — when Phase 0 (`context-framing`) creates the engagement folder, or when a paused/active engagement is resumed — and holds it in working context for the rest of the session. There is **no shared pointer file** to read; nothing depends on a global "active" file a second concurrent session could overwrite.
2. If no engagement is established yet (a fresh session picking up earlier work), resolve it with the resume procedure in `skills/investigation-reset/SKILL.md`: scan `memory/clients/*/engagements/*/current-context.md` for a `state:` of `active` or `paused`, present the matches, and have the user pick one. If none, stop: "No active engagement found. Start a new engagement or resume a paused one."
3. ENGAGEMENT_PATH = the established/selected path (e.g., `memory/clients/acme-corp/engagements/2026-06-18-api-latency/`). CLIENT_NAME = the segment between `memory/clients/` and `/engagements/`.
4. All phase file reads/writes use ENGAGEMENT_PATH as the base — e.g., `<ENGAGEMENT_PATH>/action-plan.md`.

Then read these files:

- `<ENGAGEMENT_PATH>/action-plan.md` — the approved action plan.
- `<ENGAGEMENT_PATH>/signals-map.md` — for the business impact numbers and the SLI/SLO grounding.
- `<ENGAGEMENT_PATH>/hypotheses.md` — for the confirmed/open/ruled-out status of each hypothesis.
- `memory/long-term/stakeholder-profiles.md` — for the profile of the intended reader. If no matching profile exists, ask the user which profile to use or whether to create one.
- `memory/long-term/terminology.md` — to ensure first-use definitions for any acronym the reader's profile says they expect.
- `memory/long-term/brand/brand-spec.md` — **mandatory.** The Dynatrace brand specification. Governs voice, sentence-case headings, serial commas, product-name capitalization, footer text, and the sources-block style for this deliverable.

## Output format: markdown vs. HTML

The one-pager has two output modes. Choose before starting.

| Mode | When to use | Output file |
|---|---|---|
| **Markdown** | Internal circulation, async review, or when the reader will consume it as a document | `<ENGAGEMENT_PATH>/one-pager-YYYY-MM-DD.md` |
| **HTML** | Leadership presentation, slide-adjacent review, or when brand fidelity matters for the audience | `<deliverable-name>.html` in the project root |

The HTML format is preferred when the one-pager will be projected or shared in a leadership review session. It renders DT Flow fonts, uses the actual Insights lockup, and applies Dynatrace wave backgrounds. The markdown format is the intermediate that feeds the pptx-builder skill — if a deck will be produced, write the markdown alongside the HTML.

## Content structure

A one-pager has five sections, in this order, and fits on a single page.

1. **Problem summary (2–3 sentences).** What is the problem? What is the urgency? What is the audience being asked to decide? Lead with what changed in the business, not with what was observed in telemetry.
2. **Business impact.** Quantify where possible. "Conversion on iOS checkout has declined 8% week-over-week. At current volume, this is approximately $X/week in revenue at risk." If the numbers carry confidence intervals or assumptions, name them in one short clause. Avoid false precision.
3. **Top findings (3–5 bullets).** The confirmed hypotheses, the open ones with high ICE, and the instrumentation gaps that matter. Each finding is a sentence — what was found and what evidence supports it. No more than five bullets.
4. **Recommended actions.** Each with an **owner** and a **timeframe**. Pair every recommendation with the cost or risk in the same line. "Roll back iOS payment SDK to 4.11 — Mobile platform lead, within 24h of H-01 confirmation. Cost: reintroduces a known checkout bug fixed in 4.12; mitigation is targeted patch if vendor can ship in <72h."
5. **Risks and decision asks.** One short paragraph or three bullets. Surface the questions the leader needs to answer. End with the specific decision being requested.

## Style rules

- **Lead with business impact, not technical detail.** The opening sentence should mean something to a non-engineer reading the document for the first time.
- **No acronyms without first-use definition.** Even if the reader knows SLO, write "Service Level Objective (SLO)" on first use, then SLO thereafter — unless the stakeholder profile says otherwise.
- **One page maximum.** If it doesn't fit, the findings are not yet sharp enough.
- **Match the tone to the named stakeholder profile.** A Director of Reliability tolerates more technical depth than a VP of Engineering; a Head of Data Analytics expects time windows and segmentations stated explicitly. Read the profile first.
- **Tradeoffs in the same paragraph as recommendations.** Never put the cost of an action in a separate "appendix" section. If it costs something, say so where you say what to do.
- **No hedging language.** "May possibly indicate" is noise. State the finding; state the confidence; let the reader decide.
- **Cite externally sourced facts in a footnotes block.** Any fact pulled from `docs.dynatrace.com` or `community.dynatrace.com` (per `skills/external-research/SKILL.md`) keeps its URL + retrieval date — but in an exec one-pager, those references live in a short "Sources" footnote block at the bottom of the page, not inline, so the prose reads clean. Every load-bearing claim must trace back to a source — carry through the citation the Phase 2 plan already holds rather than asserting it fresh here.

## Brand conformance

The one-pager must follow `memory/long-term/brand/brand-spec.md`. Apply these rules during drafting (not as a post-hoc cleanup):

- **Sentence case for all headings.** Section titles read "Recommended actions," not "Recommended Actions."
- **Serial commas.** "Owner, timeframe, and cost" — always with the final comma.
- **Active voice and plain language.** Per styleguide.dynatrace.com: front-load each sentence with the keyword and purpose; avoid hedging modifiers; American English spelling.
- **Product names use approved capitalization** (brand-spec §7). On first formal mention apply `®` to **Dynatrace®**, **OneAgent®**, **Smartscape®**, **Grail®**. Use "Dynatrace Cluster" (not "Dynatrace Server"), "extension" (not "plugin" or "add-on"), "Dynatrace web UI" (not "Dynatrace interface"), "ready-made" (not "out-of-the-box").
- **Davis AI** and its variants — **generative AI**, **causal AI**, **predictive AI** — are capitalized as shown.
- **Footer:** `© 2026 Dynatrace, LLC.   Confidential` in gray (`#6F747F`) at the bottom of the page. Insights Forge one-pagers are Confidential by default — do not relabel unless the user explicitly says the deliverable is being shared with a customer or partner.
- **Header lockup:** use `DT Insights Lockup RGB/BAE9730_Insights-Lockup-Horizontal-RGB_REV.svg` on dark backgrounds. This is the REV variant — full-color reversed for dark surfaces. Never substitute a text approximation or custom cube-glyph when the actual SVG file is present. Size to ~24–26px height.
- **Typography (when rendered):** headings in DT Flow Medium; body in DT Flow Light; Arial is the licensed fallback. Load via `@font-face` from `DTFlow/`. The Markdown intermediate does not encode font — that gets applied at render time.
- **Color use:** sparing. Reserve Accent 6 (magenta, `#C93FDB`) for instrumentation gaps and risks; Accent 1 (teal, `#49C2B3`) for confirmed findings; Accent 3 (royal blue, `#1966FF`) for primary CTAs and "open" hypotheses. Do not use red or green — Dynatrace charts don't carry traffic-light semantics.

## HTML visual format — additional procedure

When producing the HTML deliverable, follow this procedure in addition to the content structure above.

### Dynatrace wave backgrounds

Wave assets live in `Data-Visual-waves/` as Adobe Illustrator `.ai` files. They are PDF-compatible and can be converted to PNG for web use. **Do not use `.ai` files directly as HTML background images.**

**Rendering `.ai` files to PNG:**
```bash
qlmanage -t -s 2800 -o assets/ Data-Visual-waves/<subfolder>/<file>.ai
# Output lands as <file>.ai.png — rename to assets/<name>.png
```
Render at `-s 2800` for retina-quality output (2× the 960px page width). Copy rendered PNGs into `assets/` in the project root.

**Wave series selection — readability is the deciding factor:**

| Series | Visual character | Use for | Avoid when |
|---|---|---|---|
| `datalargebeam` | Smooth continuous curved beams | Header backgrounds; any section with body text or labels | Never avoid — safe at all text sizes |
| `datatrail` | Single thin arc line | Secondary dark sections (decision ask, callout strips) | Never avoid — minimal noise |
| `databeam` | Bold sweeping arc | Decorative backgrounds where text is large (≥18px) | Small body text ≤13px |
| `dataflow` | Scattered particle dots | Sections with sparse or very large text only | **Do not use behind body text** — dots fragment letterforms at ≤13px and fail readability |
| `datablocks` | Geometric ribbon blocks | Spacious decorative zones | Dense text areas |
| `dataparticles` | Fine particle fields | **Check before use** — some files in this series were saved without PDF compatibility and render as a blank placeholder. Test with `qlmanage` before committing |

**Applying wave backgrounds in CSS:**

Always layer a dark left-to-right gradient overlay above the wave image so text on the left reads cleanly:

```css
background:
  linear-gradient(to right, rgba(7,16,30,0.90) 0%, rgba(7,16,30,0.72) 42%, rgba(7,16,30,0.32) 100%),
  url('assets/wave-bg.png') center / cover no-repeat;
```

Adjust the right-side opacity (`0.32`) to taste — lower values show more wave, higher values increase text contrast. For sections with denser small text, use `0.45` or higher on the right stop. Never use a wave image without the overlay.

**After placing a wave background, always screenshot the section and verify:**
1. All text at actual render size (not just the large headline — check labels and body copy too)
2. Right-side content — the wave is brightest there and the overlay is thinnest
3. If any text zone fails, increase the right-side overlay opacity or switch to a smoother wave series

### Two-column layout balance

The HTML one-pager uses a two-column body grid. Both columns must terminate at approximately the same height — visible blank space at a column's bottom reads as unfinished to a senior audience.

**Diagnosing imbalance:** If the left column is taller than the right, look for redundant paragraphs first. The most common pattern: a section title states the claim, role cards or a pull quote provide the evidence, and then a paragraph between them repeats both. If the title + evidence already communicate the point, the paragraph is filler — cut it, do not compress it.

**Test before cutting:** ask whether removing the paragraph loses any information not already present in the title or the evidence elements. If the answer is no, remove it.

**Uniform grid component heights:** when a row of equal-width cells contains text of varying length (e.g., a five-step framework row), use `display: flex; flex-direction: column` on each cell and a `min-height` on the top section equal to the tallest cell's natural height. This ensures all cells share the same top-section height and the description sections fill remaining space equally. Measure rendered heights to confirm uniformity; do not rely on estimating from the source text.

### Accessibility requirements for HTML deliverables

Apply these standards during initial build, not as a post-hoc pass.

**Font sizes:**
- Body text: minimum **12px**
- Labels, section eyebrows, metadata: minimum **11px**
- Never place readable text below 11px regardless of weight

**Color contrast (WCAG AA):**
- Normal text (≤18px regular or ≤14px bold): minimum **4.5:1** contrast ratio
- Large text (≥18px regular or ≥14px bold): minimum **3:1**
- Known failure: white text on brand teal `#49C2B3` = ~2.5:1 — use darkened teal `#1A7A70` (5.8:1) for any teal text on light backgrounds
- Known failure: teal `#49C2B3` as an eyebrow label on `#1A2440` navy = ~2.2:1 — use `rgba(255,255,255,0.8)` instead
- Run a contrast check on every colored text instance, not just the main body copy

**Semantic HTML:**
- Use `<header>`, `<main>`, `<section>`, `<footer>`, `<blockquote>` rather than generic `<div>` where the element has semantic meaning
- Add `aria-hidden="true"` to all decorative elements (wave backgrounds, dividers, icon glyphs, pseudo-element orbs)
- Add `aria-label` to role abbreviations and icon-only groups so screen readers receive the full label
- Add `role="list"` and `role="listitem"` to visual card groups that function as lists

## Finalizing

Phase 3 is **packaging, not re-review.** The substance, framing, priorities, and risks were settled by the persona panel on the Phase 2 plan, which arrives here already approved. Do not re-open findings, re-rank recommendations, or re-litigate the message — summarize the approved plan into the one-pager faithfully. No critique lens runs in Phase 3; the deliverable inherits the panel-reviewed plan.

These mechanical gates remain — they are formatting, legibility, and fidelity checks, not critique. Run each as a checklist; do not treat a screenshot glance as sufficient.

- **One-page constraint.** After drafting, read the whole page once. If it does not fit on a single page, cut — do not compress. If it will not cut to one page, the underlying plan was not sharp enough; that is a Phase 2 problem, not a wording problem.

- **Plan-fidelity gate.** Read `<ENGAGEMENT_PATH>/action-plan.md` and the drafted one-pager side by side and confirm:
  1. **Identical recommendation rank order.** The recommended-actions section lists actions in the same order the action plan ranks them. No silent re-ordering, promotion, or demotion.
  2. **Tradeoff in the same paragraph.** Every recommendation carries its cost or risk on the same line, not in a separate risks section.
  3. **Business-impact-first opening.** The first sentence states what changed in the business, not what was observed in telemetry.
  4. **Open hypotheses keep their uncertainty qualifier.** Any hypothesis carried in from `hypotheses.md` with Status "open" must read as open in the one-pager — "if confirmed," "pending H-01 validation," or the action gated on confirmation. The no-hedging brand rule strips *weasel words* ("may possibly indicate"); it does **not** license upgrading an open hypothesis to a confident claim. Confirmed reads confirmed; open reads open.

- **Brand and accessibility gate.** Verify each item below explicitly, not by a single screenshot glance:
  - **WCAG AA contrast on every colored text instance** (not just body copy). White on brand teal `#49C2B3` is ~2.5:1 and fails — use darkened teal `#1A7A70` (5.8:1) for teal text on light backgrounds. Teal `#49C2B3` as an eyebrow on `#1A2440` navy is ~2.2:1 and fails — use `rgba(255,255,255,0.8)`. Normal text needs ≥4.5:1; large text (≥18px regular or ≥14px bold) needs ≥3:1.
  - **No `dataflow` particle wave behind body text.** Confirm every text-dense section uses `datalargebeam` or `datatrail`; the scattered dots fragment letterforms at ≤13px in the thin-overlay right-side zones.
  - **Required aria attributes present.** `aria-hidden="true"` on all decorative elements (wave backgrounds, dividers, icon glyphs, orbs); `aria-label` on role abbreviations and icon-only groups; `role="list"`/`role="listitem"` on visual card groups that function as lists.
  - **Brand text rules.** Sentence-case headings, serial commas, and `®` on first formal mention of **Dynatrace®**, **OneAgent®**, **Smartscape®**, **Grail®**. Approved product-name capitalization per brand-spec §7.

- **HTML legibility.** Screenshot the full rendered page and both text-heavy sections (header and any dark strip) at actual size. Confirm every text element is legible before marking the deliverable done. This is the visual confirmation of the contrast and wave checks above, not a substitute for them.

- **Handoff gate.** If only the HTML was produced, write the companion `<ENGAGEMENT_PATH>/one-pager-YYYY-MM-DD.md` **before** the deck step — pptx-builder reads only the markdown file. The companion must carry forward the HTML design decisions (wave series chosen, color assignments for confirmed findings vs. open hypotheses vs. risks, the safe-contrast color substitutions) so the deck stays consistent with the rendered one-pager.

## Output

- **Markdown:** the agent writes `one-pager-YYYY-MM-DD.md` inside `<ENGAGEMENT_PATH>/`. This file feeds the pptx-builder skill.
- **HTML:** the agent writes `<deliverable-name>.html` in the project root, with supporting assets in `assets/` (rendered wave PNGs, lockup SVG). The HTML file is self-contained when opened from the project root.

The agent then **prompts the user to approve PPTX generation** — it does not automatically invoke the pptx skill. The Phase 3 gate is between the one-pager and the deck.

**Note for pptx-builder:** the pptx-builder skill reads from the markdown one-pager file at `<ENGAGEMENT_PATH>/one-pager-YYYY-MM-DD.md`. If only the HTML was produced, write a companion markdown summary before invoking the deck skill.

## Common pitfalls

- **Opening with telemetry instead of business impact.** "p95 latency on cart-service rose 200ms" buries the lede. Start with "checkout conversion dropped 8% week-over-week; here is what's driving it."
- **Burying tradeoffs in a risks-appendix.** Pair them with the recommendations they belong to.
- **Skipping the stakeholder profile.** Every leader reads differently. Read the profile before drafting, not after.
- **Re-opening the message in Phase 3.** The one-pager summarizes a plan the persona panel already reviewed and you already had approved at the Phase 2 gate. Do not introduce new findings, re-rank recommendations, or re-frame the argument here — that work belongs to Phase 2. If the summary surfaces a genuine new problem, that is a signal to reopen Phase 2, not to patch it in the one-pager.
- **Auto-generating the PPTX.** The Phase 3 gate is the one-pager. Wait for explicit user approval before invoking the pptx skill.
- **Using a particle wave (dataflow series) behind body text.** The scattered dots compete with letterforms at ≤13px and fail readability in the text-dense right-side zones where the overlay is thinnest. Use `datalargebeam` or `datatrail` for any section containing small text.
- **Using a text approximation for the Insights lockup.** The actual REV SVG is in `DT Insights Lockup RGB/`. Use it. Custom cube-glyph approximations are not brand-compliant.
- **Omitting `Dynatrace®` on first mention.** Brand spec §7 requires the registered trademark symbol on first formal mention in every deliverable.
- **Skipping the readability screenshot check.** The wave background gradient overlay looks sufficient in the CSS but the right-side stats and action cards are the failure zones — always verify visually at render size, not by reading the CSS opacity values.
- **Column imbalance from redundant paragraphs.** A section title that states the claim + cards/bullets that provide evidence does not need a paragraph repeating both. When the left column runs long, look for this pattern first before restructuring the layout.
- **Not producing a markdown companion when only HTML is delivered.** The pptx-builder skill requires `one-pager-YYYY-MM-DD.md` as its input. If the user later asks for a deck, the absence of the markdown file will block that step.
