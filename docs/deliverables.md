# Phase 3 deliverables — brand, layout, voice

Phase 3 is where the workspace earns its keep — a one-page written summary and a PowerPoint deck, both brand-conformant and tuned to a *named* stakeholder. This page walks you through what the brand spec actually requires, how the one-pager and deck come together, and how to spot-check brand conformance before sending.

If you remember one thing: the **brand spec is authoritative**. The agent will not improvise off-palette colors, off-brand fonts, or made-up layouts — and you shouldn't either. The spec lives at [`memory/long-term/brand/brand-spec.md`](../memory/long-term/brand/brand-spec.md) and is loaded before any Phase 3 artifact gets produced.

## What the brand spec covers

The spec is the single source of truth for these eight dimensions:

| Dimension | Where in the spec |
|---|---|
| Color palette (HEX values) | Color section |
| Typography (DT Flow Medium / DT Flow Light, Arial fallback) | Typography section |
| Slide format (16:9, 13.33" × 7.5") | Header |
| Layout templates (64 named slide layouts) | Layout patterns section |
| Logo lockups (horizontal preferred for headers) | Logo usage section |
| Voice and tone | Voice section, sourced from `styleguide.dynatrace.com` |
| Product-name capitalization (Dynatrace®, OneAgent®, Grail®, Smartscape®, AppEngine, ActiveGate, Davis AI) | Terminology section |
| Footer conventions | Footer section |

Each of these is sourced from one of three places — the spec's "Sources" table lists which source confirms which dimension. When the official PowerPoint template and the brand PDF disagree, the **PowerPoint wins** because it's what gets rendered.

**Source files in this repo.**

- [`Dynatrace_Brand_Insights-Forge.pptx`](../Dynatrace_Brand_Insights-Forge.pptx) — the rendered theme; source of truth.
- [`DTFlow/`](../DTFlow/) — the DT Flow typeface files.
- [`memory/long-term/brand/`](../memory/long-term/brand/) — the spec and supporting reference notes.

## What the one-pager looks like

Produced by [`skills/exec-onepager/SKILL.md`](../skills/exec-onepager/SKILL.md). One page, written for a *named* stakeholder pulled from [`memory/long-term/stakeholder-profiles.md`](../memory/long-term/stakeholder-profiles.md). This isn't decoration — the voice and emphasis genuinely change between stakeholders. A VP of Reliability and a VP of Product get different one-pagers from the same investigation:

- VP of Reliability — error-budget framing, SLO impact, on-call burden, post-incident learnings.
- VP of Product — feature impact, customer-experience surface, release velocity, competitive considerations.

There is no fixed template. The one-pager follows a five-beat arc — TL;DR, then 01 Problem, 02 Guide, 03 Plan, 04 Stakes, 05 The ask — and the skill selects a component for each beat from the catalog in `skills/exec-onepager/reference/layout-system.md` based on what the story needs (a symptom table or a bold claim for the problem, phase cards or numbered steps for the plan, and so on). The sanitized reference implementation at `skills/exec-onepager/reference/reference-onepager.html` shows one complete recipe and passes the brand gate. Open the `SKILL.md` to see the five steps.

The exec-onepager skill runs in five steps: recipe selection, content draft, brand-humanizer pre-pass, HTML build, and brand gate. The brand-humanizer pre-pass (Step 3) runs on all drafted copy before any HTML is assembled, catching AI writing patterns and DT voice violations while the copy is still in plain text and easy to fix.

## What the deck looks like

Produced by [`skills/pptx-builder/SKILL.md`](../skills/pptx-builder/SKILL.md), **only after** the one-pager is approved. The order matters — it's much easier to expand a tight one-pager into a deck than to compress a sprawling deck into a one-pager.

The in-repo `tools/pptx-generator.py` is the primary renderer — the skill writes a JSON deck spec into the engagement folder and runs the generator against the official template (the external pptx skill is only a fallback, and a markdown outline the last resort). Practical implications you'll see in the output:

- **Slide format.** 16:9 widescreen, 13.33" × 7.5". No square slides, no 4:3.
- **Typography.** DT Flow Medium / DT Flow Light. Arial is the rendering-side fallback only — if a viewer doesn't have DT Flow installed, the slide falls back gracefully. The agent never substitutes a different font on its own.
- **Layouts.** 64 named layouts from the template — content card, chart, table, swimlane, gantt, timeline, funnel, hashtag-stat, and so on. The agent picks from this set, not freeform.
- **Logo lockup.** Horizontal lockup preferred for slide title bars and one-pager headers where horizontal space allows.
- **Wave backgrounds and branded charts.** A closing or decision-required slide can carry one of the two brand wave backgrounds with a dark overlay (`wave_background` / `wave_overlay_opacity` spec fields — the generator turns the text white and keeps the footer), and chart slides use the six brand series colors automatically — never red or green.
- **Product names.** Capitalized and trademarked as the spec requires. The agent never coins variants like "Dynatraces" or "the Dynatrace platform" when the spec says "Dynatrace®".

## Voice and tone

Voice comes from `styleguide.dynatrace.com/docs/best-practices/top-10-tips` and from the matching stakeholder profile. **No critique lens runs in Phase 3** — the voice and framing were already enforced upstream, while the work could still change:

- The [Consultative lens](../.claude/agents/consultative-lens.md) ran a framing pass on the issue tree and hypotheses in Phase 1, and reviewed the action plan as a panel member in Phase 2, so the firm's voice is baked into the plan the one-pager summarizes.
- The [Customer lens](../.claude/agents/customer-lens.md) and [Skeptic lens](../.claude/agents/skeptic-lens.md) were both on the Phase 2 persona panel, so user-impact grounding and the hostile-leadership questions are already answered in the approved plan.

Phase 3 inherits that reviewed plan and packages it faithfully — it does not re-open the message. The deliverable stays in voice because the plan it summarizes was already in voice. You can still ask for any lens on demand at the Phase 3 gate, but none runs automatically. If you want to know exactly which lens catches what and when it runs, [lenses.md](lenses.md) has the full breakdown.

## Spot-checking before you send

Before you send a one-pager, run the mechanical check first — `python3 tools/onepager-lint.py <file.html>` lints the **brand gates themselves**: gate 1 (one-page fit, via a headless Chrome render and PDF page count, with a content-budget comparison against the reference one-pager when Chrome is unavailable), gate 3 (em dashes, banned phrasings, trademark first-mentions, sentence-case headings), gate 4 (aria/role attributes, font-size minimums), gate 5 (sources-block citation format, footer boilerplate), plus the design-system checks (declared tokens, palette, font fallback). FAILs are mechanical certainties to fix; WARNs are heuristics to confirm by eye; exit 3 means the page-fit check couldn't run and you should do the manual print preview. The agent runs this itself at the Phase 3 brand gate; running it yourself before sending is a belt-and-suspenders habit. Then you can ask the agent for an explicit verification pass:

> *"Verify this one-pager against the brand spec — colors, typography, layout, terminology."*

The agent will load [`memory/long-term/brand/brand-spec.md`](../memory/long-term/brand/brand-spec.md), walk the artifact section by section, and flag anything off-spec. This catches the kinds of drift that are easy to miss: a trademarked product name without the ®, an Arial fallback that shouldn't be visible, a HEX value that's close to but not exactly the palette.

## Look inside

| What you'll find | Where to look |
|---|---|
| The authoritative brand spec | [`memory/long-term/brand/brand-spec.md`](../memory/long-term/brand/brand-spec.md) |
| Supporting reference notes (which page in the source PDF maps to which pattern) | [`memory/long-term/brand/reference/`](../memory/long-term/brand/reference/) |
| The rendered PowerPoint theme | [`Dynatrace_Brand_Insights-Forge.pptx`](../Dynatrace_Brand_Insights-Forge.pptx) |
| The DT Flow typeface files | [`DTFlow/`](../DTFlow/) |
| The one-pager skill | [`skills/exec-onepager/SKILL.md`](../skills/exec-onepager/SKILL.md) |
| The deck skill | [`skills/pptx-builder/SKILL.md`](../skills/pptx-builder/SKILL.md) |
