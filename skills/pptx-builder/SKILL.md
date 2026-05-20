---
name: pptx-builder
description: Procedure for producing the Phase 3 PowerPoint deck from an approved one-pager. Use only after the one-pager has been explicitly approved by the user.
---

# PPTX Builder

## When to use

After the Phase 3 one-pager (`memory/project-space/one-pager-YYYY-MM-DD.md`) has been **explicitly approved** by the user. The PPTX is not auto-generated — the agent waits for explicit go-ahead.

Use this skill when:

- The one-pager has been approved and the user has confirmed a deck is needed for the leadership review.
- An existing deck needs revision following one-pager revisions.

## Inputs

Read these files before starting:

- `memory/project-space/one-pager-YYYY-MM-DD.md` — the approved one-pager content.
- `memory/long-term/stakeholder-profiles.md` — the profile of the intended reader, to inform pacing, depth, and visual emphasis.
- `memory/project-space/signals-map.md` and `action-plan.md` — for any supporting numbers, charts, or appendix material the one-pager pointed to.
- `memory/long-term/brand/brand-spec.md` — **mandatory.** The Dynatrace brand spec. Governs cover-slide aesthetic, section-divider pattern, content-card / chart / table layouts, footer text, chart series colors, and product-name capitalization.
- `memory/long-term/brand/reference/source-pdf-notes.md` — page-by-page index of the source brand PDF, useful when picking a layout pattern.
- `memory/long-term/brand/reference/pptx-layout-index.md` — complete catalog of the 64 named layouts in the `.pptx` template, grouped by purpose. Consult before picking a non-default layout.

## Important: this skill does not replace the standard pptx skill

If the runtime environment provides a standard pptx skill at `/mnt/skills/public/pptx/SKILL.md`, this skill's job is to **adapt the one-pager into a deck structure and then invoke that skill** to render the actual `.pptx` file. This skill is an **adapter**, not a renderer.

If the standard pptx skill is not available in the current environment, this skill falls back to writing a structured slide-by-slide markdown outline that the team can paste into their preferred deck tool. Always verify availability before assuming the renderer exists.

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

## Steps

1. **Check for the standard pptx skill** at `/mnt/skills/public/pptx/SKILL.md`. If it exists, plan to invoke it; if not, plan a structured markdown outline.
2. **Read `memory/long-term/brand/brand-spec.md`.** Carry the exact HEX values, font names (DT Flow Medium / DT Flow Light, Arial fallback), and footer text into whatever you produce next — outline notes for the human renderer, or parameters to the standard pptx skill.
3. **Map the one-pager content into the six-section structure** above. Each section becomes one or more slides per the stakeholder profile and adopts the brand pattern keyed in the table.
4. **Identify which numbers, tables, or charts need to be included.** Pull from `signals-map.md` and `action-plan.md`. Do not invent data; if a chart would be needed but the data is not in the project space, flag it and ask the user. Chart series colors follow brand-spec §5 — never use red or green.
5. **Adapt language for slide format.** Sentences become bullet fragments. Definitions move to footnotes. Long lists of caveats become a single qualifier or move to appendix. Headings remain sentence case (brand-spec §3 and §6); product names follow §7.
6. **Preserve the quality-gate outputs.** The Consultative-lens rewrites, the Customer-lens framings, and the Skeptic-lens "questions a leader will ask" are all baked into the one-pager already — do not undo them when adapting to slide format.
7. **Carry citations into a "Sources" slide or footer.** Any externally sourced fact in the one-pager (per `skills/external-research/SKILL.md`) keeps its URL + retrieval date. Put them on a final "Sources" slide for VP audiences who skim, or in a small footer on each slide where the fact appears for Director audiences who scrutinize. Do not drop citations during the adaptation.
8. **Invoke the standard pptx skill** with the structured content if available; otherwise write the structured outline to `memory/project-space/deck-outline-YYYY-MM-DD.md` for the team to render manually. When the team renders manually, instruct them to start from the official Dynatrace `.potx` (the file the brand PDF documents) rather than a blank deck — the theme colors and theme fonts are programmed into it.

## Output

- Preferred: a rendered `.pptx` file produced by the standard pptx skill.
- Fallback: `memory/project-space/deck-outline-YYYY-MM-DD.md` — a slide-by-slide markdown outline ready to be turned into a deck.

## Common pitfalls

- **Auto-generating before approval.** Phase 3 has its own gate. Wait for the user to approve the one-pager before producing the deck.
- **Re-thinking the message in the adaptation.** The one-pager is the message. The deck is its visual form. Do not introduce new findings or new framings at this step.
- **Over-packing slides.** A deck is not a one-pager in landscape format. Each slide should carry one idea well, not five ideas poorly.
- **Skipping the appendix decision.** Read the stakeholder profile. Some leaders read appendices; some never look past slide 4. Build accordingly.
- **Assuming the renderer exists.** Always check for the standard pptx skill at runtime — environments differ.
- **Going off-brand.** Using off-palette colors, title-case headings, or improvised layouts breaks the brand. Stick to the patterns in `brand-spec.md` — the eight-card grid, three-bucket layout, swimlane, gantt, timeline, hashtag-stat, table, and funnel are the approved compositions. If the content doesn't fit one of those, the content is wrong, not the template.
- **Inventing logos or icons.** Source the Insights lockup and the Dynatrace cube mark from Brandfolder. Do not generate, trace, or recolor them.
