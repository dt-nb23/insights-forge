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

## Important: this skill does not replace the standard pptx skill

If the runtime environment provides a standard pptx skill at `/mnt/skills/public/pptx/SKILL.md`, this skill's job is to **adapt the one-pager into a deck structure and then invoke that skill** to render the actual `.pptx` file. This skill is an **adapter**, not a renderer.

If the standard pptx skill is not available in the current environment, this skill falls back to writing a structured slide-by-slide markdown outline that the team can paste into their preferred deck tool. Always verify availability before assuming the renderer exists.

## Deck structure

A six-section deck adapted from the one-pager. Adjust slide counts to match the stakeholder profile — a VP wants 6–8 slides; a Director may tolerate 10–12 with more technical depth.

1. **Title slide** — Problem name, audience, date, presenter.
2. **Executive summary** — the one-pager's "Problem summary" and "Business impact" sections, on a single slide. Lead with the business number; the technical signal is secondary.
3. **Top findings** — one slide per finding, or one consolidated slide with 3–5 bullets, depending on stakeholder profile depth tolerance. Include the evidence that supports each finding (a chart, a stat, a comparison).
4. **Recommended actions** — one slide. Owner, timeframe, and cost paired with each action. Sequencing visible if it matters.
5. **Risks and decision asks** — one slide. The questions leadership needs to answer; the decisions being requested. Make the asks visually distinct (bolded, separate section, or call-out box).
6. **Appendix** — optional. Supporting detail: signals map excerpts, the issue tree, ICE table, instrumentation gap list. Only included if the stakeholder profile says they read appendices.

## Steps

1. **Check for the standard pptx skill** at `/mnt/skills/public/pptx/SKILL.md`. If it exists, plan to invoke it; if not, plan a structured markdown outline.
2. **Map the one-pager content into the six-section structure** above. Each section becomes one or more slides per the stakeholder profile.
3. **Identify which numbers, tables, or charts need to be included.** Pull from `signals-map.md` and `action-plan.md`. Do not invent data; if a chart would be needed but the data is not in the project space, flag it and ask the user.
4. **Adapt language for slide format.** Sentences become bullet fragments. Definitions move to footnotes. Long lists of caveats become a single qualifier or move to appendix.
5. **Preserve the quality-gate outputs.** The Consultative-lens rewrites, the Customer-lens framings, and the Skeptic-lens "questions a leader will ask" are all baked into the one-pager already — do not undo them when adapting to slide format.
6. **Carry citations into a "Sources" slide or footer.** Any externally sourced fact in the one-pager (per `skills/external-research/SKILL.md`) keeps its URL + retrieval date. Put them on a final "Sources" slide for VP audiences who skim, or in a small footer on each slide where the fact appears for Director audiences who scrutinize. Do not drop citations during the adaptation.
7. **Invoke the standard pptx skill** with the structured content if available; otherwise write the structured outline to `memory/project-space/deck-outline-YYYY-MM-DD.md` for the team to render manually.

## Output

- Preferred: a rendered `.pptx` file produced by the standard pptx skill.
- Fallback: `memory/project-space/deck-outline-YYYY-MM-DD.md` — a slide-by-slide markdown outline ready to be turned into a deck.

## Common pitfalls

- **Auto-generating before approval.** Phase 3 has its own gate. Wait for the user to approve the one-pager before producing the deck.
- **Re-thinking the message in the adaptation.** The one-pager is the message. The deck is its visual form. Do not introduce new findings or new framings at this step.
- **Over-packing slides.** A deck is not a one-pager in landscape format. Each slide should carry one idea well, not five ideas poorly.
- **Skipping the appendix decision.** Read the stakeholder profile. Some leaders read appendices; some never look past slide 4. Build accordingly.
- **Assuming the renderer exists.** Always check for the standard pptx skill at runtime — environments differ.
