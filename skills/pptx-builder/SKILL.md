---
name: pptx-builder
description: Procedure for producing the Phase 3 PowerPoint deck from an approved one-pager. Use only after the one-pager has been explicitly approved by the user.
---

# PPTX Builder

## When to use

After the Phase 3 one-pager (at `<ENGAGEMENT_PATH>/one-pager-YYYY-MM-DD.md`) has been **explicitly approved** by the user. The PPTX is not auto-generated — the agent waits for explicit go-ahead.

Use this skill when:

- The one-pager has been approved and the user has confirmed a deck is needed for the leadership review.
- An existing deck needs revision following one-pager revisions.

## Inputs

**Resolve the engagement path first (before reading any files):**

1. Use the `ENGAGEMENT_PATH` already established for this session. The agent fixes it once — when Phase 0 (`context-framing`) creates the engagement folder, or when a paused/active engagement is resumed — and holds it in working context for the rest of the session. There is **no shared pointer file** to read; nothing depends on a global "active" file a second concurrent session could overwrite.
2. If no engagement is established yet (a fresh session picking up earlier work), resolve it with the resume procedure in `skills/investigation-reset/SKILL.md`: scan `memory/clients/*/engagements/*/current-context.md` for a `state:` of `active` or `paused`, present the matches, and have the user pick one. If none, stop: "No active engagement found. Start a new engagement or resume a paused one."
3. ENGAGEMENT_PATH = the established/selected path (e.g., `memory/clients/acme-corp/engagements/2026-06-18-api-latency/`). CLIENT_NAME = the segment between `memory/clients/` and `/engagements/`.
4. All phase file reads use ENGAGEMENT_PATH as the base — e.g., `<ENGAGEMENT_PATH>/one-pager-YYYY-MM-DD.md`.

Then read these files:

- `<ENGAGEMENT_PATH>/one-pager-YYYY-MM-DD.md` — the approved one-pager content (markdown version). If an HTML one-pager also exists in the project root, read it alongside the markdown to extract the visual design decisions already made (wave choices, color emphasis, section structure) — the deck must be visually coherent with the one-pager, not a fresh design.
- `memory/long-term/stakeholder-profiles.md` — hub index (loaded at session init). Read the specific profile file for the intended reader (e.g., `memory/long-term/profiles/executive-sponsor.md`) to calibrate pacing, depth, and visual emphasis.
- `<ENGAGEMENT_PATH>/signals-map.md` and `<ENGAGEMENT_PATH>/action-plan.md` — for any supporting numbers, charts, or appendix material the one-pager pointed to.
- `memory/long-term/brand/brand-spec.md` — **mandatory.** The Dynatrace brand spec. Governs cover-slide aesthetic, section-divider pattern, content-card / chart / table layouts, footer text, chart series colors, and product-name capitalization.
- `memory/long-term/brand/reference/source-pdf-notes.md` — page-by-page index of the source brand PDF, useful when picking a layout pattern.
- `memory/long-term/brand/reference/pptx-layout-index.md` — complete catalog of the 64 named layouts in the `.pptx` template, grouped by purpose. Consult before picking a non-default layout.
- `DT Insights Lockup RGB/` — local SVG lockup files for all Insights variants (horizontal and vertical, in Black, Gray, REV, and White). Use these before checking Brandfolder — they are the same source files. See lockup selection rules below.
- `assets/` — pre-rendered wave PNGs already used in the HTML one-pager. Reuse them in the deck for visual consistency rather than re-rendering from scratch.

## Renderer priority

The **in-repo generator is the primary renderer.** Use `tools/pptx-generator.py` unless it is not runnable (python-pptx not installed, no Python). The external skill at `/mnt/skills/public/pptx/SKILL.md` is a secondary option — check for it only if the generator is unavailable. If neither is usable, fall back to a structured slide-by-slide markdown outline at `<ENGAGEMENT_PATH>/deck-outline-YYYY-MM-DD.md`.

## Deck structure

A six-section deck adapted from the one-pager. Adjust slide counts to match the stakeholder profile — a VP wants 6–8 slides; a Director may tolerate 10–12 with more technical depth. Each section binds to a named layout in `Dynatrace_Brand_Insights-Forge.pptx`; do not invent layouts.

| # | Slide | Layout name (bind by name, not index) | Notes |
|---|---|---|---|
| 1 | **Title slide** — problem name, audience, date, presenter | `Title slide_1 speaker` (or `Title Slide` if no presenter named) | Cover aesthetic — deep navy `#1A2440` background with particle / bokeh visual is built into the master |
| — | **Section divider** between major sections | `Section Header` | Keep to one per major transition |
| 2 | **Executive summary** — problem summary + business impact, on one slide. Lead with the business number | `Title+content+eyebrow_left` | Eyebrow = "Executive summary"; title = the headline finding; content = the business impact |
| 3 | **Top findings** — 3 findings consolidated | `3 icon cards+title` | Each card carries one finding with its evidence |
| 3 | **Top findings** — 4 findings consolidated | `4 icon cards+title` | |
| 3 | **Top findings** — one slide per finding (depth audience) | `Title+content_left` | Use when a finding needs more depth than a card |
| 4 | **Recommended actions** — 3 columns (action / owner / timeframe) | `3 text columns` | |
| 4 | **Recommended actions** — 4 columns (action / owner / timeframe / cost) | `4 text columns` | Use when cost / risk is itemized per action |
| 5 | **Risks and decision asks** — the questions leadership must answer; the decisions being requested | `Title+content+eyebrow_left` | Eyebrow = "Decision required"; magenta accent on the asks |
| 6 | **Appendix** — issue tree / signals map / instrumentation gap list | `Title+content_left` | One topic per appendix slide |
| 6 | **Appendix** — ICE table | `Title+content_left` with inline gradient-header table | |
| — | **Closing** | `Thank you slide` | Optional |

Alternative layouts (`Agenda`, `Quote`, `Customer story`, `Hero image+...`, image-led variants, `Blank_graphic`/`Blank_black`) are catalogued in `memory/long-term/brand/reference/pptx-layout-index.md`. Substitute when content warrants — never improvise on the slide master.

Every body slide carries the footer from brand-spec §8: `© 2026 Dynatrace, LLC.   Confidential` at lower-left in Light 2 gray (`#6F747F`); Dynatrace cube mark + ` | ` + page number at lower-right. Insights Forge deliverables are Confidential by default — do not relabel without explicit user instruction.

## Lockup selection by slide type

The Insights lockup SVG files are in `DT Insights Lockup RGB/`. Always pick the variant that matches the slide background — never substitute a generated or recolored version.

| Slide background | Lockup variant | File |
|---|---|---|
| Dark (cover, section divider with photo, any navy/black slide) | **REV** — full-color reversed for dark surfaces | `BAE9730_Insights-Lockup-Horizontal-RGB_REV.svg` |
| White or light gray (all body/content slides) | **Black** — single-color black for print-safe legibility | `BAE9730_Insights-Lockup-Horizontal-RGB_Black.svg` |
| Grayscale print output | **Gray** | `BAE9730_Insights-Lockup-Horizontal-RGB_Gray.svg` |
| White reversed (rare — white lockup on a non-navy dark bg) | **White** | `BAE9730_Insights-Lockup-Horizontal-RGB_White.svg` |

Use the horizontal lockup for slide title bars and one-pager headers where horizontal space is available. Use the vertical lockup for cover slides and tall layouts only. The Dynatrace cube mark (standalone glyph) goes in the lower-right footer of every body slide — it is embedded in the `.pptx` master and does not need to be separately placed.

## Wave backgrounds for dark slides

The brand spec describes the cover slide as "deep navy → black with a particle / bokeh visual (blue and magenta particles flowing diagonally)." This visual is sourced from the `Data-Visual-waves/` design kit. The same selection rules that govern the HTML one-pager apply here — **readability is the deciding factor**.

**Which slides get a wave background:** only dark slides (cover, closing, and any "decision required" accent slide). Section dividers and all body/content slides use white backgrounds per the template; do not add wave images to them.

**Wave series selection for dark slides:**

| Series | Best for | Avoid when |
|---|---|---|
| `datalargebeam` | Cover slide, closing slide — smooth continuous beams do not compete with large headline text | Never avoid on dark slides; safe at all text sizes |
| `datatrail` | Decision-required accent slides, secondary dark strips — single thin arc is minimal and decorative | Never avoid; lowest visual noise of any series |
| `dataflow` | Cover slide only, where the only text is the large title (≥40px) and the subtitle | **Do not use on any slide with body text or label text ≤18px** — particle dots fragment letterforms |
| `datablocks` | Decorative closing slides with minimal text | Dense text slides |
| `dataparticles` | **Verify before use** — some files in this series were saved without PDF compatibility and render blank. Test with `qlmanage` before including |

The one-pager already has rendered wave PNGs in `assets/`. Reuse `assets/wave-bg.png` for the cover slide to keep the visual language consistent between the one-pager and deck. If the deck needs a different wave, render the `.ai` file using the procedure in `skills/exec-onepager/SKILL.md` (wave asset rendering section).

**Applying a wave background in the deck:** in the `.pptx`, insert the PNG as a slide background image behind all other elements, then apply a dark overlay shape (rectangle, no border, fill `#1A2440` at 70–85% transparency) over it to ensure all text reads cleanly. The overlay opacity should be higher (80–85%) where body text appears, lower (65–70%) where only the large title sits.

## Steps

1. **Read `memory/long-term/brand/brand-spec.md`.** Carry the exact HEX values, font names (DT Flow Medium / DT Flow Light, Arial fallback), and footer text into whatever you produce next. Also check whether `python3 -c "import pptx"` succeeds to confirm the generator is runnable; if not, note the fallback plan now (external skill check or markdown outline).
2. **Map the one-pager content into the six-section structure** above. Each section becomes one or more slides per the stakeholder profile and adopts the brand pattern keyed in the table.
3. **Adapt language for slide format — then run the brand-humanizer pre-pass.**
   - Condense one-pager prose into slide-appropriate fragments: sentences become bullets, definitions move to footnotes, long caveats become a single qualifier or move to appendix. Headings remain sentence case (brand-spec §3 and §6); product names follow §7.
   - After condensing, read `skills/brand-humanizer/SKILL.md` and run the full procedure on all slide copy: titles, eyebrows, bullet text, card headers, stat labels, and decision asks. Slide titles are the highest-risk element — compression frequently reintroduces title case and em dashes. Fix them before generating any slide content.
4. **Identify which numbers, tables, or charts need to be included.** Pull from `signals-map.md` and `action-plan.md`. Do not invent data; if a chart would be needed but the data is not in the engagement folder, flag it and ask the user. Chart series colors follow brand-spec §5 — never use red or green.
5. **Preserve the quality-gate outputs.** The Consultative-lens rewrites, the Customer-lens framings, and the Skeptic-lens "questions a leader will ask" are all baked into the one-pager already — do not undo them when adapting to slide format.
6. **Carry citations into a "Sources" slide or footer.** Any externally sourced fact in the one-pager (per `skills/external-research/SKILL.md`) keeps its URL + retrieval date. Put them on a final "Sources" slide for VP audiences who skim, or in a small footer on each slide where the fact appears for Director audiences who scrutinize. Do not drop citations during the adaptation.
7. **Generate the deck.** Write the JSON spec to `<ENGAGEMENT_PATH>/deck-spec-YYYY-MM-DD.json` (see `tools/pptx-spec-example.json` for the format). Then run:

   ```bash
   python3 tools/pptx-generator.py <ENGAGEMENT_PATH>/deck-spec-YYYY-MM-DD.json
   ```

   The output `.pptx` saves to `<ENGAGEMENT_PATH>/deck-YYYY-MM-DD.pptx`. If the generator is unavailable, check for the external skill at `/mnt/skills/public/pptx/SKILL.md` and invoke it; if that is also absent, write the structured outline to `<ENGAGEMENT_PATH>/deck-outline-YYYY-MM-DD.md`. When the team renders manually, instruct them to start from the official Dynatrace `.potx` — the theme colors and fonts are embedded in it.

## Output

- **Preferred: run `tools/pptx-generator.py`** with a JSON spec file.
  The generator is the in-repo equivalent of the standard pptx skill.
  It handles template loading, sample-slide removal, layout dispatch,
  placeholder filling, and output path. The external skill at
  `/mnt/skills/public/pptx/SKILL.md` is a secondary option — check for it
  only if the generator is unavailable.

  ```bash
  # Generate the deck
  python3 tools/pptx-generator.py <ENGAGEMENT_PATH>/deck-spec-YYYY-MM-DD.json

  # List all available layout names
  python3 tools/pptx-generator.py --list-layouts
  ```

  Write the spec to `<ENGAGEMENT_PATH>/deck-spec-YYYY-MM-DD.json` before running.
  The output `.pptx` saves to `<ENGAGEMENT_PATH>/deck-YYYY-MM-DD.pptx` by default.
  See `tools/pptx-spec-example.json` for the full spec format with comments.

- **Fallback (if python-pptx is unavailable):** write a structured
  slide-by-slide outline to `<ENGAGEMENT_PATH>/deck-outline-YYYY-MM-DD.md`
  using the same spec fields, so a human can build it manually from the template.

## Common pitfalls

- **Auto-generating before approval.** Phase 3 has its own gate. Wait for the user to approve the one-pager before producing the deck.
- **Re-thinking the message in the adaptation.** The one-pager is the message. The deck is its visual form. Do not introduce new findings or new framings at this step.
- **Over-packing slides.** A deck is not a one-pager in landscape format. Each slide should carry one idea well, not five ideas poorly.
- **Skipping the appendix decision.** Read the stakeholder profile. Some leaders read appendices; some never look past slide 4. Build accordingly.
- **Assuming the renderer exists.** Confirm the in-repo generator is runnable at Step 1 (`python3 -c "import pptx"`); fall back to the external pptx skill only if the generator is unavailable, and to a markdown outline last.
- **Going off-brand.** Using off-palette colors, title-case headings, or improvised layouts breaks the brand. Stick to the patterns in `brand-spec.md` — the eight-card grid, three-bucket layout, swimlane, gantt, timeline, hashtag-stat, table, and funnel are the approved compositions. If the content doesn't fit one of those, the content is wrong, not the template.
- **Sourcing the lockup from Brandfolder when local files exist.** `DT Insights Lockup RGB/` contains all eight lockup variants. Use the correct variant for the slide background (REV on dark, Black on white) — do not generate, trace, or recolor any lockup regardless of source.
- **Using the wrong lockup variant.** REV on a white background makes the color lockup nearly invisible; Black on a dark background disappears. Always match the variant to the surface.
- **Using a particle wave (dataflow series) on any slide with body text.** The same failure mode from the HTML one-pager applies in the deck: particle dots compete with letterforms at small sizes. Use `datalargebeam` or `datatrail` on any dark slide that carries text below 24pt.
- **Re-rendering wave assets the HTML one-pager already rendered.** `assets/wave-bg.png` and `assets/wave-ask.png` are already at 2800px width. Reuse them for consistency and to avoid a duplicate render step.
- **Designing the deck visually independently of the one-pager.** The one-pager is the approved design reference. If an HTML one-pager exists, its color choices, section order, and wave selections are already approved — carry them into the deck rather than redesigning from the brand spec alone.
