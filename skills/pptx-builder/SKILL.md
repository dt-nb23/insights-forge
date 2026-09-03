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

- `<ENGAGEMENT_PATH>/one-pager-YYYY-MM-DD.md` — the approved one-pager content (markdown version). If the HTML one-pager also exists (at `<ENGAGEMENT_PATH>/<slug>-onepager.html`), read it alongside the markdown to extract the visual design decisions already made (wave choices, color emphasis, section structure) — the deck must be visually coherent with the one-pager, not a fresh design.
- `memory/long-term/stakeholder-profiles.md` — hub index (loaded at session init). Read the specific profile file for the intended reader (e.g., `memory/long-term/profiles/executive-sponsor.md`) to calibrate pacing, depth, and visual emphasis.
- `<ENGAGEMENT_PATH>/signals-map.md` and `<ENGAGEMENT_PATH>/action-plan.md` — for any supporting numbers, charts, or appendix material the one-pager pointed to.
- `memory/long-term/brand/brand-spec.md` — **mandatory.** The Dynatrace brand spec. Governs cover-slide aesthetic, section-divider pattern, content-card / chart / table layouts, footer text, chart series colors, and product-name capitalization.
- `memory/long-term/brand/reference/source-pdf-notes.md` — page-by-page index of the source brand PDF, useful when picking a layout pattern.
- `memory/long-term/brand/reference/pptx-layout-index.md` — complete catalog of the 64 named layouts in the `.pptx` template, grouped by purpose. Consult before picking a non-default layout.
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
| 6 | **Appendix** — issue tree / signals map / ICE table / instrumentation gap list | `Title+content_left` | One topic per appendix slide |
| — | **Closing** | `Thank you slide` | Optional |

Alternative layouts (`Agenda`, `Quote`, `Customer story`, `Hero image+...`, image-led variants, `Blank_graphic`/`Blank_black`) are catalogued in `memory/long-term/brand/reference/pptx-layout-index.md`. Substitute when content warrants — never improvise on the slide master.

Every body slide carries the footer from brand-spec §8: `© 2026 Dynatrace, LLC.   Confidential` at lower-left in Light 2 gray (`#6F747F`); Dynatrace cube mark + ` | ` + page number at lower-right. Insights Forge deliverables are Confidential by default — do not relabel without explicit user instruction.

## Wave backgrounds for dark slides

The brand spec describes the cover slide as "deep navy → black with a particle / bokeh visual (blue and magenta particles flowing diagonally)." The same selection rule that governs the HTML one-pager applies here — **readability is the deciding factor**.

**Which slides get a wave background:** only dark accent slides — the closing slide and at most one "decision required" accent slide. The cover layouts already carry the brand visual in the master, so they need no wave. Section dividers and all other body/content slides use white backgrounds per the template; do not add wave images to them.

**The two waves the workflow can use** are the pre-rendered PNGs in `assets/`, the same files the HTML one-pager uses, so the deck stays visually coherent with it:

| Spec key | File | Use for |
|---|---|---|
| `wave-bg` | `assets/wave-bg.png` | Closing slide, or any dark slide where only a large title sits over the wave (smooth beams do not compete with headline text) |
| `wave-ask` | `assets/wave-ask.png` | The decision-required accent slide — a single thin arc, the lowest visual noise, safe under body text |

The agent does not render new wave variants: the Illustrator design kit is outside the repo, and a particle-style wave under body text fragments letterforms. If the deck genuinely needs a different wave, the user renders it outside this workflow and drops the PNG into `assets/`; the spec then names it by repo-relative path.

**Applying a wave background in the deck:** set the `wave_background` key on the slide's spec entry and control the dark overlay with `wave_overlay_opacity` (0.0–1.0; the generator defaults to 0.80, which suits dark slides carrying body text — lower it toward 0.70 when only the large title sits over the wave). The generator inserts the PNG behind all content, applies the deep-navy `#1A2440` overlay, turns the slide's text white so it stays legible, and re-adds the brand-spec §8 footer line above the overlay (the layout's own footer is covered by it). Do not hand-place overlay rectangles or recolor text yourself.

## Steps

1. **Read `memory/long-term/brand/brand-spec.md`.** Carry the exact HEX values, font names (DT Flow Medium / DT Flow Light, Arial fallback), and footer text into whatever you produce next. Also check whether `python3 -c "import pptx"` succeeds to confirm the generator is runnable; if not, note the fallback plan now (external skill check or markdown outline).
2. **Map the one-pager content into the six-section structure** above. Each section becomes one or more slides per the stakeholder profile and adopts the brand pattern keyed in the table.
3. **Adapt language for slide format — then run the brand-humanizer pre-pass.**
   - Condense one-pager prose into slide-appropriate fragments: sentences become bullets, definitions move to footnotes, long caveats become a single qualifier or move to appendix. Headings remain sentence case (brand-spec §3 and §6); product names follow §7.
   - After condensing, read `skills/brand-humanizer/SKILL.md` and run the full procedure on all slide copy: titles, eyebrows, bullet text, card headers, stat labels, and decision asks. Slide titles are the highest-risk element — compression frequently reintroduces title case and em dashes. Fix them before generating any slide content.
4. **Identify which numbers, tables, or charts need to be included.** Pull from `signals-map.md` and `action-plan.md`. Do not invent data; if a chart would be needed but the data is not in the engagement folder, flag it and ask the user. Chart series colors follow brand-spec §5 — the generator applies the §5 series order (Teal → Magenta accents) to every chart automatically; never override it with red or green.
5. **Preserve the quality-gate outputs.** The Consultative-lens rewrites, the Customer-lens framings, and the Skeptic-lens "questions a leader will ask" are all baked into the one-pager already — do not undo them when adapting to slide format.
6. **Carry citations into a "Sources" slide or footer.** Any externally sourced fact in the one-pager (per `skills/external-research/SKILL.md`) keeps its URL + retrieval date. Put them on a final "Sources" slide for VP audiences who skim, or in a small footer on each slide where the fact appears for Director audiences who scrutinize. Do not drop citations during the adaptation.
7. **Generate the deck.** Write the JSON spec to `<ENGAGEMENT_PATH>/deck-spec-YYYY-MM-DD.json` (see `tools/pptx-spec-example.json` for the format). Then run, passing the output path explicitly as the second positional argument (the generator has no `--output` flag) so the deck lands in the engagement folder:

   ```bash
   python3 tools/pptx-generator.py <ENGAGEMENT_PATH>/deck-spec-YYYY-MM-DD.json <ENGAGEMENT_PATH>/deck-YYYY-MM-DD.pptx
   ```

   If the generator is unavailable, check for the external skill at `/mnt/skills/public/pptx/SKILL.md` and invoke it; if that is also absent, write the structured outline to `<ENGAGEMENT_PATH>/deck-outline-YYYY-MM-DD.md`. When the team renders manually, instruct them to start from the official Dynatrace `.potx` — the theme colors and fonts are embedded in it.
8. **Present the deck at the Phase 3 gate — do not end silently.** After generation, first run the **exclusion scan**: read the Out-of-scope exclusions in `<ENGAGEMENT_PATH>/current-context.md` and scan the deck spec JSON (every title, bullet, card, column, and appendix line) against them; remove any hit, regenerate, and report it. Then present the deck using the same Phase 3 gate frame as the one-pager (per CLAUDE.md "Gate summary block"):
   1. **Conclusion** — the decision the deck asks for, in one sentence.
   2. **What changed** — what the deck adds or condenses versus the approved one-pager (slide count, appendix decisions, charts included), and any generator warnings acted on (dropped or re-sized slots, fallback fonts).
   3. **Assumptions and confidence gaps** — any chart built from numbers the engagement folder does not fully support, any slide where compression changed a qualifier, anything the reader's profile suggests they may skip.
   4. **Out-of-scope cost** — hits from the exclusion scan, with what was removed; otherwise "No out-of-scope items arose this phase."
   5. **Approve / Redirect / Iterate** — "**Approve** to finalize the Phase 3 deliverables, **Redirect** [slide, emphasis, or structure change], or **Iterate** [lens to run on the deck]."

   Record the gate decision in `<ENGAGEMENT_PATH>/decisions-log.md` (row label `Phase 3 Deliver — deck`); on approval, set today's `last-touched:` in `current-context.md` (`phase:` stays `3`; archiving is a separate `investigation-reset` step).

## Output

- **Preferred: run `tools/pptx-generator.py`** with a JSON spec file.
  The generator is the in-repo equivalent of the standard pptx skill.
  It handles template loading, sample-slide removal, layout dispatch,
  placeholder filling, and output path. The external skill at
  `/mnt/skills/public/pptx/SKILL.md` is a secondary option — check for it
  only if the generator is unavailable.

  ```bash
  # Generate the deck (spec path, then output path — both explicit)
  python3 tools/pptx-generator.py <ENGAGEMENT_PATH>/deck-spec-YYYY-MM-DD.json <ENGAGEMENT_PATH>/deck-YYYY-MM-DD.pptx

  # List all available layout names
  python3 tools/pptx-generator.py --list-layouts
  ```

  Write the spec to `<ENGAGEMENT_PATH>/deck-spec-YYYY-MM-DD.json` before running.
  Always pass the output path (the second positional argument — there is no
  `--output` flag) so the deck lands at `<ENGAGEMENT_PATH>/deck-YYYY-MM-DD.pptx`;
  omitted, the generator defaults to `deck-<today>.pptx` next to the spec file.
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
- **Using a particle wave (dataflow series) on any slide with body text.** The same failure mode from the HTML one-pager applies in the deck: particle dots compete with letterforms at small sizes. Use `datalargebeam` or `datatrail` on any dark slide that carries text below 24pt.
- **Re-rendering wave assets the HTML one-pager already rendered.** `assets/wave-bg.png` and `assets/wave-ask.png` are already at 2800px width. Reuse them for consistency and to avoid a duplicate render step.
- **Designing the deck visually independently of the one-pager.** The one-pager is the approved design reference. If an HTML one-pager exists, its color choices, section order, and wave selections are already approved — carry them into the deck rather than redesigning from the brand spec alone.
