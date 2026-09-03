---
name: brand-spec
description: Dynatrace brand specification for Insights Forge deliverables (one-pager and PowerPoint). Authoritative for color, typography, layout, voice, terminology, and footer conventions. Load before producing any Phase 3 artifact.
metadata:
  type: reference
---

# Dynatrace brand specification — Insights Forge deliverables

This spec is the single source of truth for brand conformance on Phase 3 artifacts produced by Insights Forge. The [exec-onepager](../../../skills/exec-onepager/SKILL.md) and [pptx-builder](../../../skills/pptx-builder/SKILL.md) skills both consult this file before producing output.

## Sources

| Source | Confirms |
|---|---|
| `Dynatrace_Brand_Insights-Forge.pptx` (project root, 2026-05-19) | **Authoritative.** Theme HEX values, theme fonts with Arial fallback, slide aspect ratio (16:9, 13.33" × 7.5"), 64 named slide layouts, slide master |
| `Dynatrace_Brand_Insights-Forge.pdf` (provided 2026-05-19) | Visual reference for the same template — content-card / chart / table / swimlane / gantt / timeline / funnel / hashtag-stat / funnel patterns, cover-slide aesthetic, footer pattern |
| `BAE9730_Insights-Lockup-*.svg` (provided 2026-05-19) | Insights product lockup is available in horizontal and vertical, in color (RGB), white, black, and gray variants |
| https://styleguide.dynatrace.com/docs/best-practices/top-10-tips | Voice and editorial rules |
| https://styleguide.dynatrace.com/docs/dynatrace-terminology | Product name capitalization, trademark symbols, disallowed phrasings |

When the `.pptx` and the PDF disagree, the `.pptx` wins — the rendered theme is the source of truth. Two HEX values were rounded in the PDF and have been corrected here from theme1.xml. Source files are referenced by name; the canonical originals live in Brandfolder (the official Dynatrace asset library) and should be re-downloaded from there for production rendering rather than embedded from this repo.

**Slide format:** 16:9 widescreen, 13.33" × 7.5" (12192000 × 6858000 EMU).

## 1. Logo usage

Two product lockups are available for Insights Forge artifacts:

- **Dynatrace Insights — horizontal lockup** — preferred for slide title bars and one-pager headers when horizontal space is available.
- **Dynatrace Insights — vertical lockup** — preferred for cover slides and tall layouts.

Each lockup ships in four color variants:

- **Color (RGB)** — full color on **light** backgrounds.
- **REV (Color reversed)** — full color tuned for **dark** backgrounds (use on cover slides).
- **White** — single-color white on dark or photo backgrounds where the color logo would clash.
- **Black** — single-color black on light backgrounds when the artifact will be printed in mono.
- **Gray** — secondary applications where the logo should de-emphasize.

A standalone **Dynatrace mark** (cube glyph only, no wordmark) is used in the page-number footer at lower-right of every slide.

**Rules:**
- Cover slide: use the Insights vertical or horizontal lockup in **REV color** on the dark particle background.
- Body slides: use the Dynatrace cube mark (color or gray) in the footer page-number group at lower-right.
- One-pager: use the Insights horizontal lockup at the top, in **Color** on a white background.
- Logo files are sourced from Brandfolder (Dynatrace's official asset library); do not generate or trace replacements.

## 2. Color palette

These HEX values are the **theme colors** programmed into the official `.pptx` template and must be used verbatim in charts, callouts, and any colored UI.

### Neutrals

| Role | Name | HEX | Use |
|---|---|---|---|
| Light 1 | White | `#FFFFFF` | Slide and one-pager backgrounds; reversed text on dark fills |
| Dark 1 | Black | `#000000` | Primary text on light backgrounds |
| Light 2 | Gray | `#6F747F` | Secondary text, footer copyright, dividers |
| Dark 2 | Deep navy | `#1A2440` | Cover-slide background; high-contrast accent fills |

### Brand accents

| Role | Name | HEX | Typical use |
|---|---|---|---|
| Accent 1 | Teal | `#49C2B3` | Confirmed / success state; first chart series |
| Accent 2 | Light blue | `#3BACF0` | Informational accent; sixth chart series |
| Accent 3 | Royal blue | `#1966FF` | Primary brand accent; CTAs; second chart series |
| Accent 4 | Purple | `#5E28E5` | Heading underline gradient anchor; fourth chart series |
| Accent 5 | Violet | `#8D1CDC` | Emphasis; third chart series |
| Accent 6 | Magenta | `#C93FDB` | Warning / attention; fifth chart series; gradient terminus |

Chart-series order is defined in section 5, which is authoritative for chart palettes; the labels above mirror it.

**Gradient bar** (used as section divider and table header): linear gradient running `Accent 2 → Accent 3 → Accent 4 → Accent 6` left to right.

**Semantic mapping** (Insights Forge convention; not in the brand guide but consistent with it):
- Confirmed hypothesis → Accent 1 (teal)
- Open / under investigation → Accent 3 (royal blue)
- Ruled out → Light 2 (gray)
- Instrumentation gap / risk → Accent 6 (magenta)

## 3. Typography

The full **DT Flow** family is available in this repo at `DTFlow/` (ten weights: Hairline, Thin, Extralight, Light, Regular, Medium, Semibold, Bold, Extrabold, Heavy). The `.pptx` theme binds `DTFlow-Medium` to the heading slot and `DTFlow-Light` to the body slot.

| Slot | Font | Use |
|---|---|---|
| Headings | **DTFlow-Medium** | Slide titles, section headers, KPI numbers |
| Body | **DTFlow-Light** | Body copy, table cells, captions |
| Emphasis within body | **DTFlow-Regular** or **DTFlow-Semibold** | Sparing — when bold is needed inside running body text |
| Large display numbers | **DTFlow-Bold** or **DTFlow-Heavy** | Cover-slide titles, oversized KPI numbers on hashtag-stat slides |

**Installation:** these fonts must be installed on the rendering machine for the `.pptx` to display correctly. On macOS, double-click each `.otf` in `DTFlow/` and select Install Font. On Linux render environments (e.g., LibreOffice / Pandoc-driven PDF), copy the files to `~/.fonts/` (or `/usr/local/share/fonts/`) and run `fc-cache -fv`.

**Fallback:** Arial is the secondary face in the same theme scheme inside `Dynatrace_Brand_Insights-Forge.pptx`. If a render environment cannot install DT Flow, Arial is the brand-sanctioned substitute (Light → Regular, Medium → Bold). When this happens, note `Rendered in Arial fallback` in the deliverable footer so the reader knows the typography is degraded.

**Capitalization:** **sentence case** for headings, subtitles, and titles. Not title case. (Per styleguide.dynatrace.com: "Sentence case is less formal and easier to read than title case.")

## 4. Layout conventions

### Cover slide (deck only)
- Background: deep navy → black with a particle / bokeh visual (blue and magenta particles flowing diagonally).
- Logo: Insights vertical or horizontal lockup in **REV color**, anchored top-left, ~120pt from left and top edges.
- Title: DT Flow Medium, white, lower-third anchored.
- Subtitle (audience, date): DT Flow Light, gray (`#6F747F`), beneath title.

### Section divider
- White background.
- Short gradient bar (left-aligned, ~270pt long, 8pt thick) running `Accent 2 → Accent 3 → Accent 4 → Accent 6`.
- Section title in DT Flow Medium below the bar.

### Content slide (body)
- White background.
- Title at top-left in DT Flow Medium.
- Footer at bottom: `© 2026 Dynatrace, LLC.` in Light 2 (`#6F747F`) at lower-left; Dynatrace cube mark + ` | ` + page number at lower-right.
- Use the eight content-card grid, three-column bucket layout, swimlane, gantt, timeline, hashtag-stat, or funnel patterns from the template — do not improvise layouts.

### One-pager (written deliverable)
- Letter or A4, portrait, single page.
- Top header: Insights horizontal lockup left, problem name + date right.
- Body: single column, optional sidebar callouts using Accent 3 or Accent 6 left-border rule.
- Footer: `© 2026 Dynatrace, LLC.` lower-left in Light 2; sources block above footer in 8pt DT Flow Light.

## 5. Chart palette

When rendering charts (bar, line, donut, table):

- Series 1 → Accent 1 (teal)
- Series 2 → Accent 3 (royal blue)
- Series 3 → Accent 5 (violet)
- Series 4 → Accent 4 (purple)
- Series 5 → Accent 6 (magenta)
- Series 6 → Accent 2 (light blue)
- Series 7+ → muted tints (50% opacity of above, in same order)

**Rules:**
- Gridlines: Light 2 (`#6F747F`) at 25% opacity, horizontal only.
- Axes labels: DT Flow Light, Black.
- Chart titles: DT Flow Medium, Black, sentence case.
- Do not use red or green as chart series colors — Dynatrace charts don't carry traffic-light semantics; status is communicated through the teal / royal-blue / gray / magenta semantic mapping in section 2 instead.
- For two-state comparisons (before/after, current/projected), use Accent 3 (royal blue) and Accent 6 (magenta).

## 6. Voice and tone

Source: [styleguide.dynatrace.com](https://styleguide.dynatrace.com/) — top 10 tips for content creators.

| Rule | Application in Insights Forge deliverables |
|---|---|
| Plain language | Replace jargon-heavy phrasings; "p95 latency rose 200ms" stays, but explain it on first use for VP audiences |
| Active voice | "We confirmed the iOS SDK regression" — not "the regression was confirmed" |
| Sentence case | Headings, slide titles, section headers — never title case |
| American English | "Analyze," "behavior," "optimization" — never "analyse," "behaviour," "optimisation" |
| Serial commas | "owner, timeframe, and cost" — always with the final comma |
| Concise | Cut hedging ("may possibly indicate") and unnecessary modifiers |
| Front-load keywords | First sentence of each finding states what changed, then evidence |
| Consistent terminology | Use the product names from section 7 verbatim; do not paraphrase product capabilities |
| No arbitrary ampersands | Write "owner and timeframe," not "owner & timeframe" |
| Punctuation only in sentences | Bullets without closing punctuation are fine when they are sentence fragments |

## 7. Product terminology

Source: [styleguide.dynatrace.com/docs/dynatrace-terminology](https://styleguide.dynatrace.com/docs/dynatrace-terminology)

### Registered trademarks (use `®` on first mention in formal writing)

- **Dynatrace®**
- **OneAgent®**
- **Smartscape®** real-time dependency graph
- **Grail®** unified data lakehouse

Subsequent mentions in the same document may drop the `®`. In informal contexts (internal notes, drafts), the `®` may be omitted entirely.

### Capitalized terms (no trademark symbol required)

- **AppEngine**
- **AutomationEngine**
- **ActiveGate** (one word, capital A and G)
- **Dynatrace Hub** or **Hub**
- **Dynatrace SaaS** (not lowercase "saas")
- **Keptn** (not "keptn")
- **Davis AI** — and its variants: **generative AI**, **causal AI**, **predictive AI**. The umbrella term is **Dynatrace Intelligence**.
- **Full-Stack Monitoring** (hyphenated when referring to the capability)

### Disallowed phrasings

| Don't use | Use instead |
|---|---|
| "Dynatrace Server" | "Dynatrace Cluster" |
| "out-of-the-box" | "ready-made" |
| "plugin" or "add-on" (for most extensions) | "extension" |
| "Dynatrace interface" | "Dynatrace web UI" |

## 8. Confidentiality and legal

- **Required footer** on every slide and one-pager page: `© 2026 Dynatrace, LLC.` (update the year at the start of each calendar year). Light 2 gray (`#6F747F`), lower-left.
- **Required classification marker**: `Confidential` in Light 2 gray, set to the right of the copyright string on the same footer line. Insights Forge deliverables default to confidential classification — they contain investigation framing, hypotheses, and instrumentation gap notes that should not leave the intended audience. If a specific deliverable is being shared with a customer or partner, the user must explicitly relabel it; the agent does not silently change classification.
- **Page numbering** (deck only): Dynatrace cube mark + ` | ` + page number at lower-right, in Light 2 gray.
- **Sources**: every externally sourced fact (per `skills/external-research/SKILL.md`) carries its URL + retrieval date in the "Sources" footnote block.

## 9. Slide layout binding (deck only)

`Dynatrace_Brand_Insights-Forge.pptx` ships with 64 named slide layouts on a single slide master. The pptx-builder skill binds each section of the standard six-section deck to a specific layout by name (not by index — indices are not stable across template updates).

### Default binding for the Insights Forge deck

| Deck section | Layout name | Notes |
|---|---|---|
| 1. Title slide | `Title slide_1 speaker` | Use the speaker variant; the simpler `Title Slide` works if no presenter is named |
| Section dividers between major sections | `Section Header` | Solo divider — keep to one per major transition |
| 2. Executive summary | `Title+content+eyebrow_left` | Eyebrow = "Executive summary"; title = the headline finding; content = the business impact |
| 3. Top findings (consolidated, 3 findings) | `3 icon cards+title` | Each card carries one finding with its evidence |
| 3. Top findings (consolidated, 4 findings) | `4 icon cards+title` | |
| 3. Top findings (one slide per finding) | `Title+content_left` | Use when a finding needs more depth than a card |
| 4. Recommended actions | `3 text columns` or `4 text columns` | Columns = action, owner, timeframe, cost. Use 3-col if cost rolls up |
| 5. Risks and decision asks | `Title+content+eyebrow_left` | Eyebrow = "Decision required"; content = the asks with magenta accent |
| 6. Appendix — issue tree / signals map | `Title+content_left` | One topic per appendix slide |
| 6. Appendix — ICE table | `Title+content_left` with an inline table | Use the gradient-header table style |
| Closing | `Thank you slide` | Optional |

### Alternative layouts available

If the content needs them, these named layouts are also in-template and safe to use:

- `Agenda` — when the deck warrants an agenda slide for Director audiences.
- `Quote` — for verbatim customer or stakeholder quotes that anchor a finding.
- `Customer story`, `Customer story_stats`, `Customer story_quote` — for narrative framing when the investigation has a clear "before" story.
- `Hero image+3 cards`, `Hero image+4 cards` — when a screenshot anchors the findings.
- `2 text columns`, `3 text columns`, `4 text columns`, `6 text columns` — for grid-style comparisons.
- `Image-fullscreen`, `Content+image_left`, `Content+image_right` — for screenshot evidence.
- `Section header+photo background` — heavier divider when a section change is dramatic.
- `Blank_graphic`, `Blank_black` — when you need to compose something custom on a clean background.

A full layout index is available alongside this spec in [reference/source-pdf-notes.md](reference/source-pdf-notes.md) and via inspection of the unzipped `.pptx`.

### What not to do

- Do not bind by layout index. Names are stable; indices shift when the brand team adds layouts.
- Do not modify the slide master. All customization happens at the slide layer.
- Do not introduce a layout that does not exist in the template. If the content needs something new, ask the user.

## 10. Open questions

Resolved gaps have moved into the spec body. These remain:

- **Photography and imagery rules** — only the cover-slide aesthetic (deep navy + blue/magenta particle visual) is confirmed. The template includes photo-backed layouts (`Section header+photo background`, `Image-fullscreen`, `Hero image+...`) but the rules for selecting photography are not documented in the materials reviewed. Use the `Blank_black` or non-photo variants until the team provides guidance.
- **Iconography** — Brandfolder is referenced as the icon source, but specific icon-set names and usage rules are not documented. Avoid icon use in Phase 3 deliverables until rules are confirmed.
- **Davis® trademark status** — `Dynatrace Intelligence` is the umbrella term and `Davis AI` is the named system, with generative / causal / predictive AI as named capabilities; the styleguide does not explicitly assign `Davis®`. Treat as un-trademarked until confirmed.
